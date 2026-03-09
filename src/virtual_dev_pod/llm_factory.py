from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class LLMGateway(Protocol):
    provider: str
    model_id: str
    is_mock: bool
    reason: str

    def generate(self, prompt: str, *, max_tokens: int = 1200) -> str:
        ...


@dataclass
class MockLLM:
    provider: str = "mock"
    model_id: str = "mock"
    is_mock: bool = True
    reason: str = "Mock provider selected."

    def generate(self, prompt: str, *, max_tokens: int = 1200) -> str:
        _ = (prompt, max_tokens)
        return "MOCK_PROVIDER_ACTIVE"


@dataclass
class LangChainHuggingFaceEndpointLLM:
    model_id: str
    api_token: str
    temperature: float = 0.2
    default_max_tokens: int = 1200
    provider: str = "langchain_hf_endpoint"
    is_mock: bool = False
    reason: str = ""

    def __post_init__(self) -> None:
        try:
            from langchain_huggingface import HuggingFaceEndpoint
            from huggingface_hub import InferenceClient
        except Exception as exc:  # pragma: no cover - dependency boundary
            raise RuntimeError(
                "langchain-huggingface is not installed. Install dependencies first."
            ) from exc

        if not self.api_token:
            raise RuntimeError(
                "HUGGINGFACEHUB_API_TOKEN is required for langchain_hf_endpoint."
            )

        self._llm = HuggingFaceEndpoint(
            repo_id=self.model_id,
            huggingfacehub_api_token=self.api_token,
            max_new_tokens=self.default_max_tokens,
            temperature=self.temperature,
        )
        self._client = InferenceClient(model=self.model_id, token=self.api_token)
        self._conversation_mode = False

    def generate(self, prompt: str, *, max_tokens: int = 1200) -> str:
        if self._conversation_mode:
            return self._generate_conversational(prompt, max_tokens=max_tokens)

        try:
            result = self._llm.invoke(prompt)
            if isinstance(result, str):
                return result
            return str(result)
        except Exception as exc:
            if _is_conversational_only_error(exc):
                self._conversation_mode = True
                return self._generate_conversational(prompt, max_tokens=max_tokens)
            raise

    def _generate_conversational(self, prompt: str, *, max_tokens: int) -> str:
        messages = [{"role": "user", "content": prompt}]
        common_kwargs = {
            "messages": messages,
            "max_tokens": max_tokens or self.default_max_tokens,
            "temperature": self.temperature,
        }
        try:
            response = self._client.chat_completion(**common_kwargs)
            return _extract_chat_content(response)
        except TypeError:
            fallback_kwargs = dict(common_kwargs)
            fallback_kwargs.pop("temperature", None)
            response = self._client.chat_completion(**fallback_kwargs)
            return _extract_chat_content(response)
        except Exception:
            pass

        chat_attr = getattr(self._client, "chat", None)
        if chat_attr and hasattr(chat_attr, "completions"):
            try:
                response = chat_attr.completions.create(
                    model=self.model_id, **common_kwargs
                )
                return _extract_chat_content(response)
            except TypeError:
                fallback_kwargs = dict(common_kwargs)
                fallback_kwargs.pop("temperature", None)
                response = chat_attr.completions.create(
                    model=self.model_id, **fallback_kwargs
                )
                return _extract_chat_content(response)
        raise RuntimeError(
            "Conversation-mode fallback failed for this Hugging Face provider/model."
        )


@dataclass
class LangChainHuggingFaceLocalLLM:
    model_id: str
    temperature: float = 0.2
    default_max_tokens: int = 1200
    provider: str = "langchain_hf_local"
    is_mock: bool = False
    reason: str = ""

    def __post_init__(self) -> None:
        try:
            from langchain_community.llms import HuggingFacePipeline
            from transformers import (
                AutoModelForCausalLM,
                AutoTokenizer,
                pipeline as transformers_pipeline,
            )
        except Exception as exc:  # pragma: no cover - dependency boundary
            raise RuntimeError(
                "Local Hugging Face pipeline requires transformers and langchain-community."
            ) from exc

        tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        model = AutoModelForCausalLM.from_pretrained(self.model_id)
        pipe = transformers_pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=self.default_max_tokens,
            temperature=self.temperature,
        )
        self._llm = HuggingFacePipeline(pipeline=pipe)

    def generate(self, prompt: str, *, max_tokens: int = 1200) -> str:
        _ = max_tokens
        result = self._llm.invoke(prompt)
        if isinstance(result, str):
            return result
        return str(result)


def build_llm(
    provider: str,
    *,
    model_id: str,
    api_token: str | None,
    temperature: float,
    max_tokens: int,
    require_real_llm: bool = False,
) -> LLMGateway:
    normalized = provider.strip().lower()
    if normalized in {"mock", "offline"}:
        if require_real_llm:
            raise RuntimeError(
                "VDP_REQUIRE_REAL_LLM=true but VDP_LLM_PROVIDER is mock/offline."
            )
        return MockLLM(reason="Mock provider explicitly configured.")

    try:
        if normalized in {"langchain_hf_endpoint", "langchain_hf", "huggingface", "hf"}:
            return LangChainHuggingFaceEndpointLLM(
                model_id=model_id,
                api_token=api_token or "",
                temperature=temperature,
                default_max_tokens=max_tokens,
            )
        if normalized in {"langchain_hf_local", "hf_local"}:
            return LangChainHuggingFaceLocalLLM(
                model_id=model_id,
                temperature=temperature,
                default_max_tokens=max_tokens,
            )
    except Exception as exc:
        if require_real_llm:
            raise RuntimeError(
                f"Unable to initialize a real LLM for provider '{normalized}': {exc}"
            ) from exc
        return MockLLM(reason=f"LLM init failed for '{normalized}': {exc}")

    if require_real_llm:
        raise RuntimeError(f"Unsupported VDP_LLM_PROVIDER='{provider}'.")
    return MockLLM(reason=f"Unsupported provider '{provider}', using mock fallback.")


def llm_diagnostics(llm: LLMGateway) -> dict[str, str | bool]:
    return {
        "provider": llm.provider,
        "model_id": llm.model_id,
        "is_mock": llm.is_mock,
        "reason": llm.reason,
    }


def _is_conversational_only_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return (
        "not supported for task text-generation" in msg
        and "supported task: conversational" in msg
    )


def _extract_chat_content(response: object) -> str:
    choices = getattr(response, "choices", None)
    if choices and len(choices) > 0:
        message = getattr(choices[0], "message", None)
        if message is not None:
            content = getattr(message, "content", None)
            if content:
                return str(content)
    return str(response)
