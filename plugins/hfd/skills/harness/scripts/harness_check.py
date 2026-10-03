#!/usr/bin/env python3
"""hfd 하네스 검사기 — /hfd:wrap 검사 게이트 · /hfd:harness check. 표준 라이브러리만 사용. 파일을 수정하지 않는다.

기존 wrap_check.py 검사(HANDOFF · CHANGELOG · 메모리 · 키워드)를 그대로 두고 아래를 더했다.
  - CLAUDE.md: 200줄 이하(공식 권장), 「파일 맵」 링크가 살아 있는가            (지도 1층)
  - docs/: docs/index.md와 폴더별 index.md가 있고, 문서가 전부 등록됐는가      (지도 2·3층)
  - 기획 문서(docs/REQUEST·PRD·AGENT_DESIGN.md): 필수 칸이 비어 있지 않은가
  - 폴더 개수·이름은 검사하지 않는다 (새 폴더는 자유, 등록만 요구)

사용:
  harness_check.py --project <폴더> [--memory <폴더>] [--keywords "a,b,c"]
  harness_check.py --scan <상위폴더> [<상위폴더> ...]
종료 코드: FAIL이 하나라도 있으면 1, 아니면 0.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import unicodedata

HANDOFF_MAX_LINES = 80
HANDOFF_MAX_AGE_DAYS = 1        # wrap 직후 검사 기준
SCAN_HANDOFF_STALE_DAYS = 30    # --scan 기준 (켤 때 훅과 동일)
HANDOFF_MAX_TODO_PER_TRACK = 5
STATE_MAX_LINES = 15
STATE_MAX_LINE_CHARS = 400
APPEND_ONLY_WINDOW = 5
SAME_DATE_WARN = 2
MEMORY_MAX_LINES = 200
FRONTMATTER_CLOSE_WITHIN = 20
PRUNE_DIRS = {"node_modules", "venv", ".venv", "__pycache__", "dist", "build", ".next", ".git", "archive", "_attic"}
CLAUDE_MD_MAX_LINES = 200       # 공식 권장: "target under 200 lines per CLAUDE.md file"
PLANNER_DOCS = ("REQUEST.md", "PRD.md", "AGENT_DESIGN.md")
PROBLEM_FIELDS = ("해결하는 문제", "성공 기준")
HARNESS_FIELDS = ("프로젝트 성격", "검증 수단", "꼭 막을 것", "평가 방식")

# 윈도우 기본 인코딩(cp949 등)에서 한글 출력이 깨지거나 죽지 않게
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


class Report:
    def __init__(self):
        self.rows = []

    def add(self, status, check, reason, where=""):
        self.rows.append((status, check, reason, where))

    def count(self, status):
        return sum(1 for r in self.rows if r[0] == status)

    def print_table(self):
        print("| 결과 | 검사 | 이유 | 위치 |")
        print("|---|---|---|---|")
        for s, c, r, w in self.rows:
            print(f"| {s} | {c} | {r.replace('|', '/')} | {w} |")
        print(f"\nPASS {self.count('PASS')} · WARN {self.count('WARN')} · FAIL {self.count('FAIL')}")


def read_lines(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read().splitlines()
    except OSError:
        return None


def guess_memory_dir(project):
    project = os.path.abspath(project)
    settings = os.path.join(project, ".claude", "settings.local.json")
    try:
        with open(settings, encoding="utf-8") as f:
            val = json.load(f).get("autoMemoryDirectory", "")
        if val:
            val = os.path.expanduser(val)
            if not os.path.isabs(val):
                val = os.path.join(project, val)
            return val, "settings.local.json autoMemoryDirectory"
    except (OSError, ValueError, AttributeError):
        pass
    # macOS 파일시스템은 한글을 NFD(자모 분리)로 돌려줄 수 있다 → NFC로 맞춰야 Claude Code 폴더명과 일치
    name = re.sub(r"[^A-Za-z0-9]", "-", unicodedata.normalize("NFC", project))
    return os.path.expanduser(f"~/.claude/projects/{name}/memory"), "기본 경로(~/.claude/projects)"


# ---------------- HANDOFF ----------------
def check_handoff(project, rep, max_age_days):
    path = os.path.join(project, ".claude", "HANDOFF.md")
    lines = read_lines(path)
    rel = ".claude/HANDOFF.md"
    info = {"lines": 0, "age": None}
    if lines is None:
        rep.add("PASS", "HANDOFF", "파일 없음 (다음 할 일 없음으로 간주)", rel)
        return info
    info["lines"] = len(lines)
    if len(lines) > HANDOFF_MAX_LINES:
        rep.add("FAIL", "HANDOFF 길이", f"{len(lines)}줄 > {HANDOFF_MAX_LINES}줄", rel)
    else:
        rep.add("PASS", "HANDOFF 길이", f"{len(lines)}줄", rel)

    date, date_line = None, None
    for i, ln in enumerate(lines[:15], 1):
        m = re.search(r"(?:updated|created)\W{0,4}\s*(\d{4}-\d{2}-\d{2})", ln, re.I)
        if m:
            date, date_line = m.group(1), i
            break
    if not date:
        rep.add("FAIL", "HANDOFF 날짜", "맨 위 15줄 안에 `updated: YYYY-MM-DD` 없음", f"{rel}:1")
    else:
        try:
            age = (dt.date.today() - dt.date.fromisoformat(date)).days
            info["age"] = age
            if age > max_age_days:
                rep.add("FAIL", "HANDOFF 날짜", f"updated {date} = {age}일 전 (허용 {max_age_days}일)", f"{rel}:{date_line}")
            else:
                rep.add("PASS", "HANDOFF 날짜", f"updated {date} ({age}일 전)", f"{rel}:{date_line}")
        except ValueError:
            rep.add("FAIL", "HANDOFF 날짜", f"날짜 형식 오류: {date}", f"{rel}:{date_line}")

    done = [i for i, ln in enumerate(lines, 1) if re.search(r"^\s*[-*]\s*\[[xX]\]", ln)]
    if done:
        rep.add("FAIL", "HANDOFF 완료 항목", f"[x] {len(done)}개 남음 — 삭제해야 함", f"{rel}:{','.join(map(str, done[:8]))}")
    else:
        rep.add("PASS", "HANDOFF 완료 항목", "[x] 0개", rel)

    track, track_line, counts = "(제목 없음)", 1, {}
    order = []
    for i, ln in enumerate(lines, 1):
        m = re.match(r"^#{1,2}\s+(.*)", ln)
        if m and i > 1:
            track, track_line = m.group(1).strip()[:40], i
        if re.match(r"^\s*[-*]\s*\[ \]", ln):
            key = (track, track_line)
            if key not in counts:
                order.append(key)
            counts[key] = counts.get(key, 0) + 1
    # 할 일이 있는 트랙은 「목표」와 「읽는 순서」 칸이 있어야 다음 세션이 이 대화 없이 같은 판단을 한다 (wrap 5단계)
    bounds = []
    heads = [i for i, ln in enumerate(lines, 1) if re.match(r"^#{2}\s+", ln)]
    for k, h in enumerate(heads):
        end = heads[k + 1] - 1 if k + 1 < len(heads) else len(lines)
        bounds.append((h, end))
    missing = []
    for h, end in bounds:
        body = "\n".join(lines[h:end])
        if not re.search(r"^\s*[-*]\s*\[ \]", body, re.M):
            continue
        lack = [name for name, pat in (("목표", r"목표"), ("읽는 순서", r"읽는 순서")) if not re.search(pat, body)]
        if lack:
            missing.append((lines[h - 1].lstrip("# ").strip()[:40], h, lack))
    if missing:
        for t, l, lack in missing:
            rep.add("FAIL", "HANDOFF 맥락 칸", f"'{t}'에 {'·'.join(lack)} 없음 — 할 일만 있으면 다음 세션이 이유를 모름", f"{rel}:{l}")
    elif bounds:
        rep.add("PASS", "HANDOFF 맥락 칸", "할 일 있는 트랙 모두 목표·읽는 순서 있음", rel)

    over = [(t, l, counts[(t, l)]) for t, l in order if counts[(t, l)] > HANDOFF_MAX_TODO_PER_TRACK]
    if over:
        for t, l, c in over:
            rep.add("FAIL", "HANDOFF 트랙당 할 일", f"'{t}' 미완료 {c}개 > {HANDOFF_MAX_TODO_PER_TRACK}", f"{rel}:{l}")
    else:
        rep.add("PASS", "HANDOFF 트랙당 할 일", f"트랙 {len(order)}개, 모두 ≤{HANDOFF_MAX_TODO_PER_TRACK}", rel)
    return info


# ---------------- CHANGELOG ----------------
def current_state(lines):
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^## 현재 상태", ln):
            start = i
            break
    if start is None:
        return None, None
    body = []
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            break
        body.append((j + 1, lines[j]))
    return start + 1, body


def check_changelog(project, rep):
    path = os.path.join(project, "CHANGELOG.md")
    lines = read_lines(path)
    info = {"state_lines": None}
    if lines is None:
        rep.add("WARN", "CHANGELOG", "CHANGELOG.md 없음 — 현재 상태·세션 로그를 찾을 곳이 없음", "CHANGELOG.md")
        return info, None
    head_line, body = current_state(lines)
    state_text = None
    if head_line is None:
        rep.add("FAIL", "현재 상태", "`## 현재 상태` 제목 없음", "CHANGELOG.md")
    else:
        content = [(n, ln) for n, ln in body if ln.strip() and not re.match(r"^\s*<!--.*-->\s*$", ln)]
        info["state_lines"] = len(content)
        state_text = "\n".join(ln for _, ln in body)
        if len(content) > STATE_MAX_LINES:
            rep.add("FAIL", "현재 상태 길이", f"{len(content)}줄 > {STATE_MAX_LINES}줄 (주석·빈 줄 제외)", f"CHANGELOG.md:{head_line}")
        elif not content:
            rep.add("WARN", "현재 상태 길이", "비어 있음", f"CHANGELOG.md:{head_line}")
        else:
            rep.add("PASS", "현재 상태 길이", f"{len(content)}줄", f"CHANGELOG.md:{head_line}")
        long_lines = [(n, len(ln)) for n, ln in content if len(ln) > STATE_MAX_LINE_CHARS]
        if long_lines:
            desc = ", ".join(f"{n}줄 {c}자" for n, c in long_lines[:5])
            rep.add("FAIL", "현재 상태 한 줄 길이", f"{STATE_MAX_LINE_CHARS}자 초과: {desc}", f"CHANGELOG.md:{long_lines[0][0]}")
        else:
            rep.add("PASS", "현재 상태 한 줄 길이", f"모두 ≤{STATE_MAX_LINE_CHARS}자", "CHANGELOG.md")

    log_idx = next((i for i, ln in enumerate(lines) if re.match(r"^## 세션 로그", ln)), None)
    if log_idx is None:
        rep.add("WARN", "세션 로그", "`## 세션 로그` 제목 없음", "CHANGELOG.md")
    else:
        window = lines[log_idx + 1: log_idx + 1 + APPEND_ONLY_WINDOW]
        if any("APPEND ONLY" in ln for ln in window):
            rep.add("PASS", "APPEND ONLY 주석 위치", f"`## 세션 로그` 아래 {APPEND_ONLY_WINDOW}줄 안", f"CHANGELOG.md:{log_idx + 1}")
        else:
            where = next((i + 1 for i, ln in enumerate(lines) if "APPEND ONLY" in ln), None)
            reason = f"주석이 {where}줄에 있음 (제목은 {log_idx + 1}줄)" if where else "주석 없음"
            rep.add("FAIL", "APPEND ONLY 주석 위치", reason + " — 새 항목이 엉뚱한 곳에 들어감", f"CHANGELOG.md:{log_idx + 1}")
        dates = {}
        for ln in lines[log_idx + 1:]:
            m = re.match(r"^###\s+(\d{4}-\d{2}-\d{2})", ln)
            if m:
                dates[m.group(1)] = dates.get(m.group(1), 0) + 1
        many = {d: c for d, c in dates.items() if c > SAME_DATE_WARN}
        if many:
            rep.add("WARN", "같은 날짜 항목", ", ".join(f"{d}: {c}개" for d, c in sorted(many.items())[-5:]) + " (세션당 1개 원칙)", "CHANGELOG.md")
        else:
            rep.add("PASS", "같은 날짜 항목", f"날짜당 ≤{SAME_DATE_WARN}개", "CHANGELOG.md")
    return info, state_text


# ---------------- MEMORY ----------------
def check_frontmatter(path, lines, rep, label, required):
    if not lines or lines[0].strip() != "---":
        if required:
            rep.add("FAIL", "메모리 frontmatter", "첫 줄이 `---` 아님", f"{label}:1")
            return False
        return True
    close = None
    for i in range(1, min(len(lines), FRONTMATTER_CLOSE_WITHIN)):
        if lines[i].strip() == "---":
            close = i
            break
    if close is None:
        rep.add("FAIL", "메모리 frontmatter", f"닫는 `---`가 {FRONTMATTER_CLOSE_WITHIN}줄 안에 없음", f"{label}:1")
        return False
    bad = [i + 1 for i in range(1, close) if lines[i].lstrip().startswith("|")]
    if bad:
        rep.add("FAIL", "메모리 frontmatter", f"frontmatter 안에 표 줄 {len(bad)}개 — 본문이 메타데이터로 먹힘", f"{label}:{bad[0]}")
        return False
    return True


def check_memory(mem, rep):
    info = {"memory_lines": None, "exists": os.path.isdir(mem)}
    if not os.path.isdir(mem):
        rep.add("WARN", "메모리 폴더", "폴더 없음 — 메모리 기록이 한 번도 없거나 경로가 틀림", mem)
        return info
    idx = os.path.join(mem, "MEMORY.md")
    lines = read_lines(idx)
    if lines is None:
        rep.add("WARN", "MEMORY.md", "목차 파일 없음", idx)
        lines = []
    else:
        info["memory_lines"] = len(lines)
        if len(lines) > MEMORY_MAX_LINES:
            rep.add("FAIL", "MEMORY.md 길이", f"{len(lines)}줄 > {MEMORY_MAX_LINES}줄 (뒤쪽은 로드 안 됨)", idx)
        else:
            rep.add("PASS", "MEMORY.md 길이", f"{len(lines)}줄", idx)
    linked, broken = set(), []
    for i, ln in enumerate(lines, 1):
        for target in re.findall(r"\]\(([^)\s]+)\)", ln):
            if re.match(r"^[a-z]+://", target) or target.startswith("#"):
                continue
            t = target.split("#")[0]
            p = os.path.normpath(os.path.join(mem, os.path.expanduser(t)))
            linked.add(os.path.basename(p))
            if not os.path.exists(p):
                broken.append((i, t))
    if broken:
        rep.add("FAIL", "MEMORY.md 링크", "깨진 링크: " + ", ".join(t for _, t in broken[:6]), f"{idx}:{broken[0][0]}")
    elif lines:
        rep.add("PASS", "MEMORY.md 링크", f"링크 {len(linked)}개 모두 존재", idx)
    mds = sorted(f for f in os.listdir(mem) if f.endswith(".md") and f != "MEMORY.md")
    orphans = [f for f in mds if f not in linked]
    if orphans:
        rep.add("WARN", "목차에 없는 메모리", f"{len(orphans)}개: " + ", ".join(orphans[:6]), mem)
    fm_ok = check_frontmatter(idx, lines, rep, idx, required=False) if lines else True
    for f in mds:
        p = os.path.join(mem, f)
        fm_ok &= check_frontmatter(p, read_lines(p) or [], rep, p, required=True)
    if fm_ok:
        rep.add("PASS", "메모리 frontmatter", f"{len(mds)}개 파일 정상", mem)
    return info


# ---------------- KEYWORDS ----------------
def iter_md(root):
    if not os.path.isdir(root):
        return
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in PRUNE_DIRS]
        for f in files:
            if f.endswith((".md", ".txt")):
                yield os.path.join(d, f)


def check_keywords(project, mem, state_text, keywords, rep):
    sources = []  # (label, text, fresh) — fresh = 최근 1일 안에 고친 파일 또는 HANDOFF·현재 상태
    now = dt.datetime.now().timestamp()

    def fresh(path):
        try:
            return now - os.path.getmtime(path) <= 86400
        except OSError:
            return False

    for p in iter_md(mem):
        sources.append((f"메모리:{os.path.basename(p)}", "\n".join(read_lines(p) or []), fresh(p)))
    ho = read_lines(os.path.join(project, ".claude", "HANDOFF.md"))
    if ho is not None:
        sources.append(("HANDOFF", "\n".join(ho), True))
    if state_text:
        sources.append(("CHANGELOG 현재 상태", state_text, True))
    clp = os.path.join(project, "CLAUDE.md")
    cl = read_lines(clp)
    if cl is not None:
        sources.append(("CLAUDE.md", "\n".join(cl), fresh(clp)))
    for p in iter_md(os.path.join(project, "docs", "research")):
        sources.append((f"docs/research/{os.path.basename(p)}", "\n".join(read_lines(p) or []), fresh(p)))
    if not sources:
        rep.add("FAIL", "키워드 검색", "검색할 파일이 하나도 없음 (메모리·HANDOFF·현재 상태·CLAUDE.md·docs/research)", project)
        return
    for kw in keywords:
        low = kw.lower()
        hits = [(label, fr) for label, text, fr in sources if low in text.lower()]
        if hits:
            labels = [l for l, _ in hits]
            shown = ", ".join(labels[:3]) + (f" 외 {len(labels) - 3}곳" if len(labels) > 3 else "")
            if any(fr for _, fr in hits):
                rep.add("PASS", f"키워드 '{kw}'", f"{len(hits)}곳에서 찾음", shown)
            else:
                rep.add("WARN", f"키워드 '{kw}'", "옛 파일에서만 찾음 — 이번 세션 내용이 기록됐는지 확인", shown)
        else:
            rep.add("FAIL", f"키워드 '{kw}'", "어디에도 없음 — 다음 세션이 못 찾음", "메모리·HANDOFF·현재 상태·CLAUDE.md·docs/research")


# ---------------- 지도·CLAUDE.md·기획 문서 (hfd 추가) ----------------
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def local_links(lines, base):
    """마크다운 링크 중 로컬 경로만 (줄번호, 원래 대상, 절대경로). 코드 블록·`코드` 안의 형식 예시는 링크로 세지 않는다."""
    out = []
    in_fence = False
    for i, ln in enumerate(lines, 1):
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        ln = re.sub(r"`[^`]*`", "", ln)
        for target in LINK_RE.findall(ln):
            if re.match(r"^[a-z]+://", target) or target.startswith(("#", "mailto:")):
                continue
            t = target.split("#")[0]
            if not t:
                continue
            out.append((i, target, os.path.normpath(os.path.join(base, os.path.expanduser(t)))))
    return out


def section(lines, title):
    """`## <title>`로 시작하는 절의 (시작 줄번호, 본문 줄 목록)."""
    start = next((i for i, ln in enumerate(lines) if re.match(rf"^##\s+{re.escape(title)}", ln)), None)
    if start is None:
        return None, []
    body = []
    for j in range(start + 1, len(lines)):
        if re.match(r"^##\s", lines[j]):
            break
        body.append((j + 1, lines[j]))
    return start + 1, body


def check_claude_md(project, rep):
    path = next((p for p in (os.path.join(project, "CLAUDE.md"), os.path.join(project, ".claude", "CLAUDE.md")) if os.path.isfile(p)), None)
    if not path:
        rep.add("WARN", "CLAUDE.md", "없음 — /hfd:bootstrap으로 만들 수 있음", "CLAUDE.md")
        return
    rel = os.path.relpath(path, project)
    lines = read_lines(path) or []
    if len(lines) > CLAUDE_MD_MAX_LINES:
        rep.add("FAIL", "CLAUDE.md 길이", f"{len(lines)}줄 > {CLAUDE_MD_MAX_LINES}줄 (공식 권장) — 특정 파일용 규칙은 .claude/rules/, 가끔 쓰는 자료는 스킬로", rel)
    else:
        rep.add("PASS", "CLAUDE.md 길이", f"{len(lines)}줄", rel)
    head, body = section(lines, "파일 맵")
    if head is None:
        rep.add("FAIL", "CLAUDE.md 파일 맵", "「## 파일 맵」 칸 없음 — 지도 1층이 없어 에이전트가 문서 위치를 모름", rel)
        return
    links = local_links([ln for _, ln in body], os.path.dirname(path))
    broken = [t for _, t, p in links if not os.path.exists(p)]
    if broken:
        rep.add("FAIL", "CLAUDE.md 파일 맵 링크", "깨진 링크: " + ", ".join(broken[:6]), f"{rel}:{head}")
    else:
        rep.add("PASS", "CLAUDE.md 파일 맵 링크", f"링크 {len(links)}개 모두 존재", f"{rel}:{head}")
    docs_index = os.path.join(project, "docs", "index.md")
    if os.path.isfile(docs_index) and not any(p == os.path.normpath(docs_index) for _, _, p in links):
        rep.add("FAIL", "CLAUDE.md 파일 맵", "docs/index.md가 파일 맵에 없음 — 지도 1층에서 2층으로 못 내려감", f"{rel}:{head}")


def check_docs_map(project, rep):
    docs = os.path.join(project, "docs")
    if not os.path.isdir(docs):
        return
    problems = 0
    for d, dirs, files in os.walk(docs):
        dirs[:] = sorted(x for x in dirs if x not in PRUNE_DIRS and not x.startswith("."))
        rel_d = os.path.relpath(d, project)
        idx = os.path.join(d, "index.md")
        if not os.path.isfile(idx):
            rep.add("FAIL", "문서 지도 index.md", f"{rel_d}/ 에 index.md 없음 — 이 폴더 문서를 찾아갈 지도가 없음", rel_d)
            problems += 1
            continue
        lines = read_lines(idx) or []
        links = local_links(lines, d)
        broken = [t for _, t, p in links if not os.path.exists(p)]
        if broken:
            rep.add("FAIL", "문서 지도 링크", "깨진 링크: " + ", ".join(broken[:6]), f"{rel_d}/index.md")
            problems += 1
        targets = {p for _, _, p in links}
        # 폴더를 가리키는 링크는 폴더 자체나 그 폴더의 index.md 둘 다 인정
        targets |= {os.path.dirname(p) for p in targets if os.path.basename(p) == "index.md"}
        members = [os.path.join(d, f) for f in files if f.endswith(".md") and f != "index.md"]
        members += [os.path.join(d, x) for x in dirs]
        orphans = [os.path.relpath(m, d) for m in members if os.path.normpath(m) not in targets]
        if orphans:
            rep.add("FAIL", "문서 지도 등록", f"index.md에 없는 항목 {len(orphans)}개: " + ", ".join(orphans[:6]), f"{rel_d}/index.md")
            problems += 1
    if not problems:
        rep.add("PASS", "문서 지도 (docs/)", "모든 폴더에 index.md, 모든 문서 등록, 깨진 링크 없음", "docs/")


def check_planner_docs(project, rep):
    for name in PLANNER_DOCS:
        path = os.path.join(project, "docs", name)
        lines = read_lines(path)
        if lines is None:
            continue
        rel = f"docs/{name}"
        empty = []
        for title, fields in (("문제 정의", PROBLEM_FIELDS), ("하네스 설정", HARNESS_FIELDS)):
            head, body = section(lines, title)
            if head is None:
                empty.append(f"「## {title}」 칸 없음")
                continue
            for f in fields:
                row = next((ln for _, ln in body if re.match(rf"^\s*[-*]\s*{re.escape(f)}\s*:", ln)), None)
                if row is None:
                    empty.append(f"{f} 없음")
                elif not re.sub(r"_+|\(.*?\)", "", row.split(":", 1)[1]).strip():
                    empty.append(f"{f} 비어 있음")
        head, body = section(lines, "기능 목록")
        if head is None:
            empty.append("「## 기능 목록」 칸 없음")
        else:
            rows = [ln for _, ln in body if ln.strip().startswith("|")]
            data = [r for r in rows[2:]] if len(rows) >= 2 else []
            if not data:
                empty.append("기능 목록이 비어 있음")
            for r in data:
                cells = [c.strip() for c in r.strip().strip("|").split("|")]
                if len(cells) < 3 or not cells[1]:
                    empty.append(f"확인 방법 빈 줄: {cells[0][:30] if cells else r[:30]}")
        if empty:
            rep.add("FAIL", "기획 문서 필수 칸", "; ".join(empty[:6]), rel)
        else:
            rep.add("PASS", "기획 문서 필수 칸", "문제 정의 · 하네스 설정 · 기능 목록 모두 채워짐", rel)


# ---------------- RUN ----------------
def check_user_verbatim(project, rep):
    """wrap 1단계 f) — 이번 세션 사용자 원문 파일이 최근 1일 안에 만들어졌나."""
    import glob
    import time
    files = glob.glob(os.path.join(project, "docs", "references", "*user-verbatim*.md"))
    fresh = [f for f in files if time.time() - os.path.getmtime(f) < 86400]
    if fresh:
        rep.add("PASS", "사용자 원문", f"{len(fresh)}개 (최근 1일)", os.path.relpath(fresh[0], project))
    else:
        rep.add("FAIL", "사용자 원문", "최근 1일 안에 만든 `docs/references/<날짜>-user-verbatim.md` 없음 — wrap 1단계 f)", "docs/references/")


def run_project(project, mem, keywords, max_age_days):
    rep = Report()
    h = check_handoff(project, rep, max_age_days)
    c, state_text = check_changelog(project, rep)
    m = check_memory(mem, rep)
    check_claude_md(project, rep)
    check_docs_map(project, rep)
    check_planner_docs(project, rep)
    if keywords:  # wrap 실행(키워드 있음)일 때만. --scan은 옛 프로젝트 기준선이라 제외
        check_keywords(project, mem, state_text, keywords, rep)
        check_user_verbatim(project, rep)
    return rep, {**h, **c, **m}


def find_projects(roots):
    found = []
    for root in roots:
        root = os.path.abspath(os.path.expanduser(root))
        if not os.path.isdir(root):
            print(f"[경고] 폴더 없음: {root}", file=sys.stderr)
            continue
        for d, dirs, files in os.walk(root):
            dirs[:] = sorted(x for x in dirs if x not in PRUNE_DIRS and not x.startswith("."))
            if "CHANGELOG.md" in files or os.path.isfile(os.path.join(d, ".claude", "HANDOFF.md")):
                found.append(d)
    return found


def scan(roots):
    projects = find_projects(roots)
    if not projects:
        print("대상 프로젝트를 하나도 찾지 못함 (CHANGELOG.md 또는 .claude/HANDOFF.md 있는 폴더). 경로를 확인하세요.")
        return 1
    home = os.path.expanduser("~")
    print(f"점검 대상 {len(projects)}곳 (수정 없음, HANDOFF 날짜 기준 {SCAN_HANDOFF_STALE_DAYS}일)\n")
    print("| 프로젝트 | HANDOFF 줄/경과일 | 현재 상태 줄 | MEMORY 줄 | FAIL | WARN | 주요 FAIL |")
    print("|---|---|---|---|---|---|---|")
    total_fail = 0
    for p in projects:
        mem, _ = guess_memory_dir(p)
        rep, info = run_project(p, mem, [], SCAN_HANDOFF_STALE_DAYS)
        fails = [r for r in rep.rows if r[0] == "FAIL"]
        total_fail += len(fails)
        ho = "-" if not info["lines"] else f"{info['lines']}/{info['age'] if info['age'] is not None else '?'}일"
        st = "-" if info.get("state_lines") is None else str(info["state_lines"])
        ml = "-" if info.get("memory_lines") is None else str(info["memory_lines"])
        top = "; ".join(sorted({r[1] for r in fails}))[:120] or "-"
        print(f"| {p.replace(home, '~')} | {ho} | {st} | {ml} | {len(fails)} | {rep.count('WARN')} | {top} |")
    print(f"\n합계 FAIL {total_fail}")
    return 1 if total_fail else 0


def main():
    ap = argparse.ArgumentParser(description="hfd 하네스 검사기")
    ap.add_argument("--project")
    ap.add_argument("--memory")
    ap.add_argument("--keywords", default="")
    ap.add_argument("--scan", nargs="+", metavar="ROOT")
    a = ap.parse_args()
    if a.scan:
        sys.exit(scan(a.scan))
    if not a.project:
        ap.error("--project 또는 --scan 필요")
    project = os.path.abspath(os.path.expanduser(a.project))
    if not os.path.isdir(project):
        print(f"FAIL: 프로젝트 폴더 없음: {project}")
        sys.exit(1)
    if a.memory:
        mem, how = os.path.abspath(os.path.expanduser(a.memory)), "--memory 인자"
    else:
        mem, how = guess_memory_dir(project)
    keywords = [k.strip() for k in a.keywords.split(",") if k.strip()]
    print(f"프로젝트: {project}\n메모리: {mem} ({how})\n키워드: {', '.join(keywords) or '(없음)'}\n")
    rep, _ = run_project(project, mem, keywords, HANDOFF_MAX_AGE_DAYS)
    if not keywords:
        rep.add("WARN", "키워드 검색", "--keywords 없음 — 다음 세션이 찾을 수 있는지 확인 안 함", "")
    rep.print_table()
    sys.exit(1 if rep.count("FAIL") else 0)


if __name__ == "__main__":
    main()
