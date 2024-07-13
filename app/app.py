import gradio as gr
import ollama
import weaviate

client = weaviate.Client("http://localhost:8080")

def retrieve_and_format_solution(question_prompt):
    try:
        # Generate embedding for the user's question prompt
        response = ollama.embeddings(
            model="mxbai-embed-large",
            prompt=question_prompt
        )
        query_embedding = response["embedding"]

        # Perform similarity search in Weaviate
        near_vector = {
            "vector": query_embedding,
            "certainty": 0.7
        }

        result = client.query.get(
            "Question",
            ["question_text", "solution_text", "solution_image"]
        ).with_near_vector(near_vector).do()
        
        question = result['data']['Get']['Question'][0]

        solution_text = question['solution_text']
        solution_images = question['solution_image']

        # Insert images in the solution text
        for i, img in enumerate(solution_images):
            solution_text = solution_text.replace(f"[image{i+1}]", f"<img src='{img}' alt='Solution Image {i+1}'>")

        return solution_text
    except Exception as e:
        return f"An error occurred: {e}"

def get_response(prompt):
    try:
        formatted_solution = retrieve_and_format_solution(prompt)
        
        # Generate a response combining the prompt and retrieved solution
        output = ollama.generate(
            model="llama2",
            prompt=f"Using this data: {formatted_solution}. Respond to this prompt: {prompt}"
        )

        return output['response']
    except Exception as e:
        return f"An error occurred: {e}"

iface = gr.Interface(
    fn=get_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
