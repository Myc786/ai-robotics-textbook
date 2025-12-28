import cohere
import openai
from typing import List, Dict, Any
from src.config.settings import settings
from src.models.response import RetrievedChunk
import time


class GenerationService:
    def __init__(self):
        self.cohere_client = cohere.Client(api_key=settings.cohere_api_key)

        # Set up OpenRouter if API key is available
        if settings.openrouter_api_key:
            self.openrouter_client = openai.OpenAI(
                api_key=settings.openrouter_api_key,
                base_url=settings.openrouter_base_url
            )
            self.model = settings.openrouter_model
            self.use_openrouter = True
        else:
            self.model = "command-r-plus"  # Using Cohere's command model for generation
            self.use_openrouter = False

    async def generate_response(self, query: str, context_chunks: List[Dict[str, Any]],
                               temperature: float = 0.1) -> Dict[str, Any]:
        """
        Generate a response based on the query and provided context chunks.

        Args:
            query: The user's query
            context_chunks: List of relevant context chunks
            temperature: Generation temperature (lower for more deterministic)

        Returns:
            Dictionary containing response text, confidence, and metadata
        """
        # Build the context from chunks
        context = ""
        for i, chunk in enumerate(context_chunks):
            context += f"Document {i+1}: {chunk['content']}\n\n"

        # Build the prompt
        prompt = f"""
        You are an assistant that answers questions based only on the provided documents.
        Your answer must be grounded in the provided documents and you must not make up any information.
        If the answer is not available in the provided documents, respond with: "This information is not available in the provided book content."

        Documents:
        {context}

        Question: {query}

        Answer:
        """

        # Generate response using either Cohere or OpenRouter
        if self.use_openrouter:
            # Use OpenRouter API
            response = self.openrouter_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=500
            )
            response_text = response.choices[0].message.content.strip()
        else:
            # Use Cohere API
            response = self.cohere_client.chat(
                model=self.model,
                message=prompt,
                temperature=temperature,
                max_tokens=500,
                stop_sequences=["Question:", "Answer:"]
            )
            response_text = response.text.strip()

        # Calculate confidence based on the model's confidence indicators
        # For now, using a simple approach - in practice, this could be more sophisticated
        response_text = response_text

        # Determine confidence
        confidence = self._calculate_confidence(response_text, context_chunks)

        return {
            "response_text": response_text,
            "confidence_score": confidence,
            "retrieved_chunks": context_chunks
        }

    def _calculate_confidence(self, response_text: str, context_chunks: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence in the generated response.
        
        Args:
            response_text: The generated response text
            context_chunks: The context chunks used for generation
            
        Returns:
            Confidence score between 0 and 1
        """
        # If the response indicates the information is not available, return low confidence
        if "not available in the provided book content" in response_text.lower():
            return 0.0
        
        # Calculate confidence based on how much of the context was used
        # This is a simplified approach - more sophisticated methods could analyze
        # semantic similarity between context and response
        if context_chunks:
            # Base confidence on the average similarity score of retrieved chunks
            avg_similarity = sum(chunk.get("similarity_score", 0) for chunk in context_chunks) / len(context_chunks)
            return min(avg_similarity, 1.0)  # Ensure it doesn't exceed 1.0
        else:
            return 0.0

    async def generate_refusal_response(self) -> Dict[str, Any]:
        """
        Generate a standard refusal response when information is not found.
        
        Returns:
            Dictionary containing refusal response
        """
        return {
            "response_text": "This information is not available in the provided book content.",
            "confidence_score": 0.0,
            "retrieved_chunks": []
        }

    async def validate_response_quality(self, query: str, response: str, context_chunks: List[Dict[str, Any]]) -> bool:
        """
        Validate if the generated response is of sufficient quality.
        
        Args:
            query: The original query
            response: The generated response
            context_chunks: The context chunks used
            
        Returns:
            True if response quality is acceptable, False otherwise
        """
        # Check if response is a refusal message
        if "not available in the provided book content" in response.lower():
            return True  # This is a valid response type
        
        # Check if response is not empty and seems relevant
        if len(response.strip()) > 0:
            # Simple check: response should contain some information
            return True
        
        return False