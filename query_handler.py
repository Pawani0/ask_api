import json

with open("data.json", "r") as file:
    qa_data = json.load(file)

def get_answer(query: str) -> str:
    query_lower = query.strip().lower()
    return qa_data.get(query_lower, "Sorry, I didn't understand that question.")
