import asyncio
import json
import os
import sys
import wave
import subprocess
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import httpx
from dotenv import load_dotenv
from livekit import rtc, api

# Load environment variables
load_dotenv()

BASE_URL = "http://127.0.0.1:8000/api/v1"
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "wss://tri-am-bmdl413w.livekit.cloud")
THREAD_ID = "07be00b9-c6da-4801-8ba2-7558205b92b2"
BOOK_ID = "195d9623-03d0-483a-ac09-52d9137f2471"
CONTEXT_ID = "dd123da9-95ed-4736-8c79-3161262c2a15"
VOICE_WAV = Path("Có-những-phương-pháp.wav")
LOCAL_AGENT_NAME = "triam-voice-agent-local"

def get_supabase_token() -> str:
    supabase_url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_KEY")
    email = os.getenv("SUPABASE_TEST_EMAIL")
    password = os.getenv("SUPABASE_TEST_PASSWORD")
    
    if not supabase_url or not anon_key or not email or not password:
        raise ValueError("Missing Supabase credentials in .env file")
        
    print(f"Logging in Supabase user: {email}...")
    url = f"{supabase_url.rstrip('/')}/auth/v1/token?grant_type=password"
    resp = httpx.post(
        url,
        headers={
            "apikey": anon_key,
            "Content-Type": "application/json",
        },
        json={
            "email": email,
            "password": password,
        },
        timeout=30,
    )
    resp.raise_for_status()
    payload = resp.json()
    return payload["access_token"]

def generate_local_livekit_token(thread_id: str, book_id: str, context_id: str) -> str:
    import uuid
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError("Missing LIVEKIT_API_KEY or LIVEKIT_API_SECRET in environment")
        
    room_name = f"triam_{thread_id[:8]}_{uuid.uuid4().hex[:6]}"
    print(f"Generating local token for Room: {room_name}")
    
    metadata = {
        "thread_id": thread_id,
        "context_id": context_id,
        "document_ids": [book_id],
    }
    
    agent_dispatch = api.RoomAgentDispatch(
        agent_name=LOCAL_AGENT_NAME,
        metadata=json.dumps(metadata),
    )
    room_config = api.RoomConfiguration(agents=[agent_dispatch])
    
    token = (
        api.AccessToken(api_key, api_secret)
        .with_identity(f"user_test_{uuid.uuid4().hex[:6]}")
        .with_grants(api.VideoGrants(room_join=True, room=room_name))
        .with_room_config(room_config)
    )
    
    return token.to_jwt()

async def check_db_messages(access_token: str, thread_id: str) -> list[dict]:
    print(f"Checking messages in database for thread: {thread_id}...")
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}/threads/{thread_id}/messages",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

async def publish_wav_as_mic(room: rtc.Room, wav_path: Path) -> None:
    with wave.open(str(wav_path), "rb") as wav:
        sample_rate = wav.getframerate()
        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        total_frames = wav.getnframes()

        if sample_width != 2:
            raise RuntimeError(f"WAV must be 16-bit PCM, got sample width={sample_width}")

        print(
            f"🎙️ Publishing WAV as mic track: {wav_path} "
            f"({sample_rate} Hz, {channels} ch, {total_frames / sample_rate:.2f}s)"
        )

        source = rtc.AudioSource(sample_rate, channels)
        track = rtc.LocalAudioTrack.create_audio_track("voice-question", source)
        options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE)
        await room.local_participant.publish_track(track, options)

        # Send audio in chunks
        chunk_ms = 20
        chunk_frames = sample_rate * chunk_ms // 1000
        
        while True:
            pcm = wav.readframes(chunk_frames)
            if not pcm:
                break
            samples_per_channel = len(pcm) // (sample_width * channels)
            frame = rtc.AudioFrame(
                pcm,
                sample_rate,
                channels,
                samples_per_channel,
            )
            await source.capture_frame(frame)
            await asyncio.sleep(chunk_ms / 1000)

    print("📤 Finished sending WAV audio track.")
    await source.wait_for_playout()
    await asyncio.sleep(1.0)

async def run_voice_test():
    print("=" * 60)
    print("🚀 RUNNING LOCALIZED VOICE AGENT TEST FLOW (DEV + ENV OVERRIDE)")
    print("=" * 60)

    if not VOICE_WAV.exists():
        raise FileNotFoundError(f"Missing WAV file: {VOICE_WAV}")

    # Backup and temporarily modify .env to override settings.LIVEKIT_AGENT_NAME
    env_path = Path(".env")
    if not env_path.exists():
        raise FileNotFoundError(".env file not found in project root")
        
    print("Backup and modifying .env file to override LIVEKIT_AGENT_NAME...")
    original_env = env_path.read_text(encoding="utf-8")
    
    try:
        lines = original_env.splitlines()
        modified_lines = []
        found = False
        for line in lines:
            if line.startswith("LIVEKIT_AGENT_NAME="):
                modified_lines.append(f"LIVEKIT_AGENT_NAME={LOCAL_AGENT_NAME}")
                found = True
            else:
                modified_lines.append(line)
        if not found:
            modified_lines.append(f"LIVEKIT_AGENT_NAME={LOCAL_AGENT_NAME}")
            
        env_path.write_text("\n".join(modified_lines), encoding="utf-8")
        
        # Step 1: Start local agent worker in 'dev' mode (automatically uses a random HTTP port)
        print(f"🎬 Starting local worker in DEV mode with overridden agent name: {LOCAL_AGENT_NAME}...")
        
        # We open a subprocess to run the worker in 'dev' mode
        worker_proc = subprocess.Popen(
            [sys.executable, "-m", "app.services.agent_voice_gpt_realtime", "dev"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Thread to read worker stdout and print it out to keep us updated
        def log_worker_output():
            print("--- LOCAL WORKER STARTING LOGS ---")
            for line in iter(worker_proc.stdout.readline, ""):
                print(f"[WORKER LOG] {line.strip()}")
                if "registered worker" in line or "initialized" in line:
                    print("--- LOCAL WORKER RUNNING ---")
            worker_proc.stdout.close()
            
        import threading
        log_thread = threading.Thread(target=log_worker_output, daemon=True)
        log_thread.start()
        
        # Give the worker a few seconds to boot and connect to LiveKit
        await asyncio.sleep(6.0)

        # Step 2: Login Supabase (to verify DB later)
        try:
            access_token = get_supabase_token()
            print("✅ Supabase login successful!")
        except Exception as e:
            print(f"❌ Supabase login failed: {e}")
            worker_proc.terminate()
            return

        # Step 3: Generate LiveKit Token targeting LOCAL_AGENT_NAME
        try:
            token = generate_local_livekit_token(THREAD_ID, BOOK_ID, CONTEXT_ID)
            print("✅ Custom LiveKit token generated targeting local worker!")
        except Exception as e:
            print(f"❌ Failed to generate LiveKit token: {e}")
            worker_proc.terminate()
            return

        # Step 4: Connect to LiveKit Room
        room = rtc.Room()
        greeting_received = asyncio.Event()
        user_voice_transcript_received = asyncio.Event()
        assistant_transcript_received = asyncio.Event()
        assistant_chat_received = asyncio.Event()

        transcripts = []
        chats = []

        @room.on("data_received")
        def on_data_received(packet: rtc.DataPacket):
            try:
                text = packet.data.decode("utf-8")
            except Exception:
                return

            sender = packet.participant.identity if packet.participant else "unknown"

            # Check for lk.chat messages (greeting or text outputs)
            if packet.topic == "lk.chat" and packet.participant and "agent" in sender.lower():
                if not greeting_received.is_set():
                    print(f"\n👋 [AGENT GREETING] Chat: {text}")
                    greeting_received.set()
                else:
                    print(f"\n💬 [AGENT REPLY] Chat: {text}")
                    chats.append(text)
                    assistant_chat_received.set()
                return

            # Check for transcripts
            if packet.topic != "lk.transcript":
                return

            try:
                payload = json.loads(text)
            except Exception:
                print(f"⚠️ Non-JSON transcript on lk.transcript: {text[:160]}")
                return

            if not isinstance(payload, dict) or payload.get("type") != "transcript":
                return

            role = str(payload.get("role", ""))
            body = str(payload.get("text", ""))
            if not body:
                return

            transcripts.append(payload)
            print(f"📝 [TRANSCRIPT] {role.upper()}: {body}")

            if role == "user":
                user_voice_transcript_received.set()
            elif role == "assistant" and greeting_received.is_set():
                assistant_transcript_received.set()

        print(f"🔌 Connecting to LiveKit URL: {LIVEKIT_URL}...")
        try:
            await room.connect(LIVEKIT_URL, token)
            print("✅ Connected to LiveKit room!")
        except Exception as e:
            print(f"❌ Connection to LiveKit room failed: {e}")
            worker_proc.terminate()
            return

        # Step 5: Wait for Agent Greeting
        print("⏳ Waiting for Agent greeting message...")
        try:
            # We give it plenty of time in case worker is still completing registration
            await asyncio.wait_for(greeting_received.wait(), timeout=45)
        except asyncio.TimeoutError:
            print("❌ Timeout waiting for agent greeting. Disconnecting...")
            await room.disconnect()
            worker_proc.terminate()
            return

        # Step 6: Send Wav File
        print("🎙️ Starting to play voice file...")
        try:
            await publish_wav_as_mic(room, VOICE_WAV)
        except Exception as e:
            print(f"❌ Error sending voice file: {e}")
            await room.disconnect()
            worker_proc.terminate()
            return

        # Step 7: Wait for transcripts and reply
        print("⏳ Waiting for transcription of user audio...")
        try:
            await asyncio.wait_for(user_voice_transcript_received.wait(), timeout=35)
        except asyncio.TimeoutError:
            print("⚠️ Timeout waiting for user voice transcription.")

        print("⏳ Waiting for agent reply...")
        try:
            await asyncio.wait_for(assistant_transcript_received.wait(), timeout=60)
        except asyncio.TimeoutError:
            print("⚠️ Timeout waiting for assistant transcript.")

        try:
            await asyncio.wait_for(assistant_chat_received.wait(), timeout=20)
        except asyncio.TimeoutError:
            print("⚠️ No assistant lk.chat payload received after voice response.")

        # Sleep a bit to allow final DB persistence on worker side
        print("⏳ Waiting for database sync...")
        await asyncio.sleep(4.0)

        # Step 8: Disconnect and terminate worker
        await room.disconnect()
        print("🔌 Disconnected from LiveKit room.")
        
        print("Stopping local worker process...")
        worker_proc.terminate()
        worker_proc.wait()
        print("✅ Local worker process stopped.")

    finally:
        # Step 9: Restore original .env file immediately
        print("Restoring original .env file...")
        env_path.write_text(original_env, encoding="utf-8")
        print("✅ Original .env file restored.")

    # Step 10: Verify DB
    try:
        messages = await check_db_messages(access_token, THREAD_ID)
        print(f"\n📊 Database Messages in thread {THREAD_ID}: {len(messages)}")
        for item in messages:
            role = "USER" if item.get("is_user") else "AGENT"
            text = str(item.get("text", ""))
            created_at = item.get("created_at")
            print(f"   [{created_at}] {role}: {text}")
    except Exception as e:
        print(f"❌ Failed to fetch database messages: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_voice_test())
    except KeyboardInterrupt:
        print("\nTest cancelled by user.")
