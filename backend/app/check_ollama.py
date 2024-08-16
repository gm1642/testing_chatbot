import ollama
import httpx

def check_ollama_access():
    try:
        # Initialize Ollama client
        ollama_client = ollama.Client()
        ollama_client.base_url = "http://ollama:11434"
        
        # Send a test request
        response = ollama_client.embeddings(model="mxbai-embed-large", prompt="qa_concat")
        
        # Print response
        print("Ollama API Response:", response)
        return True
    
    except httpx.ConnectError as e:
        print(f"Connection error: {e}")
        return False
    
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        return False
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    if check_ollama_access():
        print("Ollama is accessible.")
    else:
        print("Failed to access Ollama.")
