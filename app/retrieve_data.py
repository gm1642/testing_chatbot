import weaviate
import ollama

client = weaviate.Client("http://localhost:8080")

def retrieve_and_format_solution(question_prompt):
    # Generate embedding for the user's question prompt
    response = ollama.embeddings(
        model="mxbai-embed-large",
        prompt=question_prompt
    )
    query_embedding = response["embedding"]

    # Perform similarity search in Weaviate
    query = {
        "class": "Question",
        "nearVector": {
            "vector": query_embedding,
            "certainty": 0.7
        },
        "limit": 1
    }

    result = client.query.get(query, ["question_text", "solution_text", "solution_image"])
    question = result['data']['Get']['Question'][0]

    solution_text = question['solution_text']
    solution_images = question['solution_image']

    # Insert images in the solution text
    for i, img in enumerate(solution_images):
        solution_text = solution_text.replace(f"[image{i+1}]", f"<img src='{img}' alt='Solution Image {i+1}'>")

    return solution_text

# Example usage with a user prompt
user_prompt = "Consider a channel over which either symbol x_A or symbol x_B is transmitted..."
formatted_solution = retrieve_and_format_solution(user_prompt)
print(formatted_solution)
