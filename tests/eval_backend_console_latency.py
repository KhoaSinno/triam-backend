"""
tests/eval_backend_console_latency.py
=====================================================================
Script tự động quét và phân tích độ trễ thực nghiệm từ các tệp log
chạy thử trực tiếp trên Backend Console (hệ thống BE không thông qua FE):
- logs/agent_eval/voice_console_*.log

Cách chạy:
    python tests/eval_backend_console_latency.py
=====================================================================
"""

import json
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONSOLE_LOG_DIR = PROJECT_ROOT / "logs" / "agent_eval"


def load_console_trace_events():
    events = []
    log_files = sorted(CONSOLE_LOG_DIR.glob("voice_console_*.log"))
    
    print(f"📖 Đang quét {len(log_files)} tệp log console trong: {CONSOLE_LOG_DIR.relative_to(PROJECT_ROOT)}/\n")
    
    file_counts = {}
    for log_path in log_files:
        count = 0
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "AGENT_TRACE" in line:
                    parts = line.split("AGENT_TRACE ")
                    if len(parts) > 1:
                        event_info = parts[1].split(" | ")
                        event_type = event_info[0].strip()
                        if len(event_info) > 1:
                            try:
                                data = json.loads(event_info[1].strip())
                                data["event_type"] = event_type
                                data["source_file"] = log_path.name
                                events.append(data)
                                count += 1
                            except Exception:
                                pass
        file_counts[log_path.name] = count
        print(f"  • {log_path.name:<38}: {count} sự kiện AGENT_TRACE")

    print(f"\n✅ Tổng cộng nạp được {len(events)} sự kiện AGENT_TRACE từ Backend Console logs.\n")
    return events


def calculate_backend_console_latency():
    events = load_console_trace_events()
    if not events:
        print("❌ Không tìm thấy sự kiện AGENT_TRACE nào trong các tệp voice_console_*.log.")
        return

    router_latencies = []
    query_guard_latencies = []
    retrieval_latencies = []
    web_search_latencies = []
    tool_total_latencies = []
    turn_total_latencies = []

    for ev in events:
        stages = ev.get("stage_latency_ms") or {}
        
        if "grounding_total" in stages:
            router_latencies.append(stages["grounding_total"])
        if "query_guard" in stages:
            query_guard_latencies.append(stages["query_guard"])
        if "retrieval" in stages:
            retrieval_latencies.append(stages["retrieval"])
        if "web_search" in stages:
            web_search_latencies.append(stages["web_search"])
        if "tool_total" in stages:
            tool_total_latencies.append(stages["tool_total"])
        if "turn_total" in stages:
            turn_total_latencies.append(stages["turn_total"])

    rows = [
        ("Semantic Grounding Router", "Semantic Grounding Router", router_latencies),
        ("Chốt chặn câu hỏi", "Query Guard Validation", query_guard_latencies),
        ("Truy xuất tri thức RAG", "Retrieval (Hybrid Search + Cohere Reranker)", retrieval_latencies),
        ("Tìm kiếm Web mở rộng", "Tavily Web Search API", web_search_latencies),
        ("Tổng hợp công cụ RAG", "Total Tool Execution", tool_total_latencies),
        ("Tổng lượt thoại Console", "Voice Turn Total (Backend Console)", turn_total_latencies),
    ]

    print("=" * 96)
    print("📊 BẢNG TỔNG HỢP ĐỘ TRỄ THỰC NGHIỆM KHI CHẠY TRỰC TIẾP TRÊN BACKEND CONSOLE (KHÔNG QUA FE)")
    print("=" * 96)
    print(f"{'Giai đoạn xử lý':<25} | {'Chỉ số đo lường':<38} | {'P50 (ms)':<8} | {'P90 (ms)':<8} | {'P95 (ms)':<8} | số mẫu")
    print("-" * 96)

    for stage_name, metric_name, data in rows:
        if data:
            p50 = int(round(np.percentile(data, 50)))
            p90 = int(round(np.percentile(data, 90)))
            p95 = int(round(np.percentile(data, 95)))
            cnt = len(data)
            print(f"{stage_name:<25} | {metric_name:<38} | {p50:8d} | {p90:8d} | {p95:8d} | {cnt:5d}")
        else:
            print(f"{stage_name:<25} | {metric_name:<38} | {'N/A':<8} | {'N/A':<8} | {'N/A':<8} | {0:5d}")

    print("=" * 96 + "\n")


if __name__ == "__main__":
    calculate_backend_console_latency()
