"""
Groq LLM Client with automatic key rotation.
Tries GROQ_API_KEY1, GROQ_API_KEY2, GROQ_API_KEY3 in order.
Caches the first valid key for the lifetime of the process.
"""
import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../../.env"))

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

_active_key: Optional[str] = None


def _get_keys() -> list[str]:
    return [k for k in [
        os.getenv("GROQ_API_KEY1"),
        os.getenv("GROQ_API_KEY2"),
        os.getenv("GROQ_API_KEY3"),
    ] if k]


def _test_key(key: str) -> bool:
    """Returns True if the key is valid (HTTP 200)."""
    try:
        r = requests.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": "ping"}],
                "max_tokens": 5,
                "temperature": 0.0,
            },
            timeout=10,
        )
        return r.status_code == 200
    except Exception:
        return False


def get_active_key() -> str:
    """Return the first valid Groq API key, caching the result."""
    global _active_key
    if _active_key:
        return _active_key
    for key in _get_keys():
        if _test_key(key):
            _active_key = key
            return key
    raise RuntimeError("No valid Groq API key found. Check GROQ_API_KEY1/2/3 in .env")


def call_groq(
    prompt: str,
    system_prompt: str = "You are a helpful AI assistant.",
    max_tokens: int = 4096,
    temperature: float = 0.01,
    model: str = None,
) -> str:
    """
    Call Groq API with automatic key rotation.
    Returns the assistant message content as a string.
    """
    global _active_key
    model = model or GROQ_MODEL
    keys = _get_keys()

    # Try active key first, then fallback to others
    if _active_key:
        ordered_keys = [_active_key] + [k for k in keys if k != _active_key]
    else:
        ordered_keys = keys

    last_error = None
    for key in ordered_keys:
        try:
            r = requests.post(
                GROQ_API_URL,
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                timeout=60,
            )
            if r.status_code == 200:
                _active_key = key
                return r.json()["choices"][0]["message"]["content"]
            elif r.status_code in (401, 403, 429):
                # Key expired, rate limited, or invalid — try next
                if key == _active_key:
                    _active_key = None
                last_error = f"HTTP {r.status_code}: {r.text[:100]}"
                continue
            else:
                last_error = f"HTTP {r.status_code}: {r.text[:100]}"
                continue
        except Exception as e:
            last_error = str(e)
            continue

    raise RuntimeError(f"All Groq API keys failed. Last error: {last_error}")
