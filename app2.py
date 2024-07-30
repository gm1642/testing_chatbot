import weaviate
import ollama
import gradio as gr
import json

# Connect to Weaviate locally
client = weaviate.connect_to_local()
import weaviate.classes as wvc
from weaviate.classes.config import Property, DataType

# Load the data from the JSON file
with open('data/questions.json', 'r') as f:
    qa_pairs = json.load(f)

# Define the collection name
collection_name = "Death1"

# Create the collection if it doesn't exist
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

            # Concatenate the question and answer
            qa_concat = question_text + " " + solution_text

            # Generate an embedding for the concatenated string
            response = ollama.embeddings(model="mxbai-embed-large", prompt=qa_concat)

            # Store the data object with properties and embedding
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
add_to_db(qa_pairs)
# Step 1: Retrieve and display the solution
def retrieve_solution(prompt):
    response = ollama.embeddings(model="mxbai-embed-large", prompt=prompt)
    results = collection.query.near_vector(near_vector=response["embedding"], limit=1)
    
    if results.objects:
        solution_text = results.objects[0].properties["solution_text"]
        return solution_text
    else:
        return "No matching data found."

# Step 2: Generate a response using the retrieved solution and user prompt
def generate_response(retrieved_solution, user_prompt):
    prompt = f"Using this data: {retrieved_solution}. Respond to this prompt: {user_prompt}"
    output = ollama.generate(model="phi3", prompt=prompt)
    return output['response']

retrieved_solution = ""

def gradio_interface(initial_prompt, follow_up_prompt):
    global retrieved_solution  # Declare the variable as global
    if follow_up_prompt == "":
        # Step 1: Retrieve solution
        retrieved_solution = retrieve_solution(initial_prompt)
        return retrieved_solution, "", gr.update(visible=True), gr.update(visible=True, value="")
    else:
        # Step 2: Generate response
        response = generate_response(retrieved_solution, follow_up_prompt)
        return retrieved_solution, response, gr.update(visible=False), gr.update(visible=False)

iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter your initial prompt here..."),
        gr.Textbox(lines=2, placeholder="Enter your follow-up prompt here...", visible=True)
    ],
    outputs=[
        gr.Markdown(label="Exact Retrieved Solution",show_label=True),
        gr.Markdown(label="Response to User Prompt",show_label=True),

    ]
)

if __name__ == "__main__":
    iface.launch()