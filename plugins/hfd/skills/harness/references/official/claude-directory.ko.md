<!-- 원문: https://code.claude.com/docs/ko/claude-directory · 받은 날: 2026-09-23 · hfd 킷이 원문 그대로 보관 (tools/build_refs.py). 손으로 고치지 않는다. -->

> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# .claude 디렉토리 탐색

> Claude Code가 CLAUDE.md, settings.json, hooks, skills, commands, subagents, workflows, rules, auto memory를 읽는 위치입니다. 프로젝트의 .claude 디렉토리와 홈 디렉토리의 ~/.claude를 탐색합니다.

export const ClaudeExplorer = () => {
  const A = useMemo(() => ({href, children}) => <a href={href} style={{
    color: 'var(--ce-accent)',
    textDecoration: 'none',
    borderBottom: '1px dotted var(--ce-accent)'
  }}>{children}</a>, []);
  const C = useMemo(() => ({children}) => <code style={{
    fontFamily: 'var(--ce-mono)',
    fontSize: '0.92em',
    padding: '1px 4px',
    borderRadius: '3px',
    background: 'var(--ce-surface)',
    border: '0.5px solid var(--ce-border-subtle)'
  }}>{children}</code>, []);
  const commandsNote = useMemo(() => <>Commands and skills are now the same mechanism. For new workflows, use <A href="/docs/en/skills">skills/</A> instead: same <C>/name</C> invocation, plus you can bundle supporting files.</>, []);
  const FILE_TREE = useMemo(() => ({
    project: {
      label: 'your-project/',
      children: [{
        id: 'claude-md',
        label: 'CLAUDE.md',
        type: 'file',
        icon: 'md',
        color: '#6A9BCC',
        badge: 'committed',
        oneLiner: 'Project instructions Claude reads every session',
        when: 'Loaded into context at the start of every session',
        description: 'Project-specific instructions that shape how Claude works in this repository. Put your conventions, common commands, and architectural context here so Claude operates with the same assumptions your team does.',
        tips: ['Target under 200 lines. Longer files still load in full but may reduce adherence', <>CLAUDE.md loads into every session. If something only matters for specific tasks, move it to a <A href="/docs/en/skills">skill</A> or a path-scoped <A href="/docs/en/memory#organize-rules-with-claude/rules/">rule</A> so it loads only when needed</>, 'List the commands you run most, like build, test, and format, so Claude knows them without you spelling them out each time', <>Run <C>/memory</C> to open and edit CLAUDE.md from within a session</>, <>Also works at <C>.claude/CLAUDE.md</C> if you prefer to keep the project root clean</>, <>If your repo already has an <C>AGENTS.md</C> for other coding agents, Claude Code <A href="/docs/en/memory#agents-md">can read that</A> on its own or alongside CLAUDE.md</>],
        exampleIntro: 'This example is for a TypeScript and React project. It lists the build and test commands, the framework conventions Claude should follow, and project-specific rules like export style and file layout.',
        example: `# Project conventions

## Commands
- Build: \`npm run build\`
- Test: \`npm test\`
- Lint: \`npm run lint\`

## Stack
- TypeScript with strict mode
- React 19, functional components only

## Rules
- Named exports, never default exports
- Tests live next to source: \`foo.ts\` -> \`foo.test.ts\`
- All API routes return \`{ data, error }\` shape`,
        docsLink: '/en/memory'
      }, {
        id: 'mcp-json',
        label: '.mcp.json',
        type: 'file',
        icon: 'json',
        color: '#9B7BC4',
        badge: 'committed',
        oneLiner: 'Project-scoped MCP servers, shared with your team',
        when: <>Servers connect when the session begins. Tool schemas are deferred by default and load on demand via <A href="/docs/en/mcp#scale-with-mcp-tool-search">tool search</A></>,
        description: <>Configures Model Context Protocol (MCP) servers that give Claude access to external tools: databases, APIs, browsers, and more. This file holds the project-scoped servers your whole team uses. Personal servers you want to keep to yourself go in <C>~/.claude.json</C> instead.</>,
        tips: [<>Use environment variable references for secrets: <C>{'${NOTION_TOKEN}'}</C></>, <>Lives at the project root, not inside <C>.claude/</C></>, <>For servers only you need, run <C>claude mcp add --scope user</C>. This writes to <C>~/.claude.json</C> instead of <C>.mcp.json</C></>],
        exampleIntro: <>This example configures the Notion MCP server so Claude can read and update pages in your workspace. The <C>{'${NOTION_TOKEN}'}</C> reference is read from your shell environment when Claude Code starts the server, so the token never lands in the file.</>,
        example: `{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "\${NOTION_TOKEN}"
      }
    }
  }
}`,
        docsLink: '/en/mcp'
      }, {
        id: 'worktreeinclude',
        label: '.worktreeinclude',
        type: 'file',
        icon: 'md',
        color: '#8FA876',
        badge: 'committed',
        oneLiner: 'Gitignored files to copy into new worktrees',
        when: <>Read when Claude creates a git worktree via <C>--worktree</C>, the <C>EnterWorktree</C> tool, or subagent <C>isolation: worktree</C></>,
        description: <>Lists gitignored files to copy from your main repository into each new worktree. Worktrees are fresh checkouts, so untracked files like <C>.env</C> are missing by default. Patterns here use <C>.gitignore</C> syntax. Only files that match a pattern and are also gitignored get copied, so tracked files are never duplicated.</>,
        tips: [<>Lives at the project root, not inside <C>.claude/</C></>, <>Git-only: if you configure a <A href="/docs/en/hooks#worktreecreate">WorktreeCreate hook</A> for a different VCS, this file is not read. Copy files inside your hook script instead</>, <>Also applies to parallel sessions in the <A href="/docs/en/desktop#work-in-parallel-with-sessions">desktop app</A></>],
        exampleIntro: 'This example copies your local environment files and a secrets config into every worktree Claude creates. Comments start with # and blank lines are ignored, same as .gitignore.',
        example: `# Local environment
.env
.env.local

# API credentials
config/secrets.json`,
        docsLink: '/en/worktrees#copy-gitignored-files-into-worktrees'
      }, {
        id: 'dot-claude',
        label: '.claude/',
        type: 'folder',
        icon: 'folder',
        color: 'var(--ce-accent)',
        oneLiner: 'Project-level configuration, rules, and extensions',
        description: 'Everything Claude Code reads that is specific to this project. If you use git, commit most files here so your team shares them; a few, like settings.local.json, are gitignored when Claude Code saves settings to them. Each file badge shows which.',
        children: [{
          id: 'settings-json',
          label: 'settings.json',
          type: 'file',
          icon: 'json',
          color: 'var(--ce-text-3)',
          badge: 'committed',
          oneLiner: 'Permissions, hooks, and configuration',
          when: <>Overrides global <C>~/.claude/settings.json</C>. Local settings, CLI flags, and managed settings override this</>,
          description: 'Settings that Claude Code applies directly. Permissions control which commands and tools Claude can use; hooks run your scripts at specific points in a session. Unlike CLAUDE.md, which Claude reads as guidance, these are enforced whether Claude follows them or not.',
          contains: [<><A href="/docs/en/permissions">permissions</A>: allow, deny, or prompt before Claude uses specific tools or commands</>, <><A href="/docs/en/hooks">hooks</A>: run your own scripts on events like before a tool call or after a file edit</>, <><A href="/docs/en/statusline">statusLine</A>: customize the line shown at the bottom while Claude works</>, <><A href="/docs/en/settings-reference#available-settings">model</A>: pick a default model for this project</>, <><A href="/docs/en/settings-reference#environment-variables">env</A>: environment variables set in every session</>, <><A href="/docs/en/output-styles">outputStyle</A>: select a custom output style from output-styles/</>],
          tips: [<>Bash permission patterns support wildcards: <C>Bash(npm test *)</C> matches any command starting with <C>npm test</C></>, <>Array settings like <C>permissions.allow</C> combine across all scopes; scalar settings like <C>model</C> use the most specific value</>],
          exampleIntro: <>This example allows <C>npm test</C> and <C>npm run</C> commands without prompting, blocks <C>rm -rf</C>, and runs Prettier on files after Claude edits or writes them.</>,
          example: `{
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
}`,
          docsLink: '/en/settings'
        }, {
          id: 'settings-local-json',
          label: 'settings.local.json',
          type: 'file',
          icon: 'json',
          color: 'var(--ce-text-3)',
          badge: 'gitignored',
          oneLiner: 'Your personal settings overrides for this project',
          when: 'Highest of the user-editable settings files; CLI flags and managed settings still take precedence',
          description: 'Personal settings that take precedence over the project defaults. Same JSON format as settings.json, gitignored when Claude Code saves a setting to it. Use this when you need different permissions or defaults than the team config.',
          tips: [<>Same schema as settings.json. Array settings like <C>permissions.allow</C> combine across scopes; scalar settings like <C>model</C> use the local value</>, <>When Claude Code saves a setting to this file in a repository that doesn't already ignore it, it adds <C>**/.claude/settings.local.json</C> to your global git excludes file: <C>core.excludesFile</C> from your global git config when it's set to an absolute or <C>~</C>-prefixed path, otherwise <C>$XDG_CONFIG_HOME/git/ignore</C>, or <C>~/.config/git/ignore</C>. To share the ignore rule with your team, also add it to the project <C>.gitignore</C></>],
          exampleIntro: 'This example adds Docker permissions on top of whatever the team settings.json allows.',
          example: `{
  "permissions": {
    "allow": [
      "Bash(docker *)"
    ]
  }
}`,
          docsLink: '/en/settings'
        }, {
          id: 'rules',
          label: 'rules/',
          type: 'folder',
          icon: 'folder',
          color: '#9B7BC4',
          oneLiner: 'Topic-scoped instructions, optionally gated by file paths',
          when: <>Rules without <C>paths:</C> load at session start. Rules with <C>paths:</C> load when a matching file enters context</>,
          description: [<>Project instructions split into topic files that can load conditionally based on file paths. A rule without <C>paths:</C> frontmatter loads at session start like CLAUDE.md; a rule with <C>paths:</C> loads only when Claude reads a matching file.</>, <>Like CLAUDE.md, rules are guidance Claude reads, not configuration Claude Code enforces. For guaranteed behavior use <A href="/docs/en/hooks">hooks</A> or <A href="/docs/en/permissions">permissions</A>.</>],
          tips: [<>Use <C>paths:</C> frontmatter with globs to scope rules to directories or file types</>, <>Subdirectories work: <C>.claude/rules/frontend/react.md</C> is discovered automatically</>, 'When CLAUDE.md approaches 200 lines, start splitting into rules'],
          docsLink: '/en/memory#organize-rules-with-claude/rules/',
          children: [{
            id: 'rule-testing',
            label: 'testing.md',
            type: 'file',
            icon: 'md',
            color: '#9B7BC4',
            badge: 'committed',
            oneLiner: 'Test conventions scoped to test files',
            when: <>Loaded when Claude reads a file matching the <C>paths:</C> globs below</>,
            description: <>An example rule that only loads when Claude is working on test files. The <C>paths:</C> globs in the frontmatter define which files trigger it; here, anything ending in .test.ts or .test.tsx. For other files, this rule is not loaded into context.</>,
            example: `---
paths:
  - "**/*.test.ts"
  - "**/*.test.tsx"
---

# Testing Rules

- Use descriptive test names: "should [expected] when [condition]"
- Mock external dependencies, not internal modules
- Clean up side effects in afterEach`
          }, {
            id: 'rule-api',
            label: 'api-design.md',
            type: 'file',
            icon: 'md',
            color: '#9B7BC4',
            badge: 'committed',
            oneLiner: 'API conventions scoped to backend code',
            when: <>Loaded when Claude reads a file matching the <C>paths:</C> glob below</>,
            description: <>A second example showing a rule scoped to backend code. The <C>paths:</C> glob matches files under src/api/, so these conventions load only when Claude is editing API routes.</>,
            example: `---
paths:
  - "src/api/**/*.ts"
---

# API Design Rules

- All endpoints must validate input with Zod schemas
- Return shape: { data: T } | { error: string }
- Rate limit all public endpoints`
          }]
        }, {
          id: 'skills',
          label: 'skills/',
          type: 'folder',
          icon: 'folder',
          color: '#D4A843',
          oneLiner: 'Reusable prompts you or Claude invoke by name',
          when: <>Invoked with <C>/skill-name</C> or when Claude matches the task to a skill</>,
          description: <>Each skill is a folder with a SKILL.md file plus any supporting files it needs. By default, both you and Claude can invoke a skill. Use frontmatter to control that: <C>disable-model-invocation: true</C> for user-only workflows like <C>/deploy</C>, or <C>user-invocable: false</C> to hide from the <C>/</C> menu while Claude can still invoke it.</>,
          tips: [<>Skills accept arguments: <C>/deploy staging</C> passes "staging" as <C>$ARGUMENTS</C>. Use <C>$0</C>, <C>$1</C>, and so on for positional access</>, <>The <C>description</C> frontmatter determines when Claude auto-invokes the skill</>, 'Bundle reference docs alongside SKILL.md. Claude knows the skill directory path and can read supporting files when you mention them'],
          docsLink: '/en/skills',
          children: [{
            id: 'skill-review',
            label: 'security-review/',
            type: 'folder',
            icon: 'folder',
            color: '#D4A843',
            oneLiner: 'A skill bundling SKILL.md with supporting files',
            children: [{
              id: 'skill-review-md',
              label: 'SKILL.md',
              type: 'file',
              icon: 'md',
              color: '#D4A843',
              badge: 'committed',
              oneLiner: 'Entrypoint: trigger, invocability, instructions',
              when: <>User types <C>/security-review &lt;target&gt;</C>; Claude cannot auto-invoke this skill</>,
              description: [<>This skill uses <C>disable-model-invocation: true</C> so only you can trigger it; Claude never invokes it on its own.</>, <>The <C>!`...`</C> line runs a shell command and injects its output into the prompt. <C>$ARGUMENTS</C> substitutes whatever you typed after the skill name. Claude sees the skill directory path, so mentioning a bundled file like checklist.md lets Claude read it.</>],
              example: `---
description: Reviews code changes for security vulnerabilities, authentication gaps, and injection risks
disable-model-invocation: true
argument-hint: <branch-or-path>
---

## Diff to review

!\`git diff $ARGUMENTS\`

Audit the changes above for:

1. Injection vulnerabilities (SQL, XSS, command)
2. Authentication and authorization gaps
3. Hardcoded secrets or credentials

Use checklist.md in this skill directory for the full review checklist.

Report findings with severity ratings and remediation steps.`
            }, {
              id: 'skill-checklist',
              label: 'checklist.md',
              type: 'file',
              icon: 'md',
              color: '#D4A843',
              badge: 'committed',
              oneLiner: 'Supporting file bundled with the skill',
              when: 'Claude reads it on demand while running the skill',
              description: <>Skills can bundle any supporting files: reference docs, templates, scripts. The skill directory path is prepended to SKILL.md, so Claude can read bundled files by name. For scripts in bash injection commands, use the <C>{'${CLAUDE_SKILL_DIR}'}</C> placeholder.</>,
              example: `# Security Review Checklist

## Input Validation
- [ ] All user input sanitized before DB queries
- [ ] File upload MIME types validated
- [ ] Path traversal prevented on file operations

## Authentication
- [ ] JWT tokens expire after 24 hours
- [ ] API keys stored in environment variables
- [ ] Passwords hashed with bcrypt or argon2`
            }]
          }]
        }, {
          id: 'commands',
          label: 'commands/',
          type: 'folder',
          icon: 'folder',
          color: '#788C5D',
          oneLiner: <>Single-file prompts invoked with <C>/name</C></>,
          note: commandsNote,
          when: <>User types <C>/command-name</C></>,
          description: <>A file at <C>commands/deploy.md</C> creates <C>/deploy</C> the same way a skill at <C>skills/deploy/SKILL.md</C> does, and both can be auto-invoked by Claude. Skills use a directory with SKILL.md, letting you bundle reference docs, templates, or scripts alongside the prompt.</>,
          tips: [<>Use <C>$ARGUMENTS</C> in the file to accept parameters: <C>/fix-issue 123</C></>, 'If a skill and command share a name, the skill takes precedence', 'New commands should usually be skills instead; commands remain supported'],
          docsLink: '/en/skills',
          children: [{
            id: 'cmd-example',
            label: 'fix-issue.md',
            type: 'file',
            icon: 'md',
            color: '#788C5D',
            badge: 'committed',
            oneLiner: <>Invoked as <C>/fix-issue &lt;number&gt;</C></>,
            note: commandsNote,
            description: [<>An example command for fixing a GitHub issue. Type <C>/fix-issue 123</C> and the <C>!`...`</C> line runs <C>gh issue view 123</C> in your shell, injecting the output into the prompt before Claude sees it.</>, <><C>$ARGUMENTS</C> substitutes whatever you typed after the command name. For positional access, use <C>$0</C> <C>$1</C> and so on.</>],
            example: `---
argument-hint: <issue-number>
---

!\`gh issue view $ARGUMENTS\`

Investigate and fix the issue above.

1. Trace the bug to its root cause
2. Implement the fix
3. Write or update tests
4. Summarize what you changed and why`
          }]
        }, {
          id: 'output-styles',
          label: 'output-styles/',
          type: 'folder',
          icon: 'folder',
          color: '#5AA7A7',
          oneLiner: 'Project-scoped output styles, if your team shares any',
          when: 'Files read at startup; the style you select with outputStyle applies to every response',
          description: <>Output styles are usually personal, so most live in <C>~/.claude/output-styles/</C>. Put one here if your team shares a style, like a review mode everyone uses. See <A href="#ce-global-output-styles">the Global tab</A> for the full explanation and example.</>,
          docsLink: '/en/output-styles',
          children: []
        }, {
          id: 'agents',
          label: 'agents/',
          type: 'folder',
          icon: 'folder',
          color: '#C46686',
          oneLiner: 'Specialized subagents with their own context window',
          when: 'Runs in its own context window when you or Claude invoke it',
          description: 'Each markdown file defines a subagent with its own system prompt, tool access, and optionally its own model. Subagents run in a fresh context window, keeping the main conversation clean. Useful for parallel work or isolated tasks.',
          tips: ['Each agent gets a fresh context window, separate from your main session', <>Restrict tool access per agent with the <C>tools:</C> frontmatter field</>, 'Type @ and pick an agent from the autocomplete to delegate directly'],
          docsLink: '/en/sub-agents',
          children: [{
            id: 'agent-reviewer',
            label: 'code-reviewer.md',
            type: 'file',
            icon: 'md',
            color: '#C46686',
            badge: 'committed',
            oneLiner: 'Subagent for isolated code review',
            when: 'Claude spawns it for review tasks, or you @-mention it from the autocomplete',
            description: <>An example subagent restricted to read-only tools. The <C>description</C> frontmatter tells Claude when to delegate to it automatically; <C>tools:</C> limits it to Read, Grep, and Glob so it can inspect code but never edit. The body becomes the subagent's system prompt.</>,
            example: `---
name: code-reviewer
description: Reviews code for correctness, security, and maintainability
tools: Read, Grep, Glob
---

You are a senior code reviewer. Review for:

1. Correctness: logic errors, edge cases, null handling
2. Security: injection, auth bypass, data exposure
3. Maintainability: naming, complexity, duplication

Every finding must include a concrete fix.`
          }]
        }, {
          id: 'workflows',
          label: 'workflows/',
          type: 'folder',
          icon: 'folder',
          color: '#C46686',
          oneLiner: 'Dynamic workflow scripts that orchestrate many subagents',
          when: 'Loaded at startup; each file becomes a /<name> command',
          description: <>Each <C>.js</C> file is a <A href="/docs/en/workflows">dynamic workflow</A>: a script the runtime executes to spawn and coordinate many subagents. Workflows are written by Claude and saved here from <C>/workflows</C> rather than authored from scratch.</>,
          tips: [<>Save a run from <C>/workflows</C> with <C>s</C> to create one of these</>, <>A project workflow takes precedence over a personal one in <C>~/.claude/workflows/</C> with the same name</>],
          docsLink: '/en/workflows'
        }, {
          id: 'agent-memory',
          label: 'agent-memory/',
          type: 'folder',
          icon: 'folder',
          color: '#C46686',
          badge: 'committed',
          autogen: true,
          oneLiner: 'Subagent persistent memory, separate from your main session auto memory',
          when: 'First 200 lines (capped at 25KB) of MEMORY.md loaded into the subagent system prompt when it runs',
          description: <>Subagents with <C>memory: project</C> in their frontmatter get a dedicated memory directory here. This is distinct from your <A href="/docs/en/memory#auto-memory">main session auto memory</A> at <C>~/.claude/projects/</C>: each subagent reads and writes its own MEMORY.md, not yours.</>,
          tips: [<>Only created for subagents that set the <C>memory:</C> frontmatter field</>, <>This directory holds project-scoped subagent memory, meant to be shared with your team. To keep memory out of version control use <C>memory: local</C>, which writes to <C>.claude/agent-memory-local/</C> instead. For cross-project memory use <C>memory: user</C>, which writes to <C>~/.claude/agent-memory/</C></>, <>The main session auto memory is a different feature; see <C>~/.claude/projects/</C> in the Global tab</>],
          docsLink: '/en/sub-agents#enable-persistent-memory',
          children: [{
            id: 'agent-memory-sub',
            label: '<agent-name>/',
            type: 'folder',
            icon: 'folder',
            color: '#C46686',
            autogen: true,
            children: [{
              id: 'agent-memory-md',
              label: 'MEMORY.md',
              type: 'file',
              icon: 'md',
              color: '#C46686',
              badge: 'committed',
              autogen: true,
              oneLiner: 'The subagent writes and maintains this file automatically',
              when: 'Loaded into the subagent system prompt when the subagent starts',
              description: <>Works the same as your <A href="/docs/en/memory#auto-memory">main auto memory</A>: the subagent creates and updates this file itself. You do not write it. The subagent reads it at the start of each task and writes back what it learns.</>,
              example: `# code-reviewer memory

## Patterns seen
- Project uses custom Result<T, E> type, not exceptions
- Auth middleware expects Bearer token in Authorization header
- Tests use factory functions in test/factories/

## Recurring issues
- Missing null checks on API responses (src/api/*)
- Unhandled promise rejections in background jobs`
            }]
          }]
        }]
      }]
    },
    global: {
      label: '~/',
      children: [{
        id: 'claude-json',
        label: '.claude.json',
        type: 'file',
        icon: 'json',
        color: 'var(--ce-text-3)',
        badge: 'local',
        oneLiner: 'App state and UI preferences',
        when: <>Read at session start for your preferences and MCP servers. Claude Code writes back to it when you change settings in <C>/config</C> or approve trust prompts</>,
        description: <>Holds state that does not belong in settings.json: theme, OAuth session, per-project trust decisions, your personal MCP servers, and UI toggles. Mostly managed through <C>/config</C> rather than editing directly.</>,
        tips: [<>IDE toggles like <C>autoConnectIde</C> and <C>externalEditorContext</C> live here, not in settings.json</>, <>The <C>projects</C> key tracks per-project state like trust-dialog acceptance and last-session metrics. Permission rules you approve in-session go to <C>.claude/settings.local.json</C> instead</>, <>MCP servers here are yours only: user scope applies across all projects, local scope is per-project but not committed. Team-shared servers go in <C>.mcp.json</C> at the project root instead</>],
        example: `{
  "autoConnectIde": true,
  "externalEditorContext": true,
  "mcpServers": {
    "my-tools": {
      "command": "npx",
      "args": ["-y", "@example/mcp-server"]
    }
  }
}`,
        docsLink: '/en/settings-reference#global-config-settings'
      }, {
        id: 'global-dot-claude',
        label: '.claude/',
        type: 'folder',
        icon: 'folder',
        color: 'var(--ce-accent)',
        oneLiner: 'Your personal configuration across all projects',
        description: 'The global counterpart to your project .claude/ directory. Files here apply to every project you work in and are never committed to any repository.',
        children: [{
          id: 'global-claude-md',
          label: 'CLAUDE.md',
          type: 'file',
          icon: 'md',
          color: '#6A9BCC',
          badge: 'local',
          oneLiner: 'Personal preferences across every project',
          when: 'Loaded at the start of every session, in every project',
          description: 'Your global instruction file. Loaded alongside the project CLAUDE.md at session start, so both are in context together. When instructions conflict, project-level instructions take priority. Keep this to preferences that apply everywhere: response style, commit format, personal conventions.',
          tips: ['Keep it short since it loads into context for every project, alongside that project\'s own CLAUDE.md', 'Good for response style, commit format, and personal conventions'],
          example: `# Global preferences

- Keep explanations concise
- Use conventional commit format
- Show the terminal command to verify changes
- Prefer composition over inheritance`,
          docsLink: '/en/memory'
        }, {
          id: 'global-settings',
          label: 'settings.json',
          type: 'file',
          icon: 'json',
          color: 'var(--ce-text-3)',
          badge: 'local',
          oneLiner: 'Default settings for all projects',
          when: 'Your defaults. Project and local settings.json override any keys you also set there',
          description: [<>Same keys as project <C>settings.json</C>: permissions, hooks, model, environment variables, and the rest. Put settings here that you want in every project, like permissions you always allow, a preferred model, or a notification hook that runs regardless of which project you're in.</>, <>Settings follow a precedence order: project <C>settings.json</C> overrides any matching keys you set here. This is different from CLAUDE.md, where global and project files are both loaded into context rather than merged key by key.</>],
          example: `{
  "permissions": {
    "allow": [
      "Bash(git log *)",
      "Bash(git diff *)"
    ]
  }
}`,
          docsLink: '/en/settings'
        }, {
          id: 'keybindings',
          label: 'keybindings.json',
          type: 'file',
          icon: 'json',
          color: 'var(--ce-text-3)',
          badge: 'local',
          oneLiner: 'Custom keyboard shortcuts',
          when: 'Read at session start and hot-reloaded when you edit the file',
          description: <>Rebind keyboard shortcuts in the interactive CLI. Run <C>/keybindings</C> to create or open this file with a schema reference. Ctrl+C, Ctrl+D, Ctrl+M, and Caps Lock are reserved and cannot be rebound.</>,
          exampleIntro: <>This example binds <C>Ctrl+E</C> to open your external editor and unbinds <C>Ctrl+U</C> by setting it to <C>null</C>. The <C>context</C> field scopes bindings to a specific part of the CLI, here the main chat input.</>,
          example: `{
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
}`,
          docsLink: '/en/keybindings'
        }, {
          id: 'themes',
          label: 'themes/',
          type: 'folder',
          icon: 'folder',
          color: '#5AA7A7',
          oneLiner: 'Custom color themes',
          when: <>Read at session start and hot-reloaded when files change. Listed in <C>/theme</C></>,
          description: <>Each <C>.json</C> file defines a custom color theme: a built-in <C>base</C> preset plus an <C>overrides</C> map of color tokens. Create one interactively with <C>/theme</C> or write the JSON by hand. Selecting a custom theme stores <C>custom:&lt;slug&gt;</C> as your theme preference.</>,
          example: `{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}`,
          docsLink: '/en/terminal-config#create-a-custom-theme',
          children: []
        }, {
          id: 'global-projects',
          label: 'projects/',
          type: 'folder',
          icon: 'folder',
          color: '#E8A45C',
          autogen: true,
          oneLiner: "Auto memory: Claude's notes to itself, per project",
          when: 'MEMORY.md loaded at session start; topic files read on demand',
          description: 'Auto memory lets Claude accumulate knowledge across sessions without you writing anything. Claude saves notes as it works: build commands, debugging insights, architecture notes. Each project gets its own memory directory keyed by the repository path.',
          tips: [<>On by default. Toggle with <C>/memory</C> or <C>autoMemoryEnabled</C> in settings</>, 'MEMORY.md is the index loaded each session. The first 200 lines, or 25KB, whichever comes first, are read', 'Topic files like debugging.md are read on demand, not at startup', 'These are plain markdown. Edit or delete them anytime'],
          docsLink: '/en/memory#auto-memory',
          children: [{
            id: 'memory-dir',
            label: '<project>/memory/',
            type: 'folder',
            icon: 'folder',
            color: '#E8A45C',
            autogen: true,
            oneLiner: "Claude's accumulated knowledge for one project",
            children: [{
              id: 'memory-md',
              label: 'MEMORY.md',
              type: 'file',
              icon: 'md',
              color: '#E8A45C',
              badge: 'local',
              autogen: true,
              oneLiner: 'Claude writes and maintains this file automatically',
              when: 'First 200 lines (capped at 25KB) loaded at session start',
              description: 'Claude creates and updates this file as it works; you do not write it yourself. It acts as an index that Claude reads at the start of every session, pointing to topic files for detail. You can edit or delete it, but Claude will keep updating it.',
              example: `# Memory Index

## Project
- [build-and-test.md](build-and-test.md): npm run build (~45s), Vitest, dev server on 3001
- [architecture.md](architecture.md): API client singleton, refresh-token auth

## Reference
- [debugging.md](debugging.md): auth token rotation and DB connection troubleshooting`,
              docsLink: '/en/memory'
            }, {
              id: 'memory-topic',
              label: 'debugging.md',
              type: 'file',
              icon: 'md',
              color: '#E8A45C',
              badge: 'local',
              autogen: true,
              oneLiner: 'Topic notes Claude writes when MEMORY.md gets long',
              when: 'Claude reads this when a related task comes up',
              description: 'An example of a topic file Claude creates when MEMORY.md grows too long. Claude picks the filename based on what it splits out: debugging.md, architecture.md, build-commands.md, or similar. You never create these yourself. Claude reads a topic file back only when the current task relates to it.',
              example: `---
name: Debugging patterns
description: Auth token rotation and database connection troubleshooting for this project
type: reference
---

## Auth Token Issues
- Refresh token rotation: old token invalidated immediately
- If 401 after refresh: check clock skew between client and server

## Database Connection Drops
- Connection pool: max 10 in dev, 50 in prod
- Always check \`docker compose ps\` first`
            }]
          }]
        }, {
          id: 'global-rules',
          label: 'rules/',
          type: 'folder',
          icon: 'folder',
          color: '#9B7BC4',
          oneLiner: 'User-level rules that apply to every project',
          when: <>Rules without <C>paths:</C> load at session start. Rules with <C>paths:</C> load when a matching file enters context</>,
          description: 'Same as project .claude/rules/ but applies everywhere. Use this for conventions you want across all your work, like personal code style or commit message format.',
          docsLink: '/en/memory#organize-rules-with-claude/rules/',
          children: []
        }, {
          id: 'global-skills',
          label: 'skills/',
          type: 'folder',
          icon: 'folder',
          color: '#D4A843',
          oneLiner: 'Personal skills available in every project',
          when: <>Invoked with <C>/skill-name</C> in any project</>,
          description: 'Skills you built for yourself that work everywhere. Same structure as project skills: each is a folder with SKILL.md, scoped to your user account instead of a single project.',
          docsLink: '/en/skills',
          children: []
        }, {
          id: 'global-commands',
          label: 'commands/',
          type: 'folder',
          icon: 'folder',
          color: '#788C5D',
          oneLiner: 'Personal single-file commands available in every project',
          note: commandsNote,
          when: <>User types <C>/command-name</C> in any project</>,
          description: 'Same as project commands/ but scoped to your user account. Each markdown file becomes a command available everywhere.',
          docsLink: '/en/skills',
          children: []
        }, {
          id: 'global-output-styles',
          label: 'output-styles/',
          type: 'folder',
          icon: 'folder',
          color: '#5AA7A7',
          oneLiner: 'Custom instruction sets that adjust how Claude works',
          when: 'Files read at startup; the style you select with outputStyle applies to every response',
          description: [<>Each markdown file defines an output style: a set of instructions for Claude that, by default, also replaces the built-in software-engineering task instructions. Use this to adapt Claude Code for uses beyond coding, or to add teaching or review modes.</>, <>Select a built-in or custom style with <C>/output-style</C>, <C>/config</C>, or the <C>outputStyle</C> key in settings. Styles here are available in every project; project-level styles with the same name take precedence.</>],
          tips: ['Built-in styles Default, Proactive, Concise, Explanatory, and Learning are included with Claude Code; custom styles go here', <>Set <C>keep-coding-instructions: true</C> in frontmatter to keep the default task instructions alongside your additions</>, 'Switching styles mid-session applies from your next message; in the terminal, a style file you create or edit mid-session is picked up after a restart'],
          docsLink: '/en/output-styles',
          children: [{
            id: 'output-style-example',
            label: 'teaching.md',
            type: 'file',
            icon: 'md',
            color: '#5AA7A7',
            badge: 'local',
            oneLiner: 'Example style that adds explanations and leaves small changes for you',
            when: <>Active when <C>outputStyle</C> in settings is set to <C>teaching</C></>,
            description: <>With this style, Claude adds a "Why this approach" note after each task and leaves TODO(human) markers for changes under 10 lines instead of writing them itself. Select it by setting <C>outputStyle</C> to the filename without .md, or to the <C>name</C> field if you set one in frontmatter.</>,
            example: `---
description: Explains reasoning and asks you to implement small pieces
keep-coding-instructions: true
---

After completing each task, add a brief "Why this approach" note
explaining the key design decision.

When a change is under 10 lines, ask the user to implement it
themselves by leaving a TODO(human) marker instead of writing it.`
          }]
        }, {
          id: 'global-agents',
          label: 'agents/',
          type: 'folder',
          icon: 'folder',
          color: '#C46686',
          oneLiner: 'Personal subagents available in every project',
          when: 'Claude delegates or you @-mention in any project',
          description: 'Subagents defined here are available across all your projects. Same format as project agents.',
          docsLink: '/en/sub-agents',
          children: []
        }, {
          id: 'global-workflows',
          label: 'workflows/',
          type: 'folder',
          icon: 'folder',
          color: '#C46686',
          oneLiner: 'Personal dynamic workflows available in every project',
          when: 'Loaded at startup; each file becomes a /<name> command',
          description: <>Workflow scripts saved here are available across all your projects. A project workflow with the same name in <C>.claude/workflows/</C> takes precedence.</>,
          docsLink: '/en/workflows',
          children: []
        }, {
          id: 'global-agent-memory',
          label: 'agent-memory/',
          type: 'folder',
          icon: 'folder',
          color: '#C46686',
          autogen: true,
          oneLiner: <>Persistent memory for subagents with <C>memory: user</C></>,
          when: 'Loaded into the subagent system prompt when the subagent starts',
          description: <>Subagents with <C>memory: user</C> in their frontmatter store knowledge here that persists across all projects. For project-scoped subagent memory, see <C>.claude/agent-memory/</C> instead.</>,
          docsLink: '/en/sub-agents#enable-persistent-memory',
          children: []
        }]
      }]
    }
  }), []);
  const BADGE_STYLES = useMemo(() => ({
    committed: {
      bg: 'rgba(85,138,66,0.08)',
      color: 'var(--ce-badge-committed)',
      border: 'rgba(85,138,66,0.15)',
      label: 'committed'
    },
    gitignored: {
      bg: 'rgba(217,119,87,0.06)',
      color: 'var(--ce-badge-gitignored)',
      border: 'rgba(217,119,87,0.15)',
      label: 'gitignored'
    },
    local: {
      bg: 'rgba(115,114,108,0.06)',
      color: 'var(--ce-badge-local)',
      border: 'rgba(115,114,108,0.12)',
      label: 'local only'
    },
    autogen: {
      bg: 'rgba(232,164,92,0.1)',
      color: 'var(--ce-badge-autogen)',
      border: 'rgba(232,164,92,0.2)',
      label: 'Claude writes'
    }
  }), []);
  const allNodes = useMemo(() => {
    const flatten = (nodes, acc, path, parentId) => {
      for (const node of nodes) {
        const nextPath = [...path, node.label];
        acc[node.id] = {
          ...node,
          path: nextPath,
          parentId
        };
        if (node.children) flatten(node.children, acc, nextPath, node.id);
      }
      return acc;
    };
    const project = flatten(FILE_TREE.project.children, {}, [FILE_TREE.project.label]);
    const global = flatten(FILE_TREE.global.children, {}, [FILE_TREE.global.label]);
    for (const id in project) project[id].root = 'project';
    for (const id in global) global[id].root = 'global';
    return {
      ...project,
      ...global
    };
  }, [FILE_TREE]);
  const allFolderIds = useMemo(() => Object.keys(allNodes).filter(id => allNodes[id].type === 'folder'), [allNodes]);
  const DEFAULT_EXPANDED = ['dot-claude', 'rules', 'skills', 'skill-review', 'commands', 'agents', 'agent-memory', 'agent-memory-sub', 'global-dot-claude', 'global-output-styles', 'global-projects', 'memory-dir'];
  const [mounted, setMounted] = useState(false);
  const [activeRoot, setActiveRoot] = useState('project');
  const [selectedId, setSelectedId] = useState('claude-md');
  const [expandedFolders, setExpandedFolders] = useState(() => new Set(DEFAULT_EXPANDED));
  const [forceMobile, setForceMobile] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const copyTimeoutRef = useRef(null);
  const rootRef = useRef(null);
  useEffect(() => {
    setMounted(true);
    const applyHash = scroll => {
      const hash = window.location.hash.slice(1);
      if (!hash.startsWith('ce-')) return;
      const id = hash.slice(3);
      const node = allNodes[id];
      if (!node) return;
      setActiveRoot(node.root);
      setSelectedId(id);
      setExpandedFolders(new Set(allFolderIds));
      if (scroll && rootRef.current) rootRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    };
    applyHash(false);
    const onHashChange = () => applyHash(true);
    const onFsChange = () => setIsFullscreen(!!document.fullscreenElement);
    window.addEventListener('hashchange', onHashChange);
    document.addEventListener('fullscreenchange', onFsChange);
    return () => {
      if (copyTimeoutRef.current) clearTimeout(copyTimeoutRef.current);
      window.removeEventListener('hashchange', onHashChange);
      document.removeEventListener('fullscreenchange', onFsChange);
    };
  }, []);
  useEffect(() => {
    if (!mounted || !rootRef.current) return;
    const hash = window.location.hash.slice(1);
    if (hash.startsWith('ce-') && allNodes[hash.slice(3)]) {
      rootRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  }, [mounted]);
  if (!mounted) return null;
  const selected = allNodes[selectedId];
  const tree = FILE_TREE[activeRoot];
  const isCopied = copiedId === selected.id;
  const toggleFolder = id => {
    const next = new Set(expandedFolders);
    next.has(id) ? next.delete(id) : next.add(id);
    setExpandedFolders(next);
  };
  const switchRoot = root => {
    if (root === activeRoot) return;
    setActiveRoot(root);
    const firstId = FILE_TREE[root].children[0].id;
    setSelectedId(firstId);
    try {
      history.replaceState(null, '', '#ce-' + firstId);
    } catch (e) {}
  };
  const toggleFullscreen = () => {
    if (!rootRef.current) return;
    if (document.fullscreenElement) document.exitFullscreen(); else rootRef.current.requestFullscreen().catch(() => {});
  };
  const selectNode = n => {
    setSelectedId(n.id);
    if (n.type === 'folder' && !expandedFolders.has(n.id)) toggleFolder(n.id);
    try {
      history.replaceState(null, '', '#ce-' + n.id);
    } catch (e) {}
  };
  const iconBtn = {
    width: 28,
    flexShrink: 0,
    borderRadius: '6px',
    border: 'none',
    cursor: 'pointer',
    background: 'transparent',
    color: 'var(--ce-text-4)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  };
  const visibleFolderIds = allFolderIds.filter(id => allNodes[id].root === activeRoot);
  const allExpanded = visibleFolderIds.every(id => expandedFolders.has(id));
  const toggleAllFolders = () => {
    const next = new Set(expandedFolders);
    visibleFolderIds.forEach(id => allExpanded ? next.delete(id) : next.add(id));
    setExpandedFolders(next);
  };
  const onTreeKeyDown = e => {
    if (!['ArrowDown', 'ArrowUp', 'ArrowRight', 'ArrowLeft'].includes(e.key)) return;
    const visible = [];
    const walk = nodes => {
      for (const n of nodes) {
        visible.push(n.id);
        if (n.children && expandedFolders.has(n.id)) walk(n.children);
      }
    };
    walk(tree.children);
    const i = visible.indexOf(selectedId);
    if (i === -1) return;
    e.preventDefault();
    if (e.key === 'ArrowDown' && i < visible.length - 1) selectNode(allNodes[visible[i + 1]]); else if (e.key === 'ArrowUp' && i > 0) selectNode(allNodes[visible[i - 1]]); else if (e.key === 'ArrowRight' && selected.type === 'folder') {
      if (!expandedFolders.has(selectedId)) toggleFolder(selectedId); else if (selected.children && selected.children.length) selectNode(allNodes[selected.children[0].id]);
    } else if (e.key === 'ArrowLeft') {
      if (selected.type === 'folder' && expandedFolders.has(selectedId)) toggleFolder(selectedId); else if (selected.parentId) selectNode(allNodes[selected.parentId]);
    }
  };
  const copyExample = (id, text) => {
    const done = () => {
      setCopiedId(id);
      if (copyTimeoutRef.current) clearTimeout(copyTimeoutRef.current);
      copyTimeoutRef.current = setTimeout(() => setCopiedId(null), 2000);
    };
    const fallback = () => {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try {
        if (document.execCommand('copy')) done();
      } catch (e) {}
      document.body.removeChild(ta);
    };
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }
  };
  const renderIcon = (icon, color, size) => {
    const sz = size || 14;
    if (icon === 'folder') {
      return <svg width={sz} height={sz} viewBox="0 0 14 14" fill="none">
          <path d="M1.5 3.5a1 1 0 0 1 1-1h2.6l1 1.2h5.4a1 1 0 0 1 1 1v5.8a1 1 0 0 1-1 1h-9a1 1 0 0 1-1-1V3.5z" fill={color} fillOpacity="0.15" stroke={color} strokeWidth="1" />
        </svg>;
    }
    if (icon === 'json') {
      return <svg width={sz} height={sz} viewBox="0 0 14 14" fill="none">
          <rect x="2" y="1.5" width="10" height="11" rx="1.5" fill={color} fillOpacity="0.15" stroke={color} strokeWidth="1" />
          <text x="7" y="9" fontSize="6" fontFamily="monospace" fill={color} textAnchor="middle" fontWeight="700">{'{}'}</text>
        </svg>;
    }
    return <svg width={sz} height={sz} viewBox="0 0 14 14" fill="none">
        <rect x="2" y="1.5" width="10" height="11" rx="1.5" fill={color} fillOpacity="0.15" stroke={color} strokeWidth="1" />
        <line x1="4.5" y1="5" x2="9.5" y2="5" stroke={color} strokeWidth="1" />
        <line x1="4.5" y1="7" x2="9.5" y2="7" stroke={color} strokeWidth="1" />
        <line x1="4.5" y1="9" x2="8" y2="9" stroke={color} strokeWidth="1" />
      </svg>;
  };
  const renderNode = (node, depth) => {
    const isFolder = node.type === 'folder';
    const isExpanded = expandedFolders.has(node.id);
    const isSelected = selectedId === node.id;
    return <div key={node.id}>
        <button role="treeitem" tabIndex={-1} onClick={() => selectNode(node)} aria-selected={isSelected} aria-expanded={isFolder ? isExpanded : undefined} style={{
      display: 'flex',
      alignItems: 'center',
      gap: '5px',
      width: '100%',
      padding: `4px 8px 4px ${8 + depth * 16}px`,
      background: isSelected ? 'var(--ce-accent-bg)' : 'transparent',
      borderTop: 'none',
      borderRight: 'none',
      borderBottom: 'none',
      borderLeft: isSelected ? '2px solid var(--ce-accent)' : '2px solid transparent',
      outline: 'none',
      cursor: 'pointer',
      textAlign: 'left',
      fontFamily: 'var(--ce-mono)',
      fontSize: '13.5px',
      color: isSelected ? 'var(--ce-accent)' : 'var(--ce-text-2)',
      fontWeight: isSelected ? 550 : 400,
      transition: 'all 0.1s'
    }}>
          {isFolder ? <span onClick={e => {
      e.stopPropagation();
      toggleFolder(node.id);
    }} style={{
      fontSize: '14px',
      color: 'var(--ce-text-4)',
      width: '20px',
      height: '20px',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      cursor: 'pointer',
      borderRadius: '4px',
      marginLeft: '-6px',
      flexShrink: 0
    }} onMouseEnter={e => {
      e.currentTarget.style.background = 'var(--ce-arrow-hover)';
      e.currentTarget.style.color = 'var(--ce-text-2)';
    }} onMouseLeave={e => {
      e.currentTarget.style.background = 'transparent';
      e.currentTarget.style.color = 'var(--ce-text-4)';
    }}>{isExpanded ? '▾' : '▸'}</span> : <span style={{
      width: '14px',
      flexShrink: 0
    }} />}
          {renderIcon(node.icon, node.color)}
          <span style={{
      flex: 1,
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      whiteSpace: 'nowrap'
    }}>{node.label}</span>
          {node.badge && BADGE_STYLES[node.badge] && <span title={BADGE_STYLES[node.badge].label} style={{
      width: 6,
      height: 6,
      borderRadius: '50%',
      background: BADGE_STYLES[node.badge].color,
      flexShrink: 0,
      opacity: 0.7
    }} />}
        </button>
        {isFolder && isExpanded && node.children && <div role="group">{node.children.map(child => renderNode(child, depth + 1))}</div>}
      </div>;
  };
  return <>
    <style>{`
      .ce-root {
        --ce-mono: var(--font-mono, ui-monospace, monospace);
        --ce-accent: #D97757;
        --ce-accent-bg: rgba(217,119,87,0.06);
        --ce-accent-border: rgba(217,119,87,0.12);
        --ce-bg: #fff;
        --ce-surface: #FAFAF7;
        --ce-surface-hover: #F0EEE6;
        --ce-border: #E8E6DC;
        --ce-border-subtle: #F0EEE6;
        --ce-text: #141413;
        --ce-text-2: #5E5D59;
        --ce-text-3: #73726C;
        --ce-text-4: #9C9A92;
        --ce-text-5: #B8B6AE;
        --ce-sep: #D1CFC5;
        --ce-code-header: #F5F4ED;
        --ce-code-bg: #1A1918;
        --ce-arrow-hover: rgba(0,0,0,0.08);
        --ce-badge-committed: #3d6b2e;
        --ce-badge-gitignored: #b85c3a;
        --ce-badge-local: #5e5d59;
        --ce-badge-autogen: #b07520;
        --ce-when-text: #4a7fb5;
      }
      .dark .ce-root {
        --ce-bg: #1a1918;
        --ce-surface: #232221;
        --ce-surface-hover: #2e2d2b;
        --ce-border: #3a3936;
        --ce-border-subtle: #2e2d2b;
        --ce-text: #e8e6dc;
        --ce-text-2: #c4c2b8;
        --ce-text-3: #9c9a92;
        --ce-text-4: #73726c;
        --ce-text-5: #5e5d59;
        --ce-sep: #4a4946;
        --ce-code-header: #2e2d2b;
        --ce-code-bg: #0d0d0c;
        --ce-arrow-hover: rgba(255,255,255,0.08);
        --ce-badge-committed: #6fa85c;
        --ce-badge-gitignored: #e08a60;
        --ce-badge-local: #9c9a92;
        --ce-badge-autogen: #e8a45c;
        --ce-when-text: #8bb4e0;
      }
      .ce-mobile-fallback { display: none; border: 1px solid rgba(0,0,0,0.1); background: rgba(0,0,0,0.03); }
      .dark .ce-mobile-fallback { border-color: rgba(255,255,255,0.15); background: rgba(255,255,255,0.04); }
      @media (max-width: 700px) {
        .ce-root:not(.ce-force) { display: none !important; }
        .ce-mobile-fallback { display: block; }
      }
    `}</style>
    {!forceMobile && <div className="ce-mobile-fallback" style={{
    padding: '14px 16px',
    borderRadius: '8px',
    fontSize: '14px'
  }}>
      The interactive explorer works best on a larger screen. See the <a href="#file-reference" style={{
    color: '#D97757'
  }}>file reference table</a> below, or <button onClick={() => setForceMobile(true)} style={{
    border: 'none',
    background: 'none',
    padding: 0,
    color: '#D97757',
    textDecoration: 'underline',
    cursor: 'pointer',
    font: 'inherit'
  }}>show the explorer anyway</button>.
    </div>}
    <div ref={rootRef} className={forceMobile ? 'ce-root ce-force' : 'ce-root'} style={{
    borderRadius: isFullscreen ? 0 : '12px',
    border: '1px solid var(--ce-border)',
    background: 'var(--ce-bg)',
    display: 'flex',
    alignItems: 'stretch',
    overflow: 'hidden',
    fontFamily: 'var(--font-sans, -apple-system, sans-serif)',
    ...isFullscreen && ({
      height: '100vh'
    })
  }}>
      {}
      <div style={{
    width: 'min(240px, 35%)',
    minWidth: '180px',
    flexShrink: 0,
    borderRight: '1px solid var(--ce-border-subtle)',
    background: 'var(--ce-surface)',
    display: 'flex',
    flexDirection: 'column'
  }}>
        <div style={{
    padding: '8px 8px 4px',
    borderBottom: '1px solid var(--ce-border-subtle)',
    display: 'flex',
    gap: '4px'
  }}>
          {['project', 'global'].map(root => <button key={root} onClick={() => switchRoot(root)} style={{
    flex: 1,
    padding: '6px 0',
    borderRadius: '6px',
    border: 'none',
    cursor: 'pointer',
    fontFamily: 'var(--ce-mono)',
    fontSize: '11.5px',
    background: activeRoot === root ? 'var(--ce-accent-bg)' : 'transparent',
    color: activeRoot === root ? 'var(--ce-accent)' : 'var(--ce-text-4)',
    fontWeight: activeRoot === root ? 600 : 430
  }}>
              {root === 'project' ? 'Project' : 'Global (~/)'}
            </button>)}
          <button onClick={toggleAllFolders} title={allExpanded ? 'Collapse all' : 'Expand all'} style={{
    ...iconBtn,
    fontSize: 11
  }}>
            {allExpanded ? '⊟' : '⊞'}
          </button>
          <button onClick={toggleFullscreen} title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'} style={{
    ...iconBtn,
    fontSize: 13
  }}>
            {isFullscreen ? '⤡' : '⛶'}
          </button>
        </div>
        <div role="tree" aria-label="Configuration files" tabIndex={0} onKeyDown={onTreeKeyDown} style={{
    padding: '6px 0',
    overflowY: 'auto',
    flex: 1,
    outline: 'none'
  }}>
          {tree.children.map(node => renderNode(node, 0))}
        </div>
      </div>

      {}
      <div style={{
    flex: 1,
    minWidth: 0,
    padding: '20px 24px',
    minHeight: '400px',
    overflowY: 'auto'
  }}>
            <span aria-live="polite" style={{
    position: 'absolute',
    width: 1,
    height: 1,
    overflow: 'hidden',
    clip: 'rect(0 0 0 0)'
  }}>{selected.label} selected</span>
            {}
            <div style={{
    fontFamily: 'var(--ce-mono)',
    fontSize: '11px',
    color: 'var(--ce-text-4)',
    marginBottom: '10px',
    cursor: 'default'
  }}>
              {selected.path.map((seg, i) => <span key={i}>
                  <span style={{
    color: i === selected.path.length - 1 ? 'var(--ce-accent)' : 'var(--ce-text-4)'
  }}>{seg.replace(/\/$/, '')}</span>
                  {i < selected.path.length - 1 && <span style={{
    color: 'var(--ce-sep)'
  }}> / </span>}
                </span>)}
            </div>

            {}
            <div style={{
    display: 'flex',
    alignItems: 'flex-start',
    gap: '10px',
    marginBottom: '10px'
  }}>
              <span style={{
    flexShrink: 0,
    display: 'flex'
  }}>{renderIcon(selected.icon, selected.color, 24)}</span>
              <div style={{
    flex: 1,
    minWidth: 0
  }}>
                <div style={{
    fontSize: '22px',
    fontWeight: 600,
    color: 'var(--ce-text)',
    letterSpacing: '-0.3px',
    lineHeight: '26px'
  }}>{selected.label}</div>
                {selected.oneLiner && <div style={{
    fontSize: '15px',
    color: 'var(--ce-text-3)',
    marginTop: '3px'
  }}>{selected.oneLiner}</div>}
              </div>
              <div style={{
    display: 'flex',
    gap: '4px',
    flexShrink: 0
  }}>
                {[selected.autogen && 'autogen', selected.badge].filter(Boolean).map(k => {
    const s = BADGE_STYLES[k];
    if (!s) return null;
    return <span key={k} style={{
      fontFamily: 'var(--ce-mono)',
      fontSize: '10px',
      fontWeight: 600,
      textTransform: 'uppercase',
      letterSpacing: '0.3px',
      padding: '2px 6px',
      borderRadius: '4px',
      background: s.bg,
      color: s.color,
      border: `0.5px solid ${s.border}`
    }}>{s.label}</span>;
  })}
              </div>
            </div>

            {}
            {selected.note && <div style={{
    padding: '10px 12px',
    borderRadius: '8px',
    marginBottom: '14px',
    background: 'rgba(217,119,87,0.06)',
    border: '1px solid rgba(217,119,87,0.2)',
    borderLeft: '3px solid var(--ce-accent)',
    fontSize: '15px',
    color: 'var(--ce-text-2)',
    lineHeight: 1.6
  }}>
                {selected.note}
              </div>}

            {}
            {selected.when && <div style={{
    padding: '8px 12px',
    borderRadius: '6px',
    background: 'rgba(106,155,204,0.06)',
    border: '0.5px solid rgba(106,155,204,0.12)',
    fontSize: '15px',
    color: 'var(--ce-when-text)',
    marginBottom: '16px'
  }}>
                <div style={{
    fontSize: '10px',
    fontWeight: 700,
    textTransform: 'uppercase',
    letterSpacing: '0.4px',
    opacity: 0.65,
    marginBottom: '3px'
  }}>When it loads</div>
                <div style={{
    fontWeight: 500
  }}>{selected.when}</div>
              </div>}

            {}
            {selected.description && <div style={{
    fontSize: '16px',
    color: 'var(--ce-text-2)',
    lineHeight: 1.65,
    marginBottom: '16px'
  }}>
                {Array.isArray(selected.description) ? selected.description.map((para, i) => <div key={i} style={{
    marginBottom: i < selected.description.length - 1 ? '12px' : 0
  }}>{para}</div>) : selected.description}
              </div>}

            {}
            {selected.contains && selected.contains.length > 0 && <div style={{
    marginBottom: '16px'
  }}>
                <div style={{
    fontSize: '11px',
    fontWeight: 700,
    color: 'var(--ce-text-4)',
    textTransform: 'uppercase',
    letterSpacing: '0.4px',
    marginBottom: '8px'
  }}>Common keys</div>
                {selected.contains.map((item, i) => <div key={i} style={{
    display: 'flex',
    gap: '7px',
    fontSize: '15px',
    color: 'var(--ce-text-2)',
    lineHeight: 1.5,
    marginBottom: '5px'
  }}>
                    <span style={{
    fontSize: '7px',
    color: 'var(--ce-text-4)',
    marginTop: '6px'
  }}>●</span>
                    <span>{item}</span>
                  </div>)}
              </div>}

            {}
            {selected.tips && selected.tips.length > 0 && <div style={{
    padding: '12px 14px',
    borderRadius: '8px',
    background: 'var(--ce-surface)',
    border: '1px solid var(--ce-border-subtle)',
    marginBottom: '16px'
  }}>
                <div style={{
    fontSize: '11px',
    fontWeight: 700,
    color: 'var(--ce-accent)',
    textTransform: 'uppercase',
    letterSpacing: '0.4px',
    marginBottom: '6px'
  }}>Tips</div>
                {selected.tips.map((tip, i) => <div key={i} style={{
    display: 'flex',
    gap: '7px',
    fontSize: '14.5px',
    color: 'var(--ce-text-2)',
    marginBottom: i < selected.tips.length - 1 ? '5px' : 0
  }}>
                    <span style={{
    fontSize: '7px',
    color: 'var(--ce-accent)',
    marginTop: '6px'
  }}>●</span>
                    <span>{tip}</span>
                  </div>)}
              </div>}

            {}
            {selected.example && <div style={{
    marginBottom: '16px'
  }}>
                {selected.exampleIntro && <div style={{
    fontSize: '15px',
    color: 'var(--ce-text-2)',
    lineHeight: 1.6,
    marginBottom: '10px'
  }}>
                    {selected.exampleIntro}
                  </div>}
                <div style={{
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '6px 10px',
    background: 'var(--ce-code-header)',
    border: '1px solid var(--ce-border)',
    borderRadius: '8px 8px 0 0'
  }}>
                  <span style={{
    fontFamily: 'var(--ce-mono)',
    fontSize: '11px',
    fontWeight: 600,
    color: 'var(--ce-text-3)'
  }}>{selected.label}</span>
                  <button onClick={() => copyExample(selected.id, selected.example)} style={{
    padding: '3px 8px',
    borderRadius: '4px',
    fontSize: '11px',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'all 0.15s',
    background: isCopied ? 'rgba(85,138,66,0.08)' : 'var(--ce-code-header)',
    border: isCopied ? '0.5px solid rgba(85,138,66,0.2)' : '0.5px solid var(--ce-border)',
    color: isCopied ? '#558A42' : 'var(--ce-text-3)'
  }}>
                    {isCopied ? '✓ Copied' : 'Copy'}
                  </button>
                </div>
                <pre style={{
    margin: 0,
    padding: '12px 14px',
    background: 'var(--ce-code-bg)',
    color: '#E8E6DC',
    fontFamily: 'var(--ce-mono)',
    fontSize: '13px',
    lineHeight: 1.65,
    borderRadius: '0 0 8px 8px',
    overflowX: 'auto',
    whiteSpace: 'pre'
  }}>{selected.example}</pre>
              </div>}

            {}
            {selected.docsLink && <a href={selected.docsLink} style={{
    display: 'inline-flex',
    padding: '5px 12px',
    borderRadius: '6px',
    background: 'var(--ce-accent-bg)',
    border: '1px solid var(--ce-accent-border)',
    color: 'var(--ce-accent)',
    fontSize: '12px',
    fontWeight: 600,
    textDecoration: 'none'
  }}>Full docs →</a>}

            {}
            {selected.children && selected.children.length > 0 && <div style={{
    marginTop: '20px'
  }}>
                <div style={{
    fontSize: '11px',
    fontWeight: 700,
    color: 'var(--ce-text-4)',
    textTransform: 'uppercase',
    letterSpacing: '0.4px',
    marginBottom: '8px'
  }}>Contents</div>
                <div style={{
    display: 'flex',
    flexDirection: 'column',
    gap: '4px'
  }}>
                  {selected.children.map(child => <button key={child.id} onClick={() => selectNode(child)} style={{
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '6px 8px',
    width: '100%',
    background: 'var(--ce-surface)',
    borderRadius: '6px',
    border: 'none',
    cursor: 'pointer',
    textAlign: 'left',
    transition: 'background 0.1s'
  }} onMouseEnter={e => e.currentTarget.style.background = 'var(--ce-surface-hover)'} onMouseLeave={e => e.currentTarget.style.background = 'var(--ce-surface)'}>
                      {renderIcon(child.icon, child.color, 13)}
                      <span style={{
    fontFamily: 'var(--ce-mono)',
    fontSize: '12px',
    color: 'var(--ce-text-2)'
  }}>{child.label}</span>
                      {child.oneLiner && <span style={{
    fontSize: '11px',
    color: 'var(--ce-text-4)',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap'
  }}>{child.oneLiner}</span>}
                    </button>)}
                </div>
              </div>}
      </div>
    </div>
    </>;
};

Claude Code는 프로젝트 디렉토리와 홈 디렉토리의 `~/.claude`에서 지침, 설정, skills, subagents, 메모리를 읽습니다. 프로젝트 파일을 git에 커밋하여 팀과 공유합니다. `~/.claude`의 파일은 모든 프로젝트에 적용되는 개인 설정입니다.

Windows에서 `~/.claude`는 `%USERPROFILE%\.claude`로 확인됩니다. [`CLAUDE_CONFIG_DIR`](/docs/ko/env-vars)을 설정하면, 이 페이지의 모든 `~/.claude` 경로가 대신 해당 디렉토리 아래에 있습니다.

대부분의 사용자는 `CLAUDE.md`와 `settings.json`만 편집합니다. 리포지토리에 이미 다른 코딩 에이전트용 `AGENTS.md`가 있는 경우, Claude Code는 [자체적으로 또는 `CLAUDE.md`와 함께 읽을 수 있습니다](/docs/ko/memory#agents-md). 디렉토리의 나머지는 선택 사항입니다. 필요에 따라 skills, rules, subagents를 추가합니다.

<h2 id="explore-the-directory">
  디렉토리 탐색
</h2>

트리의 파일을 클릭하여 각 파일이 무엇을 하는지, 언제 로드되는지, 예제를 확인합니다.

<ClaudeExplorer />

<h2 id="what’s-not-shown">
  표시되지 않는 항목
</h2>

탐색기는 작성하고 편집하는 파일을 다룹니다. 관련된 몇 가지 파일은 다른 위치에 있습니다.

| 파일                      | 위치                              | 목적                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ----------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `managed-settings.json` | 시스템 수준, OS에 따라 다름               | 재정의할 수 없는 엔터프라이즈 강제 설정입니다. [좁은 예외](/docs/ko/settings#security-keys-where-the-stricter-value-applies)를 제외하고는 재정의할 수 없습니다. [파일을 저장할 위치](/docs/ko/managed-settings#deploy-a-managed-settings-file) 및 [Claude Code가 사용하는 관리되는 소스](/docs/ko/managed-settings#precedence-within-the-managed-tier)를 참조하세요.                                                                                                                                                                                                                                                                                                                                                         |
| `CLAUDE.local.md`       | 프로젝트 루트                         | 이 프로젝트에 대한 개인 기본 설정으로, CLAUDE.md와 함께 로드됩니다. 수동으로 생성하고 `.gitignore`에 추가합니다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `AGENTS.md`             | 프로젝트 루트, `.claude/`, 또는 모든 디렉터리 | AI 코딩 에이전트를 위해 작성하는 프로젝트 지침입니다. Claude Code는 [이를 로드](/docs/ko/memory#agents-md)할 수 있으며, `CLAUDE.md`와 함께 로드할 수도 있습니다.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 설치된 플러그인                | `~/.claude/plugins`             | 복제된 마켓플레이스, 설치된 플러그인 버전, `installed_plugins.json` 설치 기록, 플러그인별 데이터로, `claude plugin` 명령으로 관리됩니다. [claude.ai 계정에서 동기화된](/docs/ko/plugins-reference#synced-plugins) 플러그인은 `~/.claude/plugins/synced/`로 다운로드됩니다. 마켓플레이스 [`command` 소스](/docs/ko/plugin-marketplaces#command-sources)에서 링크 모드로 설치된 플러그인의 경우, Claude Code는 복사본 대신 여기에 링크를 저장하고, 플러그인의 파일은 명령이 출력하는 디렉터리에 남아 있습니다. `command` 소스는 Claude Code v2.1.229 이상이 필요합니다. 로컬 디렉터리 마켓플레이스에서 상대 경로로 나열된 플러그인도 캐시 복사본이 아닌 소스 디렉터리에서 [제자리에 로드](/docs/ko/plugins-reference#plugin-caching-and-file-resolution)됩니다. [플러그인 캐싱](/docs/ko/plugins-reference#plugin-caching-and-file-resolution)에서 고아 버전이 정리되는 방식을 참조하세요. |

`~/.claude`는 또한 작업할 때 Claude Code가 작성하는 데이터를 보유합니다. 트랜스크립트, 프롬프트 기록, 파일 스냅샷, 캐시, 로그입니다. 아래의 [애플리케이션 데이터](#application-data)를 참조하세요.

<h2 id="choose-the-right-file">
  올바른 파일 선택
</h2>

다양한 종류의 사용자 정의는 다양한 파일에 있습니다. 이 표를 사용하여 변경 사항이 어디에 속하는지 찾습니다.

| 원하는 작업                       | 편집                                       | 범위         | 참조                                        |
| :--------------------------- | :--------------------------------------- | :--------- | :---------------------------------------- |
| Claude에 프로젝트 컨텍스트 및 규칙 제공    | `CLAUDE.md`                              | 프로젝트 또는 전역 | [메모리](/docs/ko/memory)                         |
| 특정 도구 호출 허용 또는 차단            | `settings.json` `permissions` 또는 `hooks` | 프로젝트 또는 전역 | [권한](/docs/ko/permissions), [Hooks](/docs/ko/hooks) |
| 도구 호출 전후에 스크립트 실행            | `settings.json` `hooks`                  | 프로젝트 또는 전역 | [Hooks](/docs/ko/hooks)                        |
| 세션에 대한 환경 변수 설정              | `settings.json` `env`                    | 프로젝트 또는 전역 | [설정](/docs/ko/settings-reference#all-settings) |
| 개인 재정의를 git에서 제외             | `settings.local.json`                    | 프로젝트만      | [설정 범위](/docs/ko/settings#where-settings-live) |
| `/name`으로 호출하는 프롬프트 또는 기능 추가 | `skills/<name>/SKILL.md`                 | 프로젝트 또는 전역 | [Skills](/docs/ko/skills)                      |
| 자신의 도구가 있는 특화된 subagent 정의   | `agents/*.md`                            | 프로젝트 또는 전역 | [Subagents](/docs/ko/sub-agents)               |
| 스크립트에서 많은 subagent 조율        | `workflows/*.js`                         | 프로젝트 또는 전역 | [동적 워크플로우](/docs/ko/workflows)                 |
| MCP를 통해 외부 도구 연결             | `.mcp.json`                              | 프로젝트만      | [MCP](/docs/ko/mcp)                            |
| Claude가 응답을 포맷하는 방식 변경       | `output-styles/*.md`                     | 프로젝트 또는 전역 | [출력 스타일](/docs/ko/output-styles)               |

<h2 id="file-reference">
  파일 참조
</h2>

이 표는 탐색기가 다루는 모든 파일을 나열합니다. 프로젝트 범위 파일은 `.claude/` 아래의 리포지토리에 있습니다 (또는 `CLAUDE.md`, `.mcp.json`, `.worktreeinclude`의 경우 루트에 있음). 전역 범위 파일은 `~/.claude/`에 있으며 모든 프로젝트에 적용됩니다.

<Note>
  이 파일에 입력한 내용을 재정의할 수 있는 여러 가지가 있습니다.

  * 조직에서 배포한 [관리 설정](/docs/ko/server-managed-settings)이 모든 것보다 우선합니다. [설정 우선순위의 예외](/docs/ko/settings#exceptions-to-managed-settings-precedence) 제외
  * `--permission-mode` 또는 `--settings`와 같은 CLI 플래그는 해당 세션에 대해 `settings.json`을 재정의합니다.
  * 일부 환경 변수는 동등한 설정보다 우선하지만, 이는 다양합니다. 각각에 대해 [환경 변수 참조](/docs/ko/env-vars)를 확인하세요.

  전체 순서는 [설정 우선순위](/docs/ko/settings#settings-precedence)를 참조하세요.
</Note>

파일 이름을 클릭하여 위의 탐색기에서 해당 노드를 엽니다.

| 파일                                                  | 범위        | 커밋 | 기능                                                                      | 참조                                                              |
| --------------------------------------------------- | --------- | -- | ----------------------------------------------------------------------- | --------------------------------------------------------------- |
| [`CLAUDE.md`](#ce-claude-md)                        | 프로젝트 및 전역 | ✓  | 매 세션마다 로드되는 지침                                                          | [메모리](/docs/ko/memory)                                               |
| [`rules/*.md`](#ce-rules)                           | 프로젝트 및 전역 | ✓  | 주제 범위 지침, 선택적으로 경로 제한                                                   | [규칙](/docs/ko/memory#organize-rules-with-claude/rules/)              |
| [`settings.json`](#ce-settings-json)                | 프로젝트 및 전역 | ✓  | 권한, hooks, 환경 변수, 모델 기본값                                                | [설정](/docs/ko/settings)                                              |
| [`settings.local.json`](#ce-settings-local-json)    | 프로젝트만     |    | 개인 재정의, Claude Code가 설정을 저장할 때 gitignored                               | [설정 범위](/docs/ko/settings#where-settings-live)                       |
| [`.mcp.json`](#ce-mcp-json)                         | 프로젝트만     | ✓  | 팀 공유 MCP 서버                                                             | [MCP 범위](/docs/ko/mcp#mcp-installation-scopes)                       |
| [`.worktreeinclude`](#ce-worktreeinclude)           | 프로젝트만     | ✓  | 새 worktrees로 복사할 Gitignored 파일                                          | [Worktrees](/docs/ko/worktrees#copy-gitignored-files-into-worktrees) |
| [`skills/<name>/SKILL.md`](#ce-skills)              | 프로젝트 및 전역 | ✓  | `/name`으로 호출되거나 자동 호출되는 재사용 가능한 프롬프트                                    | [Skills](/docs/ko/skills)                                            |
| [`commands/*.md`](#ce-commands)                     | 프로젝트 및 전역 | ✓  | 단일 파일 프롬프트; skills와 동일한 메커니즘                                            | [Skills](/docs/ko/skills)                                            |
| [`output-styles/*.md`](#ce-output-styles)           | 프로젝트 및 전역 | ✓  | Claude의 작동 방식을 조정하는 사용자 정의 지침 세트                                        | [출력 스타일](/docs/ko/output-styles)                                     |
| [`agents/*.md`](#ce-agents)                         | 프로젝트 및 전역 | ✓  | 자신의 프롬프트와 도구가 있는 subagent 정의                                            | [Subagents](/docs/ko/sub-agents)                                     |
| [`workflows/*.js`](#ce-workflows)                   | 프로젝트 및 전역 | ✓  | Claude가 작성하고 `/workflows`에서 저장한 동적 워크플로우 스크립트; 각 파일은 `/<name>` 명령어가 됩니다 | [동적 워크플로우](/docs/ko/workflows)                                       |
| [`agent-memory/<name>/`](#ce-agent-memory)          | 프로젝트 및 전역 | ✓  | Subagents의 지속적 메모리                                                      | [지속적 메모리](/docs/ko/sub-agents#enable-persistent-memory)              |
| [`~/.claude.json`](#ce-claude-json)                 | 전역만       |    | 앱 상태, OAuth, UI 토글, 개인 MCP 서버                                           | [전역 설정](/docs/ko/settings-reference#global-config-settings)          |
| [`projects/<project>/memory/`](#ce-global-projects) | 전역만       |    | 자동 메모리: Claude의 세션 간 자체 메모                                              | [자동 메모리](/docs/ko/memory#auto-memory)                                |
| [`keybindings.json`](#ce-keybindings)               | 전역만       |    | 사용자 정의 키보드 단축키                                                          | [키바인딩](/docs/ko/keybindings)                                         |
| [`themes/*.json`](#ce-themes)                       | 전역만       |    | 사용자 정의 색상 테마                                                            | [사용자 정의 테마](/docs/ko/terminal-config#create-a-custom-theme)          |

<h2 id="frontmatter-fields-by-file">
  파일별 프론트매터 필드
</h2>

Skills, command 파일, subagents, output styles, 그리고 rules는 파일 상단의 YAML [프론트매터](/docs/ko/glossary#frontmatter)에서 구성을 읽으며, 각각은 자신의 필드 집합을 허용합니다. 이 표는 각 파일의 필드 이름을 나열하고 이들을 설명하는 참조로 연결합니다.

| 파일                       | 프론트매터 필드                                                                                                                                                                                                                                                                      | 참조                                                            |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `skills/<name>/SKILL.md` | `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility` | [Skill 프론트매터](/docs/ko/skills#frontmatter-reference)               |
| `commands/*.md`          | `name`과 `paths`를 제외한 skill 필드                                                                                                                                                                                                                                                 | [Skill 프론트매터](/docs/ko/skills#frontmatter-reference)               |
| `agents/*.md`            | `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, `color`, `initialPrompt`, `omitClaudeMd`, `experimental`                                            | [Subagent 프론트매터](/docs/ko/sub-agents#supported-frontmatter-fields) |
| `output-styles/*.md`     | `name`, `description`, `keep-coding-instructions`, `force-for-plugin`                                                                                                                                                                                                         | [Output style 프론트매터](/docs/ko/output-styles#frontmatter)           |
| `rules/*.md`             | `paths`                                                                                                                                                                                                                                                                       | [Rule 프론트매터](/docs/ko/memory#rules-frontmatter-reference)          |

[플러그인](/docs/ko/plugins-reference#plugin-agent-frontmatter)에서 제공되는 Agents는 subagent 필드의 부분 집합을 준수합니다.

<h2 id="troubleshoot-configuration">
  설정 문제 해결
</h2>

설정, hook, 파일이 적용되지 않으면, [설정 디버그](/docs/ko/debug-your-config)에서 검사 명령과 증상 우선 조회 표를 참조하세요.

<h2 id="application-data">
  애플리케이션 데이터
</h2>

작성한 설정 외에도 `~/.claude`에는 Claude Code가 세션 중에 작성하는 데이터가 저장됩니다. 이 파일들은 평문입니다. 도구를 통과하는 모든 것은 디스크의 트랜스크립트에 기록됩니다: 파일 내용, 명령 출력, 붙여넣은 텍스트.

<h3 id="cleaned-up-automatically">
  자동으로 정리됨
</h3>

Claude Code는 [`cleanupPeriodDays`](/docs/ko/settings-reference#cleanupperioddays)보다 오래된 아래 경로의 파일들을 삭제합니다. 보존 기간을 안전하게 결정할 수 있는 한 말입니다. 기본값은 30일이고 최소값은 1입니다. `0`으로 설정하면 유효성 검사 오류가 발생합니다. 동일한 나이 기준이 [고아 worktrees의 자동 제거](/docs/ko/worktrees#clean-up-subagent-and-background-session-worktrees)에도 적용됩니다.

| `~/.claude/` 아래 경로                                                                                                              | 내용                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `projects/<project>/<session>.jsonl`                                                                                            | 전체 대화 트랜스크립트: 모든 메시지, 도구 호출 및 도구 결과                                                                                                                                                                                         |
| `projects/<project>/<session>.orphaned-<timestamp>-<suffix>.jsonl`, `projects/<project>/<session>.jsonl.superseded-<timestamp>` | Claude Code가 덮어쓰거나 삭제하는 대신 따로 보관한 세션의 이전 트랜스크립트입니다. 세션 선택기에 나타나지 않습니다                                                                                                                                                       |
| `projects/<project>/<session>/subagents/`                                                                                       | [Subagent](/docs/ko/sub-agents) 대화 트랜스크립트, 상위 세션 트랜스크립트가 오래되면 함께 제거됨                                                                                                                                                             |
| `projects/<project>/<session>/tool-results/`                                                                                    | 별도 파일로 유출된 대형 도구 출력                                                                                                                                                                                                         |
| `file-history/<session>/`                                                                                                       | Claude Code가 변경한 파일의 편집 전 스냅샷, [checkpoint 복원](/docs/ko/checkpointing)에 사용됨. 가장 최근의 100개 checkpoint에 대한 스냅샷을 보유합니다. 보존된 checkpoint가 참조하지 않는 스냅샷 파일은 각 파일의 첫 번째 스냅샷을 제외하고 삭제됩니다                                                   |
| `plans/`                                                                                                                        | [plan mode](/docs/ko/permission-modes#analyze-before-you-edit-with-plan-mode) 중에 작성된 Plan 파일                                                                                                                                     |
| `debug/`                                                                                                                        | 세션별 디버그 로그, 디버그 로깅이 켜져 있을 때 작성됨. 예를 들어 [`--debug`](/docs/ko/cli-reference#cli-flags)로 시작하거나 `/debug`를 실행할 때                                                                                                                      |
| `paste-cache/`                                                                                                                  | 대형 붙여넣기의 내용                                                                                                                                                                                                                 |
| `image-cache/<session>/`                                                                                                        | Claude Code v2.1.274 이전 버전에서 저장한 첨부 이미지입니다. 이후 버전은 붙여넣은 이미지와 첨부 이미지를 `~/.claude` 외부에 저장하며, [`CLAUDE_CODE_TMPDIR`](/docs/ko/env-vars)이 제어하는 임시 디렉토리 아래 각 세션에 대한 `images/` 디렉토리에 저장합니다. 스윕은 나이에 관계없이 여기에 있는 다른 세션의 남은 디렉토리를 제거합니다. |
| `uploads/<session>/`                                                                                                            | 웹 또는 모바일 앱에서 첨부한 파일 및 모바일 앱에서 첨부한 사진. [Remote Control](/docs/ko/remote-control) 세션에 메시지를 보낼 때입니다. [cloud session](/docs/ko/claude-code-on-the-web)에 대한 첨부는 대신 해당 세션의 자체 클라우드 환경에 저장되며, 사용자의 머신에는 저장되지 않습니다.                           |
| `session-env/`                                                                                                                  | 세션별 환경 메타데이터                                                                                                                                                                                                                |
| `tasks/`                                                                                                                        | 작업 도구로 작성된 작업 목록, 목록당 하나의 디렉토리                                                                                                                                                                                              |
| `shell-snapshots/`                                                                                                              | 시작 시 캡처된 별칭, 함수 및 셸 옵션. [Bash tool](/docs/ko/tools-reference#bash-tool-behavior)에 의해 각 명령에 적용됩니다. 정상 종료 시 제거됩니다. 스윕은 충돌 후 남은 것을 정리합니다.                                                                                           |
| `backups/`                                                                                                                      | `~/.claude.json`의 이전 버전, Claude Code가 파일을 다시 쓸 때 복사됨. Claude Code는 가장 최신 5개와 구문 분석할 수 없는 모든 버전의 복사본을 유지합니다.                                                                                                                 |
| `feedback-bundles/`                                                                                                             | `/feedback`에 의해 작성된 수정된 트랜스크립트 아카이브. 타사 제공자에게 또는 Anthropic 자격증명이 구성되지 않았을 때 Anthropic 계정 팀에 보내기 위해                                                                                                                          |
| `feedback/drafts/`                                                                                                              | 대기 중인 [Claude 작성 피드백](/docs/ko/tools-reference#sendfeedback-tool-behavior). `/feedback`에서 검토 대기 중입니다. `cleanupPeriodDays` 또는 30일 후 스윕됨. 큐가 10개 초안 제한에 도달하면 Claude Code는 가장 오래된 초안을 삭제하여 공간을 확보합니다.                               |
| `usage-data/`                                                                                                                   | `report.html` 및 [`/insights`](/docs/ko/costs#analyze-your-usage-patterns)에 의해 작성된 타임스탬프 보고서 복사본, 그리고 이를 구축하는 데 사용되는 캐시된 세션별 분석 데이터                                                                                               |
| `skills/.trash/`, `plugins/.trash/`                                                                                             | [Skills](/docs/ko/skills#how-synced-skills-behave) 및 [plugins](/docs/ko/plugins-reference#synced-plugins). claude.ai 동기화가 제거한 것. 예를 들어 claude.ai에서 하나를 끄거나 동기화를 중지한 후. 파일은 스윕이 삭제할 때까지 복구할 수 있도록 여기에 남아 있습니다                          |
| `todos/`, `statsig/`, `logs/`                                                                                                   | 이전 버전의 레거시 디렉토리입니다. 더 이상 작성되지 않습니다. 스윕은 내용을 제거한 다음 빈 디렉토리를 제거합니다.                                                                                                                                                           |

`sessions/`의 세션 파일, 자동 메모리, Claude Desktop 및 Cowork 트랜스크립트는 각각 자체 보존 규칙을 따릅니다:

* **`sessions/`**: 실행 중인 각 세션에 대해 하나의 작은 파일을 보유합니다. 동시 세션 및 충돌을 감지하는 데 사용됩니다. 나이 기반 스윕의 일부가 아닙니다: Claude Code는 세션이 종료될 때 각 파일을 제거하고 다음 시작 시 충돌 남은 것을 정리합니다.
* **자동 메모리**: 스윕은 프로젝트의 [자동 메모리](/docs/ko/memory#auto-memory) 디렉토리 `projects/<project>/memory/`의 메모리 파일을 삭제하지 않습니다. Claude Code는 전체 보존 기간 동안 비어 있었던 경우에만 해당 디렉토리를 제거합니다. v2.1.228 이전에는 스윕이 메모리 디렉토리 내의 폴더를 세션 데이터로 취급하고 그 아래의 오래된 파일을 삭제할 수 있었습니다.
* **Claude Desktop 및 Cowork 트랜스크립트**: Claude Code는 Claude Desktop 또는 Cowork에서 시작하거나 가장 최근에 계속한 세션의 트랜스크립트를 모든 나이에서 유지합니다. 이 트랜스크립트에 나이 제한을 주려면 [`desktopSessionCleanupPeriodDays`](/docs/ko/settings-reference#desktopsessioncleanupperioddays)를 설정하세요. [관리 설정](/docs/ko/managed-settings)이 `cleanupPeriodDays`를 설정하면 Claude Code는 대신 해당 기간 후에 이 트랜스크립트를 삭제합니다. Claude Code v2.1.248 이상 필요; 이전 버전은 `cleanupPeriodDays` 후에 삭제합니다.

Claude Code는 다음 경우에 나이 기반 스윕을 건너뜁니다:

* **Bare mode**: [`--bare`](/docs/ko/headless#start-faster-with-bare-mode)로 `claude -p`를 실행할 때, Claude Code는 해당 세션에서 스윕을 실행하지 않습니다.
* **일시 중지된 스윕**: Claude Code가 보존 기간을 안전하게 결정할 수 없으면 보존 정리 스윕을 일시 중지합니다. [`retention_sweep` 이벤트](/docs/ko/monitoring-usage#retention-sweep-event)는 이를 일시 중지하는 각 구성을 나열합니다. 원인이 읽거나 구문 분석할 수 없는 설정 파일이거나 `cleanupPeriodDays` 또는 `desktopSessionCleanupPeriodDays`가 명시적으로 설정된 설정 오류인 경우, Claude Code는 설정 오류를 수정할 때까지 `/status`에 경고를 표시합니다. [관리 설정](/docs/ko/server-managed-settings)이 `cleanupPeriodDays`를 제공하면 Claude Code는 어느 경우든 관리 값에서 스윕을 실행합니다.

<h3 id="kept-until-you-delete-them">
  삭제할 때까지 유지됨
</h3>

보존 정리 스윕은 아래 경로를 제거하지 않습니다. Claude Code는 삭제할 때까지 유지합니다. 단, 로그아웃할 때 삭제하는 두 개의 캐시는 제외합니다.

| `~/.claude/` 아래 경로     | 내용                                                                                                                                                                                                                               |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `history.jsonl`        | 입력한 모든 프롬프트, 타임스탬프 및 프로젝트 경로 포함. 위쪽 화살표 회상, `Ctrl+R` 히스토리 검색 및 `!` 셸 명령 완성에 사용됩니다.                                                                                                                                               |
| `stats-cache.json`     | `/usage`에 표시된 집계된 토큰 및 비용 수                                                                                                                                                                                                      |
| `remote-settings.json` | [서버 관리 설정](/docs/ko/server-managed-settings)의 캐시된 복사본. 조직의 경우 또는 조직이 구성하지 않은 경우 `{}`. 세션이 [이를 가져올](/docs/ko/server-managed-settings#platform-availability) 때만 존재합니다. Claude Code는 시작 시 및 세션 중 매시간 업데이트를 확인합니다. Claude Code는 로그아웃할 때 삭제합니다. |
| `cache/changelog.md`   | Claude Code 변경 로그의 캐시된 복사본, `/release-notes`에 표시됨. 백그라운드에서 새로 고쳐집니다.                                                                                                                                                             |
| `policy-limits.json`   | 조직의 캐시된 기능 정책 설정. 일부 계정 유형에만 존재합니다. 자동으로 새로 고쳐집니다. `policy-limits.json.stamp.json` 사이드카는 캐시가 속한 계정 또는 API 키를 기록합니다. Claude Code는 로그아웃할 때 두 파일을 모두 삭제합니다.                                                                         |

<span id="state-files-to-keep" />

사용하는 기능에 따라 다른 파일이 나타납니다. 캐시 및 잠금 파일은 안전하게 삭제할 수 있습니다. 이 상태 파일을 유지하세요:

* `.credentials.json`: 사용자의 [로그인 자격증명](/docs/ko/authentication#credential-management)
* `agent-memory/`: [subagent 메모리](/docs/ko/sub-agents#enable-persistent-memory)
* `jobs/` 및 `daemon/`: [background session](/docs/ko/agent-view#where-state-is-stored) 상태

<h3 id="plaintext-storage">
  평문 저장소
</h3>

트랜스크립트 및 히스토리는 저장 시 암호화되지 않습니다. OS 파일 권한만이 유일한 보호입니다. 도구가 `.env` 파일을 읽거나 명령이 자격증명을 인쇄하면 해당 값이 `projects/<project>/<session>.jsonl`에 기록됩니다. 노출을 줄이려면:

* `cleanupPeriodDays`를 낮춰 Claude Code가 트랜스크립트를 유지하는 기간을 단축하세요
* [`desktopSessionCleanupPeriodDays`](/docs/ko/settings-reference#desktopsessioncleanupperioddays)를 설정하여 Claude Desktop 및 Cowork 트랜스크립트에도 나이 제한을 주세요
* [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/docs/ko/env-vars) 환경 변수를 설정하여 모든 모드에서 트랜스크립트 및 프롬프트 히스토리 작성을 건너뛰세요. 비대화형 모드에서는 대신 `-p`와 함께 `--no-session-persistence`를 전달하거나 TypeScript Agent SDK에서 `persistSession: false`를 설정할 수 있습니다. Python SDK에는 동등한 옵션이 없습니다.
* [권한 규칙](/docs/ko/permissions)을 사용하여 자격증명 파일의 읽기를 거부하세요

<h3 id="clear-local-data">
  로컬 데이터 지우기
</h3>

`claude project purge`를 실행하여 Claude Code가 한 프로젝트에 대해 보유한 상태를 삭제합니다. 다음을 삭제합니다:

* `projects/` 아래의 트랜스크립트 및 자동 메모리
* 세션별 `tasks/`, `debug/` 및 `file-history/` 항목
* `history.jsonl`의 일치하는 프롬프트 라인
* `~/.claude.json`의 프로젝트 항목

프로젝트의 세션에서 붙여넣거나 첨부한 이미지는 `~/.claude` 대신 Claude Code의 임시 디렉토리 아래에 저장되므로 purge는 이를 제거하지 않습니다. [보존 스윕](#cleaned-up-automatically)은 `cleanupPeriodDays`보다 오래되면 삭제합니다.

명령은 전체 삭제 계획을 인쇄하고 아무것도 제거하기 전에 확인을 요청합니다.

아래 예제는 `~/work/my-repo`를 자리 표시자로 사용합니다. 프로젝트의 경로로 바꾸세요. 경로와 일치하는 상태가 없으면 명령은 오류를 인쇄하고 상태 1로 종료합니다.

아무것도 삭제하지 않고 계획 미리 보기:

```bash theme={null}
claude project purge ~/work/my-repo --dry-run
```

계획은 각 일치하는 항목과 포함된 이유를 나열합니다:

```text theme={null}
Purge plan for /home/user/work/my-repo:

  dir:    /home/user/.claude/projects/-home-user-work-my-repo
           project transcripts (.jsonl) and memory/
  config: projects["/home/user/work/my-repo"]
           project entry in ~/.claude.json (trust, history, MCP servers)
  filter: /home/user/.claude/history.jsonl
           12 prompt(s) typed in this project

shell-snapshots/ are not project-scoped and will not be touched
backups/ may still contain this project entry in old .claude.json snapshots (/home/user/.claude/backups); at most 5 are kept and they rotate out automatically
Dry run: 3 item(s) would be deleted.
```

단일 확인 프롬프트로 삭제:

```bash theme={null}
claude project purge ~/work/my-repo
```

명령은 동일한 계획을 인쇄한 다음 `Delete 3 item(s) for /home/user/work/my-repo? This cannot be undone. [y/N]`를 묻고 `y`로 답변한 경우에만 삭제합니다.

대화형 목록에서 프로젝트를 선택하려면 경로를 생략하세요.

스크립트에서 사용하기 위해 확인 프롬프트를 건너뛰세요:

```bash theme={null}
claude project purge ~/work/my-repo --yes
```

경로 대신 `--all`을 전달하여 한 번에 모든 프로젝트의 상태를 purge합니다. 이는 `history.jsonl`을 필터링하는 대신 완전히 삭제합니다. `-i`를 전달하여 삭제 계획을 한 번에 하나씩 단계별로 진행합니다.

명령은 `shell-snapshots/` 및 `backups/`를 그대로 두는데, 이는 프로젝트 범위가 아니기 때문이며 계획 출력에서 이에 대해 경고합니다.

위의 [애플리케이션 데이터 경로](#state-files-to-keep)를 제외한 모든 경로를 직접 삭제할 수도 있습니다. 새 세션은 영향을 받지 않습니다. 아래 표는 과거 세션에서 손실되는 것을 보여줍니다.

| 삭제                                                                                                                   | 손실되는 것                                                                                                                                |
| -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `~/.claude/projects/`                                                                                                | 과거 세션의 재개, 계속 및 되감기, 그리고 모든 프로젝트의 자동 메모리                                                                                              |
| `~/.claude/history.jsonl`                                                                                            | 위쪽 화살표 프롬프트 회상, `Ctrl+R` 히스토리 검색 및 `!` 셸 명령 완성                                                                                        |
| `~/.claude/paste-cache/`                                                                                             | 회상된 프롬프트의 붙여넣은 텍스트. [대형 콘텐츠 붙여넣기](/docs/ko/terminal-config#paste-large-content) 참조                                                         |
| `~/.claude/uploads/`                                                                                                 | 과거 [Remote Control](/docs/ko/remote-control) 세션이 경로로 참조하는 첨부                                                                               |
| `~/.claude/file-history/`                                                                                            | 과거 세션의 checkpoint 복원                                                                                                                  |
| `~/.claude/stats-cache.json`                                                                                         | `/usage`에 표시된 과거 합계                                                                                                                   |
| `~/.claude/usage-data/`                                                                                              | 과거 [`/insights`](/docs/ko/costs#analyze-your-usage-patterns) 보고서 및 이를 구축하는 데 사용된 캐시된 분석 데이터                                                |
| `~/.claude/feedback-bundles/`                                                                                        | Anthropic 계정 팀에 아직 보내지 않은 피드백 및 버그 보고서 아카이브                                                                                           |
| `~/.claude/feedback/drafts/`                                                                                         | 보내지 않은 [Claude 작성 피드백](/docs/ko/tools-reference#sendfeedback-tool-behavior)                                                                |
| `~/.claude/remote-settings.json`                                                                                     | 없음. 다음 시작 시 다시 가져옵니다.                                                                                                                 |
| `~/.claude/cache/changelog.md`                                                                                       | 없음. 백그라운드에서 새로 고쳐집니다.                                                                                                                 |
| `~/.claude/policy-limits.json`                                                                                       | 없음. 자동으로 새로 고쳐집니다.                                                                                                                    |
| `~/.claude/tasks/`                                                                                                   | 재개된 세션이 선택할 작업 목록                                                                                                                     |
| `~/.claude/skills/.trash/`, `~/.claude/plugins/.trash/`                                                              | [동기화된 skills](/docs/ko/skills#how-synced-skills-behave) 및 [동기화된 plugins](/docs/ko/plugins-reference#synced-plugins)를 복구할 기회. Claude Code가 제거한 것 |
| `~/.claude/debug/`, `~/.claude/plans/`, `~/.claude/session-env/`, `~/.claude/shell-snapshots/`, `~/.claude/backups/` | 사용자 대면 없음                                                                                                                             |
| `~/.claude/todos/`, `~/.claude/statsig/`, `~/.claude/logs/`, `~/.claude/image-cache/`                                | 없음. 현재 버전에서 작성되지 않는 레거시 디렉토리.                                                                                                         |

`~/.claude.json`, `~/.claude/settings.json` 또는 `~/.claude/plugins/`를 삭제하지 마세요. 이들은 인증, 기본 설정 및 설치된 plugins을 보유합니다.

<h2 id="related-resources">
  관련 리소스
</h2>

* [Claude의 메모리 관리](/docs/ko/memory): CLAUDE.md, rules, auto memory 작성 및 구성
* [설정 구성](/docs/ko/settings): 권한, hooks, 환경 변수, 모델 기본값 설정
* [Skills 생성](/docs/ko/skills): 재사용 가능한 프롬프트 및 워크플로우 구축
* [Subagents 구성](/docs/ko/sub-agents): 자신의 컨텍스트가 있는 특화된 에이전트 정의
