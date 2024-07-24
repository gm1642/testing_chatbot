import weaviate
import ollama
import gradio as gr
client = weaviate.connect_to_local()
import weaviate.classes as wvc
from weaviate.classes.config import Property, DataType
import json
# Load the data from the JSON file
with open('data/questions.json', 'r') as f:
    qa_pairs = json.load(f)

# Create a new data collection
collection = client.collections.create(
    name = "death", # Name of the data collection
    properties=[
        # Property(name="text", data_type=DataType.TEXT),
        Property(name="question_id", data_type=DataType.TEXT),
        Property(name="year", data_type=DataType.INT),
        Property(name="subject", data_type=DataType.TEXT),
        Property(name="question_text", data_type=DataType.TEXT),
        Property(name="question_image_link", data_type=DataType.TEXT_ARRAY),
        Property(name="solution_text", data_type=DataType.TEXT),
        Property(name="solution_image_link", data_type=DataType.TEXT_ARRAY),
        Property(name="tags", data_type=DataType.TEXT_ARRAY),
        Property(name="difficulty", data_type=DataType.TEXT),
    ], # Name and data type of the property
    
)



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
            # print(question_image_link)
            solution_image_links = pair["solution_image"] 
            # print(solution_image_links)
            tags = pair["tags"] 
            difficulty = pair["difficulty"]
            
            # Concatenate the question and answer
            qa_concat = question_text + " " + solution_text
            # print(qa_concat)

            # Generate an embedding for the concatenated string
            response = ollama.embeddings(model="mxbai-embed-large", prompt=qa_concat)
            # print(response["embedding"])

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
                vector = response["embedding"] )
       
            

# Generate a response combining the prompt and data we retrieved in step 2
def get_response(prompt):
  # generate an embedding for the prompt and retrieve the most relevant doc
  response = ollama.embeddings(
   model = "mxbai-embed-large",prompt = prompt)
#   embedding = response['embedding']
  results = collection.query.near_vector(near_vector =response["embedding"],limit = 1)
  print("fetched results after matching the prompt", results)

  if results.objects:  # Check if the list is not empty
        data = results.objects[0].properties["solution_text"]
        print("Data retrieved after matching from prompt:", data)
        output = ollama.generate(
            model="phi3", prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
        )
        return output['response']
  else:
        return "No matching data found."

add_to_db(qa_pairs)
# Create a Gradio interface
iface = gr.Interface(
    fn=get_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text",
)

if __name__ == "__main__":
    iface.launch()