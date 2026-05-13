"""
utils/llm_factory.py
Returns a configured ChatOpenAI or ChatAnthropic instance
based on the LLM_PROVIDER setting.
"""
from __future__ import annotations

from functools import lru_cache

from langchain_core.language_models.chat_models import BaseChatModel
from config.settings import LLM_PROVIDER, LLM_MODEL, OPENAI_API_KEY, ANTHROPIC_API_KEY


@lru_cache(maxsize=1)
def get_llm() -> BaseChatModel:
    """
    Lazily initialise and cache the LLM client.
    Supports 'openai' and 'anthropic' providers.
    """
    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=LLM_MODEL or "claude-3-5-sonnet-20241022",
            anthropic_api_key=ANTHROPIC_API_KEY,
            temperature=0,
        )

    # Default: OpenAI
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=LLM_MODEL or "gpt-4o",
        openai_api_key=OPENAI_API_KEY,
        temperature=0,
    )
