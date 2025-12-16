import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.core.vector_db import vector_db_client
from src.services.vector_store_service import vector_store_service

async def check_and_fix_collection():
    print("Checking Qdrant collection...")

    try:
        # Get collection info
        collection_info = await vector_db_client.get_collection_info(
            collection_name=vector_store_service.collection_name
        )

        vector_size = collection_info.config.params.vectors.size
        print(f"Current collection '{vector_store_service.collection_name}' has vector size: {vector_size}")

        if vector_size != 1024:
            print(f"Vector size is {vector_size}, but we need 1024 for the new model.")
            print("We need to delete the existing collection and recreate it with 1024 dimensions.")

            # Delete the existing collection
            await vector_db_client.delete_collection(
                collection_name=vector_store_service.collection_name
            )
            print(f"Deleted collection '{vector_store_service.collection_name}'")

            # Reinitialize the collection with correct dimensions
            await vector_store_service.initialize_collection()
            print("Recreated collection with 1024 dimensions")
        else:
            print("Collection already has correct dimensions (1024). No changes needed.")

    except Exception as e:
        print(f"Collection doesn't exist or error occurred: {e}")
        print("Initializing collection with correct dimensions...")
        await vector_store_service.initialize_collection()

if __name__ == "__main__":
    asyncio.run(check_and_fix_collection())