#!/usr/bin/env bash
# Ratel social pipeline — one-command setup.
#
#   ./install.sh            check everything, install what is missing
#   ./install.sh --check    report only, change nothing
#
# Safe to re-run. Everything it installs is idempotent.

set -uo pipefail
CHECK_ONLY=false
[ "${1:-}" = "--check" ] && CHECK_ONLY=true

green() { printf '\033[32m✓\033[0m %s\n' "$1"; }
warn()  { printf '\033[33m!\033[0m %s\n' "$1"; }
fail()  { printf '\033[31m✗\033[0m %s\n' "$1"; }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

MISSING=0
need() { command -v "$1" >/dev/null 2>&1; }

head_ "Core tools"

if need node; then
  NODE_MAJOR=$(node -v | sed 's/v\([0-9]*\).*/\1/')
  if [ "$NODE_MAJOR" -ge 18 ]; then green "node $(node -v)"; else fail "node $(node -v) — need 18+"; MISSING=1; fi
else
  fail "node missing — install from https://nodejs.org or: brew install node"; MISSING=1
fi

if need ffmpeg; then
  green "ffmpeg $(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
else
  if $CHECK_ONLY; then fail "ffmpeg missing"; MISSING=1
  elif need brew; then warn "installing ffmpeg…"; brew install ffmpeg >/dev/null 2>&1 && green "ffmpeg installed" || { fail "ffmpeg install failed"; MISSING=1; }
  else fail "ffmpeg missing — brew install ffmpeg"; MISSING=1; fi
fi

if need python3; then green "python3 $(python3 --version 2>&1 | awk '{print $2}')"
else fail "python3 missing — brew install python"; MISSING=1; fi

head_ "HyperFrames (video + image rendering)"

if need npx; then
  if $CHECK_ONLY; then
    npx --yes hyperframes skills check 2>&1 | tail -3 || warn "could not check HyperFrames skills"
  else
    warn "installing/updating HyperFrames skills…"
    if npx --yes hyperframes skills update >/dev/null 2>&1; then
      green "HyperFrames skills up to date"
    else
      fail "HyperFrames skills update failed — run: npx hyperframes skills update"; MISSING=1
    fi
  fi
else
  fail "npx missing (comes with node)"; MISSING=1
fi

head_ "Design skills (vendored, no install needed)"

if [ -d .agents/skills ] && [ -L .claude/skills/animate ]; then
  green "$(find .agents/skills -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ') skills vendored in .agents/skills, symlinked into .claude/skills"
else
  fail ".agents/skills missing — re-clone the repo, these ship with it"; MISSING=1
fi

head_ "Voiceover"

VB_APP="/Applications/Voicebox.app"
if [ -d "$VB_APP" ]; then
  green "Voicebox installed (free, local, no API key)"
  VB_PORT=$(ps -Ao command | grep -o '[v]oicebox-server .*--port [0-9]*' | grep -o '[0-9]*$' | head -1)
  if [ -n "${VB_PORT:-}" ]; then
    green "Voicebox server running on 127.0.0.1:$VB_PORT"
  else
    warn "Voicebox not running — open it once so its local API comes up"
  fi
else
  warn "Voicebox not installed (optional but recommended — free and local)"
  warn "  https://voicebox.sh  →  download, then open once to fetch a TTS model"
fi

if [ -f "$HOME/.heygen/credentials" ]; then
  green "HeyGen credentials present (TTS + music library)"
else
  warn "HeyGen not signed in — optional. Run: npx hyperframes auth login"
fi

head_ "Tracker (Notion metrics)"

if [ -f tracker/requirements.txt ]; then
  if $CHECK_ONLY; then
    warn "tracker deps not verified in --check mode"
  else
    python3 -m pip install --quiet -r tracker/requirements.txt 2>/dev/null \
      && green "tracker deps installed" \
      || warn "tracker deps failed — try: python3 -m pip install -r tracker/requirements.txt"
  fi
else
  warn "no tracker/requirements.txt"
fi

head_ "Manual steps (cannot be scripted)"
cat <<'EOF'
  1. Connect Notion and Google Calendar in Claude Code's integrations panel.
     These authenticate through your account, not through .mcp.json.
  2. Copy tracker/.env.example to tracker/.env and fill it in, if you use the tracker.
  3. Open Voicebox once and download a TTS model (Qwen CustomVoice is the
     recommended one — it ships preset speakers, so no voice recording needed).
EOF

echo
if [ "$MISSING" -eq 0 ]; then
  printf '\033[32mReady.\033[0m Open this repo in Claude Code and run /draft, /post, /video or /strategy.\n'
else
  printf '\033[31mSome required tools are missing — see above.\033[0m\n'
  exit 1
fi
