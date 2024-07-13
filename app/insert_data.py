import json
import weaviate
import ollama

client = weaviate.Client("http://localhost:8080")

with open('/data/questions.json') as f:
    question_data = json.load(f)

for item in question_data:
    question_id = item["question_id"]
    question_text = item["question_text"]
    solution_text = item["solution_text"]
    solution_images = item["solution_image"]

    qa_concat = question_text + " " + solution_text
    response = ollama.embeddings(model="mxbai-embed-large", prompt=qa_concat)
    embedding = response["embedding"]

    client.data_object.create({
        "question_id": question_id,
        "question_text": question_text,
        "solution_text": solution_text,
        "solution_image": solution_images,
        "vector": embedding
    }, "Question")
