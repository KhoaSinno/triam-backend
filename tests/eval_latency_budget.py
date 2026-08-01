"""
tests/eval_latency_budget.py
=====================================================================
Script tự động đọc nhật ký vận hành thực tế (AGENT_TRACE), tính toán
và hiển thị bảng phân bổ độ trễ thực nghiệm (Latency Budget) theo mốc
P50 (Median), P90 và P95 cho Luận văn TRIAM (Bảng 9.7 / Bảng 9.3).

Cách chạy:
    python -m tests.eval_latency_budget
hoặc:
    python tests/eval_latency_budget.py
=====================================================================
"""

import json
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PARSED_JSON = PROJECT_ROOT / "logs" / "ragas_eval" / "parsed_live_logs.json"
RAW_LOG_FILES = [
    PROJECT_ROOT / "log_live_context_1.md",
    PROJECT_ROOT / "log_live_context_2_1.md",
    PROJECT_ROOT / "log_live_context_2.md",
    PROJECT_ROOT / "log_live_context_3_1.md",
    PROJECT_ROOT / "log_live_context_3.md",
]


def load_trace_events() -> list[dict]:
    events = []
    
    # 1. Ưu tiên đọc từ file JSON đã parse sẵn
    if PARSED_JSON.exists():
        try:
            with open(PARSED_JSON, "r", encoding="utf-8") as f:
                events = json.load(f)
            if events:
                print(f"📖 Đã nạp thành công {len(events)} sự kiện trace từ {PARSED_JSON.relative_to(PROJECT_ROOT)}")
                return events
        except Exception as e:
            print(f"⚠️ Không nạp được {PARSED_JSON.name}: {e}. Đang quét lại log thô...")

    # 2. Dự phòng: Đọc trực tiếp từ các tệp log thô .md
    for log_path in RAW_LOG_FILES:
        if not log_path.exists():
            continue
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "AGENT_TRACE" in line:
                    parts = line.split("AGENT_TRACE ")
                    if len(parts) > 1:
                        event_info = parts[1].split(" | ")
                        if len(event_info) > 1:
                            try:
                                data = json.loads(event_info[1].strip())
                                data["event_type"] = event_info[0].strip()
                                events.append(data)
                            except Exception:
                                pass

    print(f"📖 Đã quét trực tiếp {len(events)} sự kiện AGENT_TRACE từ các tệp log thô.")
    return events


def calculate_latency_budget():
    events = load_trace_events()
    if not events:
        print("❌ Không tìm thấy dữ liệu log AGENT_TRACE để tính toán.")
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
        ("Tổng lượt thoại", "Voice Turn Total", turn_total_latencies),
    ]

    print("\n" + "=" * 92)
    print("📊 BẢNG TỔNG HỢP KẾT QUẢ ĐO ĐỘ TRỄ THỰC NGHIỆM TRỢ LÝ THOẠI RAG (LUẬN VĂN TRIAM)")
    print("=" * 92)
    print(f"{'Giai đoạn xử lý':<25} | {'Chỉ số đo lường':<38} | {'P50 (ms)':<8} | {'P90 (ms)':<8} | {'P95 (ms)':<8}")
    print("-" * 92)

    for stage_name, metric_name, data in rows:
        if data:
            p50 = int(round(np.percentile(data, 50)))
            p90 = int(round(np.percentile(data, 90)))
            p95 = int(round(np.percentile(data, 95)))
            print(f"{stage_name:<25} | {metric_name:<38} | {p50:8d} | {p90:8d} | {p95:8d}")
        else:
            print(f"{stage_name:<25} | {metric_name:<38} | {'N/A':<8} | {'N/A':<8} | {'N/A':<8}")

    print("=" * 92 + "\n")


if __name__ == "__main__":
    calculate_latency_budget()
