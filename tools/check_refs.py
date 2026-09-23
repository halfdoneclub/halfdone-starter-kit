#!/usr/bin/env python3
"""누락 검사 — references 가 원문을 빠짐없이 담았는지 센다. 하나라도 빠지면 종료 코드 1.

1. Claude Code 디렉토리 탐색 데이터의 모든 값(필드 265개)이 methodology.md 에 있다
2. OpenAI 트리 원문이 methodology.md 에 글자 그대로 있다
3. 공식 문서 링크 2개가 methodology.md 와 harness/SKILL.md 에 있다
4. official/ 사본 본문이 sources/ 원문과 바이트 단위로 같다
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cc_directory as cc  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "plugins/hfd/skills/harness/references"
SKILL = ROOT / "plugins/hfd/skills/harness/SKILL.md"
LINKS = ["https://openai.com/ko-KR/index/harness-engineering/", "https://code.claude.com/docs/ko/claude-directory"]
FIELDS = ("label", "oneLiner", "note", "when", "description", "contains", "tips", "exampleIntro", "example", "docsLink")


def main() -> int:
    md = (REF / "methodology.md").read_text(encoding="utf-8")
    missing, checked = [], 0

    tree = cc.load()
    for root in (tree["project"], tree["global"]):
        for n, path, _ in cc.walk(root):
            for f in FIELDS:
                for v in cc.as_list(n.get(f)):
                    checked += 1
                    if v not in md:
                        missing.append(f"methodology.md ← 디렉토리 {'/'.join(path)} :: {f}")

    checked += 1
    openai_tree = (ROOT / "sources/openai/harness-engineering-트리.txt").read_text(encoding="utf-8").rstrip()
    if openai_tree not in md:
        missing.append("methodology.md ← OpenAI 트리")

    skill = SKILL.read_text(encoding="utf-8") if SKILL.exists() else ""
    for url in LINKS:
        checked += 2
        if url not in md:
            missing.append(f"methodology.md ← 링크 {url}")
        if url not in skill:
            missing.append(f"harness/SKILL.md ← 링크 {url}")

    for src, _, name in __import__("build_refs").OFFICIAL:
        checked += 1
        body = (ROOT / "sources" / src).read_text(encoding="utf-8")
        copy = (REF / "official" / name).read_text(encoding="utf-8")
        if not copy.endswith(body):
            missing.append(f"official/{name} ← 원문과 다름")

    print(f"검사한 값 {checked}개 · 빠진 것 {len(missing)}개")
    for m in missing:
        print("  빠짐:", m)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
