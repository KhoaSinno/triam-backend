# Flow Live Assistant Gemini (Voice-to-Voice Realtime Q&A)

## [Gemini: SDK genai](https://ai.google.dev/gemini-api/docs/live-api/get-started-sdk)

## 1. Set up WebSocket, Gemini Live Session

- **Aim:** Set up real-time connection with lowest latency between Client and AI model.

- **Logic flow:**
  - **Flutter:**
    - Send request WebSocket to endpoint `/ws/live-assistant/{book_id}`.
    - Setup AudioRecorder (PCM 16-bit, 16kHz, mono) và AudioPlayer engine (available PCM 24kHz).
  - **Backend:**
    - Accept WebSocket connection.
    - Create `genai.Client.aio.live.connect` with model `gemini-2.5-flash-native-audio-latest`.
    - Prompting `SYSTEM_INSTRUCTION` (role TRIAM as assistant) and registering 2 tools: `search_book_knowledge` and `search_web`.

## 2. Full-Duplex Streaming

- **Aim:** Listening user speech and responding with audio simultaneously (operating like a phone call).

- **Logic flow:**
  - **Backend run background tasks parallel (`asyncio.gather`):**
    - **Process 1 (`send_to_gemini`):**
      - Listen for raw PCM bytes from WebSocket (Flutter sends them).
      - Stream these audio chunks directly to Gemini via the `send_realtime_input` function.
    - **Process 2 (`receive_from_gemini`):**
      - Continuously receive responses from Gemini through the `async for response in session.receive()` loop.
      - If the response contains audio data (`inline_data`), the backend sends the byte chunks directly (24kHz PCM) back to Flutter via WebSocket for immediate playback (without waiting for the AI to finish speaking the entire sentence).

## 3. Active Tool Calling (RAG + Web Search)

- **Aim:** Providing information from books or internet when users ask specific questions, instead of letting the AI "fabricate" answers (hallucination).

- **Logic flow:**
  - While (`receive_from_gemini`), if see `tool_call` return, Backend will pause streaming audio and execute the tool function:
    - **Case 1: `search_book_knowledge` (Priority)**
      - Get the User's question (e.g., "Tại sao tác giả nói Quả trứng có trước con gà?").
      - Use the `AsyncOpenAI` library (`text-embedding-3-small`) to convert the question into a vector (Embedding).
      - Call the RPC `match_book_knowledge` down to Supabase to query vector similarity, scanning text chunks within the current `book_id`.
    - **Case 2: `search_web`**
      - Call the Tavily API (`AsyncTavilyClient`) to search for real-time/update information on the web.
  - **Send response back to AI:**
    - Aggregate the retrieved text content.
    - Send the results back to Gemini through `session.send_tool_response`.
    - Gemini reads this context, understands the issue, and continues generating audio responses for the user (returning to step 2).

## 4. Graceful Disconnect

- **Aim:** Free up hardware resources and network when the conversation ends.
- **Logic flow:**
  - **Flutter:** The user presses the stop button -> Stop recording -> Close WebSocket sink.
  - **Backend:**
    - Catch the `WebSocketDisconnect` exception.
    - Stop the asyncio loops, automatically disconnect from the Gemini Live Session to prevent memory leaks.
