"""Claude Code '.claude 디렉토리 탐색' 데이터를 마크다운·HTML로 그린다.

데이터: sources/anthropic/claude-directory.tree.json (scripts/extract_claude_directory.mjs가 원문에서 생성)
공식 페이지의 상세 패널 순서를 그대로 따른다:
이름 → 한 줄 → 표시(badge) → 안내(note) → When it loads → 설명 → Common keys → Tips → 예시 → Full docs → Contents
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TREE_JSON = ROOT / "sources/anthropic/claude-directory.tree.json"
PAGE_KO = "https://code.claude.com/docs/ko/claude-directory"
BADGE = {"committed": "COMMITTED", "gitignored": "GITIGNORED", "local": "LOCAL", "autogen": "AUTOGEN"}
BADGE_KO = {"committed": "git에 커밋 · 팀 공유", "gitignored": "git 제외", "local": "내 컴퓨터에만", "autogen": "Claude가 자동 생성"}


def load() -> dict:
    return json.loads(TREE_JSON.read_text(encoding="utf-8"))


def walk(node: dict, path: list[str] | None = None, depth: int = 0):
    path = (path or []) + [node["label"].rstrip("/")]
    yield node, path, depth
    for c in node.get("children", []):
        yield from walk(c, path, depth + 1)


def badges(n: dict) -> list[str]:
    out = ["autogen"] if n.get("autogen") else []
    if n.get("badge"):
        out.append(n["badge"])
    return out


def as_list(v) -> list[str]:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


# ---------------- 마크다운 ----------------

def tree_md(root: dict) -> str:
    lines = []
    for n, _, d in walk(root):
        tag = " ".join(f"[{BADGE[b]}]" for b in badges(n))
        one = f" — {n['oneLiner']}" if n.get("oneLiner") else ""
        lines.append("  " * d + n["label"] + (f"  {tag}" if tag else "") + one)
    return "```\n" + "\n".join(lines) + "\n```"


def node_md(n: dict, path: list[str]) -> str:
    o = [f"#### `{'/'.join(path)}`"]
    if n.get("oneLiner"):
        o.append(f"*{n['oneLiner']}*\n")
    if badges(n):
        o.append("- **표시:** " + ", ".join(f"{BADGE[b]} ({BADGE_KO[b]})" for b in badges(n)))
    if n.get("note"):
        o.append(f"- **안내:** {n['note']}")
    if n.get("when"):
        o.append(f"- **When it loads:** {n['when']}")
    desc = as_list(n.get("description"))
    if desc:
        o.append("- **설명:** " + desc[0])
        o.extend(f"  \n  {p}" for p in desc[1:])
    if n.get("contains"):
        o.append("- **Common keys:**")
        o.extend(f"  - {c}" for c in n["contains"])
    if n.get("tips"):
        o.append("- **Tips:**")
        o.extend(f"  - {t}" for t in n["tips"])
    if n.get("exampleIntro"):
        o.append(f"- **예시 설명:** {n['exampleIntro']}")
    if n.get("example"):
        o.append(f"\n```\n{n['example']}\n```")
    if n.get("docsLink"):
        o.append(f"\n[Full docs →]({n['docsLink']})")
    if n.get("children"):
        o.append("\n- **Contents:** " + ", ".join(f"`{c['label']}`" for c in n["children"]))
    return "\n".join(o) + "\n"


def full_md(tree: dict) -> str:
    out = [
        f"원문: [{PAGE_KO}]({PAGE_KO}) — 「디렉토리 탐색」. 트리의 파일을 누르면 나오는 상세 내용(무엇을 하는지, 언제 불러오는지, 팁, 예시, 공식 문서 링크)을 **원문 그대로** 옮겼다. 탐색기 데이터는 한국어판에서도 영어 원문이다.\n",
        "표시: `COMMITTED` git에 커밋·팀 공유 · `GITIGNORED` git 제외 · `LOCAL` 내 컴퓨터에만 · `AUTOGEN` Claude가 자동 생성\n",
        "#### 트리 — Project (`your-project/`)\n", tree_md(tree["project"]),
        "\n#### 트리 — Global (`~/`)\n", tree_md(tree["global"]),
        "\n#### 파일·폴더별 상세 — Project\n",
    ]
    out += [node_md(n, p) for n, p, d in walk(tree["project"]) if d > 0]
    out.append("\n#### 파일·폴더별 상세 — Global (`~/`)\n")
    out += [node_md(n, p) for n, p, d in walk(tree["global"]) if d > 0]
    return "\n".join(out)


# ---------------- HTML (공식 페이지처럼 클릭형) ----------------

def inline(s: str) -> str:
    """마크다운 인라인(`코드`, [글](주소))만 HTML로."""
    s = html.escape(s, quote=False)
    s = re.sub(r"`` (.+?) ``", r"<code>\1</code>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


def node_id(prefix: str, path: list[str]) -> str:
    return prefix + "-" + re.sub(r"[^a-zA-Z0-9]+", "-", "/".join(path)).strip("-").lower()


def tree_html(root: dict, prefix: str) -> str:
    items = []
    for n, p, d in walk(root):
        if d == 0:
            continue
        is_dir = n["label"].endswith("/")
        dot = "".join(f'<span class="dot {b}" title="{BADGE[b]}"></span>' for b in badges(n)[-1:])
        items.append(
            f'<button class="node{" dir" if is_dir else ""}" data-target="{node_id(prefix, p)}" style="padding-left:{8 + (d - 1) * 16}px">'
            f'<span class="ic">{"▸" if is_dir else "·"}</span><span class="nm">{html.escape(n["label"])}</span>{dot}</button>'
        )
    return "\n".join(items)


def panel_html(n: dict, path: list[str], prefix: str) -> str:
    h = [f'<article class="detail" id="{node_id(prefix, path)}">']
    h.append(f'<div class="crumb">{html.escape(" / ".join(path))}</div>')
    tags = "".join(f'<span class="badge {b}">{BADGE[b]}</span>' for b in badges(n))
    h.append(f'<div class="head"><h4>{html.escape(n["label"])}</h4>{tags}</div>')
    if n.get("oneLiner"):
        h.append(f'<p class="one">{inline(n["oneLiner"])}</p>')
    if n.get("note"):
        h.append(f'<div class="note">{inline(n["note"])}</div>')
    if n.get("when"):
        h.append(f'<div class="when"><div class="lbl">WHEN IT LOADS</div><div>{inline(n["when"])}</div></div>')
    for para in as_list(n.get("description")):
        h.append(f'<p class="desc">{inline(para)}</p>')
    if n.get("contains"):
        h.append('<div class="box"><div class="lbl">COMMON KEYS</div><ul>' + "".join(f"<li>{inline(c)}</li>" for c in n["contains"]) + "</ul></div>")
    if n.get("tips"):
        h.append('<div class="box tips"><div class="lbl">TIPS</div><ul>' + "".join(f"<li>{inline(t)}</li>" for t in n["tips"]) + "</ul></div>")
    if n.get("example"):
        if n.get("exampleIntro"):
            h.append(f'<p class="desc">{inline(n["exampleIntro"])}</p>')
        h.append(f'<div class="ex"><div class="exbar"><span>{html.escape(n["label"])}</span><button class="copy">Copy</button></div>'
                 f'<pre><code>{html.escape(n["example"])}</code></pre></div>')
    if n.get("docsLink"):
        h.append(f'<a class="full" href="{n["docsLink"]}" target="_blank" rel="noopener">Full docs →</a>')
    if n.get("children"):
        kids = "".join(f'<button class="kid" data-target="{node_id(prefix, path + [c["label"].rstrip("/")])}">{html.escape(c["label"])}</button>' for c in n["children"])
        h.append(f'<div class="box"><div class="lbl">CONTENTS</div><div class="kids">{kids}</div></div>')
    h.append("</article>")
    return "".join(h)


EXPLORER_CSS = """
.cx{border:1px solid var(--line);border-radius:14px;overflow:hidden;display:grid;grid-template-columns:300px 1fr;background:var(--surface);margin:18px 0}
.cx .side{border-right:1px solid var(--line);background:var(--code);max-height:760px;overflow:auto}
.cx .tabs{display:flex;gap:4px;padding:10px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--code)}
.cx .tab{font:13px ui-monospace,Menlo,monospace;border:0;background:none;color:var(--muted);padding:6px 10px;border-radius:8px;cursor:pointer}
.cx .tab.on{background:var(--accent-soft);color:var(--accent);font-weight:700}
.cx .node{display:flex;align-items:center;gap:6px;width:100%;border:0;background:none;color:var(--ink);text-align:left;
 font:13.5px/1.2 ui-monospace,Menlo,monospace;padding-top:7px;padding-bottom:7px;padding-right:10px;cursor:pointer;border-left:3px solid transparent}
.cx .node:hover{background:var(--surface)}.cx .node.on{background:var(--surface);border-left-color:var(--accent);color:var(--accent);font-weight:700}
.cx .ic{width:12px;color:var(--muted)}.cx .nm{flex:1}
.cx .dot{width:7px;height:7px;border-radius:50%}.dot.committed{background:#5c9a4a}.dot.gitignored{background:#d0754c}.dot.local{background:#8f8d86}.dot.autogen{background:#d49a4c}
.cx .main{padding:22px 26px;max-height:760px;overflow:auto}
.cx .crumb{font:12.5px ui-monospace,Menlo,monospace;color:var(--muted)}
.cx .head{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:6px 0 2px}.cx .head h4{margin:0;font-size:24px}
.cx .badge{font:700 11px ui-monospace,Menlo,monospace;padding:3px 8px;border-radius:6px;border:1px solid var(--line)}
.badge.committed{color:#5c9a4a}.badge.gitignored{color:#d0754c}.badge.local{color:var(--muted)}.badge.autogen{color:#d49a4c}
.cx .one{color:var(--muted);margin:4px 0 14px}
.cx .when{border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:10px 0;background:var(--b-soft)}
.cx .lbl{font:700 11px/1.4 ui-monospace,Menlo,monospace;letter-spacing:.5px;color:var(--muted);margin-bottom:4px}
.cx .note{border-left:3px solid var(--accent);background:var(--accent-soft);padding:8px 12px;border-radius:6px;margin:10px 0;font-size:14.5px}
.cx .box{border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:12px 0}.cx .box ul{margin:0;padding-left:18px}
.cx .tips .lbl{color:var(--accent)}
.cx .ex{border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:10px 0}
.cx .exbar{display:flex;justify-content:space-between;align-items:center;padding:6px 10px;background:var(--code);font:12px ui-monospace,Menlo,monospace;color:var(--muted)}
.cx .copy{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:6px;font-size:12px;padding:2px 8px;cursor:pointer}
.cx .ex pre{margin:0;border:0;border-radius:0;max-height:420px}
.cx .full{display:inline-block;margin-top:8px;padding:5px 12px;border-radius:6px;background:var(--accent-soft);color:var(--accent);font-weight:700;font-size:13px;text-decoration:none}
.cx .kids{display:flex;flex-wrap:wrap;gap:6px}.cx .kid{font:12.5px ui-monospace,Menlo,monospace;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:6px;padding:3px 8px;cursor:pointer}
.cx.js .detail{display:none}.cx.js .detail.on{display:block}
.cx:not(.js) .detail{border-bottom:1px dashed var(--line);padding-bottom:18px;margin-bottom:18px}
@media (max-width:900px){.cx{grid-template-columns:1fr}.cx .side{max-height:320px;border-right:0;border-bottom:1px solid var(--line)}}
"""

EXPLORER_JS = """
document.querySelectorAll('.cx').forEach(function(cx){
  cx.classList.add('js');
  function show(id){
    cx.querySelectorAll('.detail').forEach(function(d){d.classList.toggle('on', d.id===id)});
    cx.querySelectorAll('.node').forEach(function(b){b.classList.toggle('on', b.dataset.target===id)});
    var m=cx.querySelector('.main'); if(m) m.scrollTop=0;
  }
  function tab(which){
    cx.querySelectorAll('.tab').forEach(function(t){t.classList.toggle('on', t.dataset.tab===which)});
    cx.querySelectorAll('.tree').forEach(function(t){t.hidden = t.dataset.tab!==which});
    var first=cx.querySelector('.tree[data-tab="'+which+'"] .node'); if(first) show(first.dataset.target);
  }
  cx.addEventListener('click', function(e){
    var b=e.target.closest('[data-target]'); if(b){ var id=b.dataset.target;
      var t=id.split('-')[0]; if(cx.querySelector('.tab.on').dataset.tab!==t) tab(t); show(id); return; }
    var tb=e.target.closest('.tab'); if(tb){ tab(tb.dataset.tab); return; }
    var c=e.target.closest('.copy'); if(c){ var code=c.closest('.ex').querySelector('code').innerText;
      navigator.clipboard && navigator.clipboard.writeText(code); c.textContent='Copied'; setTimeout(function(){c.textContent='Copy'},1200); }
  });
  tab('p');
});
"""


def explorer_html(tree: dict) -> str:
    panels = [panel_html(n, p, "p") for n, p, d in walk(tree["project"]) if d > 0]
    panels += [panel_html(n, p, "g") for n, p, d in walk(tree["global"]) if d > 0]
    return (
        f'<p>원문: <a href="{PAGE_KO}" target="_blank" rel="noopener">{PAGE_KO}</a> — 트리의 파일을 누르면 무엇을 하는지, 언제 불러오는지, 예시와 공식 문서 링크가 나온다. '
        '내용은 원문(영어) 그대로다. 모든 상세 내용은 이 페이지 안에 글자로 들어 있어 검색·fetch로 찾을 수 있다.</p>'
        '<div class="cx"><div class="side"><div class="tabs">'
        '<button class="tab on" data-tab="p">Project</button><button class="tab" data-tab="g">Global (~/)</button></div>'
        f'<nav class="tree" data-tab="p">{tree_html(tree["project"], "p")}</nav>'
        f'<nav class="tree" data-tab="g" hidden>{tree_html(tree["global"], "g")}</nav>'
        f'</div><div class="main">{"".join(panels)}</div></div>'
    )
