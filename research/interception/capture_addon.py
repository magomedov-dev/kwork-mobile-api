"""mitmproxy-аддон: пишет запросы/ответы к api.kwork.ru в JSONL для анализа.

Запуск:
    mitmdump --listen-port 8080 -s research/interception/capture_addon.py

Каждый флоу к хосту api.kwork.* сохраняется одной строкой JSON в
research/captures/kwork_flows.jsonl (каталог captures/ в .gitignore).
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path("research/captures/kwork_flows.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)


def _truncate(text: str, limit: int = 4000) -> str:
    return text if len(text) <= limit else text[:limit] + f"…(+{len(text) - limit})"


def response(flow) -> None:
    host = flow.request.pretty_host
    if "kwork" not in host:
        return

    try:
        req_body = flow.request.get_text(strict=False) or ""
    except Exception:
        req_body = "<binary>"
    try:
        resp_body = flow.response.get_text(strict=False) or ""
    except Exception:
        resp_body = "<binary>"

    record = {
        "method": flow.request.method,
        "host": host,
        "path": flow.request.path.split("?")[0],
        "status": flow.response.status_code,
        "req": _truncate(req_body),
        "resp": _truncate(resp_body),
    }
    with OUT.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    # краткий лог в консоль mitmdump
    print(f"[kwork] {record['method']} {record['path']} -> {record['status']}")
