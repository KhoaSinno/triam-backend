import asyncio
import os
from livekit.plugins.google.realtime import RealtimeModel
from dotenv import load_dotenv
from livekit import agents

load_dotenv(".env")
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

async def main():
    try:
        model = RealtimeModel(api_key=api_key, voice="Puck", model="gemini-2.5-flash-native-audio-latest")
        print("Model created.")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
