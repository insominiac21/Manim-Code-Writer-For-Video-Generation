"""
Groq LLM Client with automatic key rotation and 429 cooldown tracking.
Tries GROQ_API_KEY1, GROQ_API_KEY2, GROQ_API_KEY3, GROQ_API_KEY4 in order.
Keys from the same Groq org share an org-level rate limit, so when all
keys are rate-limited we wait for the shortest cooldown to expire.
"""
import os
import time
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../../.env"))

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Tracks the earliest time each key is safe to use again (epoch seconds).
# Key = api_key string, Value = float timestamp.
_key_cooldown: dict[str, float] = {}


def _get_keys() -> list[str]:
    return [k for k in [
        os.getenv("GROQ_API_KEY1"),
        os.getenv("GROQ_API_KEY2"),
        os.getenv("GROQ_API_KEY3"),
        os.getenv("GROQ_API_KEY4"),
    ] if k]


def _mark_cooldown(key: str, retry_after_header: Optional[str] = None, default_sec: float = 60.0):
    """Mark a key as rate-limited until retry_after seconds from now."""
    try:
        wait = float(retry_after_header) if retry_after_header else default_sec
    except (TypeError, ValueError):
        wait = default_sec
    _key_cooldown[key] = time.time() + wait
    print(f"[Groq] Key ...{key[-6:]} rate-limited; cooldown {wait:.0f}s")


def _available_keys() -> list[str]:
    """Return keys that are not currently in cooldown, sorted by soonest available."""
    now = time.time()
    keys = _get_keys()
    available = [k for k in keys if _key_cooldown.get(k, 0) <= now]
    return available


def call_groq(
    prompt: str,
    system_prompt: str = "You are a helpful AI assistant.",
    max_tokens: int = 4096,
    temperature: float = 0.01,
    model: str = None,
) -> str:
    """
    Call Groq API with per-key cooldown tracking.
    If all keys are rate-limited, waits for the soonest one to become available.
    """
    model = model or GROQ_MODEL
    all_keys = _get_keys()
    if not all_keys:
        raise RuntimeError("No Groq API keys configured. Check GROQ_API_KEY1/2/3/4 in .env")

    def _is_success(resp) -> bool:
        """Distinguish real LLM content from HTTP error strings returned by _try_key."""
        if not resp:
            return False
        s = str(resp)
        return not s.startswith(("HTTP ", "Connection", "Read timed", "timeout", "Max retries"))

    last_error = None
    # One pass: try every available key
    for key in _available_keys():
        response = _try_key(key, model, system_prompt, prompt, max_tokens, temperature)
        if _is_success(response):
            return response
        last_error = response  # error string — continue to next key

    # All keys are in cooldown — wait for the soonest one
    now = time.time()
    soonest_key = min(all_keys, key=lambda k: _key_cooldown.get(k, 0))
    wait = max(0.0, _key_cooldown.get(soonest_key, 0) - now)
    if wait > 0:
        print(f"[Groq] All keys rate-limited. Waiting {wait:.1f}s for cooldown...")
        time.sleep(wait + 0.5)  # small buffer

    # Retry once after waiting
    for key in all_keys:
        if _key_cooldown.get(key, 0) <= time.time():
            response = _try_key(key, model, system_prompt, prompt, max_tokens, temperature)
            if _is_success(response):
                return response
            last_error = response

    raise RuntimeError(f"All Groq API keys failed. Last error: {last_error}")


def _try_key(key: str, model: str, system_prompt: str, prompt: str,
             max_tokens: int, temperature: float):
    """
    Attempt a single Groq API call with the given key.
    Returns the response string on success, or an error string on failure.
    """
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
            # Clear any cooldown on success
            _key_cooldown.pop(key, None)
            return r.json()["choices"][0]["message"]["content"]
        elif r.status_code == 429:
            retry_after = r.headers.get("retry-after") or r.headers.get("x-ratelimit-reset-requests")
            _mark_cooldown(key, retry_after, default_sec=60.0)
            return f"HTTP 429: {r.text[:200]}"
        elif r.status_code in (401, 403):
            _mark_cooldown(key, default_sec=3600.0)  # bad key — long cooldown
            return f"HTTP {r.status_code}: {r.text[:100]}"
        else:
            return f"HTTP {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return str(e)


# ---------------------------------------------------------------------------
# REMOVED: get_active_key() / _test_key()
# Those functions consumed real API quota just to validate keys on startup.
# Keys are now tested lazily when first used.
# ---------------------------------------------------------------------------
