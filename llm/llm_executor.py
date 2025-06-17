from typing import List, Dict, Any
from openai import OpenAI
from llm.prompt_constants import SYSTEM_PROMPT


class IMessageBuilder:
    """Interface for building messages for LLM loads."""

    def build(self, user_content: List[Dict[str, Any]]) -> list:
        raise NotImplementedError


class OpenAIMessageBuilder(IMessageBuilder):
    """Builds messages in OpenAI API format."""

    def build(self, user_content: List[Dict[str, Any]]) -> list:
        messages = [
            {"role": "system", "content": [{"type": "text", "text": SYSTEM_PROMPT}]},
            {"role": "user", "content": user_content},
        ]
        return messages


class ILLMClient:
    """Interface for LLM client."""

    def create_completion(self, model: str, messages: list, **kwargs) -> str:
        raise NotImplementedError


class OpenAILLMClient(ILLMClient):
    """OpenAI LLM client implementation."""

    def __init__(self):
        self.client = OpenAI()

    def create_completion(self, model: str, messages: list, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=model, messages=messages, **kwargs
        )
        # Assumes response.choices[0].message.content is the answer
        return response.choices[0].message.content if response.choices else ""


class LlmExecutor:
    """
    Handles OpenAI chat completions using SOLID and Clean Code principles.
    """

    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        temperature: float = 0.4,
        max_tokens: int = 5552,
        message_builder: IMessageBuilder = None,
        llm_client: ILLMClient = None,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.message_builder = message_builder or OpenAIMessageBuilder()
        self.llm_client = llm_client or OpenAILLMClient()

    def run_completion(
        self,
        user_content: List[Dict[str, Any]],
        response_format: dict = {"type": "text"},
        top_p: float = 1,
        frequency_penalty: float = 0,
        presence_penalty: float = 0,
    ) -> str:
        messages = self.message_builder.build(user_content)
        return self.llm_client.create_completion(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format=response_format,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
