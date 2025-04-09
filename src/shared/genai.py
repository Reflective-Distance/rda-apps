from .environment import ensure_environment_initialized

ensure_environment_initialized()

import os
from utils.env_builder import require
from utils.genai import openai_provider as genai_provider

_genai_service = None


@require("GENAI_BASE_URL", "GENAI_API_KEY", "GENAI_DEFAULT_MODEL")
def get_service():
    """
    Returns the GenAI service, initializing it only on first call.
    """
    global _genai_service

    # Configuration values
    base_url = os.environ.get("GENAI_BASE_URL")
    api_key = os.environ.get("GENAI_API_KEY")
    default_model = os.environ.get("GENAI_DEFAULT_MODEL")

    if _genai_service is None:
        _genai_service = genai_provider.create_genai_service(
            base_url, api_key, default_model
        )

    return _genai_service


def reset_service():
    """
    Resets the GenAI service, forcing re-initialization on next use.
    Useful for updating configuration or in tests.
    """
    global _genai_service
    _genai_service = None
