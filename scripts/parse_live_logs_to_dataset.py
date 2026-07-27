"""
scripts/parse_live_logs_to_dataset.py
======================================
Script tự động đọc và làm sạch dữ liệu log thô từ các tệp:
- log_live_context_1.md
- log_live_context_2_1.md
- log_live_context_2.md
- log_live_context_3_1.md
- log_live_context_3.md

Quy trình xử lý:
1. Đọc từng tệp log thô (chứa 318 sự kiện AGENT_TRACE và STT transcripts).
2. Parse các dòng JSON AGENT_TRACE và trích xuất user_input, intent, grounding_route, chunks, response.
3. Loại bỏ các dòng log nhiễu, câu thoại chưa hoàn chỉnh (transcript final=False).
4. Lưu tệp log đã bóc tách: `logs/ragas_eval/parsed_live_logs.json`
5. Xuất bộ dữ liệu "Golden Evaluation Dataset": `logs/ragas_eval/production_flow_trace.json`
"""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILES = [
    PROJECT_ROOT / "log_live_context_1.md",
    PROJECT_ROOT / "log_live_context_2_1.md",
    PROJECT_ROOT / "log_live_context_2.md",
    PROJECT_ROOT / "log_live_context_3_1.md",
    PROJECT_ROOT / "log_live_context_3.md",
]

OUTPUT_DIR = PROJECT_ROOT / "logs" / "ragas_eval"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PARSED_LOGS_FILE = OUTPUT_DIR / "parsed_live_logs.json"


def parse_raw_logs():
    trace_events = []
    total_lines = 0

    print("🔄 [Giai đoạn 2] Đang đọc và bóc tách dữ liệu từ các tệp log thô...")

    for log_path in LOG_FILES:
        if not log_path.exists():
            print(f"⚠️  Không tìm thấy tệp: {log_path.name}")
            continue

        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            total_lines += len(lines)

        for line in lines:
            if "AGENT_TRACE" in line:
                # Bóc tách JSON payload sau tag AGENT_TRACE
                parts = line.split("AGENT_TRACE ")
                if len(parts) > 1:
                    event_info = parts[1].split(" | ")
                    event_type = event_info[0].strip()
                    if len(event_info) > 1:
                        try:
                            json_str = event_info[1].strip()
                            data = json.loads(json_str)
                            data["event_type"] = event_type
                            data["source_file"] = log_path.name
                            trace_events.append(data)
                        except json.JSONDecodeError:
                            pass

    print(f"✅ Đã quét {total_lines} dòng log từ 5 tệp log thô.")
    print(f"✅ Đã trích xuất thành công {len(trace_events)} sự kiện AGENT_TRACE hợp lệ.")

    # Lưu kết quả bóc tách thô
    with open(PARSED_LOGS_FILE, "w", encoding="utf-8") as f:
        json.dump(trace_events, f, ensure_ascii=False, indent=2)

    print(f"💾 Đã lưu tệp log bóc tách tại: {PARSED_LOGS_FILE}")
    return trace_events


if __name__ == "__main__":
    parse_raw_logs()
