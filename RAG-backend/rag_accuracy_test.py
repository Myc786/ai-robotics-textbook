# RAG-backend/rag_accuracy_test.py

import requests
import json
import os

# --- Configuration ---
RAG_BACKEND_URL = os.getenv("RAG_BACKEND_URL", "http://localhost:8000/api/v1/query")

# Dummy test queries and expected (simplified) responses
# In a real scenario, this would be a more comprehensive dataset
test_cases = [
    {
        "query": "What is Physical AI?",
        "expected_keywords": ["intelligent systems", "physical world", "sensors", "actuators"]
    },
    {
        "query": "How do humanoid robots move?",
        "expected_keywords": ["actuators", "control systems"]
    },
    {
        "query": "Tell me about ROS 2 nodes.",
        "expected_keywords": ["nodes", "topics", "services"]
    },
    {
        "query": "What is Gazebo used for?",
        "expected_keywords": ["simulation", "digital twins"]
    },
    {
        "query": "Explain Vision-Language-Action systems.",
        "expected_keywords": ["computer vision", "language understanding", "action planning"]
    },
    {
        "query": "What is a capstone project in robotics?",
        "expected_keywords": ["integrating concepts", "multi-agent", "demonstrations"]
    },
    {
        "query": "Who developed physical AI?", # Off-topic example
        "expected_keywords": []
    },
    {
        "query": "What is the capital of France?", # Off-topic example
        "expected_keywords": []
    },
]

def run_accuracy_test():
    print(f"Running RAG accuracy test against {RAG_BACKEND_URL}...")
    correct_answers = 0
    total_questions = len(test_cases)

    for i, test_case in enumerate(test_cases):
        query = test_case["query"]
        expected_keywords = test_case["expected_keywords"]
        is_off_topic_expected = not bool(expected_keywords)

        print(f"\nTest Case {i+1}: Query: '{query}'")
        try:
            response = requests.post(RAG_BACKEND_URL, json={"query": query})
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()

            answer = data.get("answer", "").lower()
            sources = data.get("sources", [])

            is_correct = False
            if is_off_topic_expected:
                # For off-topic queries, expect a generic refusal and no sources
                if "sorry" in answer or "cannot answer" in answer and not sources:
                    is_correct = True
                    print("  Result: CORRECT (Off-topic refusal detected).")
                else:
                    print("  Result: INCORRECT (Expected off-topic refusal, but got relevant answer or sources).")
            else:
                # For on-topic queries, check for keywords and sources
                keywords_found = [kw for kw in expected_keywords if kw.lower() in answer]
                if len(keywords_found) >= len(expected_keywords) * 0.5 and len(sources) > 0:
                    is_correct = True
                    print(f"  Result: CORRECT ({len(keywords_found)}/{len(expected_keywords)} keywords found, sources present).")
                else:
                    print(f"  Result: INCORRECT (Keywords missing or no sources. Found: {keywords_found}).")

            if is_correct:
                correct_answers += 1

        except requests.exceptions.RequestException as e:
            print(f"  Error making request: {e}")
        except json.JSONDecodeError:
            print(f"  Error: Could not decode JSON response: {response.text}")
        except Exception as e:
            print(f"  An unexpected error occurred: {e}")

    accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    print(f"\n--- Test Summary ---")
    print(f"Total Questions: {total_questions}")
    print(f"Correct Answers: {correct_answers}")
    print(f"Accuracy: {accuracy:.2f}%")

    return accuracy

if __name__ == "__main__":
    # Before running, ensure:
    # 1. The FastAPI RAG backend is running (e.g., python -m uvicorn RAG-backend.main:app --reload --port 8000)
    # 2. RAG_BACKEND_URL environment variable is set if not localhost:8000
    accuracy_score = run_accuracy_test()
    if accuracy_score >= 90:
        print("RAG accuracy target met! (>=90%)")
    else:
        print("RAG accuracy below target (<90%). Further improvements needed.")
