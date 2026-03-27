import os
from dataclasses import dataclass


class LLMProvider:
    async def complete(self, prompt: str) -> str:
        raise NotImplementedError


@dataclass
class MockLLMProvider(LLMProvider):
    async def complete(self, prompt: str) -> str:
        return f"MOCK_RESPONSE: {prompt[:180]}"


def get_provider(name: str = "mock") -> LLMProvider:
    if os.getenv("MOCK_LLM", "true").lower() == "true" or name == "mock":
        return MockLLMProvider()
    raise NotImplementedError(
        f"Provider '{name}' is not implemented. "
        "Set MOCK_LLM=true to use the mock provider, "
        "or add a real provider implementation (e.g. Ollama, OpenAI)."
    )
