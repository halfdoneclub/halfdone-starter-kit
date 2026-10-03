#!/usr/bin/env python3
"""wrap 1단계 f) — 세션 원본 기록(jsonl)에서 사용자 원문 전체를 md로 뽑는다.

사용: python3 export_user_verbatim.py --project <작업 폴더> [--session <jsonl 경로>] [--date YYYY-MM-DD]
- --session 생략 시: ~/.claude/projects/<열린 폴더 변환 이름>/ 에서 가장 최근 jsonl
- 사용자 메시지(text)와 선택지 답변(AskUserQuestion 결과·도구 거절 사유)을 시간순 그대로 옮긴다. 요약하지 않는다.
- 스킬 본문·시스템 알림·작업 알림은 뺀다. 32자 이상 긴 토큰은 *** 로 가린다.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import re
import unicodedata

KST = dt.timezone(dt.timedelta(hours=9))


def project_dir_name(path: str) -> str:
    path = unicodedata.normalize("NFC", os.path.abspath(path))
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def latest_session(cwd: str) -> str | None:
    d = os.path.expanduser(f"~/.claude/projects/{project_dir_name(cwd)}")
    files = sorted(glob.glob(os.path.join(d, "*.jsonl")), key=os.path.getmtime)
    return files[-1] if files else None


def redact(s: str) -> str:
    return re.sub(r"[A-Za-z0-9+/=_\-]{32,}", "***", s)


def esc(s: str) -> str:
    return s.replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--session")
    ap.add_argument("--date", default=dt.datetime.now(KST).strftime("%Y-%m-%d"))
    a = ap.parse_args()
    sess = a.session or latest_session(os.getcwd()) or latest_session(a.project)
    if not sess:
        raise SystemExit("세션 jsonl을 찾지 못함 — --session으로 경로를 주세요")
    out = [f"# {a.date} 세션 — 사용자 원문 전체\n",
           "> 이 세션에서 사용자가 쓴 메시지와 선택지 답변 전부(시간순, 요약 없음). **판단이 갈리면 이 파일이 이긴다.**\n",
           f"> 원본: `{sess}`\n"]
    n_msg = n_ans = 0
    for line in open(sess, encoding="utf-8"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") != "user":
            continue
        try:
            t = dt.datetime.fromisoformat(d.get("timestamp", "").replace("Z", "+00:00")).astimezone(KST).strftime("%m-%d %H:%M")
        except ValueError:
            t = ""
        c = d.get("message", {}).get("content")
        blocks = [{"type": "text", "text": c}] if isinstance(c, str) else (c or [])
        for b in blocks:
            if b.get("type") == "text":
                x = b["text"].strip()
                if (not x or x.startswith("<system-reminder>") or "<task-notification>" in x
                        or x.startswith("Base directory for this skill")):
                    continue
                m = re.search(r"<command-name>(.*?)</command-name>", x)
                if m:
                    args = re.search(r"<command-args>(.*?)</command-args>", x, re.S)
                    x = f"`{m.group(1)}` " + (args.group(1).strip() if args else "")
                out.append(f"\n---\n\n## [{t}] 메시지\n\n{esc(redact(x))}\n")
                n_msg += 1
            elif b.get("type") == "tool_result":
                cc = b.get("content")
                if isinstance(cc, list):
                    cc = " ".join(i.get("text", "") for i in cc if isinstance(i, dict))
                cc = str(cc or "")
                if any(k in cc for k in ("The user answered", "Your questions have been answered", "doesn't want to proceed")):
                    cc = cc.split("Read the answers carefully")[0].split("You can now continue")[0]
                    out.append(f"\n---\n\n## [{t}] 선택지 답변 / 거절 사유\n\n{esc(redact(cc.strip()))}\n")
                    n_ans += 1
    dst = os.path.join(a.project, "docs", "references", f"{a.date}-user-verbatim.md")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "w", encoding="utf-8").write("".join(out))
    print(f"저장: {dst} (메시지 {n_msg} · 선택지 답변 {n_ans})")


if __name__ == "__main__":
    main()
