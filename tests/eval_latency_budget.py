"""
tests/eval_latency_budget.py
=====================================================================
Script tự động đọc nhật ký vận hành thực tế (AGENT_TRACE), tính toán
và hiển thị bảng phân bổ độ trễ server-side theo mốc P50 (Median), P90
và P95. Mỗi ``trace_id`` chỉ đóng góp tối đa một quan sát cho mỗi stage.

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


def load_trace_events() -> list[dict]:  # noqa: C901
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


def completed_voice_traces(events: list[dict]) -> list[dict]:
    """Return one terminal voice trace per trace ID.

    A trace is emitted repeatedly as routing, retrieval and watchdog events
    occur.  Aggregating all those events would silently give a busy trace more
    statistical weight.  The final ``turn_completed`` event is the canonical
    source for latency values; when duplicate completions exist, retain the one
    with the most recorded stages.
    """
    by_trace_id: dict[str, dict] = {}
    for event in events:
        if event.get("event_type") != "turn_completed" or event.get("input_mode") != "voice":
            continue
        trace_id = str(event.get("trace_id") or "")
        if not trace_id:
            continue
        previous = by_trace_id.get(trace_id)
        if previous is None or len(event.get("stage_latency_ms") or {}) > len(previous.get("stage_latency_ms") or {}):
            by_trace_id[trace_id] = event
    return list(by_trace_id.values())


def stage_values(traces: list[dict], stage_name: str) -> list[int]:
    values: list[int] = []
    for trace in traces:
        value = (trace.get("stage_latency_ms") or {}).get(stage_name)
        if value is None:
            continue
        try:
            values.append(int(value))
        except (TypeError, ValueError):
            print(f"⚠️ Bỏ qua giá trị latency không hợp lệ | trace_id={trace.get('trace_id')} | stage={stage_name}")
    return values


def calculate_latency_budget():
    events = load_trace_events()
    if not events:
        print("❌ Không tìm thấy dữ liệu log AGENT_TRACE để tính toán.")
        return

    traces = completed_voice_traces(events)
    if not traces:
        print("❌ Không tìm thấy trace voice đã hoàn tất để tính latency.")
        return

    router_latencies = stage_values(traces, "grounding_total")
    query_guard_latencies = stage_values(traces, "query_guard")
    retrieval_latencies = stage_values(traces, "retrieval")
    web_search_latencies = stage_values(traces, "web_search")
    tool_total_latencies = stage_values(traces, "tool_total")
    turn_total_latencies = stage_values(traces, "turn_total")

    rows = [
        ("Semantic Grounding Router", "Semantic Grounding Router", router_latencies),
        ("Chốt chặn câu hỏi", "Query Guard Validation", query_guard_latencies),
        ("Truy xuất tri thức RAG", "Retrieval (Hybrid Search + Cohere Reranker)", retrieval_latencies),
        ("Tìm kiếm Web mở rộng", "Tavily Web Search API", web_search_latencies),
        ("Tổng hợp công cụ RAG", "Total Tool Execution", tool_total_latencies),
        ("Tổng lượt thoại", "Voice Turn Total", turn_total_latencies),
    ]

    print("\n" + "=" * 92)
    print("📊 BẢNG ĐỘ TRỄ SERVER-SIDE TRỢ LÝ THOẠI RAG (MỖI TRACE MỘT QUAN SÁT)")
    print("=" * 92)
    print(f"{'Giai đoạn xử lý':<25} | {'Chỉ số đo lường':<38} | {'n':<5} | {'P50 (ms)':<8} | {'P90 (ms)':<8} | {'P95 (ms)':<8}")
    print("-" * 92)

    for stage_name, metric_name, data in rows:
        if data:
            p50 = int(round(np.percentile(data, 50)))
            p90 = int(round(np.percentile(data, 90)))
            p95 = int(round(np.percentile(data, 95)))
            print(f"{stage_name:<25} | {metric_name:<38} | {len(data):<5d} | {p50:8d} | {p90:8d} | {p95:8d}")
        else:
            print(f"{stage_name:<25} | {metric_name:<38} | {0:<5d} | {'N/A':<8} | {'N/A':<8} | {'N/A':<8}")

    print(f"Ghi chú: Voice Turn Total là server-side turn latency của {len(traces)} trace, không phải TTFA phía ứng dụng.")
    print("=" * 92 + "\n")


if __name__ == "__main__":
    calculate_latency_budget()
