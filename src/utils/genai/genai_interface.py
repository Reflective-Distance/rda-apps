"""
Generic interfaces for GenAI clients and services
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Protocol, runtime_checkable


@runtime_checkable
class GenAIResponseProtocol(Protocol):
    """Protocol defining what a GenAI response should be able to do"""
    
    def failure(self) -> bool:
        """Check if the response contains an error"""
        ...
        
    def unwrap(self) -> str:
        """Unwrap the response content"""
        ...


@runtime_checkable
class GenAIClientProtocol(Protocol):
    """Protocol defining what a GenAI client should be able to do"""
    
    base_url: str
    model: str
    
    def get_active_model_names(self) -> List[str]:
        """Get a list of active model names"""
        ...
        
    def completion(
        self, prompt: str, context: Optional[str] = None, 
        model: Optional[str] = None, temperature: float = 0
    ) -> GenAIResponseProtocol:
        """Process a completion request synchronously"""
        ...
        
    async def async_completion(
        self, prompt: str, context: Optional[str] = None, 
        model: Optional[str] = None, temperature: float = 0
    ) -> GenAIResponseProtocol:
        """Process a completion request asynchronously"""
        ...


class GenAIServiceInterface(ABC):
    """Base interface for GenAI services"""
    
    @abstractmethod
    def get_base_url(self) -> str:
        """Get the base URL used by the client"""
        pass
        
    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model used by the client"""
        pass
        
    @abstractmethod
    def get_active_model_names(self) -> List[str]:
        """Get a list of active model names"""
        pass
        
    @abstractmethod
    def process_single_prompt(
        self, content: str, context: Optional[str] = None,
        model: Optional[str] = None, temperature: float = 0
    ) -> GenAIResponseProtocol:
        """Process a single prompt synchronously"""
        pass
        
    @abstractmethod
    async def process_single_prompt_async(
        self, content: str, context: Optional[str] = None,
        model: Optional[str] = None, temperature: float = 0
    ) -> GenAIResponseProtocol:
        """Process a single prompt asynchronously"""
        pass
    