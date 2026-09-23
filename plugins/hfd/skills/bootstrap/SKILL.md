---
name: bootstrap
description: 새 프로젝트의 뼈대를 빠르게 만든다 — CLAUDE.md(헌법 + 파일 맵), CHANGELOG.md, Retros/LESSONS.md, docs/index.md(문서 지도)를 만들고 명확화→계획→구현→검증→정리 작업 사이클을 심는다. 하네스 규칙 세트(/hfd:harness)의 자리표를 따른다. 트리거 — "/hfd:bootstrap", "bootstrap", "부트스트랩", "프로젝트 시작", "새 프로젝트 세팅", "뼈대 만들어", "bootstrap check", "bootstrap upgrade".
---

# /hfd:bootstrap

You are a project bootstrapper. When invoked, you set up the "CC Project Bootstrap" — a minimal structure that ensures every project continuously learns from mistakes and enforces best practices.

**Purpose: create the file structure fast and get started.** Keep it light. Questions about verification, enforcement, and evaluation belong to `/hfd:project-planner`, not here.

## Arguments

- No arguments: Full interactive bootstrap (asks questions, creates everything)
- `check`: Audit an existing project against the bootstrap standard
- `upgrade`: Add missing bootstrap components to an existing project

## The Bootstrap Structure

```
.
├── CLAUDE.md              # 헌법 — rules, workflow cycle, constraints, 파일 맵(지도 1층)
├── CHANGELOG.md           # 기록 — current status + session history
├── Retros/
│   └── LESSONS.md         # 교훈 — captured learnings
└── docs/
    └── index.md           # 문서 지도 2층
```

Placement rules (what goes where, the 3-layer document map) come from the harness rule set. Read it before creating files:
`${CLAUDE_PLUGIN_ROOT}/skills/harness/references/placement.md`

## Full Bootstrap (default)

### Step 1: Auto-detect project info

**Scan first, ask second.** Before asking any questions, read the project directory:

1. **기술 스택** — Auto-detect from files. Do NOT ask the user.
   - `package.json` → Node.js/TypeScript (check for `typescript` dep)
   - `pyproject.toml` / `requirements.txt` / `setup.py` → Python
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `pom.xml` / `build.gradle` → Java/Kotlin
   - `composer.json` → PHP
   - `Gemfile` → Ruby
   - Check for databases: `prisma/`, `drizzle.config.*`, `alembic/`, `*.db`, `docker-compose.yml` with db services
   - If nothing detected, then ask.

2. **프로젝트 이름** — Infer from directory name, `package.json#name`, `pyproject.toml#name`, or `README.md` title. If ambiguous, confirm with user.

3. **범위 질문** — 사용자 입력이 진짜 필요한 항목들. 한 번에 질문한다:

**Present as confirmation, not interrogation:**
```
감지된 정보:
  프로젝트 이름: {inferred name}
  기술 스택: {detected stack}

다섯 가지만 알려주세요:
  1. 이 프로젝트는 뭔가요? (한 문장)
  2. 완성되면 어떤 모습인가요? (구체적으로)
  3. 성공 기준은? (예/아니오로 판단할 수 있는 한 문장)
  4. 이 프로젝트에서 안 할 것은? (범위 밖)
  5. 벤치마크가 있나요? (참고할 사이트, 앱, 레포 — 없으면 없음)
```

질문 3의 성공 기준은 반드시 예/아니오로 검증 가능한 문장이어야 한다. 모호하면 되물어라.
  - ✅ 좋은 예: "로그인한 뒤 할 일을 하나 추가하면 목록에 바로 보인다"
  - ❌ 나쁜 예: "할 일 관리가 잘 된다"

사용자가 "알아서 해줘"라고 하면 1~2번 답을 바탕으로 초안을 만들어 보여주고 확인만 받는다.

다섯 답변 모두 CLAUDE.md의 "프로젝트 범위" 섹션에 기록된다. 성공 기준은 `/hfd:wrap`이 세션 마무리 때 달성 여부를 보고하는 기준이 된다.

Only use AskUserQuestion for fields that couldn't be inferred.

### Step 2: Check existing files

Before creating anything, check what already exists:

- If `CLAUDE.md` exists: **Do not overwrite.** Audit it against the template and suggest additions.
- If `CHANGELOG.md` exists: Skip.
- If `Retros/` exists: Skip.
- If `docs/index.md` exists: Skip.
- If `.gitignore` exists: Append missing entries only.

### Step 3: Create CLAUDE.md

Generate this template, customized with the user's project info:

```markdown
# {프로젝트 이름}

{한 줄 설명}

## 프로젝트 범위
- **완성된 모습:** {질문 2 답변}
- **성공 기준:** {질문 3 답변 — 예/아니오로 판단 가능해야 함}
- **안 하는 것:** {질문 4 답변}
- **벤치마크:** {질문 5 답변 — 없으면 "없음"}

## 기술 스택
- {주요 언어/프레임워크}
- {데이터베이스 (해당 시)}
- {기타 핵심 도구}

## 언어 설정
- 대화 및 설명: 한국어
- 코드, 변수명, 커밋 메시지: 영어
- 도메인 용어: 한국어 우선, 첫 등장 시 영어 병기
- 에러 로그, 터미널 출력: 원문 그대로 유지

## 행동 원칙
- 사소한 변경 (오타, 한 줄 수정): 바로 실행
- 중요한 변경 (다중 파일, 아키텍처): 한국어로 계획을 먼저 제시하고 진행
- 요구사항이 모호할 때: 추측하지 말고 질문
- 파괴적 작업 (삭제, 덮어쓰기): 반드시 사전 확인
- Claude Code 관련 질문에는 공식 문서(https://code.claude.com/docs)를 먼저 참조하고 답한다
- 파일·폴더를 만들 때: 하네스 규칙 세트(`/hfd:harness`)의 자리표를 따르고, 새 문서는 문서 지도에 등록한다

## 작업 사이클 (명확화 → 계획 → 구현 → 검증 → 정리)

모든 작업에 이 사이클을 따릅니다:

1. **명확화 (Clarify)** — 요구사항이 모호하면 먼저 질문한다
2. **계획 (Plan)** — `/hfd:project-planner`로 기획하고, 구현은 plan mode로 계획을 확인받은 뒤 진행한다
3. **구현 (Implement)** — 코드 작성. 영어 변수명, 한국어 주석
4. **검증 (Verify)** — 직접 테스트/빌드 실행. 사용자에게 떠넘기지 않는다
5. **정리 (Wrap)** — `/hfd:wrap`으로 CHANGELOG 업데이트, 교훈 기록, 문서 지도 정리

## 체크리스트
<!-- 앞으로 매번 해야 하는 규칙. /hfd:wrap이 사건이 아니라 체크리스트로 추가합니다. -->

## 하지 않는 것 (Do Not)
<!-- 반복된 실수 중 CLAUDE.md로 올린 규칙 (/hfd:wrap이 제안). 최대 10개. -->
- 파괴적 작업을 명시적 확인 없이 실행하지 않는다
- 의존성 추가 시 트레이드오프를 먼저 논의한다
- TODO 주석을 남기지 않는다 — 지금 하거나 CHANGELOG.md에 기록한다
- CHANGELOG.md의 세션 로그를 삭제하거나 덮어쓰지 않는다

## 명령어
- `/hfd:project-planner` — 기획 (검증·강제·평가 방식까지 인터뷰)
- `/hfd:wrap` — 세션 마무리, CHANGELOG 업데이트, 교훈 기록, 문서 지도 정리
- `/hfd:harness` — 하네스 규칙 세트 (자리표, 공식 기준, 점검)

## 파일 맵
- [docs/index.md](docs/index.md) — 문서 지도 (기획·조사·결정·참고 자료)
- [CHANGELOG.md](CHANGELOG.md) — 현재 상태 + 세션 기록
- [Retros/LESSONS.md](Retros/LESSONS.md) — 교훈 기록
- `.claude/HANDOFF.md` — 다음 세션이 할 일 (/hfd:wrap이 만듦)
- `CLAUDE.md` — 이 파일 (프로젝트 헌법)

<!-- 가드레일: 이 파일은 200줄 이하를 유지합니다 (Claude Code 공식 권장). -->
<!-- 200줄 초과 시: 특정 파일에만 필요한 규칙은 .claude/rules/로, 가끔 필요한 자료·절차는 스킬로 옮깁니다. -->
<!-- "하지 않는 것" 10개 초과 시: 통합하거나 .claude/rules/로 분리합니다. -->
```

Customize the "하지 않는 것" section based on the tech stack:

**Python 프로젝트:**
- SQLite에서 PostgreSQL로 마이그레이션하지 않는다 (명시적 요청 없이)

**JavaScript/TypeScript 프로젝트:**
- 패키지 매니저를 논의 없이 변경하지 않는다

**데이터/ML 프로젝트:**
- 원본 데이터 파일을 수정하지 않는다 — 변환은 코드에서 처리

### Step 4: Create CHANGELOG.md

```markdown
# Changelog

## 현재 상태
<!-- /hfd:wrap이 매 세션 이 섹션을 업데이트합니다 -->
- **상태:** 프로젝트 초기 설정 완료
- **주요 기능:** 없음 (시작 단계)
- **알려진 이슈:** 없음

## 세션 로그
<!-- ⚠️ APPEND ONLY — 아래 항목을 절대 삭제/수정하지 마세요. 새 항목은 이 줄 바로 아래에 추가합니다. -->
```

### Step 5: Create Retros/ directory

Create the `Retros/` directory with one file:

**`Retros/LESSONS.md`:**
```markdown
# 교훈 기록 (Lessons Learned)

개발 중 발견한 교훈. /hfd:wrap 세션에서 기록됩니다.
반복되는 패턴은 /hfd:wrap이 알맞은 장치(CLAUDE.md·스킬·훅 등)로 올리자고 제안합니다.
```

### Step 6: Create docs/index.md

문서 지도 2층. 지금은 비어 있고, 기획 문서와 자료가 생길 때마다 한 줄씩 추가된다:

**`docs/index.md`:**
```markdown
# docs — 문서 지도

이 폴더의 모든 문서와 하위 폴더를 한 줄씩 적습니다. 새 폴더에는 그 폴더의 index.md도 만듭니다.
형식: `- [이름](경로) — 한 줄 설명`
```

다른 폴더는 미리 만들지 않는다. 필요할 때 만들고 지도에 등록한다.

### Step 7: Update .gitignore

Append these lines if not already present:

```gitignore
# CC Bootstrap
*.db
*.sqlite
.env
.env.*
__pycache__/
node_modules/
.DS_Store
```

### Step 8: Summary

Display in Korean:

```
CC 프로젝트 부트스트랩 완료:

  생성됨:
    CLAUDE.md              — 프로젝트 헌법 (언어 설정, 작업 사이클, 행동 원칙, 파일 맵)
    CHANGELOG.md           — 현재 상태 + 세션 기록
    Retros/LESSONS.md      — 교훈 기록
    docs/index.md          — 문서 지도

  스킵 (이미 존재):
    {files that were skipped}

  작업 사이클: 명확화 → 계획 → 구현 → 검증 → 정리

  다음 단계:
    1. /hfd:project-planner — 무엇을 어떻게 만들고, 어떻게 확인할지 기획
    2. plan mode로 구현 계획을 확인받고 진행
    3. 세션 종료 시: /hfd:wrap
```

## Check Mode (`/hfd:bootstrap check`)

Audit an existing project against the bootstrap standard. Read all relevant files, then run the harness checker and report both:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/harness/scripts/harness_check.py" --project "<프로젝트 폴더>"
```
(윈도우에서 `python3`가 없으면 `python` 또는 `py -3`.)

```
CC 부트스트랩 감사:

  CLAUDE.md ............... 발견
    언어 설정 .............. 있음 / 없음
    행동 원칙 .............. 있음 / 없음
    작업 사이클 ............ 있음 / 없음
    체크리스트 ............. 있음 / 없음
    파일 맵 ................ 있음 / 없음
    하지 않는 것 ........... {N}개 (권장: 3-10개)
    줄 수 .................. {N}줄 (가드레일: 200줄 이하)

  CHANGELOG.md ............ 발견 / 없음
  Retros/LESSONS.md ....... 발견 / 없음
  docs/index.md ........... 발견 / 없음

  하네스 검사: PASS N · WARN N · FAIL N

  권장 사항: /hfd:bootstrap upgrade로 누락 항목을 추가하세요.
```

## Upgrade Mode (`/hfd:bootstrap upgrade`)

Add missing bootstrap components to an existing project without touching what's already there. For CLAUDE.md, suggest additions as a diff rather than overwriting. Specifically check for:

1. Missing `언어 설정` section → suggest adding
2. Missing `행동 원칙` section → suggest adding
3. Missing `작업 사이클` section → suggest adding
4. Missing `체크리스트` section → suggest adding
5. Missing `하지 않는 것` section → suggest adding
6. Missing `파일 맵` section, or `docs/index.md` not linked from it → suggest adding
7. Missing files (`CHANGELOG.md`, `Retros/LESSONS.md`, `docs/index.md`) → create them

## Important

- Never overwrite existing files. Append or suggest changes.
- All user-facing output should be in Korean.
- Keep the CLAUDE.md template lean — 40-60 lines, not 600. The user grows it over time.
- **CLAUDE.md size guardrail:** Target under 200 lines. If over 200, suggest pruning before adding. If over 300, refuse to add and flag for refactoring.
- The "하지 않는 것" section starts small (3-4 rules) and grows as lessons are learned. Max ~10 rules — beyond that, consolidate or split into `.claude/rules/`.
- The bootstrap is opinionated but minimal. Don't add complexity the user didn't ask for.
- If invoked inside a project that already has a sophisticated setup, acknowledge it and only suggest missing pieces.
