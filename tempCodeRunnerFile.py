or i, d in enumerate(documents):
        #   # Generate embeddings
        #   response = ollama.embeddings(model = "mxbai-embed-large",
        #                                prompt = d)

        #   # Add data object with text and embedding
        #   batch.add_object(
        #       properties = {"text" : d},
        #       vector = response["embedding"],
        #                   )