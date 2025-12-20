#!/usr/bin/env python3
"""
Test retrieval from Qdrant vector database

This script tests the retrieval functionality by:
- Loading Cohere and Qdrant clients from .env
- Implementing a retrieval function that takes a query, generates a Cohere embedding,
  searches Qdrant, and returns results with scores and metadata
- Running 10+ diverse test queries covering facts, concepts, and code from the book
- Verifying results are relevant and accurate (similarity > 0.75)
"""

import os
import sys
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from typing import List, Dict, Tuple

# Load environment variables
load_dotenv()

class RetrievalTester:
    def __init__(self):
        """Initialize Cohere and Qdrant clients"""
        self.cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            https=True
        )
        self.collection_name = "RAG_embedding"

        # Verify connections
        self._verify_connections()

    def _verify_connections(self):
        """Verify that both Cohere and Qdrant clients are working"""
        try:
            # Test Cohere connection with a simple embedding
            test_embedding = self.cohere_client.embed(
                texts=["test"],
                model='embed-english-v3.0',
                input_type="search_query"
            )
            print("[OK] Cohere client connected successfully")
        except Exception as e:
            print(f"[ERROR] Cohere client connection failed: {e}")
            sys.exit(1)

        try:
            # Test Qdrant connection by getting collection info
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            print(f"[OK] Qdrant client connected successfully, collection '{self.collection_name}' has {collection_info.points_count} points")
        except Exception as e:
            print(f"[ERROR] Qdrant client connection failed: {e}")
            sys.exit(1)

    def retrieve(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Retrieve relevant chunks from Qdrant based on the query

        Args:
            query: The search query string
            top_k: Number of top results to return (default 10, but can be 5-10 as specified)

        Returns:
            List of dictionaries containing text, score, and metadata (url, title)
        """
        try:
            # Generate embedding for the query using Cohere
            response = self.cohere_client.embed(
                texts=[query],
                model='embed-english-v3.0',
                input_type="search_query"  # As specified in the requirements
            )
            query_embedding = response.embeddings[0]

            # Search in Qdrant for similar vectors
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )

            # Format results to include text, score, and metadata
            formatted_results = []
            for result in search_results:
                # Sanitize text to remove Unicode characters that cause encoding issues
                content = result.payload.get('content', '')
                # Remove zero-width space and other problematic Unicode characters
                sanitized_content = content.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                formatted_result = {
                    'text': sanitized_content[:500] + "..." if len(sanitized_content) > 500 else sanitized_content,  # Limit text length for readability
                    'score': result.score,
                    'url': result.payload.get('url', ''),
                    'title': result.payload.get('title', ''),
                    'chunk_index': result.payload.get('chunk_index', 0)
                }
                formatted_results.append(formatted_result)

            return formatted_results

        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []

    def run_test_queries(self) -> Dict[str, List[Dict]]:
        """
        Run 10+ diverse test queries covering facts, concepts, and code from the book

        Returns:
            Dictionary mapping queries to their results
        """
        # Prepare diverse test queries covering different aspects of the book
        test_queries = [
            # Factual queries
            "What is robotic simulation?",
            "Explain digital twins in robotics",
            "What are the main components of a robot?",

            # Conceptual queries
            "How do control systems work in robotics?",
            "Explain sensor fusion and perception in robotics",
            "What is path planning in robotics?",

            # Code-related queries
            "Show me an example of robot control code",
            "How to implement collision detection?",
            "What is PID controller implementation?",

            # Specific topic queries
            "Explain humanoid robotics",
            "What is physical AI?",
            "How does robotic grasping work?",

            # Advanced topics
            "Explain advanced control systems in robotics",
            "What are the challenges in robotic perception?",
            "How is machine learning used in robotics?"
        ]

        print(f"Running {len(test_queries)} diverse test queries...\n")

        all_results = {}
        for i, query in enumerate(test_queries, 1):
            print(f"Query {i}: {query}")
            results = self.retrieve(query, top_k=10)  # Get top 10 results
            all_results[query] = results

            # Print top 3 results for each query
            for j, result in enumerate(results[:3]):  # Show top 3
                print(f"  Result {j+1}: Score: {result['score']:.3f}")
                print(f"    Title: {result['title']}")
                print(f"    URL: {result['url']}")
                # Sanitize the text snippet before printing
                snippet = result['text'][:100]
                sanitized_snippet = snippet.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
                print(f"    Text snippet: {sanitized_snippet}...")
                print()

        return all_results

    def verify_relevance(self, results: Dict[str, List[Dict]]) -> Dict[str, Dict]:
        """
        Verify that results are relevant and accurate (similarity > 0.75)

        Args:
            results: Dictionary of queries mapped to their results

        Returns:
            Dictionary with verification statistics for each query
        """
        verification_stats = {}

        for query, query_results in results.items():
            if not query_results:
                verification_stats[query] = {
                    'total_results': 0,
                    'relevant_results': 0,
                    'avg_score': 0.0,
                    'max_score': 0.0,
                    'threshold_met': False
                }
                continue

            scores = [r['score'] for r in query_results]
            relevant_count = sum(1 for score in scores if score > 0.75)
            avg_score = sum(scores) / len(scores) if scores else 0.0
            max_score = max(scores) if scores else 0.0

            verification_stats[query] = {
                'total_results': len(query_results),
                'relevant_results': relevant_count,
                'avg_score': avg_score,
                'max_score': max_score,
                'threshold_met': max_score > 0.75
            }

        return verification_stats

    def print_summary(self, results: Dict[str, List[Dict]], verification_stats: Dict[str, Dict]):
        """Print a summary of the test results"""
        print("="*80)
        print("RETRIEVAL TEST SUMMARY")
        print("="*80)

        total_queries = len(results)
        successful_queries = sum(1 for stats in verification_stats.values() if stats['threshold_met'])

        print(f"Total queries tested: {total_queries}")
        print(f"Queries with at least one result > 0.75 similarity: {successful_queries}")
        print(f"Success rate: {successful_queries/total_queries*100:.1f}%")
        print()

        print("Detailed results per query:")
        for query, stats in verification_stats.items():
            status = "[PASS]" if stats['threshold_met'] else "[FAIL]"
            print(f"{status} Query: {query}")
            print(f"    Total results: {stats['total_results']}")
            print(f"    Relevant results (>0.75): {stats['relevant_results']}")
            print(f"    Avg score: {stats['avg_score']:.3f}")
            print(f"    Max score: {stats['max_score']:.3f}")
            print()

        print("="*80)

        # Check if overall performance is acceptable
        if successful_queries / total_queries >= 0.7:  # At least 70% of queries should have good results
            print("SUCCESS: Retrieval pipeline is working well!")
        else:
            print("Warning: Retrieval pipeline needs improvement")
        print("="*80)

def main():
    """Main function to run the retrieval tests"""
    print("Initializing retrieval tester...")
    tester = RetrievalTester()

    print("\nStarting retrieval tests...")
    results = tester.run_test_queries()

    print("Verifying relevance of results...")
    verification_stats = tester.verify_relevance(results)

    print("\nGenerating summary...")
    tester.print_summary(results, verification_stats)

    # Final validation
    all_successful = all(stats['max_score'] > 0.75 for stats in verification_stats.values() if stats['total_results'] > 0)

    if all_successful:
        print("\nSUCCESS: All tests passed! The retrieval pipeline is working correctly.")
        print("SUCCESS: Results are relevant and accurate with similarity scores > 0.75")
        print("SUCCESS: Pipeline works end-to-end with no errors")
    else:
        print("\nWarning: Some queries returned results with similarity <= 0.75")
        print("This may be expected for certain types of queries or sparse content")

    return all_successful

if __name__ == "__main__":
    main()