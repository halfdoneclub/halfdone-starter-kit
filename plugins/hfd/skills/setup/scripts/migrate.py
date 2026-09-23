#!/usr/bin/env python3
"""hfd 킷 설치 뒤 한 번: 옛 스타터 킷(cc-starter-kit) 설치본을 정리한다. 표준 라이브러리만 사용.

정리 대상 (이것만):
  - ~/.claude/settings.json 의 훅 항목 중 command 에 아래 파일 이름이 들어간 것
      hooks/session-start-context.sh · hooks/hallucination-guard.mjs
      hooks/session-end-autocapture.sh · hooks/precompact-handoff.sh   (구 킷 v2)
  - ~/.claude/hooks/ 의 같은 이름 파일
  - ~/.claude/skills/bootstrap, ~/.claude/skills/wrap  (옛 스타터 킷 스킬로 확인될 때만)
절대 건드리지 않는 것: 위 목록 밖의 모든 훅(사용자 안전 훅·ORCA·OMC 등), settings.local.json, 프로젝트 설정.

사용:
  migrate.py plan                 바꿀 목록만 보여준다 (아무것도 바꾸지 않음)
  migrate.py apply --yes          백업 후 정리하고, 결과를 검증한다
  migrate.py restore <백업폴더>    원래대로 되돌린다
경로는 CLAUDE_CONFIG_DIR(없으면 ~/.claude)을 따른다.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

CONF = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
SETTINGS = CONF / "settings.json"
OLD_HOOK_FILES = ("session-start-context.sh", "hallucination-guard.mjs", "session-end-autocapture.sh", "precompact-handoff.sh")
# 옛 스타터 킷 스킬인지 확인하는 표시 문구 (하나라도 있어야 대상)
SKILL_MARKS = {
    "bootstrap": ("CC Project Bootstrap",),
    "wrap": ("wrap_check", "APPEND ONLY", "HANDOFF"),
}


def is_old_hook(cmd: str) -> bool:
    return any(f"hooks/{name}" in cmd.replace("\\", "/") for name in OLD_HOOK_FILES)


def load_settings() -> dict:
    if not SETTINGS.exists():
        return {}
    return json.loads(SETTINGS.read_text(encoding="utf-8"))


def all_handlers(settings: dict):
    for event, groups in (settings.get("hooks") or {}).items():
        for gi, group in enumerate(groups or []):
            for hi, h in enumerate(group.get("hooks") or []):
                yield event, gi, hi, h.get("command", "") if isinstance(h, dict) else ""


def plan() -> dict:
    settings = load_settings()
    hooks = [(e, c) for e, _, _, c in all_handlers(settings) if is_old_hook(c)]
    keep = [(e, c) for e, _, _, c in all_handlers(settings) if not is_old_hook(c)]
    files = [CONF / "hooks" / n for n in OLD_HOOK_FILES if (CONF / "hooks" / n).exists()]
    skills, skipped = [], []
    for name, marks in SKILL_MARKS.items():
        d = CONF / "skills" / name
        f = d / "SKILL.md"
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if f"name: {name}" in text and any(m in text for m in marks):
            skills.append(d)
        else:
            skipped.append(f"{d} (옛 스타터 킷 스킬로 확인 안 됨 — 건드리지 않음)")
    return {"hooks": hooks, "keep": keep, "files": files, "skills": skills, "skipped": skipped}


def show(p: dict) -> None:
    print(f"설정 파일: {SETTINGS}")
    print(f"\n[정리할 훅 항목] {len(p['hooks'])}개")
    for e, c in p["hooks"]:
        print(f"  - {e}: {c}")
    print(f"\n[옮길 훅 파일] {len(p['files'])}개")
    for f in p["files"]:
        print(f"  - {f}")
    print(f"\n[옮길 옛 스킬] {len(p['skills'])}개")
    for d in p["skills"]:
        print(f"  - {d}")
    for s in p["skipped"]:
        print(f"  · 건너뜀: {s}")
    print(f"\n[그대로 두는 훅 항목] {len(p['keep'])}개 (사용자 안전 훅·다른 도구 훅 — 건드리지 않음)")
    for e, c in p["keep"]:
        print(f"  = {e}: {c[:110]}")
    if not (p["hooks"] or p["files"] or p["skills"]):
        print("\n정리할 것이 없습니다.")


def apply() -> int:
    p = plan()
    show(p)
    if not (p["hooks"] or p["files"] or p["skills"]):
        return 0
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = CONF / "backups" / f"hfd-setup-{stamp}"
    backup.mkdir(parents=True)
    manifest = {"created": stamp, "settings": None, "moved": []}

    if p["hooks"]:
        shutil.copy2(SETTINGS, backup / "settings.json")
        manifest["settings"] = str(SETTINGS)
        settings = load_settings()
        for event in list((settings.get("hooks") or {}).keys()):
            groups = []
            for group in settings["hooks"][event] or []:
                kept = [h for h in (group.get("hooks") or []) if not (isinstance(h, dict) and is_old_hook(h.get("command", "")))]
                if kept:
                    group = {**group, "hooks": kept}
                    groups.append(group)
            if groups:
                settings["hooks"][event] = groups
            else:
                del settings["hooks"][event]
        tmp = SETTINGS.with_suffix(".json.hfd-tmp")
        tmp.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, SETTINGS)

    for src in list(p["files"]) + list(p["skills"]):
        dest = backup / src.relative_to(CONF)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        manifest["moved"].append({"from": str(src), "backup": str(dest)})
    (backup / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # 사후 검증: 옛 훅 0개, 나머지 훅은 전부 그대로
    after = plan()
    ok = not after["hooks"] and sorted(after["keep"]) == sorted(p["keep"]) and not after["files"] and not after["skills"]
    if not ok:
        print("\n[검증 실패] 예상과 다름 → 자동 복원합니다.")
        restore(backup)
        return 1
    print(f"\n[완료] 옛 훅 {len(p['hooks'])}개 정리 · 파일 {len(p['files'])}개 · 옛 스킬 {len(p['skills'])}개 백업으로 이동")
    print(f"그대로 둔 훅 {len(p['keep'])}개 확인됨.")
    print(f"백업: {backup}")
    print(f'되돌리기: python3 "{Path(__file__).resolve()}" restore "{backup}"')
    return 0


def restore(backup: Path) -> int:
    backup = Path(backup)
    manifest = json.loads((backup / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("settings"):
        shutil.copy2(backup / "settings.json", manifest["settings"])
    for m in manifest["moved"]:
        src, dest = Path(m["backup"]), Path(m["from"])
        if dest.exists():
            print(f"  이미 있음, 건너뜀: {dest}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
    print(f"복원 완료: {backup}")
    return 0


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in ("plan", "apply", "restore"):
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    if cmd == "plan":
        show(plan())
        return 0
    if cmd == "apply":
        if "--yes" not in sys.argv:
            print("apply 는 사용자 확인 뒤 --yes 와 함께 실행합니다. 먼저 plan 으로 목록을 보여주세요.")
            return 2
        return apply()
    if len(sys.argv) < 3:
        print("restore <백업폴더>")
        return 2
    return restore(Path(sys.argv[2]))


if __name__ == "__main__":
    sys.exit(main())
