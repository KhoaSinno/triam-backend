import os

from dotenv import load_dotenv

# Load env variables
load_dotenv()


def test_tts():
    api_key = os.getenv("TTS_GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: TTS_GOOGLE_API_KEY not found in .env file!")
        return

    # Print masked key for safety
    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "Too short"
    print(f"🔑 Loaded API Key: {masked_key}")

    try:
        from google.api_core.client_options import ClientOptions
        from google.cloud import texttospeech
    except ImportError:
        print("❌ Error: google-cloud-texttospeech is not installed! Please run 'uv add google-cloud-texttospeech'.")
        return

    print("🚀 Initializing Google TTS Client using API Key...")
    try:
        options = ClientOptions(api_key=api_key)
        client = texttospeech.TextToSpeechClient(client_options=options)
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return

    text = "Xin chào, đây là thử nghiệm giọng đọc Google Chirp tiếng Việt chất lượng cao trong hệ thống Tri Âm."
    print(f"🗣️ Synthesizing text: '{text}'")

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure voice selection (using the production Iapetus Chirp 3 HD voice)
    voice = texttospeech.VoiceSelectionParams(language_code="vi-VN", name="vi-VN-Chirp3-HD-Iapetus")

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    try:
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        output_filename = "test_tts_output.mp3"
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)

        file_size = os.path.getsize(output_filename)
        print(f"✅ Success! Generated audio saved to '{output_filename}' ({file_size} bytes).")

    except Exception as e:
        print(f"❌ Google TTS API call failed: {e}")
        print("\n💡 Tip: If you get a permission or block error, double check that your API key restrictions in Google Cloud Console allow the 'Cloud Text-to-Speech API'.")


if __name__ == "__main__":
    test_tts()
