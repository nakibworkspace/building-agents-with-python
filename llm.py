"""
LocalLLM — interface every backend implements.

This is the seam. The agent above this file only knows about two things:
  1. Constructing a LocalLLM(model_path) where model_path encodes the provider.
  2. Calling .generate(prompt) -> str.

Everything below this file is provider-specific.
"""

import os
from typing import List, Optional

import requests

try:
    from llama_cpp import Llama  # noqa: F401
    _HAS_LLAMA_CPP = True
except ImportError:
    _HAS_LLAMA_CPP = False


class LocalLLM:
    """
    Provider-agnostic LLM client.

    Examples:
        LocalLLM("ollama:llama3.2:latest")       # Ollama backend
        LocalLLM("models/llama-3.gguf")          # llama-cpp-python (if installed)
    """

    def __init__(
        self,
        model_path: str,
        temperature: float = 0.2,
        max_tokens: int = 512,
        n_ctx: int = 2048,
    ):
        self.max_tokens = max_tokens
        self.temperature = temperature

        # Pick a backend
        if model_path.startswith("ollama:"):
            self.backend = OllamaBackend(model_path.split(":", 1)[1])
        elif model_path.endswith(".gguf") and _HAS_LLAMA_CPP:
            self.backend = LlamaCppBackend(model_path, n_ctx=n_ctx)
        else:
            # Fallback: assume it's an Ollama tag
            self.backend = OllamaBackend(model_path)

    def generate(self, prompt: str, temperature: float = None, stop: Optional[List[str]] = None) -> str:
        temp = temperature if temperature is not None else self.temperature
        return self.backend.generate(
            prompt=prompt,
            temperature=temp,
            max_tokens=self.max_tokens,
            stop=stop,
        )


# --- Backends ---


class OllamaBackend:
    """Calls a local Ollama server via HTTP."""

    def __init__(self, model: str):
        self.model = model
        self.base_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")
        # Fail fast so the user sees a clear error
        try:
            requests.get(f"{self.base_url}/api/tags", timeout=5).raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"Could not reach Ollama at {self.base_url}. "
                f"Is `ollama serve` running? Error: {e}"
            ) from e

    def generate(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        stop: Optional[List[str]],
    ) -> str:
        stop_seqs = stop if stop is not None else ["</s>", "\n\n", "User:", "Assistant:"]
        r = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "stop": stop_seqs,
                },
            },
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["response"].strip()


class LlamaCppBackend:
    """Loads a GGUF file directly via llama-cpp-python."""

    def __init__(self, model_path: str, n_ctx: int = 2048):
        from llama_cpp import Llama
        self.llama = Llama(model_path=model_path, n_ctx=n_ctx, verbose=False, seed=-1)

    def generate(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        stop: Optional[List[str]],
    ) -> str:
        stop_seqs = stop if stop is not None else ["</s>", "\n\n", "User:", "Assistant:"]
        response = self.llama(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop_seqs,
        )
        return response["choices"][0]["text"].strip()
