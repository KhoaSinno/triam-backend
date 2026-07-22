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

async def test_36():
    try:
        res = await client.chat.completions.create(
            model="gemini-3.6-flash",
            messages=[{"role": "user", "content": "Hello! Reply with 'OK'."}]
        )
        print("Response for gemini-3.6-flash:")
        print("  choice:", res.choices[0])
        print("  content:", repr(res.choices[0].message.content))
    except Exception as e:
        print("Error testing gemini-3.6-flash:", type(e), e)

if __name__ == "__main__":
    asyncio.run(test_36())
