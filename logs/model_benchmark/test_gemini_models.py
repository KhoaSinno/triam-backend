import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.GEMINI_BASE_URL,
    timeout=30.0
)

candidate_models = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
]

async def test_model(model_name: str):
    try:
        res = await client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Hello! Reply with 'OK'."}],
            max_tokens=10
        )
        text = res.choices[0].message.content.strip()
        print(f"[SUCCESS] Model '{model_name}' works! Response: {text}")
        return True
    except Exception as e:
        print(f"[FAILED] Model '{model_name}' error: {e}")
        return False

async def main():
    print("Testing candidate Gemini model names against Gemini API...")
    for m in candidate_models:
        await test_model(m)

if __name__ == "__main__":
    asyncio.run(main())
