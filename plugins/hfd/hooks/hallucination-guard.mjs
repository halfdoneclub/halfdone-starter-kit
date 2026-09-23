#!/usr/bin/env node
/**
 * Hallucination Guard for Claude Code
 *
 * Blocks Edit/Write on files not Read in this session.
 * Tracks which files have been Read.
 * Forces re-read after failed Edits.
 *
 * Hooks config (hfd 킷: plugins/hfd/hooks/hooks.json):
 *   PreToolUse  (Edit|Write):  --pre
 *   PostToolUse (Read|Grep):   --post
 *   PostToolUseFailure (Edit): --fail
 *
 * hfd 킷판: 사용자 로컬 설치본(6/9판) 기준. 바뀐 점 — 표준 입력을 readFileSync(0)으로 읽음(윈도우 대응),
 *            옛 설치본 훅이 사용자 설정에 남아 있으면 두 번 실행되지 않게 아무것도 하지 않음(/hfd:setup으로 정리).
 */

import {
  readFileSync, writeFileSync, existsSync,
  mkdirSync, readdirSync, statSync, unlinkSync
} from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';

// --- Config ---
const STATE_DIR = join(homedir(), '.claude', '.guard');
const PREVIEW_LINES = 20;
const STATE_TTL_MS = 24 * 60 * 60 * 1000;

// --- 옛 설치본이 사용자 설정에 남아 있으면 그쪽이 이미 동작한다 → 건너뜀 ---
try {
  const confDir = process.env.CLAUDE_CONFIG_DIR || join(homedir(), '.claude');
  const settings = readFileSync(join(confDir, 'settings.json'), 'utf8');
  if (settings.includes('hooks/hallucination-guard.mjs')) process.exit(0);
} catch {}

// --- Parse input ---
let input;
try {
  input = JSON.parse(readFileSync(0, 'utf8'));
} catch {
  process.exit(0);
}

const mode = process.argv[2]; // --pre | --post | --fail
const tool = input.tool_name || '';
const toolInput = input.tool_input || {};
const sessionId = (input.session_id || 'default').replace(/[^a-zA-Z0-9_-]/g, '_');

// --- State ---
if (!existsSync(STATE_DIR)) mkdirSync(STATE_DIR, { recursive: true });
const stateFile = join(STATE_DIR, `${sessionId}.json`);

function load() {
  try {
    const raw = JSON.parse(readFileSync(stateFile, 'utf8'));
    return new Set(raw.readFiles || []);
  } catch {
    return new Set();
  }
}

function save(readFiles) {
  writeFileSync(stateFile, JSON.stringify({ readFiles: [...readFiles] }));
}

function preview(filePath) {
  try {
    return readFileSync(filePath, 'utf8')
      .split('\n')
      .slice(0, PREVIEW_LINES)
      .map((l, i) => `${i + 1}\t${l}`)
      .join('\n');
  } catch {
    return '(unable to read)';
  }
}

// Cleanup stale state files ~1% of invocations
if (Math.random() < 0.01) {
  try {
    const now = Date.now();
    for (const f of readdirSync(STATE_DIR)) {
      const fp = join(STATE_DIR, f);
      try { if (now - statSync(fp).mtimeMs > STATE_TTL_MS) unlinkSync(fp); } catch {}
    }
  } catch {}
}

// ============================================================
// POST: track reads
// ============================================================
if (mode === '--post') {
  const readFiles = load();
  let changed = false;

  if (tool === 'Read' && toolInput.file_path) {
    readFiles.add(toolInput.file_path);
    changed = true;
  }

  // Grep on a specific file (not dir) counts as read
  if (tool === 'Grep' && toolInput.path) {
    try {
      if (existsSync(toolInput.path) && statSync(toolInput.path).isFile()) {
        readFiles.add(toolInput.path);
        changed = true;
      }
    } catch {}
  }

  if (changed) save(readFiles);
  process.exit(0);
}

// ============================================================
// FAIL: force re-read after failed Edit
// ============================================================
if (mode === '--fail') {
  if (tool === 'Edit' && toolInput.file_path) {
    const readFiles = load();
    readFiles.delete(toolInput.file_path);
    save(readFiles);
    console.log(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'PostToolUseFailure',
        additionalContext: `Edit failed on ${toolInput.file_path}. Re-read the file before retrying — your mental model of its contents is stale.`
      }
    }));
  }
  process.exit(0);
}

// ============================================================
// PRE: block Edit/Write on unread files
// ============================================================
if (mode === '--pre') {
  const filePath = toolInput.file_path;
  if (!filePath) process.exit(0);

  // New files are fine — nothing to hallucinate about
  if (!existsSync(filePath)) process.exit(0);

  const readFiles = load();
  if (readFiles.has(filePath)) process.exit(0);

  // File exists but hasn't been read → block with evidence
  const evidence = preview(filePath);
  const reason = [
    `BLOCKED: ${tool} attempted on a file not Read in this session.`,
    `File: ${filePath}`,
    ``,
    `ACTION REQUIRED — do this now, automatically:`,
    `  1. Call the Read tool: Read({ file_path: "${filePath}" })`,
    `  2. Retry the original ${tool} call.`,
    ``,
    `Reason: Editing without reading risks hallucinated content (stale mental model).`,
    ``,
    `First ${PREVIEW_LINES} lines of the file (preview only — still must Read):`,
    evidence
  ].join('\n');

  // Modern PreToolUse spec: permissionDecision + permissionDecisionReason
  // (delivers reason to both Claude conversation and user UI)
  console.log(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: reason
    }
  }));
  // Safety net: also emit to stderr so it surfaces in UIs that fall back to stderr.
  process.stderr.write(reason + '\n');
  process.exit(2);
}

process.exit(0);
