Lenovo@KhoaSinoo MINGW64 /w/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend (dev)
$ uv run python -m app.services.agent_voice_gpt_realtime console
    Agents   Starting console mode 🚀
              
2026-05-17 09:01:26.702 | DEBUG    | logging:callHandlers:1762 - Using proactor: IocpProactor
    09:01:26.701 DEBUG    asyncio            Using proactor: IocpProactor  
2026-05-17 09:01:26.706 | INFO     | logging:callHandlers:1762 - starting worker
    09:01:26.706 INFO     livekit.agents     starting worker {"version": "1.5.8", "rtc-version": "1.1.7"}
2026-05-17 09:01:26.710 | INFO     | logging:callHandlers:1762 - plugin registered
    09:01:26.710 INFO     livekit.agents     plugin registered {"plugin": "livekit.plugins.openai", "version": "1.5.8"}
2026-05-17 09:01:26.715 | INFO     | logging:callHandlers:1762 - HTTP server listening on :51907
    09:01:26.715 INFO     livekit.agents     HTTP server listening on :51907  
2026-05-17 09:01:26.721 | WARNING  | logging:callHandlers:1762 - no warmed process available for job, waiting for one to be created
    09:01:26.721 WARNING  livekit.agents     no warmed process available for job, waiting for one to be created {"job_id": "mock-job-eab5db27271c"}
2026-05-17 09:01:26.728 | INFO     | logging:callHandlers:1762 - initializing job runner
    09:01:26.728 INFO     livekit.agents     initializing job runner {"tid": 9368}
2026-05-17 09:01:26.731 | DEBUG    | logging:callHandlers:1762 - Using proactor: IocpProactor
    09:01:26.731 DEBUG    asyncio            Using proactor: IocpProactor  
2026-05-17 09:01:26.733 | INFO     | logging:callHandlers:1762 - job runner initialized
                 INFO     livekit.agents     job runner initialized {"tid": 9368, "elapsed_time": 0.0}
2026-05-17 09:01:26.777 | INFO     | __main__:entrypoint:221 - ✅ Document IDs từ metadata: ['1b893d40-e0cc-4ee3-ae5f-a7809834e6dd']
2026-05-17 09:01:26.778 | INFO     | __main__:entrypoint:222 - 🏠 Room Name (session): console
2026-05-17 09:01:26.778 | INFO     | __main__:entrypoint:223 - Bat dau phien doc sach cho Thread ID: 5bb8da1d-7326-4d67-b0b3-0b4dd9bb17d7
2026-05-17 09:01:26.807 | INFO     | __main__:entrypoint:510 - Starting realtime session with model: gpt-realtime, voice: cedar
2026-05-17 09:01:26.838 | DEBUG    | logging:callHandlers:1762 - http_session(): creating a new httpclient ctx
    09:01:26.838 DEBUG    livekit.agents     http_session(): creating a new httpclient ctx  
2026-05-17 09:01:26.842 | DEBUG    | logging:callHandlers:1762 - using audio io: `Console` -> `AgentSession` -> `TranscriptSynchronizer` -> `Console`
    09:01:26.842 DEBUG    livekit.agents     using audio io: `Console` -> `AgentSession` -> `TranscriptSynchronizer` -> `Console`  
2026-05-17 09:01:26.845 | DEBUG    | logging:callHandlers:1762 - using transcript io: `AgentSession` -> `TranscriptSynchronizer`
    09:01:26.845 DEBUG    livekit.agents     using transcript io: `AgentSession` -> `TranscriptSynchronizer`  
   Microphone Array (Realtek(R) Au   ▃ ▆ █ ▅ ▂ ▁ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:28.477 DEBUG    livekit.agents     aec warmup active, disabling interruptions for 3.00s  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▄ ▄ ▃ ▂ ▅ ▆ ▆ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:31.478 DEBUG    livekit.agents     aec warmup expired, re-enabling interruptions  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:41.798 DEBUG    livekit.agents     executing tool  
                                         {"function": "search_book_knowledge", "arguments": "{  \n  \"query\": \"Người dùng đang đọc cuốn sách nào hiện tại?\" \n}  \n", "speech_id": 
"speech_77b41c739b1e"}
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.674 DEBUG    hpack.hpack        Adding (b':method', b'POST') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.681 DEBUG    hpack.hpack        Encoding 3 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.684 DEBUG    hpack.hpack        Adding (b':authority', b'drlbwntplyteqvrpnmdi.supabase.co') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.690 DEBUG    hpack.hpack        Encoding 1 with 6 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.693 DEBUG    hpack.hpack        Encoding 24 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.696 DEBUG    hpack.hpack        Adding (b':scheme', b'https') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.700 DEBUG    hpack.hpack        Encoding 7 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.703 DEBUG    hpack.hpack        Adding (b':path', b'/rest/v1/rpc/match_book_knowledge') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.707 DEBUG    hpack.hpack        Encoding 4 with 6 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.711 DEBUG    hpack.hpack        Encoding 24 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.714 DEBUG    hpack.hpack        Adding (b'accept', b'*/*') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.718 DEBUG    hpack.hpack        Encoding 19 with 6 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.722 DEBUG    hpack.hpack        Encoding 3 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.726 DEBUG    hpack.hpack        Adding (b'accept-encoding', b'gzip, deflate, zstd') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.728 DEBUG    hpack.hpack        Encoding 16 with 6 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.733 DEBUG    hpack.hpack        Encoding 15 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.736 DEBUG    hpack.hpack        Adding (b'user-agent', b'python-httpx/0.28.1') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.739 DEBUG    hpack.hpack        Encoding 58 with 6 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▃ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.744 DEBUG    hpack.hpack        Encoding 14 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.748 DEBUG    hpack.hpack        Adding (b'x-client-info', b'supabase-py/2.28.3') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.750 DEBUG    hpack.hpack        Encoding 10 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.755 DEBUG    hpack.hpack        Encoding 13 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.760 DEBUG    hpack.hpack        Adding (b'x-supabase-client-platform', b'Windows') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.764 DEBUG    hpack.hpack        Encoding 19 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.767 DEBUG    hpack.hpack        Encoding 6 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.771 DEBUG    hpack.hpack        Adding (b'x-supabase-client-platform-version', b'11') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.774 DEBUG    hpack.hpack        Encoding 24 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.779 DEBUG    hpack.hpack        Encoding 2 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.782 DEBUG    hpack.hpack        Adding (b'x-supabase-client-runtime', b'python') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.785 DEBUG    hpack.hpack        Encoding 18 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.790 DEBUG    hpack.hpack        Encoding 5 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.793 DEBUG    hpack.hpack        Adding (b'x-supabase-client-runtime-version', b'3.12.12') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.796 DEBUG    hpack.hpack        Encoding 23 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.800 DEBUG    hpack.hpack        Encoding 5 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  
    09:01:43.803 DEBUG    hpack.hpack        Adding (b'apikey',                                                                                                                                     
                                             b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRybGJ3bnRwbHl0ZXF2cnBubWRpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUzO…  
                                             to the header table, sensitive:False, huffman:True                                                                                                     
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.808 DEBUG    hpack.hpack        Encoding 5 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.811 DEBUG    hpack.hpack        Encoding 176 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  
    09:01:43.815 DEBUG    hpack.hpack        Adding (b'authorization', b'Bearer                                                                                                                     
                                             eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRybGJ3bnRwbHl0ZXF2cnBubWRpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUzOTU…  
                                             to the header table, sensitive:True, huffman:True                                                                                                      
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.818 DEBUG    hpack.hpack        Encoding 23 with 4 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.823 DEBUG    hpack.hpack        Encoding 181 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.828 DEBUG    hpack.hpack        Adding (b'accept-profile', b'public') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.832 DEBUG    hpack.hpack        Encoding 10 with 7 bits  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.906 DEBUG    hpack.hpack        Encoding 5 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.910 DEBUG    hpack.hpack        Adding (b'content-profile', b'public') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.912 DEBUG    hpack.hpack        Encoding 11 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.916 DEBUG    hpack.hpack        Encoding 5 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.928 DEBUG    hpack.hpack        Adding (b'content-length', b'29513') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.931 DEBUG    hpack.hpack        Encoding 28 with 6 bits  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.935 DEBUG    hpack.hpack        Encoding 4 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.939 DEBUG    hpack.hpack        Adding (b'content-type', b'application/json') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.941 DEBUG    hpack.hpack        Encoding 31 with 6 bits  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:43.945 DEBUG    hpack.hpack        Encoding 11 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  2026-05-17 09:01:43.948 | DEBUG    | logging:callHandlers:1762 - Encoded header block to b"\x83A\x98\x92\xca#\xf1Rk\xa3\xd2K\xdb\xbd\x95\xd5L\x86]\x16\xd68\xc6\x82\xaeC\xff\x87D\x98b\xc2\xa1,w\x0b\x16VF)\x1aI<Q\x9c\xfdb\xebQ\xfcPY&/S\x83\xf9c\xe7P\x8f\x9b\xd9\xab\xfaRB\xcb@\xd2_\xa5=\xa12\x7fz\x8e\xaf\xd2g=KN\x94\xd7\xe5\x80.'\x97\x0f@\x8a\xf2\xb1(1jJ\xc6\xaaS\xff\x8dE\xb5\x8e1\xa0\xabW\xe9\x81.'\x97g@\x93\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%j\xe8\x1ae=\x94\xff\x86\xe4j\xa4?\x84\x7f@\x98\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%j\xe8\x1ae=\x94\xad\xdc\xb6 \xc7\xab\x82\x08\x7f@\x92\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%k-\xa9&\xa4\xbf\x85\xaf\xd2g=_@\x97\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%k-\xa9&\xa4\xabw-\x881\xea\x85ep\x89p\x8b@\x85\x1df\xea__\xff1/\xac\xb3\xc7\x88\x86\xd4l\xb98{\xc8\x1d&\xc8\x8c\x95ml\x97\xb29\x93\xad\x7f\x9coe}r\xfa\xcbY\x19\xd0mF\xcb\xeeO\xcb\xb3\xf3\xa7\x0f\xbf\xdd\xd9\x11\x92\xac\xb4~\x9b#\x99)\xdb\xea<YY\x8e\xad\xbe#\xc7@?\x7f0\x88\x95]\xb6>[k\xc8o\x06%/\xa3\xf7vG2U\xa6\x82U\xfb_1q\x94\x94\xbe\x8f\xdd\xd9\x11\x92\x9a'\x92\xf6G4o#:/\xf0\xf7\xab\x7f\x0fzox7\xef\xe4\xfe2t?\xad\x17\xe6\x16\x8d\xf8\x03\xa7~\x80K\xb1q\xc2\xed\x19\xbdc>-\xc0\xef3\xe4\xedu\xd0\xb7\xb4\x9a\x857o\xce\xc0\xeb\xe4\xbds\xf7\xdb\xef\xde3\x19\xcc\x9f\x1f\x08\xff6\xbaQ\xd8[\x14/\xac\xb3\xc7\x88\x86\xd4l\xb98{\xc8\x1d&\xc8\x8c\x95ml\x97\xb29\x93\xad\x7f\x9coe}r\xfa\xcbY\x19\xd0mF\xcb\xeeO\xcb\xb3\xf3\xa7\x0f\xbf\xdd\xd9\x11\x92\xac\xb4~\x9b#\x99)\xdb\xea<YY\x8e\xad\xbe#\xc7@?\x7f0\x88\x95]\xb6>[k\xc8o\x06%/\xa3\xf7vG2U\xa6\x82U\xfb_1q\x94\x94\xbe\x8f\xdd\xd9\x11
    09:01:43.948 DEBUG    hpack.hpack        Encoded header block to                                                                                                                                
                                             b"\x83A\x98\x92\xca#\xf1Rk\xa3\xd2K\xdb\xbd\x95\xd5L\x86]\x16\xd68\xc6\x82\xaeC\xff\x87D\x98b\xc2\xa1,w\x0b\x16VF)\x1aI<Q\x9c\xfdb\xebQ\xfcPY&/S\x83…  
                                             \xc7\xab\x82\x08\x7f@\x92\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%k-\xa9&\xa4\xbf\x85\xaf\xd2g=_@\x97\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%k-\xa9&\xa4\xabw…  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  2026-05-17 09:01:44.400 | DEBUG    | logging:callHandlers:1762 - Decoding b'?\xe1\x1f\x88a\x96\xddm_J\x05\xd54\x0f\xd2\x82\x00\x9cP\x02\xb8\x00\xdci\xa51h\xdf_\x96\x1du\xd0b\r&=LtA\xea\xfbP\x93\x8e\xc4\x150Z\x99V{^\x84\x02\xcf\xb1\xf3@\x85$\xabX?_\x8f~RJ\x07\xd9i\xb8\xdd \xc0\xeckn\xc9\xa7@\x8a$\xab\x10d\x9c\xab!#M\xa8\x86\xbf\xcfL:2^Z\x83\x9b\xd9\xabv\x87%\x07\xb6Ih\x1d\x85x\xa0\xa4~V\x1c\xc5\x81\x90\xb6\xcb\x80\x00>\xd45D\xa2\xd9\x0b\xba\xd8\xef\x9e\x91\x9a\xa4}\xa9]\x85\xa0\xe3\x93{\x8b\x84\x84-i[\x05D<\x86\xaao@\x90\xf2\xb1\x0fRKRVO\xaa\xca\xb1\xebI\x8fR?\x85\xa8\xe8\xa8\xd2\xcb@\x8b!\xeaIjJ\xd5\xd8yMA\x7f\x85\xae\xd8\xe81?@\x8dDkL4\x97\xc0\xfd-\xdc\xb6 \xc7\xab\x011@\x8aDkWa\xfa\x14\x89Z\xc2\xcb\x8f\x92\xca#\xf1Rk\xa3\xd2K\xdb\xbd\x95\xd5L\x86@\x8aDkX^\xd6\x95\tX\xd2\x7f\x9a\x00_+,\x8ckJIYY\xd7\x1bmh\xc4\xe1\x16\x91\x96\\d\xa4\x0b1\xbc_@\x8f\xf2\xb1j\xee\x7fK\r)-5\xa5b\x1e\xda\x93\x011@\x95\xf2\xb1j\xee\x7fK[Z\x13aGJ\xc8-\x9d\xccB\xac\x93R_\x82\x08\\w\xffn\x8a"K\x14t\xc1-\xeb?\x02\xfe|\x04\xe7\x97\xack\x8b\x8c\xa6\x7f\x87k|\xdfo\x8eT\xa2mw\xaf[\xea,\xd3\xefk\xa7\x0f\x0b\x05\xd7^}\xe6Y\x03K\xb2\xeb.\xb6\'\x96\n\xe0\\+\x85n\xd6\x17\x8fL\x91\x80:t\x00]\xcf\xdf\'{\xde\x03\x9du\xf6\xf3\xea\x1c|\xb3\'\x05\t\xa0\x07\x06\xc6E\xc6\xbeHgn\xc0\xf7\x88?\xaf/\xc9\xf5\xe1\xa7n\xcex\\\xbb\r\xd0\xd1\xa6n\xc4\xf1%0\xf2\xcb\xc5\xd6}\xbd\xa7\xba.\xbb\x0cx\x19^@UL^
    09:01:44.400 DEBUG    hpack.hpack        Decoding                                                                                                                                               
                                             b'?\xe1\x1f\x88a\x96\xddm_J\x05\xd54\x0f\xd2\x82\x00\x9cP\x02\xb8\x00\xdci\xa51h\xdf_\x96\x1du\xd0b\r&=LtA\xea\xfbP\x93\x8e\xc4\x150Z\x99V{^\x84\x02…  
                                             \xc0\xeckn\xc9\xa7@\x8a$\xab\x10d\x9c\xab!#M\xa8\x86\xbf\xcfL:2^Z\x83\x9b\xd9\xabv\x87%\x07\xb6Ih\x1d\x85x\xa0\xa4~V\x1c\xc5\x81\x90\xb6\xcb\x80\x00…  
                                             \xc7\xab\x011@\x8aDkWa\xfa\x14\x89Z\xc2\xcb\x8f\x92\xca#\xf1Rk\xa3\xd2K\xdb\xbd\x95\xd5L\x86@\x8aDkX^\xd6\x95\tX\xd2\x7f\x9a\x00_+,\x8ckJIYY\xd7\x1b…  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.405 DEBUG    hpack.hpack        Decoded 4096, consumed 3 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.409 DEBUG    hpack.table        Resizing header table to 4096 from 4096  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.413 DEBUG    hpack.hpack        Decoded 8, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.416 DEBUG    hpack.hpack        Decoded (b':status', b'200'), consumed 1  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.418 DEBUG    hpack.hpack        Decoded 33, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.422 DEBUG    hpack.hpack        Decoded 22, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.425 DEBUG    hpack.hpack        Decoded (b'date', b'Sun, 17 May 2026 02:01:44 GMT'), total consumed 24 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.428 DEBUG    hpack.hpack        Decoded 31, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.432 DEBUG    hpack.hpack        Decoded 22, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.435 DEBUG    hpack.hpack        Decoded (b'content-type', b'application/json; charset=utf-8'), total consumed 24 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.439 DEBUG    hpack.hpack        Decoded 30, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.442 DEBUG    hpack.hpack        Decoded 4, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.445 DEBUG    hpack.hpack        Decoded (b'content-range', b'0-9/*'), total consumed 6 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.448 DEBUG    hpack.hpack        Decoded 5, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.452 DEBUG    hpack.hpack        Decoded 15, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.456 DEBUG    hpack.hpack        Decoded (b'cf-ray', b'9fcf09345b7ca07b-SIN'), total consumed 23 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.459 DEBUG    hpack.hpack        Decoded 10, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.461 DEBUG    hpack.hpack        Decoded 6, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.464 DEBUG    hpack.hpack        Decoded (b'cf-cache-status', b'DYNAMIC'), total consumed 19 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.468 DEBUG    hpack.hpack        Decoded 26, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.471 DEBUG    hpack.hpack        Decoded 3, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.475 DEBUG    hpack.hpack        Decoded (b'content-encoding', b'gzip'), total consumed 5 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.479 DEBUG    hpack.hpack        Decoded 54, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.482 DEBUG    hpack.hpack        Decoded 7, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.486 DEBUG    hpack.hpack        Decoded (b'server', b'cloudflare'), total consumed 9 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.489 DEBUG    hpack.hpack        Decoded 56, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.492 DEBUG    hpack.hpack        Decoded 32, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.495 DEBUG    hpack.hpack        Decoded (b'strict-transport-security', b'max-age=31536000; includeSubDomains; preload'), total consumed 34 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.499 DEBUG    hpack.hpack        Decoded 59, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.501 DEBUG    hpack.hpack        Decoded 11, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.504 DEBUG    hpack.hpack        Decoded (b'vary', b'Accept-Encoding'), total consumed 13 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.507 DEBUG    hpack.hpack        Decoded 16, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.511 DEBUG    hpack.hpack        Decoded 5, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.514 DEBUG    hpack.hpack        Decoded (b'x-content-type-options', b'nosniff'), total consumed 24 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.518 DEBUG    hpack.hpack        Decoded 11, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.520 DEBUG    hpack.hpack        Decoded 5, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.523 DEBUG    hpack.hpack        Decoded (b'content-profile', b'public'), total consumed 19 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.526 DEBUG    hpack.hpack        Decoded 13, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.531 DEBUG    hpack.hpack        Decoded 1, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.533 DEBUG    hpack.hpack        Decoded (b'sb-gateway-version', <memory at 0x0000021666531540>), total consumed 17 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.537 DEBUG    hpack.hpack        Decoded 10, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.541 DEBUG    hpack.hpack        Decoded 15, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.544 DEBUG    hpack.hpack        Decoded (b'sb-project-ref', b'drlbwntplyteqvrpnmdi'), total consumed 28 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.547 DEBUG    hpack.hpack        Decoded 10, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.551 DEBUG    hpack.hpack        Decoded 26, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.554 DEBUG    hpack.hpack        Decoded (b'sb-request-id', b'019e33aa-fcf3-7655-b26c-d3363ec13b8e'), total consumed 39 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.558 DEBUG    hpack.hpack        Decoded 15, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.562 DEBUG    hpack.hpack        Decoded 1, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.565 DEBUG    hpack.hpack        Decoded (b'x-envoy-attempt-count', <memory at 0x0000021666531D80>), total consumed 19 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.568 DEBUG    hpack.hpack        Decoded 21, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.573 DEBUG    hpack.hpack        Decoded 2, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.576 DEBUG    hpack.hpack        Decoded (b'x-envoy-upstream-service-time', b'116'), total consumed 26 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.581 DEBUG    hpack.hpack        Decoded 55, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.585 DEBUG    hpack.hpack        Decoded 237, consumed 2 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  2026-05-17 09:01:44.588 | DEBUG    | logging:callHandlers:1762 - Decoded (b'set-cookie', b'__cf_bm=fCrX19LEcYJkb.2Vfi9UquxD5VJtsgPCCuy_KhT4jUw-1778983304.3737528-1.0.1.1-qreVjIb01NM02vovIvCw1L..RY
    09:01:44.587 DEBUG    hpack.hpack        Decoded (b'set-cookie',                                                                                                                                
                                             b'__cf_bm=fCrX19LEcYJkb.2Vfi9UquxD5VJtsgPCCuy_KhT4jUw-1778983304.3737528-1.0.1.1-qreVjIb01NM02vovIvCw1L..RYk1HWKtEltl0o0Q32VpWs3RQ1v_1Z8.W9.AmRQYF6B…  
                                             HttpOnly; SameSite=None; Secure; Path=/; Domain=supabase.co; Expires=Sun, 17 May 2026 02:31:44 GMT'), total consumed 240 bytes, indexed True           
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.591 DEBUG    hpack.hpack        Decoded 5, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.595 DEBUG    hpack.hpack        Decoded 16, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.598 DEBUG    hpack.hpack        Decoded (b'alt-svc', b'h3=":443"; ma=86400'), total consumed 24 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:01:44.606 DEBUG    livekit.agents     tools execution completed {"speech_id": "speech_77b41c739b1e"}
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▂ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▄ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   Microphone Array (Realtek(R) Au   ▃ ▆ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:04.638 DEBUG    livekit.agents     executing tool  
                                         {"function": "search_book_knowledge", "arguments": "{  \n  \"query\": \"Các phương pháp ghi nhớ được đề cập trong cuốn sách này là gì?\" \n} \n", 
"speech_id": "speech_c71101fff131"}
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.155 DEBUG    hpack.hpack        Adding (b':method', b'POST') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▄ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.160 DEBUG    hpack.hpack        Encoding 3 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.162 DEBUG    hpack.hpack        Adding (b':authority', b'drlbwntplyteqvrpnmdi.supabase.co') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.166 DEBUG    hpack.hpack        Encoding 1 with 6 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.169 DEBUG    hpack.hpack        Encoding 24 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.172 DEBUG    hpack.hpack        Adding (b':scheme', b'https') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.175 DEBUG    hpack.hpack        Encoding 7 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.178 DEBUG    hpack.hpack        Adding (b':path', b'/rest/v1/rpc/match_book_knowledge') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.182 DEBUG    hpack.hpack        Encoding 4 with 6 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.185 DEBUG    hpack.hpack        Encoding 24 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.188 DEBUG    hpack.hpack        Adding (b'accept', b'*/*') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.193 DEBUG    hpack.hpack        Encoding 19 with 6 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.198 DEBUG    hpack.hpack        Encoding 3 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.201 DEBUG    hpack.hpack        Adding (b'accept-encoding', b'gzip, deflate, zstd') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.204 DEBUG    hpack.hpack        Encoding 16 with 6 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.207 DEBUG    hpack.hpack        Encoding 15 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.210 DEBUG    hpack.hpack        Adding (b'user-agent', b'python-httpx/0.28.1') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.214 DEBUG    hpack.hpack        Encoding 58 with 6 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.217 DEBUG    hpack.hpack        Encoding 14 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.219 DEBUG    hpack.hpack        Adding (b'x-client-info', b'supabase-py/2.28.3') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.224 DEBUG    hpack.hpack        Encoding 10 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.227 DEBUG    hpack.hpack        Encoding 13 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.231 DEBUG    hpack.hpack        Adding (b'x-supabase-client-platform', b'Windows') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.233 DEBUG    hpack.hpack        Encoding 19 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.237 DEBUG    hpack.hpack        Encoding 6 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.240 DEBUG    hpack.hpack        Adding (b'x-supabase-client-platform-version', b'11') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.243 DEBUG    hpack.hpack        Encoding 24 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.247 DEBUG    hpack.hpack        Encoding 2 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.250 DEBUG    hpack.hpack        Adding (b'x-supabase-client-runtime', b'python') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.254 DEBUG    hpack.hpack        Encoding 18 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.257 DEBUG    hpack.hpack        Encoding 5 with 7 bits  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.260 DEBUG    hpack.hpack        Adding (b'x-supabase-client-runtime-version', b'3.12.12') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▂ ▆ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.263 DEBUG    hpack.hpack        Encoding 23 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.266 DEBUG    hpack.hpack        Encoding 5 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  
    09:02:05.270 DEBUG    hpack.hpack        Adding (b'apikey',                                                                                                                                     
                                             b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRybGJ3bnRwbHl0ZXF2cnBubWRpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUzO…  
                                             to the header table, sensitive:False, huffman:True                                                                                                     
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.275 DEBUG    hpack.hpack        Encoding 5 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.279 DEBUG    hpack.hpack        Encoding 176 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  
    09:02:05.283 DEBUG    hpack.hpack        Adding (b'authorization', b'Bearer                                                                                                                     
                                             eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRybGJ3bnRwbHl0ZXF2cnBubWRpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDUzOTU…  
                                             to the header table, sensitive:True, huffman:True                                                                                                      
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.288 DEBUG    hpack.hpack        Encoding 23 with 4 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.292 DEBUG    hpack.hpack        Encoding 181 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.295 DEBUG    hpack.hpack        Adding (b'accept-profile', b'public') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.298 DEBUG    hpack.hpack        Encoding 10 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.301 DEBUG    hpack.hpack        Encoding 5 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.306 DEBUG    hpack.hpack        Adding (b'content-profile', b'public') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.309 DEBUG    hpack.hpack        Encoding 11 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.312 DEBUG    hpack.hpack        Encoding 5 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  
    09:02:05.315 DEBUG    hpack.hpack        Adding (b'cookie',                                                                                                                                     
                                             b'__cf_bm=fCrX19LEcYJkb.2Vfi9UquxD5VJtsgPCCuy_KhT4jUw-1778983304.3737528-1.0.1.1-qreVjIb01NM02vovIvCw1L..RYk1HWKtEltl0o0Q32VpWs3RQ1v_1Z8.W9.AmRQYF6B…  
                                             to the header table, sensitive:False, huffman:True                                                                                                     
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.320 DEBUG    hpack.hpack        Encoding 32 with 6 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.325 DEBUG    hpack.hpack        Encoding 162 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.329 DEBUG    hpack.hpack        Adding (b'content-length', b'29514') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.333 DEBUG    hpack.hpack        Encoding 28 with 6 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.335 DEBUG    hpack.hpack        Encoding 4 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.338 DEBUG    hpack.hpack        Adding (b'content-type', b'application/json') to the header table, sensitive:False, huffman:True  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.342 DEBUG    hpack.hpack        Encoding 31 with 6 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.346 DEBUG    hpack.hpack        Encoding 11 with 7 bits  
   Microphone Array (Realtek(R) Au   ▃ ▇ █ ▁ ▂ ▂ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  2026-05-17 09:02:05.349 | DEBUG    | logging:callHandlers:1762 - Encoded header block to b'\x83A\x98\x92\xca#\xf1Rk\xa3\xd2K\xdb\xbd\x95\xd5L\x86]\x16\xd68\xc6\x82\xaeC\xff\x87D\x98b\xc2\xa1,w\x0b\x16VF)\x1aI<Q\x9c\xfdb\xebQ\xfcPY&/S\x83\xf9c\xe7P\x8f\x9b\xd9\xab\xfaRB\xcb@\xd2_\xa5=\xa12\x7fz\x8e\xaf\xd2g=KN\x94\xd7\xe5\x80.\'\x97\x0f@\x8a\xf2\xb1(1jJ\xc6\xaaS\xff\x8dE\xb5\x8e1\xa0\xabW\xe9\x81.\'\x97g@\x93\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%j\xe8\x1ae=\x94\xff\x86\xe4j\xa4?\x84\x7f@\x98\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%j\xe8\x1ae=\x94\xad\xdc\xb6 \xc7\xab\x82\x08\x7f@\x92\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%k-\xa9&\xa4\xbf\x85\xaf\xd2g=_@\x97\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%k-\xa9&\xa4\xabw-\x881\xea\x85ep\x89p\x8b@\x85\x1df\xea__\xff1/\xac\xb3\xc7\x88\x86\xd4l\xb98{\xc8\x1d&\xc8\x8c\x95ml\x97\xb29\x93\xad\x7f\x9coe}r\xfa\xcbY\x19\xd0mF\xcb\xeeO\xcb\xb3\xf3\xa7\x0f\xbf\xdd\xd9\x11\x92\xac\xb4~\x9b#\x99)\xdb\xea<YY\x8e\xad\xbe#\xc7@?\x7f0\x88\x95]\xb6>[k\xc8o\x06%/\xa3\xf7vG2U\xa6\x82U\xfb_1q\x94\x94\xbe\x8f\xdd\xd9\x11\x92\x9a\'\x92\xf6G4o#:/\xf0\xf7\xab\x7f\x0fzox7\xef\xe4\xfe2t?\xad\x17\xe6\x16\x8d\xf8\x03\xa7~\x80K\xb1q\xc2\xed\x19\xbdc>-\xc0\xef3\xe4\xedu\xd0\xb7\xb4\x9a\x857o\xce\xc0\xeb\xe4\xbds\xf7\xdb\xef\xde3\x19\xcc\x9f\x1f\x08\xff6\xbaQ\xd8[\x14/\xac\xb3\xc7\x88\x86\xd4l\xb98{\xc8\x1d&\xc8\x8c\x95ml\x97\xb29\x93\xad\x7f\x9coe}r\xfa\xcbY\x19\xd0mF\xcb\xeeO\xcb\xb3\xf3\xa7\x0f\xbf\xdd\xd9\x11\x92\xac\xb4~\x9b#\x99)\xdb\xea<YY\x8e\xad\xbe#\xc7@?\x7f0\x88\x95]\xb6>[k\xc8o\x06%/\xa3\xf7vG2U\xa6\x82U\xfb_1q\x94\x94\xbe\x8f\xdd\xd9\x11\x92\x9a\'\x92\xf6G4o#:/\xf0\xf7\xab\x7f\x0fzox7\xef\xe4\xfe2t?\xad\x17\xe6\x16\x8d\xf8\x03\xa7~\x80K\xb1q\xc2\xed\x19\xbdc>-\xc0\xef3\xe4\xedu\xd0\xb7\xb4\x9a\x857o\xce\xc0\xeb\xe4\xbds\xf7\xdb\xef\xde3\x19\xcc\x9f@\x8a\x19\x08Z\xd2\xb5v\x1eSP_\x85\xae\xd8\xe81?@\x8b!\xeaIjJ\xd5\xd8yMA\x7f\x85\xae\xd8\xe81?`\xff#\x8a"K\x14t\xc1-\xeb?\x02\xfe|\x04\xe7\x97\xack\x8b\x8c\xa6\x7f\x87k|\xdfo\x8eT\xa2mw\xaf[\xea,\xd3\xefk\xa7\x0f\x0b\x05\xd7^}\xe6Y\x03K\xb2\xeb.\xb6\'\x96\n\xe0\\+\x85n\xd6\x17\x8fL\x91\x80:t\x00]\xcf\xdf\'{\xde\x03\x9du\xf6\xf3\xea\x1c|\xb3\'\x05\t\xa0\x07\x06\xc6E\xc
    09:02:05.349 DEBUG    hpack.hpack        Encoded header block to                                                                                                                                
                                             b'\x83A\x98\x92\xca#\xf1Rk\xa3\xd2K\xdb\xbd\x95\xd5L\x86]\x16\xd68\xc6\x82\xaeC\xff\x87D\x98b\xc2\xa1,w\x0b\x16VF)\x1aI<Q\x9c\xfdb\xebQ\xfcPY&/S\x83…  
                                             \xc7\xab\x82\x08\x7f@\x92\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%k-\xa9&\xa4\xbf\x85\xaf\xd2g=_@\x97\xf2\xb2-\xacq\x8d\x05X\x94\x18\xb5%k-\xa9&\xa4\xabw…  
   Microphone Array (Realtek(R) Au   ▃ ▆ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
   ? for shortcuts                                                                                                                                                                                  2026-05-17 09:02:05.854 | DEBUG    | logging:callHandlers:1762 - Decoding b'?\xe1\x1f\x88a\x96\xddm_J\x05\xd54\x0f\xd2\x82\x00\x9cP\x02\xb8\x01\\\x03\x8ab\xd1\xbf_\x96\x1du\xd0b\r&=LtA\xea\xfbP\x93\x8e\xc4\x150Z\x99V{^\x84\x02\xcf\xb1\xf3@\x85$\xabX?_\x8f~RJ\x07\xe3\x18G#o\x08\x12-\xbb&\x9f@\x8a$\xab\x10d\x9c\xab!#M\xa8\x86\xbf\xcfL:2^Z\x83\x9b\xd9\xabv\x87%\x07\xb6Ih\x1d\x85x\xa0\xa4~V\x1c\xc5\x81\x90\xb6\xcb\x80\x00>\xd45D\xa2\xd9\x0b\xba\xd8\xef\x9e\x91\x9a\xa4}\xa9]\x85\xa0\xe3\x93{\x8b\x84\x84-i[\x05D<\x86\xaao@\x90\xf2\xb1\x0fRKRVO\xaa\xca\xb1\xebI\x8fR?\x85\xa8\xe8\xa8\xd2\xcb@\x8b!\xeaIjJ\xd5\xd8yMA\x7f\x85\xae\xd8\xe81?@\x8dDkL4\x97\xc0\xfd-\xdc\xb6 \xc7\xab\x011@\x8aDkWa\xfa\x14\x89Z\xc2\xcb\x8f\x92\xca#\xf1Rk\xa3\xd2K\xdb\xbd\x95\xd5L\x86@\x8aDkX^\xd6\x95\tX\xd2\
    09:02:05.854 DEBUG    hpack.hpack        Decoding                                                                                                                                               
                                             b'?\xe1\x1f\x88a\x96\xddm_J\x05\xd54\x0f\xd2\x82\x00\x9cP\x02\xb8\x01\\\x03\x8ab\xd1\xbf_\x96\x1du\xd0b\r&=LtA\xea\xfbP\x93\x8e\xc4\x150Z\x99V{^\x84…  
                                             \xc7\xab\x011@\x8aDkWa\xfa\x14\x89Z\xc2\xcb\x8f\x92\xca#\xf1Rk\xa3\xd2K\xdb\xbd\x95\xd5L\x86@\x8aDkX^\xd6\x95\tX\xd2\x7f\x9a\x00_+,\x8e5\x9b\x03\xd2…  
   Microphone Array (Realtek(R) Au   ▃ ▆ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.858 DEBUG    hpack.hpack        Decoded 4096, consumed 3 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▆ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.861 DEBUG    hpack.table        Resizing header table to 4096 from 4096  
   Microphone Array (Realtek(R) Au   ▃ ▆ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.864 DEBUG    hpack.hpack        Decoded 8, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▃ ▆ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.868 DEBUG    hpack.hpack        Decoded (b':status', b'200'), consumed 1  
   Microphone Array (Realtek(R) Au   ▃ ▆ █ ▄ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.956 DEBUG    hpack.hpack        Decoded 33, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.961 DEBUG    hpack.hpack        Decoded 22, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.975 DEBUG    hpack.hpack        Decoded (b'date', b'Sun, 17 May 2026 02:02:06 GMT'), total consumed 24 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.979 DEBUG    hpack.hpack        Decoded 31, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.981 DEBUG    hpack.hpack        Decoded 22, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.986 DEBUG    hpack.hpack        Decoded (b'content-type', b'application/json; charset=utf-8'), total consumed 24 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.989 DEBUG    hpack.hpack        Decoded 30, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.992 DEBUG    hpack.hpack        Decoded 4, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.996 DEBUG    hpack.hpack        Decoded (b'content-range', b'0-9/*'), total consumed 6 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:05.999 DEBUG    hpack.hpack        Decoded 5, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.001 DEBUG    hpack.hpack        Decoded 15, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.004 DEBUG    hpack.hpack        Decoded (b'cf-ray', b'9fcf09ba1ad5820d-SIN'), total consumed 23 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.007 DEBUG    hpack.hpack        Decoded 10, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.143 DEBUG    hpack.hpack        Decoded 6, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.147 DEBUG    hpack.hpack        Decoded (b'cf-cache-status', b'DYNAMIC'), total consumed 19 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.151 DEBUG    hpack.hpack        Decoded 26, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.154 DEBUG    hpack.hpack        Decoded 3, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.157 DEBUG    hpack.hpack        Decoded (b'content-encoding', b'gzip'), total consumed 5 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.160 DEBUG    hpack.hpack        Decoded 54, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.164 DEBUG    hpack.hpack        Decoded 7, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.167 DEBUG    hpack.hpack        Decoded (b'server', b'cloudflare'), total consumed 9 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.171 DEBUG    hpack.hpack        Decoded 56, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.173 DEBUG    hpack.hpack        Decoded 32, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.177 DEBUG    hpack.hpack        Decoded (b'strict-transport-security', b'max-age=31536000; includeSubDomains; preload'), total consumed 34 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.180 DEBUG    hpack.hpack        Decoded 59, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.184 DEBUG    hpack.hpack        Decoded 11, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.188 DEBUG    hpack.hpack        Decoded (b'vary', b'Accept-Encoding'), total consumed 13 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▁ ▇ █ ▃ ▂ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.191 DEBUG    hpack.hpack        Decoded 16, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.195 DEBUG    hpack.hpack        Decoded 5, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.198 DEBUG    hpack.hpack        Decoded (b'x-content-type-options', b'nosniff'), total consumed 24 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.201 DEBUG    hpack.hpack        Decoded 11, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.205 DEBUG    hpack.hpack        Decoded 5, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.208 DEBUG    hpack.hpack        Decoded (b'content-profile', b'public'), total consumed 19 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.212 DEBUG    hpack.hpack        Decoded 13, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.215 DEBUG    hpack.hpack        Decoded 1, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.218 DEBUG    hpack.hpack        Decoded (b'sb-gateway-version', <memory at 0x0000021661745240>), total consumed 17 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.221 DEBUG    hpack.hpack        Decoded 10, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.225 DEBUG    hpack.hpack        Decoded 15, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.227 DEBUG    hpack.hpack        Decoded (b'sb-project-ref', b'drlbwntplyteqvrpnmdi'), total consumed 28 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.231 DEBUG    hpack.hpack        Decoded 10, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.234 DEBUG    hpack.hpack        Decoded 26, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.238 DEBUG    hpack.hpack        Decoded (b'sb-request-id', b'019e33ab-508f-75b0-a4ff-47260bffe846'), total consumed 39 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.242 DEBUG    hpack.hpack        Decoded 15, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▂ ▇ █ ▂ ▄ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.245 DEBUG    hpack.hpack        Decoded 1, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▄ ▆ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.249 DEBUG    hpack.hpack        Decoded (b'x-envoy-attempt-count', <memory at 0x0000021666533DC0>), total consumed 19 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▄ ▆ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.254 DEBUG    hpack.hpack        Decoded 21, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▄ ▆ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.257 DEBUG    hpack.hpack        Decoded 3, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▄ ▆ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.260 DEBUG    hpack.hpack        Decoded (b'x-envoy-upstream-service-time', <memory at 0x0000021666531900>), total consumed 27 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▄ ▆ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.263 DEBUG    hpack.hpack        Decoded 5, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▄ ▆ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.267 DEBUG    hpack.hpack        Decoded 16, consumed 1 bytes  
   Microphone Array (Realtek(R) Au   ▄ ▆ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.270 DEBUG    hpack.hpack        Decoded (b'alt-svc', b'h3=":443"; ma=86400'), total consumed 24 bytes, indexed True  
   Microphone Array (Realtek(R) Au   ▄ ▆ █ ▃ ▃ ▁ ▂ ▁ ▁ ▁ ▁ ▁ ▁ ▁                                                                                                                                    
                                                                                                                                                                                                    
    09:02:06.278 DEBUG    livekit.agents     tools execution completed {"speech_id": "speech_c71101fff131"}
   Microphone Array (Realtek(R) Au   ▄ ▅ █ ▅ ▄ ▂ ▃ ▂ ▂ ▃ ▁ ▁ ▁ ▁   