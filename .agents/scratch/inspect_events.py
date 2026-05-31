import os
from pathlib import Path

pkg_dir = Path("w:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/.venv/Lib/site-packages/livekit/agents/voice")

for file_name in ["agent.py", "agent_session.py", "events.py"]:
    file_path = pkg_dir / file_name
    if not file_path.exists():
        continue
    content = file_path.read_text(encoding="utf-8")
    
    print(f"\n=== EMIT CALLS IN {file_name} ===")
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if "emit(" in line:
            print(f"{i+1}: {line.strip()}")
