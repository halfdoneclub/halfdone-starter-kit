#!/usr/bin/env python3
"""export_user_verbatim.py 시험 — 같은 날 다른 세션의 원문 파일을 덮어쓰지 않는지 확인한다.

실행: python3 tests/test_export_user_verbatim.py   (실패가 있으면 종료 코드 1)
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "plugins/hfd/skills/wrap/scripts/export_user_verbatim.py"
DATE = "2026-01-02"


def session(folder: Path, name: str, text: str) -> Path:
    p = folder / f"{name}.jsonl"
    p.write_text(json.dumps({"type": "user", "timestamp": "2026-01-02T03:04:05Z",
                             "message": {"content": text}}, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


def run(project: Path, sess: Path) -> None:
    subprocess.run([sys.executable, str(SCRIPT), "--project", str(project), "--session", str(sess), "--date", DATE],
                   check=True, capture_output=True)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        project = tmp / "proj"
        refs = project / "docs" / "references"
        first = session(tmp, "aaaaaaaa-1111", "첫 세션 말")
        second = session(tmp, "bbbbbbbb-2222", "둘째 세션 말")
        base = refs / f"{DATE}-user-verbatim.md"
        other = refs / f"{DATE}-user-verbatim-bbbbbbbb.md"

        run(project, first)
        assert "첫 세션 말" in base.read_text(encoding="utf-8")

        run(project, second)  # 다른 세션 → 첫 파일은 그대로, 새 이름으로 저장
        assert "첫 세션 말" in base.read_text(encoding="utf-8"), "다른 세션이 첫 파일을 덮어씀"
        assert "둘째 세션 말" in other.read_text(encoding="utf-8")

        first.write_text(first.read_text(encoding="utf-8").replace("첫 세션 말", "첫 세션 고친 말"), encoding="utf-8")
        run(project, first)  # 같은 세션 두 번째 → 같은 파일 갱신
        assert "첫 세션 고친 말" in base.read_text(encoding="utf-8")
        run(project, second)
        assert {p.name for p in refs.iterdir()} == {base.name, other.name}, "파일이 더 생김"
    print("export_user_verbatim 시험 4/4 통과")


if __name__ == "__main__":
    main()
