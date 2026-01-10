#!/usr/bin/env python3
"""Строит санитизированный справочник ответов API из перехваченных flows.

Читает research/captures/kwork_flows_test*.jsonl и для каждого уникального
эндпоинта выводит: поля запроса (только имена) и СХЕМУ ответа (ключи → типы,
без значений). Личные данные (токены, email, тексты) не попадают в вывод —
печатаются только имена полей и типы.

Запуск:  python research/build_schemas.py > docs/06-captured-responses.md
"""

from __future__ import annotations

import glob
import json
from urllib.parse import parse_qsl

COMMON_REQ = {"token", "uad", "slrememberme", "device", "password", "recaptcha_pass_token"}
MAX_DEPTH = 4


def typeof(v, depth=0):
    if isinstance(v, dict):
        if depth >= MAX_DEPTH:
            return "object"
        return {k: typeof(val, depth + 1) for k, val in list(v.items())[:40]}
    if isinstance(v, list):
        if not v:
            return "[]"
        return [typeof(v[0], depth + 1)]
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if v is None:
        return "null"
    return "str"


def render(schema, indent=0):
    pad = "  " * indent
    lines = []
    if isinstance(schema, dict):
        for k, v in schema.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                lines.extend(render(v, indent + 1))
            else:
                lines.append(f"{pad}{k}: {v}")
    elif isinstance(schema, list):
        lines.append(f"{pad}- [список]:")
        lines.extend(render(schema[0], indent + 1))
    else:
        lines.append(f"{pad}{schema}")
    return lines


def req_fields(req: str) -> list[str]:
    if req.startswith("---") or "Content-Disposition" in req:
        return ["<multipart>"]
    keys = [k for k, _ in parse_qsl(req)]
    return [k for k in dict.fromkeys(keys) if k not in COMMON_REQ] or ["—"]


def main() -> None:
    samples: dict[tuple, dict] = {}
    for path in sorted(glob.glob("research/captures/kwork_flows_test*.jsonl")):
        for line in open(path, encoding="utf-8"):
            r = json.loads(line)
            if "kwork" not in r["host"] or r["method"] != "POST":
                continue
            p = r["path"]
            # пропускаем статику
            if p.startswith(("/css", "/js", "/images", "/files", "/fonts", "/pics")):
                continue
            try:
                body = json.loads(r["resp"])
            except Exception:
                continue
            if p not in samples:
                samples[p] = {"req": req_fields(r["req"]), "schema": typeof(body)}

    print("# Справочник ответов API (по живому трафику)\n")
    print("> Санитизировано: только имена полей и типы, без реальных значений. "
          "Источник — 2 прогона приложения через mitmproxy (895 flows). "
          "Общие поля запроса (`token`, `uad`, `slrememberme`, `device`) опущены.\n")
    print(f"Подтверждено эндпоинтов с телом ответа: **{len(samples)}**.\n")
    for p in sorted(samples):
        s = samples[p]
        print(f"\n## `POST {p}`\n")
        print(f"**Поля запроса:** {', '.join('`'+f+'`' for f in s['req'])}\n")
        print("**Схема ответа:**\n")
        print("```")
        print("\n".join(render(s["schema"])))
        print("```")


if __name__ == "__main__":
    main()
