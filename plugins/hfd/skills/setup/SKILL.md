---
name: setup
description: hfd 스타터 킷을 설치한 뒤 한 번 실행 — 킷이 쓰는 준비물(Git·Python·Node.js)이 없으면 알아서 설치하고, 옛 스타터 킷(cc-starter-kit)의 스킬·훅이 남아 있으면 백업한 뒤 정리한다. 트리거 — "/hfd:setup", "hfd setup", "스타터 킷 설치", "킷 셋업", "옛 킷 정리".
disable-model-invocation: true
---

# /hfd:setup

설치 직후 한 번 실행한다. 순서대로 진행하고, 단계마다 결과를 한 줄씩 보여준다.

## 1. 준비물 확인·설치

킷의 검사기는 Python, 훅은 Git Bash(윈도우)와 Node.js로 돈다. 없으면 **알아서 설치한다.**
설치 명령은 사용자 PC를 바꾸므로, 실행 직전에 "무엇을 설치합니다" 한 줄을 알리고 진행한다.

1. 운영체제 확인: macOS / Windows.
2. 각각 있는지 확인한다.
   - Git: `git --version`
   - Python: `python3 --version` (윈도우는 `python --version` 또는 `py -3 --version`)
   - Node.js: `node --version`
3. 없는 것만 설치한다.

| 운영체제 | 설치 명령 |
|---|---|
| Windows (winget) | `winget install --id Git.Git -e --silent` · `winget install --id Python.Python.3.12 -e --silent` · `winget install --id OpenJS.NodeJS.LTS -e --silent` |
| macOS (Homebrew 있음) | `brew install git python node` |
| macOS (Homebrew 없음) | Git·Python: `xcode-select --install` (설치 창이 뜨면 사용자가 "설치"를 누른다) · Node.js: https://nodejs.org 의 LTS 설치 파일 |

- **사용자를 부르는 경우:** 관리자 암호 입력, 설치 창의 버튼 클릭처럼 사람이 해야 하는 지점에서만 멈춘다. 무엇을, 어디서 하면 되는지 한 번에 알려주고, 끝나면 이어서 진행한다.
- **winget이 없는 윈도우:** Microsoft Store의 "앱 설치 관리자(App Installer)"를 설치하면 winget이 생긴다고 안내한다.
- 설치 뒤 다시 버전을 확인한다. 새 터미널이 필요하면 Claude Code 재시작을 안내한다.

## 2. 옛 스타터 킷 정리

옛 `cc-starter-kit`의 스킬·훅이 남아 있으면, hfd 킷과 같은 스킬이 두 벌 뜨고 훅이 겹친다. 정리 스크립트가 **정해진 항목만** 백업 후 정리한다.

1. 목록 보기 (아무것도 바꾸지 않음):
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/migrate.py" plan
   ```
2. 출력된 목록을 사용자에게 보여준다: 정리할 훅, 옮길 파일·스킬, **그대로 두는 훅**. 그리고 AskUserQuestion으로 진행할지 묻는다.
3. 동의하면 실행한다 (백업 → 정리 → 검증. 검증에 실패하면 자동으로 되돌린다):
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/migrate.py" apply --yes
   ```
4. 출력된 **백업 위치와 되돌리기 명령**을 사용자에게 그대로 전한다.

- 정리 대상은 옛 킷에서 온 것뿐이다: 훅 파일 4종, bootstrap·wrap 스킬.
- 그 밖의 훅(사용자가 직접 만든 안전 훅, 다른 도구의 훅)과 `settings.local.json`은 건드리지 않는다.
- 윈도우에서 `python3`가 없으면 `python` 또는 `py -3`로 실행한다.

## 3. 따로 설치된 옛 planner 끄기

`halfdone-cc-planner` 플러그인이 설치돼 있으면, hfd 킷의 `/hfd:project-planner`와 같은 스킬이 두 벌이 된다. 끌지 묻고, 동의하면 끈다:
```bash
claude plugin disable halfdone-cc-planner@halfdone-cc-planner
```
- `claude` 명령을 못 찾으면 설치 위치로 다시 실행한다: `~/.local/bin/claude plugin disable halfdone-cc-planner@halfdone-cc-planner` (윈도우: `%USERPROFILE%\.local\bin\claude.exe`).
- 그래도 없으면 사용자에게 안내한다: `/plugin` → Installed → `halfdone-cc-planner` → **Disable**.

## 4. 자동 업데이트 켜기 (한 번)

Anthropic 공식이 아닌 마켓플레이스는 자동 업데이트가 기본으로 꺼져 있다. 사용자에게 안내한다:
`/plugin` → Marketplaces → `halfdone-starter-kit` → **Enable auto-update**

## 5. 끝 — 보고

| 무엇 | 결과 |
|---|---|
| 준비물 | Git ✓ · Python ✓ · Node.js ✓ (새로 설치한 것 표시) |
| 옛 킷 정리 | 훅 N개 · 스킬 N개 정리, 백업 위치 |
| 옛 planner | 끔 / 유지 / 없음 |
| 자동 업데이트 | 켜는 법 안내함 |

마지막 줄: "이제 새 프로젝트 폴더에서 `/hfd:bootstrap`으로 시작하세요. 변경 사항은 Claude Code를 다시 시작하면 적용됩니다."
