import requests
import json

def test_rag_backend():
    """Test script for the RAG backend functionality"""
    
    # Base URL for the RAG backend
    base_url = "http://localhost:8000"
    
    # Test the health endpoint
    print("Testing health endpoint...")
    try:
        health_response = requests.get(f"{base_url}/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✓ Health check passed: {health_data}")
        else:
            print(f"✗ Health check failed with status: {health_response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error connecting to backend: {e}")
        print("Make sure the RAG backend is running on http://localhost:8000")
        return False
    
    # Test various queries
    test_queries = [
        "What is Physical AI?",
        "How do humanoid robots move?",
        "Explain ROS 2 nodes, topics, and services",
        "What is Gazebo used for?",
        "What are Vision-Language-Action systems?",
        "Tell me about the capstone project"
    ]
    
    print("\nTesting RAG query functionality...")
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = requests.post(
                f"{base_url}/api/v1/query",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"query": query})
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  Answer: {result['answer'][:100]}...")
                print(f"  Sources: {len(result['sources'])} references")
            else:
                print(f"  ✗ Query failed with status: {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ Error querying backend: {e}")
            return False
    
    print("\n✓ All tests completed successfully!")
    return True

if __name__ == "__main__":
    print("RAG Backend Test Script")
    print("="*50)
    test_rag_backend()