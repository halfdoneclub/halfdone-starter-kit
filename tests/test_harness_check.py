#!/usr/bin/env python3
"""harness_check.py 새 항목 시험 — 가짜 프로젝트를 임시 폴더에 만들어 PASS/FAIL을 확인한다.

실행: python3 tests/test_harness_check.py   (실패가 있으면 종료 코드 1)
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

CHECK = Path(__file__).resolve().parent.parent / "plugins/hfd/skills/harness/scripts/harness_check.py"

GOOD_CLAUDE = """# 테스트 프로젝트

## 파일 맵
- [docs/index.md](docs/index.md) — 문서 지도
- [CHANGELOG.md](CHANGELOG.md) — 현재 상태 + 세션 기록
"""
GOOD_DOCS_INDEX = """# docs
- [PRD.md](PRD.md) — 기획
- [contracts/](contracts/index.md) — 계약
"""
GOOD_PRD = """# 테스트

## 문제 정의
- 해결하는 문제: 계약서를 한곳에서 찾기 어렵다
- 성공 기준: done when 거래처 이름으로 계약서를 3초 안에 연다

## 하네스 설정
- 프로젝트 성격: 웹앱
- 검증 수단: 테스트 + 브라우저 자동 클릭 확인
- 꼭 막을 것: 테스트가 실패하면 완료 금지
- 평가 방식: 기능이 실제로 동작하는지 별도 확인

## 기능 목록
| 기능 | 확인 방법 | 상태 |
|---|---|---|
| 거래처 검색 | 이름 입력 → 목록에 표시 | 실패 |
"""
import datetime as _dt
_TODAY = _dt.date.today().isoformat()
HANDOFF_THIN = f"""# HANDOFF
updated: {_TODAY}

## 트랙
- [ ] 할 일 하나
"""
LAST = """## 지난 세션 (2026-10-06 00:00)
- 하던 일: [트랙] 계약서 검색 화면을 만들던 중
- 끝낸 것: 검색창 `src/search.tsx`
- 멈춘 곳·첫 행동: 결과 정렬 전 → 정렬 기준을 사용자에게 묻기

"""
HANDOFF_GOOD = f"""# HANDOFF
updated: {_TODAY}

{LAST}## 트랙
목표(사용자 원문): "계약서를 빨리 찾고 싶다"
- [ ] 할 일 하나
**읽는 순서:** 1. `docs/PRD.md`
"""
CHANGELOG = """# Changelog

## 현재 상태
| 트랙 | 상태 | 어디 |
|---|---|---|

## 세션 로그
<!-- ⚠️ APPEND ONLY — 아래 항목을 절대 삭제/수정하지 마세요. 새 항목은 이 줄 바로 아래에 추가합니다. -->
"""


def make(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


def run(root: Path, extra: list[str] | None = None) -> tuple[int, str]:
    mem = root / "_mem"
    mem.mkdir(exist_ok=True)
    (mem / "MEMORY.md").write_text("# 메모리\n", encoding="utf-8")
    r = subprocess.run([sys.executable, str(CHECK), "--project", str(root), "--memory", str(mem)] + (extra or []),
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout


def base() -> dict[str, str]:
    return {
        "CLAUDE.md": GOOD_CLAUDE,
        "CHANGELOG.md": CHANGELOG,
        "docs/index.md": GOOD_DOCS_INDEX,
        "docs/PRD.md": GOOD_PRD,
        "docs/contracts/index.md": "# contracts\n- [a사.md](a사.md) — A사 계약\n",
        "docs/contracts/a사.md": "# A사\n",
    }


CASES = [
    # (이름, 바꿀 파일들, 기대 종료 코드, 결과에 있어야 할 문구)
    ("정상 — 고유 폴더(contracts)가 있어도 통과", {}, 0, "문서 지도 (docs/)"),
    ("CLAUDE.md 201줄", {"CLAUDE.md": GOOD_CLAUDE + "\n" * 200}, 1, "CLAUDE.md 길이"),
    ("파일 맵 칸 없음", {"CLAUDE.md": "# 테스트\n"}, 1, "「## 파일 맵」 칸 없음"),
    ("파일 맵에 docs/index.md 없음", {"CLAUDE.md": "# 테스트\n\n## 파일 맵\n- [CHANGELOG.md](CHANGELOG.md)\n"}, 1, "docs/index.md가 파일 맵에 없음"),
    ("고아 문서", {"docs/contracts/b사.md": "# B사\n"}, 1, "index.md에 없는 항목"),
    ("폴더에 index.md 없음", {"docs/designs/final.md": "# 최종\n", "docs/index.md": GOOD_DOCS_INDEX + "- [designs/](designs/final.md) — 디자인\n"}, 1, "docs/designs/ 에 index.md 없음"),
    ("깨진 링크", {"docs/index.md": GOOD_DOCS_INDEX + "- [없음.md](없음.md)\n"}, 1, "깨진 링크"),
    ("하네스 설정 빈 칸", {"docs/PRD.md": GOOD_PRD.replace("평가 방식: 기능이 실제로 동작하는지 별도 확인", "평가 방식:")}, 1, "평가 방식 비어 있음"),
    ("기능 확인 방법 빈 칸", {"docs/PRD.md": GOOD_PRD.replace("| 거래처 검색 | 이름 입력 → 목록에 표시 | 실패 |", "| 거래처 검색 |  | 실패 |")}, 1, "확인 방법 빈 줄"),
    ("archive는 등록 안 해도 됨", {"docs/archive/old.md": "# 옛날\n"}, 0, "문서 지도 (docs/)"),
    ("HANDOFF 할 일만 있고 목표·읽는 순서 없음", {".claude/HANDOFF.md": HANDOFF_THIN}, 1, "HANDOFF 맥락 칸"),
    ("HANDOFF 목표·읽는 순서 있음", {".claude/HANDOFF.md": HANDOFF_GOOD}, 0, "할 일 있는 트랙 모두 목표·읽는 순서 있음"),
    ("HANDOFF 지난 세션 칸 없음", {".claude/HANDOFF.md": HANDOFF_GOOD.replace(LAST, "")}, 1, "「## 지난 세션」 칸 없음"),
    ("HANDOFF 지난 세션 첫 행동 빈 칸", {".claude/HANDOFF.md": HANDOFF_GOOD.replace("멈춘 곳·첫 행동: 결과 정렬 전 → 정렬 기준을 사용자에게 묻기", "멈춘 곳·첫 행동:")}, 1, "첫 행동 비어 있음"),
    ("HANDOFF 지난 세션 칸 있음", {".claude/HANDOFF.md": HANDOFF_GOOD}, 0, "하던 일·끝낸 것·첫 행동 있음"),
    ("wrap 실행(키워드)인데 사용자 원문 없음", {"__extra__": "--keywords 테스트"}, 1, "사용자 원문"),
    ("wrap 실행(키워드) + 사용자 원문 있음", {"__extra__": "--keywords 테스트", "docs/references/index.md": "# references\n- [2026-10-04-user-verbatim.md](2026-10-04-user-verbatim.md) — 원문\n", "docs/references/2026-10-04-user-verbatim.md": "# 원문\n", "docs/index.md": GOOD_DOCS_INDEX + "- [references/](references/index.md) — 근거\n"}, 0, "| PASS | 사용자 원문"),
    ("bootstrap 틀의 형식 예시(코드 표시 안 링크)는 링크로 안 셈", {"docs/index.md": GOOD_DOCS_INDEX + "형식: `- [이름](경로) — 한 줄 설명`\n\n```markdown\n- [예시](없는파일.md)\n```\n"}, 0, "문서 지도 (docs/)"),
]


def main() -> int:
    bad = 0
    for name, change, want_code, want_text in CASES:
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            files = base()
            files.update(change)
            extra = files.pop("__extra__", "").split()
            make(root, files)
            code, out = run(root, extra)
            ok = code == want_code and want_text in out
            bad += not ok
            print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  (종료 {code}, 기대 {want_code})"))
            if not ok:
                print("\n".join(l for l in out.splitlines() if l.startswith("| FAIL") or l.startswith("| WARN")))
    print(f"\n{len(CASES) - bad}/{len(CASES)} 통과")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
