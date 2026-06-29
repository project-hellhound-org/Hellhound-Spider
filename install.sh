#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
#  Hellhound Spider — Installer (v13.19)
#  Installs the `spider` command with an isolated virtual environment.
# ─────────────────────────────────────────────────────────────────────

set -e

RED='\033[91m'
GRN='\033[92m'
CYN='\033[96m'
YLW='\033[93m'
RST='\033[0m'
BLD='\033[1m'

info()    { echo -e "${CYN}[*]${RST} $1"; }
success() { echo -e "${GRN}${BLD}[✓]${RST} $1"; }
warn()    { echo -e "${YLW}[!]${RST} $1"; }
error()   { echo -e "${RED}[✗]${RST} $1"; stop_animation; exit 1; }

# ── Animator Logic (Cinematic) ────────────────────────────────────────────────
ANIM_PID=0

start_animation() {
    local label="$1"
    stop_animation
    
    # Ultra-Wide Animator matching spider.py v13.19 spec
    python3 -c "
import math, time, sys
label = \"$label\"
def wave(label, t):
    res = ''
    for i, c in enumerate(label):
        if not c.isalpha(): res += c; continue
        v = math.sin(t * 10 + i * 0.4)
        if v > 0: res += f'\033[91m\033[1m{c.upper()}\033[0m'
        else: res += f'\033[31m{c.lower()}\033[0m'
    return res
def braille(t):
    chars = '⡀⡄⡆⡇⣇⣧⣷⣿'
    bar = ''
    for i in range(50):
        idx = int((math.sin(t * 5 + i * 0.2) + 1) / 2 * (len(chars) - 1))
        bar += f'\033[91m{chars[idx]}\033[0m'
    return bar
start = time.time()
try:
    while True:
        t = time.time() - start
        # Fixed width padding for labels (25 chars) to prevent jitter
        sys.stdout.write(f'\r  {wave(label, t):<35}  {braille(t)} ')
        sys.stdout.flush()
        time.sleep(0.06)
except KeyboardInterrupt:
    pass
" &
    ANIM_PID=$!
}

stop_animation() {
    if [ "$ANIM_PID" -ne 0 ]; then
        kill "$ANIM_PID" &>/dev/null || true
        wait "$ANIM_PID" 2>/dev/null || true
        printf "\r\b\b\033[K" # Move back and clear the entire line
        ANIM_PID=0
    fi
}

trap "stop_animation" EXIT INT TERM

# Parse flags
NON_INTERACTIVE=false
for arg in "$@"; do
    if [[ "$arg" == "--yes" || "$arg" == "-y" || "$arg" == "--non-interactive" ]]; then
        NON_INTERACTIVE=true
    fi
done

# ── Check Python version ───────────────────────────────────────────────────────
start_animation "PREPARING HELLHOUND"
if ! command -v python3 &>/dev/null; then
    stop_animation
    error "Python 3 not found. Install Python 3.10+ and try again."
fi
# ... (removed redundant check)
PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
    error "Python 3.10+ required. Found: $PY_VERSION"
fi
stop_animation
success "Python $PY_VERSION found"

# ── Virtual Environment Setup ────────────────────────────────────────────────
start_animation "ISOLATING CORE"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR" || error "Failed to create virtual environment. Ensure 'python3-venv' is installed."
fi
VENV_PYTHON="$VENV_DIR/bin/python3"
stop_animation
success "Virtual environment ready: $VENV_DIR"

# ── Install pip dependencies ───────────────────────────────────────────────────
start_animation "DECRYPTING DEPENDENCIES"
"$VENV_PYTHON" -m pip install --quiet --upgrade pip
"$VENV_PYTHON" -m pip install --quiet -r requirements.txt
stop_animation
success "Core dependencies installed"

# ── Optional: Playwright ───────────────────────────────────────────────────────
INSTALL_PLAYWRIGHT="n"
if [ "$NON_INTERACTIVE" = true ]; then
    # In non-interactive mode, only install Playwright if already present
    if "$VENV_PYTHON" -c "import playwright" &>/dev/null; then
        INSTALL_PLAYWRIGHT="y"
        info "Playwright detected in venv — updating..."
    else
        warn "Non-interactive mode: skipping Playwright installation"
    fi
else
    echo ""
    echo -e "  ${CYN}Playwright${RST} enables headless browser scanning for SPA targets"
    echo -e "  (React, Angular, Vue, Next.js). Requires ~150MB for Chromium.\n"
    read -r -p "  Install Playwright for SPA support? [y/N] " INSTALL_PLAYWRIGHT
    echo ""
fi

if [[ "$INSTALL_PLAYWRIGHT" =~ ^[Yy]$ ]]; then
    stop_animation
    info "Mounting SPA Engine..."
    "$VENV_PYTHON" -m pip install --quiet --upgrade playwright playwright-stealth
    
    info "Fetching Chromium (this may take a minute)..."
    # Filter Playwright's OS support warnings on Kali/unsupported distros to keep output clean.
    # These warnings are emitted on stdout, so we filter both streams.
    "$VENV_PYTHON" -m playwright install chromium 2>&1 | grep --line-buffered -vE "BEWARE|fallback" || true
    
    info "Hardening system dependencies..."
    if command -v sudo &>/dev/null && [ "$EUID" -ne 0 ]; then
        sudo "$VENV_PYTHON" -m playwright install-deps chromium 2>&1 | grep --line-buffered -vE "BEWARE|fallback" || true
    else
        "$VENV_PYTHON" -m playwright install-deps chromium 2>&1 | grep --line-buffered -vE "BEWARE|fallback" || true
    fi
    
    success "Playwright + Chromium + Dependencies installed"
fi

# ── Patchright (Bot-Bypass Fallback) ──────────────────────────────────
# Automatically deploy Patchright if Playwright is installed, as it's the required WAF fallback.
if [[ "$INSTALL_PLAYWRIGHT" =~ ^[Yy]$ ]]; then
    stop_animation
    info "Deploying Patchright bypass engine..."
    "$VENV_PYTHON" -m pip install --quiet --upgrade patchright

    info "Fetching Patchright Chromium..."
    "$VENV_PYTHON" -m patchright install chromium 2>&1 | grep --line-buffered -vE "BEWARE|fallback" || true

    success "Patchright + Chromium installed (bot-bypass ready)"
fi

# ── WhatWeb (System Technology Fingerprinter) ─────────────────────────
if ! command -v whatweb &>/dev/null; then
    stop_animation
    if command -v apt-get &>/dev/null; then
        info "Installing WhatWeb technology fingerprinter..."
        if [ "$EUID" -eq 0 ]; then
            apt-get update -qq && apt-get install -y -qq whatweb &>/dev/null || warn "Failed to install WhatWeb automatically."
        elif command -v sudo &>/dev/null; then
            sudo apt-get update -qq && sudo apt-get install -y -qq whatweb &>/dev/null || warn "Failed to install WhatWeb automatically."
        else
            warn "WhatWeb is missing and could not be installed without root/sudo. Please run: apt install whatweb"
        fi
    else
        warn "WhatWeb is missing. Please install it manually for technology fingerprinting."
    fi
    if command -v whatweb &>/dev/null; then
        success "WhatWeb technology fingerprinter installed"
    fi
fi

# ── Install the spider command ─────────────────────────────────────────────────
start_animation "FINALIZING DEPLOYMENT"

SPIDER_SRC="$SCRIPT_DIR/spider.py"
if [ ! -f "$SPIDER_SRC" ]; then
    error "spider.py not found in $SCRIPT_DIR"
fi

# Build a self-locating wrapper so the script works for ANY user, not just
# the one who ran the installer.  At runtime the wrapper resolves its own real
# path, derives SCRIPT_DIR from it, then calls the venv python from there.
# This avoids hard-coding paths that only the installer's $HOME can reach.
WRAPPER_TMP=$(mktemp)
cat <<'EOW' > "$WRAPPER_TMP"
#!/usr/bin/env bash
# Hellhound Spider — Wrapper Script (self-locating, runs without sudo)
# Resolve the real location of this wrapper even through symlinks.
SELF="$(readlink -f "${BASH_SOURCE[0]}" 2>/dev/null || realpath "${BASH_SOURCE[0]}" 2>/dev/null || echo "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SELF")" && pwd)"
EOW
# Append the concrete install-time paths as variables into the wrapper
cat <<EOW >> "$WRAPPER_TMP"
VENV_PYTHON="$VENV_PYTHON"
SPIDER_SRC="$SPIDER_SRC"
EOW
# Append the execution block (single-quoted heredoc so \$@ isn't expanded now)
cat <<'EOW' >> "$WRAPPER_TMP"
if [ ! -x "$VENV_PYTHON" ]; then
    echo "[!] Hellhound venv not found at: $VENV_PYTHON" >&2
    echo "    Re-run install.sh to repair the installation." >&2
    exit 1
fi
exec "$VENV_PYTHON" "$SPIDER_SRC" "$@"
EOW

# Determine install location — prefer /usr/local/bin, fall back to ~/.local/bin
if [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
elif sudo -n true 2>/dev/null; then
    INSTALL_DIR="/usr/local/bin"
    USE_SUDO=true
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

INSTALL_PATH="$INSTALL_DIR/spider"

# Copy and set permissions.
# Use explicit 755 (not just +x) so a restrictive umask can't leave the file
# non-executable for other users — that's what causes "Permission denied".
if [ "${USE_SUDO:-false}" = true ]; then
    sudo cp "$WRAPPER_TMP" "$INSTALL_PATH"
    sudo chmod 755 "$INSTALL_PATH"
else
    cp "$WRAPPER_TMP" "$INSTALL_PATH"
    chmod 755 "$INSTALL_PATH"
fi
rm -f "$WRAPPER_TMP"
stop_animation
success "Installed to $INSTALL_PATH"

# Sanity check: verify the installed file is actually world-executable.
# If not (e.g. ACL override or unusual filesystem), warn immediately.
if [ ! -x "$INSTALL_PATH" ]; then
    warn "WARNING: $INSTALL_PATH exists but is not executable by the current user."
    warn "Try:  sudo chmod 755 $INSTALL_PATH"
fi

# ── Install man page ──────────────────────────────────────────────────────────
MANPAGE_SRC="$SCRIPT_DIR/man/spider.1"
if [ -f "$MANPAGE_SRC" ]; then
    if [ -w "/usr/local/share/man/man1" ]; then
        MAN_DIR="/usr/local/share/man/man1"
        cp "$MANPAGE_SRC" "$MAN_DIR/spider.1"
        chmod 644 "$MAN_DIR/spider.1"
    elif sudo -n true 2>/dev/null; then
        MAN_DIR="/usr/local/share/man/man1"
        sudo mkdir -p "$MAN_DIR"
        sudo cp "$MANPAGE_SRC" "$MAN_DIR/spider.1"
        sudo chmod 644 "$MAN_DIR/spider.1"
    else
        MAN_DIR="$HOME/.local/share/man/man1"
        mkdir -p "$MAN_DIR"
        cp "$MANPAGE_SRC" "$MAN_DIR/spider.1"
        chmod 644 "$MAN_DIR/spider.1"

        # Ensure MANPATH includes the user-local man directory
        MANPATH_LINE='export MANPATH="$HOME/.local/share/man:$MANPATH"'
        MANPATH_SET=false
        for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
            if [ -f "$rc" ] && grep -qF '.local/share/man' "$rc"; then
                MANPATH_SET=true
                break
            fi
        done
        if [ "$MANPATH_SET" = false ]; then
            warn "~/.local/share/man is not in your MANPATH"
            echo ""
            echo "  Add this line to your ~/.bashrc or ~/.zshrc:"
            echo ""
            echo -e "    ${GRN}${MANPATH_LINE}${RST}"
            echo ""
        fi
    fi

    # Refresh man-db cache if mandb is available
    if command -v mandb &>/dev/null; then
        if [ -w "/usr/local/share/man" ]; then
            mandb -q 2>/dev/null || true
        elif sudo -n true 2>/dev/null; then
            sudo mandb -q 2>/dev/null || true
        else
            mandb -q 2>/dev/null || true
        fi
    else
        warn "mandb not found — 'man spider' may not work until man-db is installed"
    fi

    success "Installed man page — run 'man spider' for usage details"
fi

# ── PATH check for ~/.local/bin ────────────────────────────────────────────────
if [ "$INSTALL_DIR" = "$HOME/.local/bin" ]; then
    if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
        warn "$HOME/.local/bin is not in your PATH"
        echo ""
        echo "  Add this line to your ~/.bashrc or ~/.zshrc:"
        echo ""
        echo -e "    ${GRN}export PATH=\"\$HOME/.local/bin:\$PATH\"${RST}"
        echo ""
        echo "  Then run:  source ~/.bashrc"
        echo ""
    fi
fi

# ── Done ───────────────────────────────────────────────────────────────────────
echo ""
echo -e "  ${GRN}${BLD}Installation complete.${RST}\n"
echo -e "  Usage:"
echo -e "    ${CYN}spider${RST} https://target.com"
echo -e "    ${CYN}spider${RST} https://target.com --cookie \"session=abc\""
echo -e "    ${CYN}spider${RST} https://target.com --auth \"Bearer eyJ...\""
echo -e "    ${CYN}spider${RST} --help"
echo ""
