import weaviate
import gradio as gr
client = weaviate.connect_to_local()
import weaviate.classes as wvc
from weaviate.classes.config import Property, DataType
import json
# Load the data from the JSON file
with open('data/questions.json', 'r') as f:
    qa_pairs = json.load(f)
documents = [
  "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
  "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
  "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
  "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
  "Llamas are vegetarians and have very efficient digestive systems",
  "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]
# Create a new data collection
collection = client.collections.create(
    name = "la0aa11", # Name of the data collection
    properties=[
        Property(name="text", data_type=DataType.TEXT),
        Property(name="question_id", data_type=DataType.TEXT),
        Property(name="year", data_type=DataType.INT),
        Property(name="subject", data_type=DataType.TEXT),
        Property(name="question_text", data_type=DataType.TEXT),
        Property(name="question_image_link", data_type=DataType.TEXT),
        Property(name="solution_text", data_type=DataType.TEXT),
        Property(name="solution_image_link", data_type=DataType.TEXT),
        Property(name="tags", data_type=DataType.TEXT),
        Property(name="difficulty", data_type=DataType.TEXT),
    ], # Name and data type of the property
    
)

import ollama

# Function to add QA pairs to the Weaviate database and generate embeddings
def add_to_db(qa_pairs):
    with collection.batch.dynamic() as batch:
         for i, d in enumerate(documents):
          # Generate embeddings
          response = ollama.embeddings(model = "mxbai-embed-large",
                                       prompt = d)

          # Add data object with text and embedding
          batch.add_object(
              properties = {"text" : d},
              vector = response["embedding"],
                          )
        # for pair in qa_pairs:
        #     question_id = pair["question_id"]
        #     year = pair["year"]
        #     subject = pair["subject"]
        #     question_text = pair["question_text"]
        #     question_image_link = pair["question_image"] if pair["question_image"] else ""
        #     solution_text = pair["solution_text"]
        #     solution_image_links = pair["solution_image"] if pair["solution_image"] else []
        #     tags = pair["tags"]
        #     difficulty = pair["difficulty"]
            
        #     # Concatenate the question and answer
        #     qa_concat = question_text + " " + solution_text

        #     # Generate an embedding for the concatenated string
        #     response = ollama.embeddings(model="mxbai-embed-large", prompt=qa_concat)
        #     # embedding = response["embedding"]

        #     # Store the data object with properties and embedding
        #     batch.add_object(
        #         properties={

        #             "question_id": question_id,
        #             "year": year,
        #             "subject": subject,
        #             "question_text": question_text,
        #             "question_image_link": question_image_link,
        #             "solution_text": solution_text,
        #             "solution_image_link": solution_image_links,
        #             "tags": tags,
        #             "difficulty": difficulty,
        #             "embedding": embedding,
        #         },
        #         vector=embedding,
            # )


# Generate a response combining the prompt and data we retrieved in step 2
def get_response(prompt):
  # generate an embedding for the prompt and retrieve the most relevant doc
  response = ollama.embeddings(
   model = "mxbai-embed-large",prompt = prompt)
#   embedding = response['embedding']
  results = collection.query.near_vector(near_vector =response["embedding"],limit = 1)
  data = results.objects[0].properties["solution_text"]
  print("Data retrieved after matching from prompt:", data)
  output = ollama.generate(
   model = "llama2",prompt = f"Using this data: {data}. Respond to this prompt: {prompt}")
  return output['response']


# Create a Gradio interface
iface = gr.Interface(
    fn=get_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text",
)

if __name__ == "__main__":
    iface.launch()