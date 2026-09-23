---
name: harness
description: 하네스 규칙 세트 — 이 프로젝트의 하네스(CLAUDE.md·문서 지도·검증·강제·평가 장치)를 공식 기준(OpenAI·Anthropic·Claude Code 문서)에 맞게 짜고 점검할 때 쓰는 원문과 자리표, 검사기. 파일·폴더를 어디에 둘지, CLAUDE.md에 무엇을 넣을지, 반복되는 실수를 어떤 장치로 올릴지, 공식 구조 예시가 궁금할 때 읽는다. /hfd:bootstrap·/hfd:project-planner·/hfd:wrap이 기준으로 불러 쓴다. 트리거 — "하네스", "harness", "하네스 점검", "문서 지도", "파일 어디에 둬", "CLAUDE.md에 뭐 넣어", "공식 구조", "/hfd:harness", "/hfd:harness check".
---

# 하네스 규칙 세트 (hfd)

이 프로젝트의 하네스를 **공식 기준에 맞게** 짜고 점검하는 기준이다. 규칙은 요약하지 않는다. 필요한 원문 파일을 열어 그대로 따른다.

## 공식 문서

- OpenAI — 하네스 엔지니어링: https://openai.com/ko-KR/index/harness-engineering/
- Claude Code — .claude 디렉토리 탐색: https://code.claude.com/docs/ko/claude-directory

## 무엇을 어디서 보나

| 알고 싶은 것 | 읽을 파일 |
|---|---|
| 하네스를 처음부터 짜는 순서 (7단계) | `${CLAUDE_SKILL_DIR}/references/methodology.md` 1절 |
| 같은 문제가 반복될 때 어떤 장치를 추가하나 | `methodology.md` 2절 (Claude Code 공식 표) |
| 프로젝트 성격별 검증 수단·강제할 것·평가 방식 | `methodology.md` 3절 |
| OpenAI 공식 구조 예시 | `methodology.md` 4-1절 |
| Claude Code 파일별 역할·불러오는 시점·예시·링크 | `methodology.md` 4-2절 |
| 파일·폴더를 어디에 두나, 문서 지도 3층 | `${CLAUDE_SKILL_DIR}/references/placement.md` |
| `CLAUDE.md` 작성 규칙 (분량, 넣을 것·뺄 것) | `${CLAUDE_SKILL_DIR}/references/official/memory.md`, `official/best-practices.md` |
| CLAUDE.md·rules·skill·hook·subagent 중 무엇을 쓰나 | `${CLAUDE_SKILL_DIR}/references/official/features-overview.md` |

`official/`의 파일은 Claude Code 공식 문서를 원문 그대로 보관한 사본이다.

## 쓰는 규칙

- 이 규칙 세트로 **확인하되, 사용자가 고른 방향이 우선**이다. 규칙과 사용자 선택이 다르면 차이를 보여주고 사용자가 정하게 한다.
- 공식 문서에 없는 내용을 규칙처럼 지어내지 않는다. 근거가 필요하면 위 파일에서 해당 문장을 찾아 인용한다.
- 새 폴더·문서는 자유롭게 만든다. 조건은 지도에 등록하는 것뿐이다(`placement.md` 5절).

## 점검 — `/hfd:harness check`

검사기를 실행해 결과 표를 그대로 보여준다.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/harness_check.py" --project "<프로젝트 폴더>"
```

- 윈도우에서 `python3`가 없으면 `python` 또는 `py -3`로 실행한다.
- 파이썬이 아예 없으면 `/hfd:setup`을 먼저 실행하라고 안내한다.
- FAIL이 있으면 무엇을 어떻게 고치면 되는지 한 줄씩 설명한다. 사용자가 원하면 고친다.
