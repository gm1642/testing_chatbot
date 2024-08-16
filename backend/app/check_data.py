import weaviate

print(weaviate.__version__)
from weaviate.classes.query import MetadataQuery

client = weaviate.Client("http://localhost:8080")

def verify_schema():
    schema = client.schema.get()
    print("Schema:", schema)

verify_schema()

def insert_test_data():
    test_vector = [0.1] * 128  # Use a known vector format
    client.data_object.create(
        data_object={
            "question_id": "test",
            "question_text": "Test question",
            "solution_text": "Test solution",
            "vector": test_vector
        },
        class_name="Question"
    )

insert_test_data()

def list_objects():
    result = client.query.get(
        "Question",
        ["question_id", "question_text", "vector"]
    ).do()
    print("List of objects:", result)

list_objects()

def test_query():
    query_vector = [0.1] * 128  # Use the same vector format
    question_collection = client.collections.get("Question")
    response = question_collection.query.near_vector(
        near_vector=query_vector,  # your query vector goes here
        limit=2,
        return_metadata=MetadataQuery(distance=True)
    )

    for obj in response.objects:
        print(obj.properties)
        print(obj.metadata.distance)

test_query()
