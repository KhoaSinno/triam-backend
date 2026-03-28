import asyncio

from google import genai

from app.core.config import settings


async def check_model():
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
        http_options={'api_version': 'v1beta'}
    )

    model_id = "gemini-2.5-flash-native-audio-latest"
    print(f"Checking model: {model_id}")
    try:
        model = await client.aio.models.get(model=model_id)
        print(f"Model found: {model.name}")
        print(f"Supported methods: {model.supported_generation_methods}")
    except Exception as e:
        print(f"Error getting model: {e}")

if __name__ == "__main__":
    asyncio.run(check_model())
