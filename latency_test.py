import json
import time
import ollama

# Load the data from the JSON file
with open('data/questions.json', 'r') as f:
    qa_pairs = json.load(f)

# Function to measure latency
def measure_latency(qa_pair):
    combined_text = f"Question: {qa_pair['question_text']} Solution: {qa_pair['solution_text']}"
    prompt = f"Using this data: {combined_text}. Respond to this prompt: 'Explain the solution in fewer words.'"
    
    start_time = time.time()  # Record start time
    response = ollama.generate(model="llama3:8b-instruct-q2_K", prompt=prompt)
    end_time = time.time()  # Record end time
    
    latency = end_time - start_time  # Calculate latency
    return latency, response['response']

# Test Latency for Each Question-Answer Pair
latency_results = []
for pair in qa_pairs:
    latency, response = measure_latency(pair)
    latency_results.append({
        "question_id": pair["question_id"],
        "latency": latency,
        "response": response
    })
    print(f"Question ID: {pair['question_id']} - Latency: {latency:.4f} seconds")

# Optionally, save latency results to a file
with open('latency_results.json', 'w') as f:
    json.dump(latency_results, f, indent=4)

print("Latency testing completed.")
