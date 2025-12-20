from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_tracing_disabled, function_tool
import os
from dotenv import load_dotenv
from agents import enable_verbose_stdout_logging

enable_verbose_stdout_logging()

load_dotenv()
set_tracing_disabled(disabled=True)

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    print("Warning: OPENROUTER_API_KEY not found in environment. Please set it to run the agent.")
    exit(1)

provider = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

model = OpenAIChatCompletionsModel(
    model="mistralai/devstral-2512:free",
    openai_client=provider
)

import cohere
from qdrant_client import QdrantClient

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

cohere_client = cohere.Client(cohere_api_key)
# Connect to Qdrant
try:
    qdrant = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key
    )
    print("Successfully connected to Qdrant")
except Exception as e:
    print(f"Failed to connect to Qdrant: {e}")
    exit(1)



def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    try:
        response = cohere_client.embed(
            model="embed-english-v3.0",
            input_type="search_query",  # Use search_query for queries
            texts=[text],
        )
        return response.embeddings[0]  # Return the first embedding
    except Exception as e:
        print(f"Embedding generation failed: {str(e)}")
        raise


@function_tool
def retrieve(query):
    try:
        embedding = get_embedding(query)
        result = qdrant.query_points(
            collection_name="Hackathon-Giaic",  # Changed from "humanoid_ai_book" to match actual collection
            query=embedding,  # Using query_points with vector as query parameter
            limit=5,
            with_payload=True  # Ensure we get the payload data
        )
        # The result from query_points has different structure than search
        return [hit.payload.get("text", "") for hit in result.points if hit.payload]
    except Exception as e:
        print(f"Retrieve function failed: {str(e)}")
        return []



agent = Agent(
    name="Assistant",
    instructions="""
You are an AI tutor that has access to information from a collection called "Hackathon-Giaic".
To answer the user question, first call the tool `retrieve` with the user query.
Use ONLY the returned content from `retrieve` to answer.
If the answer is not in the retrieved content, say "I don't know".
""",
    model=model,
    tools=[retrieve]
)


result = Runner.run_sync(
    agent,
    input="what is physical ai?",
)

print(result.final_output)