import asyncio

# Set default encoding to utf-8 for Windows console
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from google import genai

from app.core.config import settings


async def list_models():
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
        http_options={'api_version': 'v1beta'}
    )

    print("Listing models for v1beta:")
    # Try awaiting the list call first
    try:
        models = await client.aio.models.list()
        for model in models:
            print(f"Model: {model.name}")
            # Check for supported generation methods if available
            # Inspecting the model object to see attributes
            if hasattr(model, 'supported_generation_methods'):
                print(f"  Supported methods: {model.supported_generation_methods}")
            if hasattr(model, 'display_name'):
                print(f"  Display Name: {model.display_name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    asyncio.run(list_models())
