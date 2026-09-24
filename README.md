# halfdone-starter-kit

하프던클럽 Claude Code 스타터 킷. 프로젝트마다 **공식 기준(OpenAI·Anthropic·Claude Code 문서)에 맞는 하네스**를 짜도록 돕는다.
하네스는 에이전트가 일하는 환경을 말한다: 규칙, 문서 지도, 검증·강제·평가 장치.

## 설치 (처음 한 번)

Claude Code에서 순서대로 입력한다.

```
/plugin marketplace add halfdoneclub/halfdone-starter-kit
/plugin install hfd@halfdone-starter-kit
```

1. Claude Code를 다시 시작한다.
2. `/hfd:setup`을 실행한다. 필요한 준비물(Git·Python·Node.js)을 설치하고, 옛 `cc-starter-kit`이 있으면 정리한다.
3. **자동 업데이트를 켠다:** `/plugin` → Marketplaces → `halfdone-starter-kit` → **Enable auto-update**.
   Anthropic 공식이 아닌 마켓플레이스는 자동 업데이트가 기본으로 꺼져 있어서, 이 단계를 한 번 해야 한다.

## 쓰는 순서

| 순서 | 명령 | 하는 일 |
|---|---|---|
| 1 | `/hfd:bootstrap` | 뼈대를 빠르게 만든다: `CLAUDE.md`(헌법 + 파일 맵), `CHANGELOG.md`, `Retros/LESSONS.md`, `docs/index.md` |
| 2 | `/hfd:project-planner` | 무엇을 만들지 기획한다. 인터뷰로 프로젝트 성격을 정하고, 그에 맞는 검증 수단·꼭 막을 것·평가 방식과 기능 목록까지 정한다 |
| 3 | plan mode | 기획 문서대로 구현 계획을 세우고, 확인을 받은 뒤 구현한다 |
| 4 | `/hfd:wrap` | 세션을 마무리한다: 기록 정리, 새 문서를 지도에 등록, 반복된 실수 → 장치 승급 제안, 검사 통과 후 커밋 |
| 언제든 | `/hfd:harness` | 하네스 규칙 세트: 공식 기준 원문, 자리표, 점검(`/hfd:harness check`) |

## 들어 있는 것

```
plugins/hfd/
├── skills/
│   ├── harness/            하네스 규칙 세트 — 공식 원문(references/), 자리표(placement.md), 검사기(scripts/)
│   ├── bootstrap/          /hfd:bootstrap
│   ├── project-planner/    /hfd:project-planner
│   ├── wrap/               /hfd:wrap
│   └── setup/              /hfd:setup
└── hooks/                  세션 시작 때 지난 작업 맥락 주입 · 안 읽은 파일 수정 막기
```

변경 이력은 [CHANGELOG.md](CHANGELOG.md).

## 공식 문서

- OpenAI — 하네스 엔지니어링: https://openai.com/ko-KR/index/harness-engineering/
- Claude Code — .claude 디렉토리 탐색: https://code.claude.com/docs/ko/claude-directory

## 관리 (킷을 고치는 사람용)

| 작업 | 명령 |
|---|---|
| 공식 원문을 references에 반영 | `python3 tools/build_refs.py && python3 tools/check_refs.py` (누락 0이어야 함) |
| Claude Code 디렉토리 원문 갱신 | `curl -sL https://code.claude.com/docs/ko/claude-directory.md -o sources/anthropic/claude-directory.ko.md && node tools/extract_claude_directory.mjs` 후 위 명령 |
| 검사기 시험 | `python3 tests/test_harness_check.py` |
| 플러그인 검증 | `claude plugin validate .` 과 `claude plugin validate plugins/hfd` |
| 배포 | `plugins/hfd/.claude-plugin/plugin.json`의 `version`을 올려야 사용자에게 업데이트가 간다 |

- OpenAI 글은 사이트가 자동 접근을 막는다(403). 트리 원문(`sources/openai/`)은 브라우저로 확인해 옮긴 사본이다.
