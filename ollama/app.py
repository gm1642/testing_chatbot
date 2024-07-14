from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

# Endpoint for generating embeddings
@app.route('/embeddings', methods=['POST'])
def generate_embeddings():
    data = request.json
    model = data.get('model')
    prompt = data.get('prompt')
    
    try:
        response = ollama.embeddings(model=model, prompt=prompt)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for generating text
@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    model = data.get('model')
    prompt = data.get('prompt')
    
    try:
        response = ollama.generate(model=model, prompt=prompt)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11434)
