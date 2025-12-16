import cohere
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def check_cohere_models():
    # Get API key from environment
    api_key = os.getenv("COHERE_API_KEY")

    if not api_key:
        print("COHERE_API_KEY not found in environment variables")
        return

    # Initialize Cohere client
    co = cohere.AsyncClient(api_key=api_key)

    try:
        print("Fetching available embedding models...")

        # Try to get the models list
        # Note: Cohere doesn't have a direct API to list all embedding models
        # So we'll test common models to see which ones work

        common_models = [
            "embed-english-v3.0",
            "embed-multilingual-v3.0",
            "embed-english-light-v3.0",
            "embed-multilingual-light-v3.0",
            "multilingual-22-12",
            "embed-multilingual-v2.0",  # This is what we were trying to use
            "embed-english-v2.0",
            "embed-english-light-v2.0"
        ]

        print("\nTesting common embedding models...")
        available_models = []

        for model in common_models:
            try:
                print(f"Testing model: {model}")
                response = await co.embed(
                    texts=["test"],
                    model=model,
                    input_type="search_document"
                )
                print(f"  SUCCESS: Model {model} is available. Embedding dimension: {len(response.embeddings[0])}")
                available_models.append((model, len(response.embeddings[0])))
            except Exception as e:
                print(f"  FAILED: Model {model} failed: {str(e)}")

        print(f"\nAvailable models with dimensions:")
        for model, dim in available_models:
            print(f"  - {model}: {dim} dimensions")

        # Check if we have a 1024-dimensional model available
        models_1024 = [(m, d) for m, d in available_models if d == 1024]
        if models_1024:
            print(f"\nFOUND: 1024-dimensional models: {[m for m, d in models_1024]}")
        else:
            print(f"\nNO 1024-dimensional models found. Available dimensions: {set([d for m, d in available_models])}")

        # Check if we have a 768-dimensional model available (for the original collection)
        models_768 = [(m, d) for m, d in available_models if d == 768]
        if models_768:
            print(f"\nFOUND: 768-dimensional models: {[m for m, d in models_768]}")
        else:
            print(f"\nNO 768-dimensional models found.")

    except Exception as e:
        print(f"Error checking models: {str(e)}")

if __name__ == "__main__":
    asyncio.run(check_cohere_models())