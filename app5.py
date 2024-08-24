import json
import ollama
import gradio as gr

# Load the data from the JSON file
with open('data/questions.json', 'r') as f:
    qa_pairs = json.load(f)

# Generate summaries and add them to each question
for pair in qa_pairs:
    if "summary" not in pair:  # Only generate if the summary doesn't exist
        pair["summary"] = ollama.generate(model="llama3:8b-instruct-q2_K", prompt=f"Summarize the following question in one to two lines: {pair['question_text']}")['response'].strip()

# Save the updated data back to the JSON file
with open('data/questions.json', 'w') as f:
    json.dump(qa_pairs, f, indent=4)

# Separate questions by subject
technical_summaries = [pair["summary"] for pair in qa_pairs if pair["subject"] == "Technical"]
aptitude_summaries = [pair["summary"] for pair in qa_pairs if pair["subject"] == "Aptitude"]

# Create a dictionary for each category
technical_dict = {pair["summary"]: pair for pair in qa_pairs if pair["subject"] == "Technical"}
aptitude_dict = {pair["summary"]: pair for pair in qa_pairs if pair["subject"] == "Aptitude"}

# Function to fetch the full question and solution data
def fetch_full_question_and_solution(selected_summary, subject):
    if subject == "Technical":
        pair = technical_dict[selected_summary]
    else:
        pair = aptitude_dict[selected_summary]
        
    full_question = f"Full Question: {pair['question_text']}"
    solution_links = pair["solution_image"]
    citations = pair.get("source", "N/A")
    solution_text = f"Solution: {pair['solution_text']}\n\nSource: {citations}"
    
    for i, img in enumerate(solution_links):
        solution_text = solution_text.replace(f"[image{i+1}]", f"<img src='{img}' alt='Solution Image {i+1}'>")
    
    return f"{full_question}\n\n{solution_text}", ""

# Function to generate a response based on follow-up question
def generate_response(selected_summary, follow_up_prompt, subject):
    if selected_summary and follow_up_prompt:
        if subject == "Technical":
            pair = technical_dict[selected_summary]
        else:
            pair = aptitude_dict[selected_summary]
            
        combined_text = f"Question: {pair['question_text']} Solution: {pair['solution_text']}"
        prompt = f"Using this data: {combined_text}. Respond to this prompt: {follow_up_prompt} in fewer words."
        output = ollama.generate(model="llama3:8b-instruct-q2_K", prompt=prompt)
        return "", output['response']
    
    return "No question selected or follow-up prompt is empty.", ""

# Gradio Interface
def gradio_interface(selected_summary, follow_up_prompt, subject):
    if follow_up_prompt == "":
        return fetch_full_question_and_solution(selected_summary, subject)
    else:
        return generate_response(selected_summary, follow_up_prompt, subject)

iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Dropdown(choices=["Technical"] + technical_summaries + ["Aptitude"] + aptitude_summaries, label="Select a Question Summary"),
        gr.Textbox(lines=2, placeholder="Enter your follow-up prompt here...", visible=True),
        gr.Radio(choices=["Technical", "Aptitude"], label="Select Subject")
    ],
    outputs=[
        gr.Markdown(label="Full Question & Exact Retrieved Solution", show_label=True),
        gr.Markdown(label="Response to User Prompt", show_label=True),
    ]
)

if __name__ == "__main__":
    iface.launch()
