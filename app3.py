import weaviate
import ollama
import gradio as gr
import json

# Connect to Weaviate locally
# client = weaviate.connect_to_local()

# Load the data from the JSON file
with open('data/questions.json', 'r') as f:
    qa_pairs = json.load(f)

# Extract question texts for the dropdown
question_texts = [pair["question_text"] for pair in qa_pairs]
question_dict = {pair["question_text"]: pair for pair in qa_pairs}  # To map question to its full data

# Function to fetch the corresponding solution data
def fetch_solution(selected_question):
    pair = question_dict[selected_question]
    solution_text = pair["solution_text"]
    solution_links = pair["solution_image"]
    for i, img in enumerate(solution_links):
        solution_text = solution_text.replace(f"[image{i+1}]", f"<img src='{img}' alt='Solution Image {i+1}'>")
    return solution_text, ""

# Function to generate a response based on follow-up question
def generate_response(selected_question, follow_up_prompt):
    if selected_question and follow_up_prompt:
        pair = question_dict[selected_question]
        combined_text = f"Question: {pair['question_text']} Solution: {pair['solution_text']}"
        prompt = f"Using this data: {combined_text}. Respond to this prompt: {follow_up_prompt} in less number of words."
        output = ollama.generate(model="llama3:8b-instruct-q2_K", prompt=prompt)
        return "", output['response']
    return "No question selected or follow-up prompt is empty.", ""

# Gradio Interface
def gradio_interface(selected_question, follow_up_prompt):
    if follow_up_prompt == "":
        return fetch_solution(selected_question)
    else:
        return generate_response(selected_question, follow_up_prompt)

iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Dropdown(choices=question_texts, label="Select a Question"),
        gr.Textbox(lines=2, placeholder="Enter your follow-up prompt here...", visible=True)
    ],
    outputs=[
        gr.Markdown(label="Exact Retrieved Solution", show_label=True),
        gr.Markdown(label="Response to User Prompt", show_label=True),
    ]
)

if __name__ == "__main__":
    iface.launch()
