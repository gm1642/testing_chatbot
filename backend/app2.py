from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pymongo import MongoClient
import weaviate
import ollama
import weaviate.classes as wvc
from weaviate.classes.config import Property, DataType
import json
import uuid
import re


client = weaviate.connect_to_local()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Connect to the MongoDB cluster
mongo_client = MongoClient(MONGO_URI)

# Select the database
mongo_db = mongo_client["exam-chatbot-assistant"]

# Select the collection
feedback_collection = mongo_db["feedback"]

class Prompt(BaseModel):
    prompt: str

class Feedback(BaseModel):
    response_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str = None

def save_feedback_to_mongo(feedback: Feedback):
    feedback_data = {
        "response_id": feedback.response_id,
        "rating": feedback.rating,
        "comment": feedback.comment
    }
    feedback_collection.insert_one(feedback_data)

@app.post("/api/feedback")
async def feedback_endpoint(feedback: Feedback):
    print(f"Received feedback: {feedback}")
    save_feedback_to_mongo(feedback)
    return {"status": "Feedback received"}

# Load the data from the JSON file
with open('app/data/questions.json', 'r') as f:
    qa_pairs = json.load(f)

# Check if the collection exists, if not, create it
collection_name = "Death"
if not client.collections.exists(collection_name):
    collection = client.collections.create(
        name=collection_name,
        properties=[
            Property(name="question_id", data_type=DataType.TEXT),
            Property(name="year", data_type=DataType.INT),
            Property(name="subject", data_type=DataType.TEXT),
            Property(name="question_text", data_type=DataType.TEXT),
            Property(name="question_image_link", data_type=DataType.TEXT_ARRAY),
            Property(name="solution_text", data_type=DataType.TEXT),
            Property(name="solution_image_link", data_type=DataType.TEXT_ARRAY),
            Property(name="tags", data_type=DataType.TEXT_ARRAY),
            Property(name="difficulty", data_type=DataType.TEXT),
        ],
    )
else:
    collection = client.collections.get(collection_name)

# Function to add QA pairs to the Weaviate database and generate embeddings
def add_to_db(qa_pairs):
    with collection.batch.fixed_size(batch_size=300) as batch:
        for pair in qa_pairs:
            question_id = pair["question_id"]
            year = pair["year"]
            subject = pair["subject"]
            question_text = pair["question_text"]
            solution_text = pair["solution_text"]
            question_image_link = pair["question_image"]
            solution_image_links = pair["solution_image"]
            tags = pair["tags"]
            difficulty = pair["difficulty"]

            qa_concat = question_text + " " + solution_text

            response = ollama.embeddings(model="mxbai-embed-large", prompt=qa_concat)

            batch.add_object(
                properties={
                    "question_id": question_id,
                    "year": year,
                    "subject": subject,
                    "question_text": question_text,
                    "question_image_link": question_image_link,
                    "solution_text": solution_text,
                    "solution_image_link": solution_image_links,
                    "tags": tags,
                    "difficulty": difficulty,
                },
                vector=response["embedding"]
            )


def get_response(prompt: str):
    response = ollama.embeddings(model="mxbai-embed-large", prompt=prompt)
    results = collection.query.near_vector(near_vector=response["embedding"], limit=10)
    best_match = results.objects[0]  
    print("fetched results after matching the prompt", results)


    if results.objects:
        data = results.objects[0].properties["solution_text"]
        print("Data retrieved after matching from prompt:", data)
        output = ollama.generate(
            model="phi3", prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
        )
        return output['response']
    else:
        return "No matching data found."
    

@app.post("/api/get_response")
async def get_response_endpoint(prompt: Prompt):
    response_text = get_response(prompt.prompt)
    response_id = str(uuid.uuid4())
    return {"response": response_text, "response_id": response_id}


# Initialize the database
add_to_db(qa_pairs)

if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    finally:
        client.close()
