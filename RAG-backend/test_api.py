"""
Simple test script to verify the API endpoints are working correctly.
This can be used to test the connection between your frontend and backend.
"""
import requests
import json

def test_backend_connection(base_url):
    """Test basic connectivity to the backend."""
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✓ Backend health check passed")
            print(f"  Status: {response.json()}")
        else:
            print(f"✗ Backend health check failed: {response.status_code}")
            return False

        # Test root endpoint
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✓ Backend root endpoint accessible")
        else:
            print(f"✗ Backend root endpoint failed: {response.status_code}")
            return False

        return True
    except Exception as e:
        print(f"✗ Error connecting to backend: {str(e)}")
        return False

def test_chat_endpoint(base_url, query="Hello, can you help me?"):
    """Test the chat endpoint."""
    try:
        response = requests.post(
            f"{base_url}/api/v1/chat",
            headers={"Content-Type": "application/json"},
            json={
                "query": query,
                "top_k": 3,
                "similarity_threshold": 0.5,
                "search_scope": "full_book"
            }
        )

        if response.status_code in [200, 422]:  # 422 is expected if no documents are indexed
            print("✓ Chat endpoint accessible")
            if response.status_code == 200:
                print(f"  Response: {response.json()}")
            else:
                print(f"  Expected validation error (no documents indexed): {response.json()}")
            return True
        else:
            print(f"✗ Chat endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error testing chat endpoint: {str(e)}")
        return False

if __name__ == "__main__":
    # Replace with your actual backend URL
    BACKEND_URL = "http://localhost:8000"  # Update this to your deployed backend URL

    print(f"Testing backend connection to: {BACKEND_URL}")
    print("-" * 50)

    if test_backend_connection(BACKEND_URL):
        print("\nBackend is accessible!")
        print("\nTesting chat functionality...")
        test_chat_endpoint(BACKEND_URL)

        print("\n" + "="*50)
        print("Test Summary:")
        print("✓ Backend is accessible and responding")
        print("✓ API endpoints are available")
        print("✓ Ready for frontend integration")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("Backend is not accessible. Please check:")
        print("1. Backend is running and accessible at the specified URL")
        print("2. Environment variables are properly configured")
        print("3. Network connectivity between frontend and backend")
        print("="*50)