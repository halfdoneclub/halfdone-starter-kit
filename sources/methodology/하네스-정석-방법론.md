# 하네스 구축 정석 방법론

> Codex든 Claude Code든 처음부터 하네스를 짜는 순서. OpenAI 하네스 글, Anthropic 하네스 글 2편, Claude Code 공식 문서를 합쳐 정리했다.

---

## 1. 처음부터 하네스를 짜는 7단계

| 단계 | 할 일 |
|---|---|
| **1. 완료 기준부터** | "다 되면 뭘 할 수 있고, 무엇으로 확인하나"를 먼저 정한다. 기능 목록을 만들고 전부 "실패"로 시작한다. |
| **2. 지도 + 문서 뼈대** | `CLAUDE.md`(Codex는 `AGENTS.md`)는 짧게(200줄 이하) 쓴다. 핵심 규칙과 "자세한 건 어디를 보라"를 담는 헌법이자 지도다. 자세한 내용은 `docs/` 아래로 나눈다. 폴더는 이 프로젝트에 필요한 것만 만든다. |
| **3. 검증 수단 연결** | 테스트·빌드·실행 명령을 에이전트가 직접 돌릴 수 있게 만든다. 앱을 띄우는 스크립트와, 결과를 눈으로 확인하는 방법(브라우저 자동화 등)도 갖춘다. |
| **4. 꼭 지킬 것만 강제** | 어기면 안 되는 몇 가지는 문서가 아니라 기계로 막는다. 훅(어기면 실행을 막는 장치)이나 린터(코드 규칙 자동 검사기)를 쓴다. |
| **5. 만드는 쪽과 채점하는 쪽 분리** | 채점 기준표를 가진 평가 에이전트를 따로 둔다. 자기 결과물을 스스로 채점하면 후하게 주기 때문이다. |
| **6. 기능 하나씩 실행** | 한 번에 기능 하나를 처리한다. 평가를 통과해야 "완료"로 표시한다. 진행 상황과 결정 기록은 계획서에 갱신한다. |
| **7. 쓰면서 키우고, 빼 본다** | 같은 문제가 반복되면 그에 맞는 장치를 추가한다(아래 2번 표). 모델이 좋아지면 장치를 하나씩 빼 보고 아직 필요한지 확인한다. |

---

## 2. 7단계에서 추가하는 기준 (Claude Code 공식 표)

| 이런 일이 생기면 | 추가 |
|---|---|
| 같은 규칙·명령을 두 번 틀림 | `CLAUDE.md`에 추가 |
| 같은 응답 형식을 계속 요구함 | output style (답변 형식 설정) |
| 작업을 시작하는 프롬프트를 계속 같은 걸 침 | 직접 부르는 스킬 |
| 같은 여러 단계 절차를 **세 번째** 붙여넣음 | 스킬 |
| Claude가 못 보는 브라우저 탭 데이터를 계속 복사해 줌 | MCP 서버 (외부 도구 연결) |
| 정의 위치를 찾느라 파일을 많이 읽음 | 코드 분석 플러그인 |
| 곁가지 작업 출력이 대화를 채움 | 서브에이전트 |
| 묻지 않아도 매번 일어나야 함 | 훅 |
| 두 번째 저장소도 같은 설정이 필요함 | 플러그인 |

---

## 3. 프로젝트마다 다른 부분 — 3·4·5단계

폴더 구조는 거의 같다. 프로젝트 성격에 따라 달라지는 것은 **검증 수단, 강제할 것, 평가 방식**이다.

| 프로젝트 성격 | 검증 수단 (3단계) | 강제할 것 예시 (4단계) | 평가 에이전트 (5단계) |
|---|---|---|---|
| 웹앱 | 테스트 + 브라우저로 자동 클릭해 확인 | 테스트가 실패하면 완료 금지 | 기능이 실제로 동작하는지 |
| 데이터 처리·자동화 스크립트 | 샘플 입력을 넣고 기대 출력과 비교 | 원본 데이터 덮어쓰기 금지 | 보통 불필요 |
| 외부 API 연동 | 실제 호출 성공 여부 | 키 하드코딩 금지 | 불필요 |
| 콘텐츠·디자인 생성 | 정답이 없으므로 채점 기준표 | 필수 요소(이미지·링크)가 빠지면 완료 금지 | 꼭 필요 (주관적 품질이라서) |

> 이 표는 공식 문서에 있는 표가 아니다. 위 원칙을 프로젝트 유형에 적용한 예시다.

---

## 4. 공식 문서 — 언제든 참고

| 문서 | 링크 |
|---|---|
| OpenAI — 하네스 엔지니어링: 에이전트 우선 세계에서 Codex 활용하기 (2026-02-11) | https://openai.com/ko-KR/index/harness-engineering/ |
| Claude Code — .claude 디렉토리 탐색 | https://code.claude.com/docs/ko/claude-directory |

<!-- 공식문서:시작 — 이 아래는 scripts/build_docs.py가 원문에서 자동 생성한다. 손으로 고치지 않는다. -->

### 4-1. OpenAI — 저장소 지식 구조 예시 (원문 그대로)

원문: [https://openai.com/ko-KR/index/harness-engineering/](https://openai.com/ko-KR/index/harness-engineering/) — 「리포지터리 지식을 기록 시스템으로 만듦」 절. 원문 캡션: "리포지터리 내 지식 저장소의 레이아웃."

```
AGENTS.md
ARCHITECTURE.md
docs/
├── design-docs/
│   ├── index.md
│   ├── core-beliefs.md
│   └── ...
├── exec-plans/
│   ├── active/
│   ├── completed/
│   └── tech-debt-tracker.md
├── generated/
│   └── db-schema.md
├── product-specs/
│   ├── index.md
│   ├── new-user-onboarding.md
│   └── ...
├── references/
│   ├── design-system-reference-llms.txt
│   ├── nixpacks-llms.txt
│   ├── uv-llms.txt
│   └── ...
├── DESIGN.md
├── FRONTEND.md
├── PLANS.md
├── PRODUCT_SENSE.md
├── QUALITY_SCORE.md
├── RELIABILITY.md
└── SECURITY.md
```

### 4-2. Claude Code — `.claude` 디렉토리 탐색 (원문 그대로)

원문: [https://code.claude.com/docs/ko/claude-directory](https://code.claude.com/docs/ko/claude-directory) — 「디렉토리 탐색」. 트리의 파일을 누르면 나오는 상세 내용(무엇을 하는지, 언제 불러오는지, 팁, 예시, 공식 문서 링크)을 **원문 그대로** 옮겼다. 탐색기 데이터는 한국어판에서도 영어 원문이다.

표시: `COMMITTED` git에 커밋·팀 공유 · `GITIGNORED` git 제외 · `LOCAL` 내 컴퓨터에만 · `AUTOGEN` Claude가 자동 생성

#### 트리 — Project (`your-project/`)

```
your-project/
  CLAUDE.md  [COMMITTED] — Project instructions Claude reads every session
  .mcp.json  [COMMITTED] — Project-scoped MCP servers, shared with your team
  .worktreeinclude  [COMMITTED] — Gitignored files to copy into new worktrees
  .claude/ — Project-level configuration, rules, and extensions
    settings.json  [COMMITTED] — Permissions, hooks, and configuration
    settings.local.json  [GITIGNORED] — Your personal settings overrides for this project
    rules/ — Topic-scoped instructions, optionally gated by file paths
      testing.md  [COMMITTED] — Test conventions scoped to test files
      api-design.md  [COMMITTED] — API conventions scoped to backend code
    skills/ — Reusable prompts you or Claude invoke by name
      security-review/ — A skill bundling SKILL.md with supporting files
        SKILL.md  [COMMITTED] — Entrypoint: trigger, invocability, instructions
        checklist.md  [COMMITTED] — Supporting file bundled with the skill
    commands/ — Single-file prompts invoked with `/name`
      fix-issue.md  [COMMITTED] — Invoked as `/fix-issue <number>`
    output-styles/ — Project-scoped output styles, if your team shares any
    agents/ — Specialized subagents with their own context window
      code-reviewer.md  [COMMITTED] — Subagent for isolated code review
    workflows/ — Dynamic workflow scripts that orchestrate many subagents
    agent-memory/  [AUTOGEN] [COMMITTED] — Subagent persistent memory, separate from your main session auto memory
      <agent-name>/  [AUTOGEN]
        MEMORY.md  [AUTOGEN] [COMMITTED] — The subagent writes and maintains this file automatically
```

#### 트리 — Global (`~/`)

```
~/
  .claude.json  [LOCAL] — App state and UI preferences
  .claude/ — Your personal configuration across all projects
    CLAUDE.md  [LOCAL] — Personal preferences across every project
    settings.json  [LOCAL] — Default settings for all projects
    keybindings.json  [LOCAL] — Custom keyboard shortcuts
    themes/ — Custom color themes
    projects/  [AUTOGEN] — Auto memory: Claude's notes to itself, per project
      <project>/memory/  [AUTOGEN] — Claude's accumulated knowledge for one project
        MEMORY.md  [AUTOGEN] [LOCAL] — Claude writes and maintains this file automatically
        debugging.md  [AUTOGEN] [LOCAL] — Topic notes Claude writes when MEMORY.md gets long
    rules/ — User-level rules that apply to every project
    skills/ — Personal skills available in every project
    commands/ — Personal single-file commands available in every project
    output-styles/ — Custom instruction sets that adjust how Claude works
      teaching.md  [LOCAL] — Example style that adds explanations and leaves small changes for you
    agents/ — Personal subagents available in every project
    workflows/ — Personal dynamic workflows available in every project
    agent-memory/  [AUTOGEN] — Persistent memory for subagents with `memory: user`
```

#### 파일·폴더별 상세 — Project

#### `your-project/CLAUDE.md`
*Project instructions Claude reads every session*

- **표시:** COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** Loaded into context at the start of every session
- **설명:** Project-specific instructions that shape how Claude works in this repository. Put your conventions, common commands, and architectural context here so Claude operates with the same assumptions your team does.
- **Tips:**
  - Target under 200 lines. Longer files still load in full but may reduce adherence
  - CLAUDE.md loads into every session. If something only matters for specific tasks, move it to a [skill](https://code.claude.com/docs/en/skills) or a path-scoped [rule](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) so it loads only when needed
  - List the commands you run most, like build, test, and format, so Claude knows them without you spelling them out each time
  - Run `/memory` to open and edit CLAUDE.md from within a session
  - Also works at `.claude/CLAUDE.md` if you prefer to keep the project root clean
  - If your repo already has an `AGENTS.md` for other coding agents, Claude Code [can read that](https://code.claude.com/docs/en/memory#agents-md) on its own or alongside CLAUDE.md
- **예시 설명:** This example is for a TypeScript and React project. It lists the build and test commands, the framework conventions Claude should follow, and project-specific rules like export style and file layout.

```
# Project conventions

## Commands
- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

## Stack
- TypeScript with strict mode
- React 19, functional components only

## Rules
- Named exports, never default exports
- Tests live next to source: `foo.ts` -> `foo.test.ts`
- All API routes return `{ data, error }` shape
```

[Full docs →](https://code.claude.com/docs/en/memory)

#### `your-project/.mcp.json`
*Project-scoped MCP servers, shared with your team*

- **표시:** COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** Servers connect when the session begins. Tool schemas are deferred by default and load on demand via [tool search](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search)
- **설명:** Configures Model Context Protocol (MCP) servers that give Claude access to external tools: databases, APIs, browsers, and more. This file holds the project-scoped servers your whole team uses. Personal servers you want to keep to yourself go in `~/.claude.json` instead.
- **Tips:**
  - Use environment variable references for secrets: `${NOTION_TOKEN}`
  - Lives at the project root, not inside `.claude/`
  - For servers only you need, run `claude mcp add --scope user`. This writes to `~/.claude.json` instead of `.mcp.json`
- **예시 설명:** This example configures the Notion MCP server so Claude can read and update pages in your workspace. The `${NOTION_TOKEN}` reference is read from your shell environment when Claude Code starts the server, so the token never lands in the file.

```
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "${NOTION_TOKEN}"
      }
    }
  }
}
```

[Full docs →](https://code.claude.com/docs/en/mcp)

#### `your-project/.worktreeinclude`
*Gitignored files to copy into new worktrees*

- **표시:** COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** Read when Claude creates a git worktree via `--worktree`, the `EnterWorktree` tool, or subagent `isolation: worktree`
- **설명:** Lists gitignored files to copy from your main repository into each new worktree. Worktrees are fresh checkouts, so untracked files like `.env` are missing by default. Patterns here use `.gitignore` syntax. Only files that match a pattern and are also gitignored get copied, so tracked files are never duplicated.
- **Tips:**
  - Lives at the project root, not inside `.claude/`
  - Git-only: if you configure a [WorktreeCreate hook](https://code.claude.com/docs/en/hooks#worktreecreate) for a different VCS, this file is not read. Copy files inside your hook script instead
  - Also applies to parallel sessions in the [desktop app](https://code.claude.com/docs/en/desktop#work-in-parallel-with-sessions)
- **예시 설명:** This example copies your local environment files and a secrets config into every worktree Claude creates. Comments start with # and blank lines are ignored, same as .gitignore.

```
# Local environment
.env
.env.local

# API credentials
config/secrets.json
```

[Full docs →](https://code.claude.com/docs/en/worktrees#copy-gitignored-files-into-worktrees)

#### `your-project/.claude`
*Project-level configuration, rules, and extensions*

- **설명:** Everything Claude Code reads that is specific to this project. If you use git, commit most files here so your team shares them; a few, like settings.local.json, are gitignored when Claude Code saves settings to them. Each file badge shows which.

- **Contents:** `settings.json`, `settings.local.json`, `rules/`, `skills/`, `commands/`, `output-styles/`, `agents/`, `workflows/`, `agent-memory/`

#### `your-project/.claude/settings.json`
*Permissions, hooks, and configuration*

- **표시:** COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** Overrides global `~/.claude/settings.json`. Local settings, CLI flags, and managed settings override this
- **설명:** Settings that Claude Code applies directly. Permissions control which commands and tools Claude can use; hooks run your scripts at specific points in a session. Unlike CLAUDE.md, which Claude reads as guidance, these are enforced whether Claude follows them or not.
- **Common keys:**
  - [permissions](https://code.claude.com/docs/en/permissions): allow, deny, or prompt before Claude uses specific tools or commands
  - [hooks](https://code.claude.com/docs/en/hooks): run your own scripts on events like before a tool call or after a file edit
  - [statusLine](https://code.claude.com/docs/en/statusline): customize the line shown at the bottom while Claude works
  - [model](https://code.claude.com/docs/en/settings-reference#available-settings): pick a default model for this project
  - [env](https://code.claude.com/docs/en/settings-reference#environment-variables): environment variables set in every session
  - [outputStyle](https://code.claude.com/docs/en/output-styles): select a custom output style from output-styles/
- **Tips:**
  - Bash permission patterns support wildcards: `Bash(npm test *)` matches any command starting with `npm test`
  - Array settings like `permissions.allow` combine across all scopes; scalar settings like `model` use the most specific value
- **예시 설명:** This example allows `npm test` and `npm run` commands without prompting, blocks `rm -rf`, and runs Prettier on files after Claude edits or writes them.

```
{
  "permissions": {
    "allow": [
      "Bash(npm test *)",
      "Bash(npm run *)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
      }]
    }]
  }
}
```

[Full docs →](https://code.claude.com/docs/en/settings)

#### `your-project/.claude/settings.local.json`
*Your personal settings overrides for this project*

- **표시:** GITIGNORED (git 제외)
- **When it loads:** Highest of the user-editable settings files; CLI flags and managed settings still take precedence
- **설명:** Personal settings that take precedence over the project defaults. Same JSON format as settings.json, gitignored when Claude Code saves a setting to it. Use this when you need different permissions or defaults than the team config.
- **Tips:**
  - Same schema as settings.json. Array settings like `permissions.allow` combine across scopes; scalar settings like `model` use the local value
  - When Claude Code saves a setting to this file in a repository that doesn't already ignore it, it adds `**/.claude/settings.local.json` to your global git excludes file: `core.excludesFile` from your global git config when it's set to an absolute or `~`-prefixed path, otherwise `$XDG_CONFIG_HOME/git/ignore`, or `~/.config/git/ignore`. To share the ignore rule with your team, also add it to the project `.gitignore`
- **예시 설명:** This example adds Docker permissions on top of whatever the team settings.json allows.

```
{
  "permissions": {
    "allow": [
      "Bash(docker *)"
    ]
  }
}
```

[Full docs →](https://code.claude.com/docs/en/settings)

#### `your-project/.claude/rules`
*Topic-scoped instructions, optionally gated by file paths*

- **When it loads:** Rules without `paths:` load at session start. Rules with `paths:` load when a matching file enters context
- **설명:** Project instructions split into topic files that can load conditionally based on file paths. A rule without `paths:` frontmatter loads at session start like CLAUDE.md; a rule with `paths:` loads only when Claude reads a matching file.
  
  Like CLAUDE.md, rules are guidance Claude reads, not configuration Claude Code enforces. For guaranteed behavior use [hooks](https://code.claude.com/docs/en/hooks) or [permissions](https://code.claude.com/docs/en/permissions).
- **Tips:**
  - Use `paths:` frontmatter with globs to scope rules to directories or file types
  - Subdirectories work: `.claude/rules/frontend/react.md` is discovered automatically
  - When CLAUDE.md approaches 200 lines, start splitting into rules

[Full docs →](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)

- **Contents:** `testing.md`, `api-design.md`

#### `your-project/.claude/rules/testing.md`
*Test conventions scoped to test files*

- **표시:** COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** Loaded when Claude reads a file matching the `paths:` globs below
- **설명:** An example rule that only loads when Claude is working on test files. The `paths:` globs in the frontmatter define which files trigger it; here, anything ending in .test.ts or .test.tsx. For other files, this rule is not loaded into context.

```
---
paths:
  - "**/*.test.ts"
  - "**/*.test.tsx"
---

# Testing Rules

- Use descriptive test names: "should [expected] when [condition]"
- Mock external dependencies, not internal modules
- Clean up side effects in afterEach
```

#### `your-project/.claude/rules/api-design.md`
*API conventions scoped to backend code*

- **표시:** COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** Loaded when Claude reads a file matching the `paths:` glob below
- **설명:** A second example showing a rule scoped to backend code. The `paths:` glob matches files under src/api/, so these conventions load only when Claude is editing API routes.

```
---
paths:
  - "src/api/**/*.ts"
---

# API Design Rules

- All endpoints must validate input with Zod schemas
- Return shape: { data: T } | { error: string }
- Rate limit all public endpoints
```

#### `your-project/.claude/skills`
*Reusable prompts you or Claude invoke by name*

- **When it loads:** Invoked with `/skill-name` or when Claude matches the task to a skill
- **설명:** Each skill is a folder with a SKILL.md file plus any supporting files it needs. By default, both you and Claude can invoke a skill. Use frontmatter to control that: `disable-model-invocation: true` for user-only workflows like `/deploy`, or `user-invocable: false` to hide from the `/` menu while Claude can still invoke it.
- **Tips:**
  - Skills accept arguments: `/deploy staging` passes "staging" as `$ARGUMENTS`. Use `$0`, `$1`, and so on for positional access
  - The `description` frontmatter determines when Claude auto-invokes the skill
  - Bundle reference docs alongside SKILL.md. Claude knows the skill directory path and can read supporting files when you mention them

[Full docs →](https://code.claude.com/docs/en/skills)

- **Contents:** `security-review/`

#### `your-project/.claude/skills/security-review`
*A skill bundling SKILL.md with supporting files*


- **Contents:** `SKILL.md`, `checklist.md`

#### `your-project/.claude/skills/security-review/SKILL.md`
*Entrypoint: trigger, invocability, instructions*

- **표시:** COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** User types `/security-review <target>`; Claude cannot auto-invoke this skill
- **설명:** This skill uses `disable-model-invocation: true` so only you can trigger it; Claude never invokes it on its own.
  
  The `` !`...` `` line runs a shell command and injects its output into the prompt. `$ARGUMENTS` substitutes whatever you typed after the skill name. Claude sees the skill directory path, so mentioning a bundled file like checklist.md lets Claude read it.

```
---
description: Reviews code changes for security vulnerabilities, authentication gaps, and injection risks
disable-model-invocation: true
argument-hint: <branch-or-path>
---

## Diff to review

!`git diff $ARGUMENTS`

Audit the changes above for:

1. Injection vulnerabilities (SQL, XSS, command)
2. Authentication and authorization gaps
3. Hardcoded secrets or credentials

Use checklist.md in this skill directory for the full review checklist.

Report findings with severity ratings and remediation steps.
```

#### `your-project/.claude/skills/security-review/checklist.md`
*Supporting file bundled with the skill*

- **표시:** COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** Claude reads it on demand while running the skill
- **설명:** Skills can bundle any supporting files: reference docs, templates, scripts. The skill directory path is prepended to SKILL.md, so Claude can read bundled files by name. For scripts in bash injection commands, use the `${CLAUDE_SKILL_DIR}` placeholder.

```
# Security Review Checklist

## Input Validation
- [ ] All user input sanitized before DB queries
- [ ] File upload MIME types validated
- [ ] Path traversal prevented on file operations

## Authentication
- [ ] JWT tokens expire after 24 hours
- [ ] API keys stored in environment variables
- [ ] Passwords hashed with bcrypt or argon2
```

#### `your-project/.claude/commands`
*Single-file prompts invoked with `/name`*

- **안내:** Commands and skills are now the same mechanism. For new workflows, use [skills/](https://code.claude.com/docs/en/skills) instead: same `/name` invocation, plus you can bundle supporting files.
- **When it loads:** User types `/command-name`
- **설명:** A file at `commands/deploy.md` creates `/deploy` the same way a skill at `skills/deploy/SKILL.md` does, and both can be auto-invoked by Claude. Skills use a directory with SKILL.md, letting you bundle reference docs, templates, or scripts alongside the prompt.
- **Tips:**
  - Use `$ARGUMENTS` in the file to accept parameters: `/fix-issue 123`
  - If a skill and command share a name, the skill takes precedence
  - New commands should usually be skills instead; commands remain supported

[Full docs →](https://code.claude.com/docs/en/skills)

- **Contents:** `fix-issue.md`

#### `your-project/.claude/commands/fix-issue.md`
*Invoked as `/fix-issue <number>`*

- **표시:** COMMITTED (git에 커밋 · 팀 공유)
- **안내:** Commands and skills are now the same mechanism. For new workflows, use [skills/](https://code.claude.com/docs/en/skills) instead: same `/name` invocation, plus you can bundle supporting files.
- **설명:** An example command for fixing a GitHub issue. Type `/fix-issue 123` and the `` !`...` `` line runs `gh issue view 123` in your shell, injecting the output into the prompt before Claude sees it.
  
  `$ARGUMENTS` substitutes whatever you typed after the command name. For positional access, use `$0` `$1` and so on.

```
---
argument-hint: <issue-number>
---

!`gh issue view $ARGUMENTS`

Investigate and fix the issue above.

1. Trace the bug to its root cause
2. Implement the fix
3. Write or update tests
4. Summarize what you changed and why
```

#### `your-project/.claude/output-styles`
*Project-scoped output styles, if your team shares any*

- **When it loads:** Files read at startup; the style you select with outputStyle applies to every response
- **설명:** Output styles are usually personal, so most live in `~/.claude/output-styles/`. Put one here if your team shares a style, like a review mode everyone uses. See [the Global tab](#ce-global-output-styles) for the full explanation and example.

[Full docs →](https://code.claude.com/docs/en/output-styles)

#### `your-project/.claude/agents`
*Specialized subagents with their own context window*

- **When it loads:** Runs in its own context window when you or Claude invoke it
- **설명:** Each markdown file defines a subagent with its own system prompt, tool access, and optionally its own model. Subagents run in a fresh context window, keeping the main conversation clean. Useful for parallel work or isolated tasks.
- **Tips:**
  - Each agent gets a fresh context window, separate from your main session
  - Restrict tool access per agent with the `tools:` frontmatter field
  - Type @ and pick an agent from the autocomplete to delegate directly

[Full docs →](https://code.claude.com/docs/en/sub-agents)

- **Contents:** `code-reviewer.md`

#### `your-project/.claude/agents/code-reviewer.md`
*Subagent for isolated code review*

- **표시:** COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** Claude spawns it for review tasks, or you @-mention it from the autocomplete
- **설명:** An example subagent restricted to read-only tools. The `description` frontmatter tells Claude when to delegate to it automatically; `tools:` limits it to Read, Grep, and Glob so it can inspect code but never edit. The body becomes the subagent's system prompt.

```
---
name: code-reviewer
description: Reviews code for correctness, security, and maintainability
tools: Read, Grep, Glob
---

You are a senior code reviewer. Review for:

1. Correctness: logic errors, edge cases, null handling
2. Security: injection, auth bypass, data exposure
3. Maintainability: naming, complexity, duplication

Every finding must include a concrete fix.
```

#### `your-project/.claude/workflows`
*Dynamic workflow scripts that orchestrate many subagents*

- **When it loads:** Loaded at startup; each file becomes a /<name> command
- **설명:** Each `.js` file is a [dynamic workflow](https://code.claude.com/docs/en/workflows): a script the runtime executes to spawn and coordinate many subagents. Workflows are written by Claude and saved here from `/workflows` rather than authored from scratch.
- **Tips:**
  - Save a run from `/workflows` with `s` to create one of these
  - A project workflow takes precedence over a personal one in `~/.claude/workflows/` with the same name

[Full docs →](https://code.claude.com/docs/en/workflows)

#### `your-project/.claude/agent-memory`
*Subagent persistent memory, separate from your main session auto memory*

- **표시:** AUTOGEN (Claude가 자동 생성), COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** First 200 lines (capped at 25KB) of MEMORY.md loaded into the subagent system prompt when it runs
- **설명:** Subagents with `memory: project` in their frontmatter get a dedicated memory directory here. This is distinct from your [main session auto memory](https://code.claude.com/docs/en/memory#auto-memory) at `~/.claude/projects/`: each subagent reads and writes its own MEMORY.md, not yours.
- **Tips:**
  - Only created for subagents that set the `memory:` frontmatter field
  - This directory holds project-scoped subagent memory, meant to be shared with your team. To keep memory out of version control use `memory: local`, which writes to `.claude/agent-memory-local/` instead. For cross-project memory use `memory: user`, which writes to `~/.claude/agent-memory/`
  - The main session auto memory is a different feature; see `~/.claude/projects/` in the Global tab

[Full docs →](https://code.claude.com/docs/en/sub-agents#enable-persistent-memory)

- **Contents:** `<agent-name>/`

#### `your-project/.claude/agent-memory/<agent-name>`
- **표시:** AUTOGEN (Claude가 자동 생성)

- **Contents:** `MEMORY.md`

#### `your-project/.claude/agent-memory/<agent-name>/MEMORY.md`
*The subagent writes and maintains this file automatically*

- **표시:** AUTOGEN (Claude가 자동 생성), COMMITTED (git에 커밋 · 팀 공유)
- **When it loads:** Loaded into the subagent system prompt when the subagent starts
- **설명:** Works the same as your [main auto memory](https://code.claude.com/docs/en/memory#auto-memory): the subagent creates and updates this file itself. You do not write it. The subagent reads it at the start of each task and writes back what it learns.

```
# code-reviewer memory

## Patterns seen
- Project uses custom Result<T, E> type, not exceptions
- Auth middleware expects Bearer token in Authorization header
- Tests use factory functions in test/factories/

## Recurring issues
- Missing null checks on API responses (src/api/*)
- Unhandled promise rejections in background jobs
```


#### 파일·폴더별 상세 — Global (`~/`)

#### `~/.claude.json`
*App state and UI preferences*

- **표시:** LOCAL (내 컴퓨터에만)
- **When it loads:** Read at session start for your preferences and MCP servers. Claude Code writes back to it when you change settings in `/config` or approve trust prompts
- **설명:** Holds state that does not belong in settings.json: theme, OAuth session, per-project trust decisions, your personal MCP servers, and UI toggles. Mostly managed through `/config` rather than editing directly.
- **Tips:**
  - IDE toggles like `autoConnectIde` and `externalEditorContext` live here, not in settings.json
  - The `projects` key tracks per-project state like trust-dialog acceptance and last-session metrics. Permission rules you approve in-session go to `.claude/settings.local.json` instead
  - MCP servers here are yours only: user scope applies across all projects, local scope is per-project but not committed. Team-shared servers go in `.mcp.json` at the project root instead

```
{
  "autoConnectIde": true,
  "externalEditorContext": true,
  "mcpServers": {
    "my-tools": {
      "command": "npx",
      "args": ["-y", "@example/mcp-server"]
    }
  }
}
```

[Full docs →](https://code.claude.com/docs/en/settings-reference#global-config-settings)

#### `~/.claude`
*Your personal configuration across all projects*

- **설명:** The global counterpart to your project .claude/ directory. Files here apply to every project you work in and are never committed to any repository.

- **Contents:** `CLAUDE.md`, `settings.json`, `keybindings.json`, `themes/`, `projects/`, `rules/`, `skills/`, `commands/`, `output-styles/`, `agents/`, `workflows/`, `agent-memory/`

#### `~/.claude/CLAUDE.md`
*Personal preferences across every project*

- **표시:** LOCAL (내 컴퓨터에만)
- **When it loads:** Loaded at the start of every session, in every project
- **설명:** Your global instruction file. Loaded alongside the project CLAUDE.md at session start, so both are in context together. When instructions conflict, project-level instructions take priority. Keep this to preferences that apply everywhere: response style, commit format, personal conventions.
- **Tips:**
  - Keep it short since it loads into context for every project, alongside that project's own CLAUDE.md
  - Good for response style, commit format, and personal conventions

```
# Global preferences

- Keep explanations concise
- Use conventional commit format
- Show the terminal command to verify changes
- Prefer composition over inheritance
```

[Full docs →](https://code.claude.com/docs/en/memory)

#### `~/.claude/settings.json`
*Default settings for all projects*

- **표시:** LOCAL (내 컴퓨터에만)
- **When it loads:** Your defaults. Project and local settings.json override any keys you also set there
- **설명:** Same keys as project `settings.json`: permissions, hooks, model, environment variables, and the rest. Put settings here that you want in every project, like permissions you always allow, a preferred model, or a notification hook that runs regardless of which project you're in.
  
  Settings follow a precedence order: project `settings.json` overrides any matching keys you set here. This is different from CLAUDE.md, where global and project files are both loaded into context rather than merged key by key.

```
{
  "permissions": {
    "allow": [
      "Bash(git log *)",
      "Bash(git diff *)"
    ]
  }
}
```

[Full docs →](https://code.claude.com/docs/en/settings)

#### `~/.claude/keybindings.json`
*Custom keyboard shortcuts*

- **표시:** LOCAL (내 컴퓨터에만)
- **When it loads:** Read at session start and hot-reloaded when you edit the file
- **설명:** Rebind keyboard shortcuts in the interactive CLI. Run `/keybindings` to create or open this file with a schema reference. Ctrl+C, Ctrl+D, Ctrl+M, and Caps Lock are reserved and cannot be rebound.
- **예시 설명:** This example binds `Ctrl+E` to open your external editor and unbinds `Ctrl+U` by setting it to `null`. The `context` field scopes bindings to a specific part of the CLI, here the main chat input.

```
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

[Full docs →](https://code.claude.com/docs/en/keybindings)

#### `~/.claude/themes`
*Custom color themes*

- **When it loads:** Read at session start and hot-reloaded when files change. Listed in `/theme`
- **설명:** Each `.json` file defines a custom color theme: a built-in `base` preset plus an `overrides` map of color tokens. Create one interactively with `/theme` or write the JSON by hand. Selecting a custom theme stores `custom:<slug>` as your theme preference.

```
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

[Full docs →](https://code.claude.com/docs/en/terminal-config#create-a-custom-theme)

#### `~/.claude/projects`
*Auto memory: Claude's notes to itself, per project*

- **표시:** AUTOGEN (Claude가 자동 생성)
- **When it loads:** MEMORY.md loaded at session start; topic files read on demand
- **설명:** Auto memory lets Claude accumulate knowledge across sessions without you writing anything. Claude saves notes as it works: build commands, debugging insights, architecture notes. Each project gets its own memory directory keyed by the repository path.
- **Tips:**
  - On by default. Toggle with `/memory` or `autoMemoryEnabled` in settings
  - MEMORY.md is the index loaded each session. The first 200 lines, or 25KB, whichever comes first, are read
  - Topic files like debugging.md are read on demand, not at startup
  - These are plain markdown. Edit or delete them anytime

[Full docs →](https://code.claude.com/docs/en/memory#auto-memory)

- **Contents:** `<project>/memory/`

#### `~/.claude/projects/<project>/memory`
*Claude's accumulated knowledge for one project*

- **표시:** AUTOGEN (Claude가 자동 생성)

- **Contents:** `MEMORY.md`, `debugging.md`

#### `~/.claude/projects/<project>/memory/MEMORY.md`
*Claude writes and maintains this file automatically*

- **표시:** AUTOGEN (Claude가 자동 생성), LOCAL (내 컴퓨터에만)
- **When it loads:** First 200 lines (capped at 25KB) loaded at session start
- **설명:** Claude creates and updates this file as it works; you do not write it yourself. It acts as an index that Claude reads at the start of every session, pointing to topic files for detail. You can edit or delete it, but Claude will keep updating it.

```
# Memory Index

## Project
- [build-and-test.md](build-and-test.md): npm run build (~45s), Vitest, dev server on 3001
- [architecture.md](architecture.md): API client singleton, refresh-token auth

## Reference
- [debugging.md](debugging.md): auth token rotation and DB connection troubleshooting
```

[Full docs →](https://code.claude.com/docs/en/memory)

#### `~/.claude/projects/<project>/memory/debugging.md`
*Topic notes Claude writes when MEMORY.md gets long*

- **표시:** AUTOGEN (Claude가 자동 생성), LOCAL (내 컴퓨터에만)
- **When it loads:** Claude reads this when a related task comes up
- **설명:** An example of a topic file Claude creates when MEMORY.md grows too long. Claude picks the filename based on what it splits out: debugging.md, architecture.md, build-commands.md, or similar. You never create these yourself. Claude reads a topic file back only when the current task relates to it.

```
---
name: Debugging patterns
description: Auth token rotation and database connection troubleshooting for this project
type: reference
---

## Auth Token Issues
- Refresh token rotation: old token invalidated immediately
- If 401 after refresh: check clock skew between client and server

## Database Connection Drops
- Connection pool: max 10 in dev, 50 in prod
- Always check `docker compose ps` first
```

#### `~/.claude/rules`
*User-level rules that apply to every project*

- **When it loads:** Rules without `paths:` load at session start. Rules with `paths:` load when a matching file enters context
- **설명:** Same as project .claude/rules/ but applies everywhere. Use this for conventions you want across all your work, like personal code style or commit message format.

[Full docs →](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)

#### `~/.claude/skills`
*Personal skills available in every project*

- **When it loads:** Invoked with `/skill-name` in any project
- **설명:** Skills you built for yourself that work everywhere. Same structure as project skills: each is a folder with SKILL.md, scoped to your user account instead of a single project.

[Full docs →](https://code.claude.com/docs/en/skills)

#### `~/.claude/commands`
*Personal single-file commands available in every project*

- **안내:** Commands and skills are now the same mechanism. For new workflows, use [skills/](https://code.claude.com/docs/en/skills) instead: same `/name` invocation, plus you can bundle supporting files.
- **When it loads:** User types `/command-name` in any project
- **설명:** Same as project commands/ but scoped to your user account. Each markdown file becomes a command available everywhere.

[Full docs →](https://code.claude.com/docs/en/skills)

#### `~/.claude/output-styles`
*Custom instruction sets that adjust how Claude works*

- **When it loads:** Files read at startup; the style you select with outputStyle applies to every response
- **설명:** Each markdown file defines an output style: a set of instructions for Claude that, by default, also replaces the built-in software-engineering task instructions. Use this to adapt Claude Code for uses beyond coding, or to add teaching or review modes.
  
  Select a built-in or custom style with `/output-style`, `/config`, or the `outputStyle` key in settings. Styles here are available in every project; project-level styles with the same name take precedence.
- **Tips:**
  - Built-in styles Default, Proactive, Concise, Explanatory, and Learning are included with Claude Code; custom styles go here
  - Set `keep-coding-instructions: true` in frontmatter to keep the default task instructions alongside your additions
  - Switching styles mid-session applies from your next message; in the terminal, a style file you create or edit mid-session is picked up after a restart

[Full docs →](https://code.claude.com/docs/en/output-styles)

- **Contents:** `teaching.md`

#### `~/.claude/output-styles/teaching.md`
*Example style that adds explanations and leaves small changes for you*

- **표시:** LOCAL (내 컴퓨터에만)
- **When it loads:** Active when `outputStyle` in settings is set to `teaching`
- **설명:** With this style, Claude adds a "Why this approach" note after each task and leaves TODO(human) markers for changes under 10 lines instead of writing them itself. Select it by setting `outputStyle` to the filename without .md, or to the `name` field if you set one in frontmatter.

```
---
description: Explains reasoning and asks you to implement small pieces
keep-coding-instructions: true
---

After completing each task, add a brief "Why this approach" note
explaining the key design decision.

When a change is under 10 lines, ask the user to implement it
themselves by leaving a TODO(human) marker instead of writing it.
```

#### `~/.claude/agents`
*Personal subagents available in every project*

- **When it loads:** Claude delegates or you @-mention in any project
- **설명:** Subagents defined here are available across all your projects. Same format as project agents.

[Full docs →](https://code.claude.com/docs/en/sub-agents)

#### `~/.claude/workflows`
*Personal dynamic workflows available in every project*

- **When it loads:** Loaded at startup; each file becomes a /<name> command
- **설명:** Workflow scripts saved here are available across all your projects. A project workflow with the same name in `.claude/workflows/` takes precedence.

[Full docs →](https://code.claude.com/docs/en/workflows)

#### `~/.claude/agent-memory`
*Persistent memory for subagents with `memory: user`*

- **표시:** AUTOGEN (Claude가 자동 생성)
- **When it loads:** Loaded into the subagent system prompt when the subagent starts
- **설명:** Subagents with `memory: user` in their frontmatter store knowledge here that persists across all projects. For project-scoped subagent memory, see `.claude/agent-memory/` instead.

[Full docs →](https://code.claude.com/docs/en/sub-agents#enable-persistent-memory)

<!-- 공식문서:끝 -->
