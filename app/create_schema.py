import weaviate

client = weaviate.Client("http://weaviate:8080")


schema = {
    "classes": [
        {
            "class": "Question",
            "description": "A class for storing GATE questions and their solutions",
            "properties": [
                {
                    "name": "question_id",
                    "dataType": ["string"],
                    "description": "The ID of the question"
                },
                {
                    "name": "question_text",
                    "dataType": ["text"],
                    "description": "The text of the question"
                },
                {
                    "name": "solution_text",
                    "dataType": ["text"],
                    "description": "The text of the solution"
                },
                {
                    "name": "solution_image",
                    "dataType": ["string[]"],
                    "description": "List of image URLs related to the solution"
                },
                {
                    "name": "vector",
                    "dataType": ["number[]"],
                    "description": "Vector representation of the question and solution"
                }
            ]
        }
    ]
}

client.schema.create(schema)
