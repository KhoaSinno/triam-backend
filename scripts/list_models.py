import asyncio
import sys

from google import genai

from app.core.config import settings

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


async def list_models():
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
        http_options={"api_version": "v1beta"},
    )

    print("Listing models for v1beta:")
    try:
        models = await client.aio.models.list()
        for model in models:
            print(f"Model: {model.name}")
            if hasattr(model, "supported_generation_methods"):
                print(f"  Supported methods: {model.supported_generation_methods}")
            if hasattr(model, "display_name"):
                print(f"  Display Name: {model.display_name}")
    except Exception as e:
        print(f"Error listing models: {e}")


if __name__ == "__main__":
    asyncio.run(list_models())
