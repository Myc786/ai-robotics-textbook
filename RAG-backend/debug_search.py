import requests
import json

# Test the search results directly
query = "What is Gazebo used for?"
response = requests.post("http://127.0.0.1:8000/api/v1/query", json={"query": query})
data = response.json()

print(f"Query: {query}")
print(f"Answer: {data['answer']}")
print(f"Sources: {data['sources']}")

print("\n--- Analysis ---")
answer_lower = data['answer'].lower()
expected_keywords = ["simulation", "digital twins"]
found_keywords = [kw for kw in expected_keywords if kw.lower() in answer_lower]
print(f"Expected keywords: {expected_keywords}")
print(f"Found keywords: {found_keywords}")
print(f"Keywords present: {len(found_keywords) >= len(expected_keywords) * 0.5}")