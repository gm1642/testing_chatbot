import json
from rake_nltk import Rake
import nltk
nltk.download('stopwords')

# Initialize Rake
rake = Rake()

# Load your JSON data
with open('question_data_final.json', 'r') as f:
    questions = json.load(f)

# Process each question and generate tags
for question in questions:
    text = question['question_text']
    rake.extract_keywords_from_text(text)
    tags = rake.get_ranked_phrases()[:5]  # Get top 5 tags
    question['tags'] = tags

# Save the updated JSON data
with open('question_data_final_with_tags.json', 'w') as f:
    json.dump(questions, f, indent=4)

print("Tags generated and saved to question_data_final_with_tags.json")
