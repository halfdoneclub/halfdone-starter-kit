#!/usr/bin/env python3
"""sources/ 원문 → plugins/hfd/skills/harness/references/ 로 옮긴다. 요약하지 않는다.

- methodology.md       = sources/methodology/하네스-정석-방법론.md 그대로
                         (7단계 · 추가 기준 9줄 · 프로젝트별 차이표 · 공식 링크 2개 · OpenAI 트리 · Claude Code 디렉토리 전체)
- official/*.md        = Claude Code 공식 문서 원문 사본 (머리말: 원문 주소 · 받은 날)

끝나면 check_refs.py 로 누락을 센다. 원문을 갱신할 때도 이 순서: 원문 다시 받기 → build_refs → check_refs.
"""
from __future__ import annotations

import datetime as dt
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
REF = ROOT / "plugins/hfd/skills/harness/references"

OFFICIAL = [
    # (원문 사본, 원문 주소, 참고 파일 이름)
    ("anthropic/memory.md", "https://code.claude.com/docs/en/memory", "memory.md"),
    ("anthropic/best-practices.md", "https://code.claude.com/docs/en/best-practices", "best-practices.md"),
    ("anthropic/features-overview.md", "https://code.claude.com/docs/en/features-overview", "features-overview.md"),
    ("anthropic/claude-directory.ko.md", "https://code.claude.com/docs/ko/claude-directory", "claude-directory.ko.md"),
]


def main() -> None:
    (REF / "official").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC / "methodology/하네스-정석-방법론.md", REF / "methodology.md")
    fetched = dt.date.fromtimestamp((SRC / "anthropic/memory.md").stat().st_mtime).isoformat()
    for src, url, name in OFFICIAL:
        body = (SRC / src).read_text(encoding="utf-8")
        head = f"<!-- 원문: {url} · 받은 날: {fetched} · hfd 킷이 원문 그대로 보관 (tools/build_refs.py). 손으로 고치지 않는다. -->\n\n"
        (REF / "official" / name).write_text(head + body, encoding="utf-8")
    print(f"references 생성: methodology.md + official/ {len(OFFICIAL)}개")


if __name__ == "__main__":
    main()
