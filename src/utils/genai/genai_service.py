"""
Implementation of a generic GenAI service
"""
from typing import Optional, List
from .genai_interface import GenAIClientProtocol, GenAIResponseProtocol, GenAIServiceInterface


class GenAIService(GenAIServiceInterface):
    def __init__(self, client: GenAIClientProtocol):
        """
        Initialize the Generative AI service with a client.
        
        Args:
            client: An instance implementing the GenAIClientProtocol
        """
        self.client = client

    def get_base_url(self) -> str:
        """Get the base URL used by the client."""
        return self.client.base_url

    def get_default_model(self) -> str:
        """Get the default model used by the client."""
        return self.client.model

    def get_active_model_names(self) -> List[str]:
        """Get a list of active model names."""
        return self.client.get_active_model_names()

    def process_single_prompt(
        self, content: str, context: Optional[str] = None, model: Optional[str] = None, temperature: float = 0
    ) -> GenAIResponseProtocol:
        """
        Process a single prompt synchronously.
        
        Args:
            content: The prompt content
            context: Optional context for the prompt
            model: Optional model override
            temperature: Temperature setting for response generation
            
        Returns:
            GenAIResponse object
        """
        return self.client.completion(content, context, model, temperature)

    async def process_single_prompt_async(
        self, content: str, context: Optional[str] = None, model: Optional[str] = None, temperature: float = 0
    ) -> GenAIResponseProtocol:
        """
        Process a single prompt asynchronously.
        
        Args:
            content: The prompt content
            context: Optional context for the prompt
            model: Optional model override
            temperature: Temperature setting for response generation
            
        Returns:
            GenAIResponse object
        """
        return await self.client.async_completion(content, context, model, temperature)
    
    