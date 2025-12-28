from typing import Dict, Any, List


class ValidationService:
    @staticmethod
    def validate_selected_text_mode(selected_text: str) -> bool:
        """
        Validate if the selected text is appropriate for the selected-text mode.
        
        Args:
            selected_text: The text selected by the user
            
        Returns:
            True if the selected text is valid, False otherwise
        """
        if not selected_text or not selected_text.strip():
            return False
        
        # Additional validation could be added here
        # For example, minimum length, content type, etc.
        if len(selected_text.strip()) < 5:  # Minimum 5 characters
            return False
            
        return True

    @staticmethod
    def validate_query_mode(query: str, mode: str, selected_text: str = None) -> Dict[str, Any]:
        """
        Validate the query parameters based on the mode.
        
        Args:
            query: The user's query
            mode: The mode ('global' or 'selected_text')
            selected_text: The selected text (required for selected_text mode)
            
        Returns:
            Dictionary with validation results
        """
        result = {
            "is_valid": True,
            "errors": []
        }
        
        # Validate query
        if not query or not query.strip():
            result["is_valid"] = False
            result["errors"].append("Query cannot be empty")
        
        # Validate mode
        if mode not in ["global", "selected_text"]:
            result["is_valid"] = False
            result["errors"].append("Mode must be either 'global' or 'selected_text'")
        
        # Validate selected_text if mode is selected_text
        if mode == "selected_text":
            if not selected_text:
                result["is_valid"] = False
                result["errors"].append("Selected text is required for selected_text mode")
            elif not ValidationService.validate_selected_text_mode(selected_text):
                result["is_valid"] = False
                result["errors"].append("Selected text is not valid")
        
        return result

    @staticmethod
    def validate_answer_content(answer: str, context: str) -> bool:
        """
        Validate that the answer is grounded in the provided context.
        
        Args:
            answer: The generated answer
            context: The context provided to generate the answer
            
        Returns:
            True if the answer is grounded in the context, False otherwise
        """
        # This is a simplified implementation
        # In a real implementation, you might use more sophisticated NLP techniques
        # to verify that the answer is grounded in the context
        
        if "not available in the provided book content" in answer.lower():
            # This is a valid response when information is not in the context
            return True
        
        # For now, we'll consider the answer valid if it's not empty
        # A more sophisticated implementation would check semantic similarity
        # between the answer and the context
        return len(answer.strip()) > 0