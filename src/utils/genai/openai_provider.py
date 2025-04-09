"""
OpenAI implementation of GenAI client
"""

from __future__ import annotations
import logging

import openai
from typing import Optional, List, Dict, Any, Type
from .genai_service import GenAIService

logger = logging.getLogger(__name__)


class GenAIResponse:
    @classmethod
    def from_response(cls, response: Any) -> GenAIResponse:
        return cls(response, exception=None)

    @classmethod
    def from_exception(cls, ex: Exception) -> GenAIResponse:
        return cls(response=None, exception=ex)

    def __init__(self, response: Any, exception: Optional[Exception] = None):
        self.error: Optional[str] = None
        self.response = None

        if exception:
            self.error = f"{str(exception)}"
        elif response:
            self.response = response
            if (
                hasattr(response, "error")
                and response.error
                and "message" in response.error
            ):
                self.error = response.error["message"]

    def failure(self) -> bool:
        return self.error is not None

    def unwrap(self) -> str:
        return self.error or self.response.choices[0].message.content.strip()

    def __repr__(self) -> str:
        return f"GenAIResponse(response={self.response}, error={self.error})"

    def __str__(self) -> str:
        return self.__repr__()


class OpenAIClient:
    """
    OpenAI implementation of the GenAI client protocol
    """

    def __init__(
        self,
        openai_client: Optional[openai.OpenAI] = None,
        async_openai_client: Optional[openai.AsyncOpenAI] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize the OpenAI Client with either provided OpenAI clients or create new ones.

        Args:
            openai_client: Pre-configured OpenAI client instance
            async_openai_client: Pre-configured AsyncOpenAI client instance
            base_url: Base URL for the OpenAI API, used if clients are not provided
            api_key: API key for the OpenAI API, used if clients are not provided
            model: Default model to use for completions
        """
        self.base_url = base_url
        self.model = model

        # Use provided clients or create new ones
        if openai_client is not None:
            self._client = openai_client
        elif base_url is not None and api_key is not None:
            self._client = openai.OpenAI(
                base_url=base_url,
                api_key=api_key,
            )
        else:
            raise ValueError(
                "Either provide an openai_client or both base_url and api_key"
            )

        if async_openai_client is not None:
            self._aclient = async_openai_client
        elif base_url is not None and api_key is not None:
            self._aclient = openai.AsyncOpenAI(
                base_url=base_url,
                api_key=api_key,
            )
        else:
            raise ValueError(
                "Either provide an async_openai_client or both base_url and api_key"
            )

    def get_active_models(self) -> List:
        return self._client.models.list()

    def get_active_model_names(self) -> List[str]:
        return [model.id for model in self.get_active_models()]

    def completion(
        self,
        prompt: str,
        context: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0,
    ) -> GenAIResponse:
        try:
            response = self._client.chat.completions.create(
                model=model or self.model,
                temperature=temperature,
                messages=self._build_messages(prompt, context),
            )
            return GenAIResponse.from_response(response)
        except openai.OpenAIError as e:
            logger.error(f"OpenAIError: {e}")
            return GenAIResponse.from_exception(e)

    async def async_completion(
        self,
        prompt: str,
        context: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0,
    ) -> GenAIResponse:
        try:
            response = await self._aclient.chat.completions.create(
                model=model or self.model,
                temperature=temperature,
                messages=self._build_messages(prompt, context),
            )
            return GenAIResponse.from_response(response)
        except openai.OpenAIError as e:
            logger.error(f"OpenAIError: {e}")
            return GenAIResponse.from_exception(e)

    def _build_messages(
        self, prompt: str, context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        messages = []
        if context:
            messages.append({"role": "developer", "content": context})
        messages.append({"role": "user", "content": prompt})
        return messages

    def __repr__(self) -> str:
        return f"OpenAIClient(model={self.model})"

    def __str__(self) -> str:
        return self.__repr__()


# Factory functions


def create_openai_client(
    base_url: str, api_key: str, default_model: Optional[str] = None
) -> OpenAIClient:
    """
    Create an OpenAIClient with the specified configuration.

    Args:
        base_url: The base URL for the OpenAI API
        api_key: The API key for authentication
        default_model: Optional default model to use

    Returns:
        Configured OpenAIClient instance
    """
    return OpenAIClient(base_url=base_url, api_key=api_key, model=default_model)


def create_genai_service(
    base_url: str,
    api_key: str,
    default_model: Optional[str] = None,
    client_class: Type = OpenAIClient,
) -> GenAIService:
    """
    Create a GenAIService with the specified client configuration.

    Args:
        base_url: The base URL for the API
        api_key: The API key for authentication
        default_model: Optional default model to use
        client_class: The client class to use (defaults to OpenAIClient)

    Returns:
        Configured GenAIService instance
    """
    client = client_class(base_url=base_url, api_key=api_key, model=default_model)
    return GenAIService(client)
