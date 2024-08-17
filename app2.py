import gradio as gr
import weaviate
import ollama
import gradio as gr
import json
import time
# Load QA pairs into a dictionary
qa_pairs = {
        "Mr. X speaks $\\qquad$ Japanese $\\qquad$ Chinese.\n(a) neither / or\n(b) either / nor\n(c) neither / nor\n(d) also / but": "(c)\n\nHere we will cheake tones.\n\nMr. X speaks neither Japanese nor Chinese.", "002A sum of money is to be distributed among $P$, $Q, R$, and $S$ in the proportion $5: 2: 4: 3$, respectively.\n\nIf R gets $R 1000$ more than $S$, what is the share of $Q$ (in Rs)?\n(a) 500\n(b) 1000\n(c) 1500\n(d) 2000": "(d)\n\n$P \\quad Q \\quad \\underset{R}{\\sim} \\quad 1=1000$ Rs.\n\n$5: 2: 4: 3$\n\nSo, Sharing of Q is $=2 \\times 1000$\n\n$=2000 \\mathrm{Rs}$", "A trapezium has vertices marked as $\\mathrm{P}, \\mathrm{Q}, \\mathrm{R}$ and $S$ (in that order anticlockwise). The side $\\mathrm{PQ}$ is parallel to side $\\mathrm{SR}$.\n\nFurther, it is given that, $\\mathrm{PQ}=11 \\mathrm{~cm}, \\mathrm{QR}=4$ $\\mathrm{cm}, \\mathrm{RS}=6 \\mathrm{~cm}$ and $S P=3 \\mathrm{~cm}$.\n\nWhat is the shortest distance between $\\mathrm{PQ}$ and $\\mathrm{SR}$ (in $\\mathrm{cm}$ )?\n(a) 1.80\n(b) 2.40\n(c) 4.20\n(d) 5.76": "(b)\n\n[image1]\n\n$$\n\\begin{aligned}\n& =\\frac{1}{2} \\times B \\times 4 \\quad H \\rightarrow \\text { Height } \\\\\n& =\\frac{1}{2} \\times 3 \\times 4 \\\\\n& =6 \\mathrm{~cm}^{2} \\\\\n\\frac{1}{2} \\times 5 \\times \\mathrm{RT} & =6 \\mathrm{~cm}^{2} \\\\\n\\text { RT } & =2.4 \\mathrm{~cm}\n\\end{aligned}\n$$",
        "The figure shows a grid formed by a collection of unit squares. The unshaded unit square in the grid represents a hole.\n\n[image1]\n\nWhat is the maximum number of squares without a \"hole in the interior\" that can be formed within the $4 \\times 4$ grid using the unit squares as building blocks?\n(a) 15\n(b) 20\n(c) 21\n(d) 26": "004https://cdn.mathpix.com/cropped/2024_07_05_7ed3cda94b26d95bc81ag-1.jpg?height=520&width=583&top_left_y=942&top_left_x=1176"}  # Load your QA pairs here

def fetch_solution(question):
    return qa_pairs.get(question, "No solution found")

def generate_followup_response(solution, followup_question):
    prompt = f"Using this data: {solution}. Respond to this prompt: {followup_question} in few words."
    output = ollama.generate(model="llama3:8b-instruct-q2_K", prompt=prompt)
    return output['response']

def gradio_interface(question, followup_question):
    solution = fetch_solution(question)
    if followup_question:
        response = generate_followup_response(solution, followup_question)
        return solution, response
    else:
        return solution, ""

iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Dropdown(label="Select a question", choices=list(qa_pairs.keys())),
        gr.Textbox(label="Ask a follow-up question", lines=2, placeholder="Enter your follow-up question here..."),
    ],
    outputs=[
        gr.Markdown(label="Solution"),
        gr.Markdown(label="Follow-up Response"),
    ]
)

if __name__ == "__main__":
    iface.launch()