// Claude Code 공식 문서 '.claude 디렉토리 탐색'의 탐색기 데이터(FILE_TREE)를 JSON으로 그대로 뽑는다.
// 원본: sources/anthropic/claude-directory.ko.md  (https://code.claude.com/docs/ko/claude-directory.md)
// 출력: sources/anthropic/claude-directory.tree.json
// 문서 속 JSX(<C>코드</C>, <A href>링크</A>)는 마크다운(`코드`, [글](주소))으로 바꾸고, 나머지 값은 손대지 않는다.
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const SRC = join(ROOT, "sources/anthropic/claude-directory.ko.md");
const OUT = join(ROOT, "sources/anthropic/claude-directory.tree.json");
const BASE = "https://code.claude.com";

const text = readFileSync(SRC, "utf8");

const jsx = (inner) =>
  inner
    .replace(/\{'(.*?)'\}/g, "$1")
    .replace(/<C>(.*?)<\/C>/g, (_, c) => (c.includes("`") ? "`` " + c + " ``" : "`" + c + "`"))
    .replace(/<A href="([^"]*)">(.*?)<\/A>/g, (_, u, t) => `[${t}](${u.startsWith("/") ? BASE + u : u})`)
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&");

const fragToString = (src) => src.replace(/<>(.*?)<\/>/g, (_, inner) => JSON.stringify(jsx(inner)));

// 상수 commandsNote
const noteMatch = text.match(/const commandsNote = useMemo\(\(\) => <>(.*?)<\/>, \[\]\);/);
if (!noteMatch) throw new Error("commandsNote not found");
const commandsNote = jsx(noteMatch[1]);

// FILE_TREE 객체 원문
const start = text.indexOf("const FILE_TREE = useMemo(() => (");
const end = text.indexOf("}), []);", start);
if (start < 0 || end < 0) throw new Error("FILE_TREE not found");
let body = text.slice(start + "const FILE_TREE = useMemo(() => (".length, end + 1);
body = fragToString(body);

const tree = new Function("commandsNote", `return (${body});`)(commandsNote);

// docsLink('/en/..')를 전체 주소로
const walk = (node, fn) => { fn(node); (node.children || []).forEach((c) => walk(c, fn)); };
let count = 0, examples = 0, links = 0;
for (const root of [tree.project, tree.global]) {
  walk(root, (n) => {
    count++;
    if (n.example) examples++;
    if (n.docsLink) { n.docsLink = BASE + "/docs" + n.docsLink; links++; }
  });
}
writeFileSync(OUT, JSON.stringify(tree, null, 2));
const leftover = JSON.stringify(tree).match(/<\/?(C|A)[ >]|<>/g);
console.error(`NODES=${count} EXAMPLES=${examples} DOCSLINKS=${links} LEFTOVER_JSX=${leftover ? leftover.length : 0}`);
