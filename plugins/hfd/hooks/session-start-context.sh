#!/bin/bash
# SessionStart hook: 세션 시작 때 HANDOFF.md · CHANGELOG 현재 상태 · LESSONS(#coding/#both)를 주입한다.
# 출력은 <system-reminder>로 첫 프롬프트 전에 들어간다.
# 원칙: 어떤 경우에도 exit 0, 빠르게 끝난다(외부 명령은 awk·head·date·stat만).
#  - HANDOFF: 날짜(updated:/created:, 없으면 파일 수정일)가 30일 초과면 한 줄 경고만. 이내면 최대 120줄 주입.
#  - CHANGELOG 「현재 상태」: 최대 40줄.
#  - LESSONS: 태그와 무관하게 모든 교훈(원래 동작 유지), 파일 상단부터 최대 40개. 넘으면 잘림 표시.
# hfd 킷판: 사용자 로컬 설치본(9/22판) 기준. 바뀐 점 — COMPACT_CONTEXT 주입 제거(지우는 곳이 없어 옛 내용이 계속 쌓임),
#            옛 설치본 훅이 설정에 남아 있으면 두 번 주입되지 않게 건너뜀(/hfd:setup 안내 한 줄만).

# 0. 옛 설치본(~/.claude/hooks/session-start-context.sh)이 사용자 설정에 아직 등록돼 있으면 그쪽이 이미 주입한다 → 건너뜀
CONF_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
if [ -f "$CONF_DIR/settings.json" ] && grep -q "hooks/session-start-context.sh" "$CONF_DIR/settings.json" 2>/dev/null; then
  echo "<hfd-notice>옛 스타터 킷 훅이 아직 켜져 있어 hfd 킷의 세션 맥락 주입을 건너뜀. /hfd:setup 을 한 번 실행하면 정리됨.</hfd-notice>"
  exit 0
fi

HANDOFF_STALE_DAYS=30
HANDOFF_MAX_LINES=120
STATE_MAX_LINES=40
LESSONS_MAX=40

# YYYY-MM-DD → epoch (macOS date -j, 없으면 GNU date -d). 실패 시 빈 값.
to_epoch() {
  date -j -f "%Y-%m-%d %H:%M:%S" "$1 00:00:00" +%s 2>/dev/null || date -d "$1" +%s 2>/dev/null
}

# 1. HANDOFF.md
if [ -f ".claude/HANDOFF.md" ]; then
  HF=".claude/HANDOFF.md"
  HDATE=$(head -n 15 "$HF" 2>/dev/null | grep -iEo 'updated[^0-9]{0,6}[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -n 1 | grep -Eo '[0-9]{4}-[0-9]{2}-[0-9]{2}')
  [ -z "$HDATE" ] && HDATE=$(head -n 15 "$HF" 2>/dev/null | grep -iEo 'created[^0-9]{0,6}[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -n 1 | grep -Eo '[0-9]{4}-[0-9]{2}-[0-9]{2}')
  HEPOCH=""
  if [ -n "$HDATE" ]; then
    HEPOCH=$(to_epoch "$HDATE")
    HSRC="updated/created $HDATE"
  fi
  if [ -z "$HEPOCH" ]; then
    HEPOCH=$(stat -f %m "$HF" 2>/dev/null || stat -c %Y "$HF" 2>/dev/null)
    HSRC="파일 수정일"
  fi
  NOW=$(date +%s)
  AGE_DAYS=0
  if [ -n "$HEPOCH" ]; then
    AGE_DAYS=$(( (NOW - HEPOCH) / 86400 ))
  fi

  if [ "$AGE_DAYS" -gt "$HANDOFF_STALE_DAYS" ]; then
    echo "<stale-handoff>$(pwd)/$HF 는 ${AGE_DAYS}일 전 기록(${HSRC})이라 자동 주입하지 않음. 지금 작업과 관련 있으면 읽고, 필요하면 사용자에게 아직 유효한지 확인.</stale-handoff>"
  else
    TOTAL=$(awk 'END{print NR}' "$HF" 2>/dev/null)
    echo "<session-handoff>"
    echo "MANDATORY OUTPUT FORMAT: Your response MUST begin with a pending-items block"
    echo "extracted from the HANDOFF DATA below. This is a hard formatting constraint —"
    echo "not a suggestion, not a guideline. It applies to EVERY session regardless of"
    echo "the user's first message content, complexity, or apparent urgency."
    echo "Do not evaluate whether to skip it. If you find yourself reasoning about"
    echo "whether this step is needed — output it anyway."
    echo ""
    echo "Format (plain markdown, no XML tags):"
    echo ""
    echo "  ---"
    echo "  **Last session:** [「## 지난 세션」 하던 일 — one line]"
    echo "  **Stopped at / first action:** [「## 지난 세션」 멈춘 곳·첫 행동 — copy its meaning exactly]"
    echo "  **Pending from last session:**"
    echo "  1. [extracted item]"
    echo "  2. [extracted item]"
    echo "  Where should we start?"
    echo "  ---"
    echo ""
    echo "Output the block above FIRST, then address the user's message."
    echo "If the HANDOFF has no 「## 지난 세션」 section, take Last session from <last-session-log> below."
    echo "The first action is what 「지난 세션」 says, not whatever changed since (new commits, merged PRs,"
    echo "server events). Those are outside updates: mention them after, never as the last session's work."
    echo "Before answering a progress or continue-work request, open the 「읽는 순서」 files of the track"
    echo "you are about to work on (originals, not summaries), together with any shared brain the project uses."
    echo ""
    echo "--- HANDOFF DATA (${HSRC}, ${AGE_DAYS}일 전) ---"
    head -n "$HANDOFF_MAX_LINES" "$HF"
    if [ "${TOTAL:-0}" -gt "$HANDOFF_MAX_LINES" ]; then
      echo ""
      echo "[잘림: 전체 ${TOTAL}줄 중 ${HANDOFF_MAX_LINES}줄만 주입. 나머지는 $HF 직접 읽기. /wrap으로 80줄 이하 정리 필요]"
    fi
    echo "</session-handoff>"
  fi
fi

# 2. CHANGELOG.md — 「현재 상태」 섹션만, 최대 40줄
if [ -f "CHANGELOG.md" ]; then
  STATE_ALL=$(awk '/^## 현재 상태/{found=1; next} found && /^## /{exit} found{print}' CHANGELOG.md 2>/dev/null)
  if [ -n "$STATE_ALL" ]; then
    STATE_TOTAL=$(printf '%s\n' "$STATE_ALL" | awk 'END{print NR}')
    echo "<project-state>"
    echo "Source: CHANGELOG.md § 현재 상태"
    printf '%s\n' "$STATE_ALL" | head -n "$STATE_MAX_LINES"
    if [ "${STATE_TOTAL:-0}" -gt "$STATE_MAX_LINES" ]; then
      echo "[잘림: 전체 ${STATE_TOTAL}줄 중 ${STATE_MAX_LINES}줄만 주입. /wrap으로 15줄 이하 정리 필요]"
    fi
    echo "</project-state>"
  fi
  # 2b. 세션 로그 맨 위 항목 1개 — 「지난 세션에 무엇을 했나」(HANDOFF는 할 일만 남기므로 여기서 보충). 최대 15줄
  LAST_LOG=$(awk '/^## 세션 로그/{f=1; next} f && /^## /{exit} f && /^### /{n++} n==1{print} n>1{exit}' CHANGELOG.md 2>/dev/null | head -n 15)
  if [ -n "$LAST_LOG" ]; then
    echo "<last-session-log>"
    echo "Source: CHANGELOG.md § 세션 로그 (newest entry)"
    printf '%s\n' "$LAST_LOG"
    echo "</last-session-log>"
  fi
fi

# 3. LESSONS.md — 모든 교훈 (제목 + 본문 첫 줄), 상단부터 최대 40개
#    getline을 쓰지 않는 상태 기계라 파일이 `### 제목`+빈 줄로 끝나도 멈추지 않는다.
if [ -f "Retros/LESSONS.md" ]; then
  PROJECT_LESSONS=$(awk -v max="$LESSONS_MAX" '
    function flush() { if (pending) { print h; if (b != "") print b; print ""; n++; pending = 0; b = "" } }
    /^### / {
      flush()
      total++; if (n < max) { h = $0; pending = 1 }
      next
    }
    /^#/ { flush(); next }
    pending && NF { b = $0; flush(); next }
    END {
      flush()
      if (total > n) print "[잘림: 교훈 총 " total "개 중 상단 " n "개만 주입. 나머지는 Retros/LESSONS.md 직접 읽기]"
    }
  ' "Retros/LESSONS.md" 2>/dev/null)

  if [ -n "$PROJECT_LESSONS" ]; then
    echo "<project-lessons>"
    echo "Source: Retros/LESSONS.md (project: $(basename "$(pwd)"))"
    echo "$PROJECT_LESSONS"
    echo "</project-lessons>"
  fi
fi

exit 0
