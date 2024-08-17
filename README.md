# RAG Chatbot with dual capability exact solution retrieval + response generation 
## To use this chatbot follow these steps
### Step 1: Download and install Ollama
### step 2: Step 2: Pull models
`
ollama pull phi3
ollama pull znbang/bge:small-en-v1.5-f32
ollama pull llama3:8b-instruct-q2_K
`
### Step 3: Install Ollama Python library
`pip install ollama`
## How to Setup a Local Vector Database Instance with Docker
### Step 1: Download and install Docker
### Step 2: Start up the Docker container with a Weaviate instance
`
docker run -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:1.24.8
`
### Step 3: Install the Weaviate Python client
`
pip install -U weaviate-client
`
### finally run app2.py
### navigate to
` http://127.0.0.1:7860/ `