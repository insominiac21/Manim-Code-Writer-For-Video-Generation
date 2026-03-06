

# Groq API Key Ping Utility
import os
import json
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

import requests

def ping_groq_keys():
    keys = [
        os.getenv("GROQ_API_KEY1"),
        os.getenv("GROQ_API_KEY2"),
        os.getenv("GROQ_API_KEY3")
    ]
    model = "llama-3.3-70b-versatile"
    test_prompt = "Ping: Respond with 'pong' if you are online."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers_template = lambda key: {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    for idx, key in enumerate(keys):
        if not key:
            print(f"❌ GROQ_API_KEY{idx+1} not found in .env")
            continue
        print(f"🔑 Testing GROQ_API_KEY{idx+1}...")
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": test_prompt}
            ],
            "max_tokens": 10,
            "temperature": 0.0
        }
        try:
            response = requests.post(url, headers=headers_template(key), json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                print(f"✅ GROQ_API_KEY{idx+1} is valid! Response: {reply.strip()[:80]}")
            elif response.status_code in (401, 403):
                print(f"❌ GROQ_API_KEY{idx+1} is expired or invalid.")
            else:
                print(f"❌ GROQ_API_KEY{idx+1} failed: {response.status_code} {response.text[:100]}")
        except Exception as e:
            print(f"❌ GROQ_API_KEY{idx+1} error: {e}")
    print("\n✅ All GROQ API key tests complete.")
    return None

if __name__ == "__main__":
    ping_groq_keys()
