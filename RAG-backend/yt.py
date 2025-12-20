import cohere
from qdrant_client import QdrantClient

# Initialize Cohere client
cohere_client = cohere.Client("eCvi7xpScMvM4abnBulKn7ySLGgQyvP0cH82sxnI")

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url="https://5a4a4153-cab7-40db-867a-321df1a243bb.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.LS9k3Bu16S8wrJ4f4zsash8et-SvGeELuG7Yfp8RrP4",
)

def get_embedding(text: str):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",
        texts=[text],
    )
    return response.embeddings[0]

def retrieve(query: str):
    embedding = get_embedding(query)

    result = qdrant_client.search(
        collection_name="Hackathon-Giaic",
        query_vector=embedding,
        limit=5
    )

    # ✅ SAFE payload access (no KeyError)
    return [
        hit.payload.get("text")
        or hit.payload.get("content")
        or hit.payload.get("page_content")
        or ""
        for hit in result
    ]

if __name__ == "__main__":
    print(retrieve("what data you have"))
