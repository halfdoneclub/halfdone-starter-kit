# 자리표 — 무엇을 어디에 두고, 어떻게 찾게 하나

hfd 킷의 공용 규칙이다. `/hfd:bootstrap`은 뼈대를 만들 때, `/hfd:project-planner`는 기획 문서를 둘 때, `/hfd:wrap`은 정리할 때 이 파일을 따른다.

**원칙 세 가지**
1. 정해진 자리에 둔다.
2. **새 폴더·새 문서는 자유롭게 만든다.** 아래 표에 없다고 막지 않는다.
3. 대신 **모든 문서는 지도에서 찾아갈 수 있어야 한다** (아래 「지도 3층」).

---

## 1. 고정 자리 — Claude Code가 정한 위치

Claude Code는 이 위치의 파일만 읽는다. 이름이나 위치를 바꾸면 도구가 못 읽는다.
파일별 역할, 불러오는 시점, 예시는 `methodology.md` 4-2절(공식 디렉토리 원문)에 있다.

| 자리 | 용도 |
|---|---|
| `CLAUDE.md` (또는 `.claude/CLAUDE.md`) | 프로젝트 헌법 + 지도 1층 (아래 2절) |
| `.claude/settings.json` | 권한·훅 (팀 공유) |
| `.claude/settings.local.json` | 개인 설정 (git 제외) |
| `.claude/rules/*.md` | 주제별 지침. `paths:`를 달면 해당 파일을 다룰 때만 불러온다 |
| `.claude/skills/<이름>/SKILL.md` | 반복 절차·참고 자료 |
| `.claude/agents/*.md` | 서브에이전트 |
| `.mcp.json` | 외부 도구 연결 |

---

## 2. `CLAUDE.md` — 헌법이자 메인 가이드

- **역할:** 모든 작업에 적용되는 핵심 규칙과, "무엇은 어디를 보라"는 안내를 담는다.
- **분량:** 공식 권장은 200줄 이하다. 검사기가 센다.
  - 원문: `official/memory.md`의 "target under 200 lines per CLAUDE.md file"
- **넣을 것·뺄 것:** `official/best-practices.md`의 Include / Exclude 표를 따른다.
- **넘칠 때 옮길 곳:** 특정 파일에만 필요한 규칙은 `.claude/rules/`로, 가끔 필요한 참고 자료나 절차는 스킬로 옮긴다.
  - 원문: `official/features-overview.md`의 "CLAUDE.md vs Rules vs Skills"
- **「파일 맵」 칸:** 지도 1층이다. 프로젝트의 주요 파일·폴더를 링크로 적는다.

---

## 3. 기본 자리 — hfd 스킬이 만드는 파일

| 자리 | 무엇 | 만드는 스킬 |
|---|---|---|
| `CHANGELOG.md` | 「현재 상태」(15줄 이하) + 「세션 로그」(APPEND ONLY) | bootstrap, wrap |
| `Retros/LESSONS.md` | 교훈 기록 | bootstrap, wrap |
| `.claude/HANDOFF.md` | 다음 세션이 할 일 (80줄 이하) | wrap |
| `docs/index.md` | 지도 2층 | bootstrap |
| `docs/REQUEST.md`, `docs/PRD.md`, `docs/AGENT_DESIGN.md` | 기획 문서 | project-planner |
| `docs/references/` | 사용자가 준 맥락 자료·링크 | project-planner |
| `docs/research/` | 조사 결론 | wrap |
| `docs/decisions/` | 결정과 이유 | wrap |
| `docs/archive/` | 넘친 옛 내용 | wrap |

- 표의 폴더는 **필요할 때만** 만든다. 빈 폴더를 미리 만들지 않는다.

---

## 4. 자유 자리 — 프로젝트 고유 폴더

- 프로젝트에 필요하면 어떤 폴더든 만든다.
  - 예: `docs/contracts/`(계약 관리), `docs/tax-invoices/`, `docs/approved-designs/`(승인된 디자인 산출물)
- **막지 않는다. 폴더 개수와 이름도 검사하지 않는다.**
- 조건은 하나다. 아래 「지도 3층」에 등록한다.

---

## 5. 지도 3층 — 에이전트가 무엇이든 찾아갈 수 있게

```
CLAUDE.md 「파일 맵」            ← 1층: 최상위 지도 (헌법 안)
 └─ docs/index.md               ← 2층: docs/ 전체 지도
     └─ docs/<폴더>/index.md    ← 3층: 폴더별 지도
```

| 층 | 무엇을 적나 |
|---|---|
| 1층 `CLAUDE.md` 「파일 맵」 | `docs/index.md`와 루트의 주요 파일·폴더 (`CHANGELOG.md`, `Retros/`, 루트에 만든 고유 폴더) |
| 2층 `docs/index.md` | `docs/` 바로 아래의 모든 파일과 폴더 |
| 3층 `docs/<폴더>/index.md` | 그 폴더 안의 모든 파일과 하위 폴더 |

**적는 형식:** 한 줄에 한 항목. 링크 + 한 줄 설명.

```markdown
- [PRD.md](PRD.md) — 제품 요구사항 · 기능 목록
- [contracts/](contracts/index.md) — 거래처별 계약서와 조건
```

**규칙**
- 새 문서나 새 폴더를 만들면 **그 자리의 index에 한 줄**을 추가한다. 새 폴더에는 `index.md`도 만든다.
- 링크는 실제로 있는 파일을 가리켜야 한다.
- 검사기가 확인한다:
  - `docs/` 아래 index에 없는 문서가 있는가 (고아 문서)
  - 깨진 링크가 있는가
  - 폴더에 `index.md`가 없는가
- `/hfd:wrap`이 세션을 마칠 때 이번 세션에 생긴 문서를 등록한다.
- `docs/archive/` 안은 등록하지 않아도 된다. 넘친 옛 내용을 원문 그대로 보관하는 곳이기 때문이다.
