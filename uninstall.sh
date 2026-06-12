#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
#  Hellhound Spider — Uninstaller
# ─────────────────────────────────────────────────────────────────────

set -e

RED='\033[91m'
GRN='\033[92m'
CYN='\033[96m'
RST='\033[0m'
BLD='\033[1m'

info()    { echo -e "${CYN}[*]${RST} $1"; }
success() { echo -e "${GRN}${BLD}[✓]${RST} $1"; }
error()   { echo -e "${RED}[✗]${RST} $1"; exit 1; }

LOCATIONS=(
    "/usr/local/bin/spider"
    "/usr/bin/spider"
    "$HOME/.local/bin/spider"
)

FOUND=false
for LOC in "${LOCATIONS[@]}"; do
    if [ -f "$LOC" ]; then
        info "Removing $LOC..."
        if [ -w "$(dirname "$LOC")" ]; then
            rm -f "$LOC"
        else
            sudo rm -f "$LOC"
        fi
        success "Removed $LOC"
        FOUND=true
    fi
done

# ── Remove man page ──────────────────────────────────────────────────────────
MAN_LOCATIONS=(
    "/usr/local/share/man/man1/spider.1"
    "/usr/share/man/man1/spider.1"
    "$HOME/.local/share/man/man1/spider.1"
)

for MLOC in "${MAN_LOCATIONS[@]}"; do
    if [ -f "$MLOC" ]; then
        info "Removing man page $MLOC..."
        if [ -w "$(dirname "$MLOC")" ]; then
            rm -f "$MLOC"
        else
            sudo rm -f "$MLOC"
        fi
        success "Removed $MLOC"
    fi
done

# Refresh man-db cache if available
if command -v mandb &>/dev/null; then
    if [ -w "/usr/local/share/man" ]; then
        mandb -q 2>/dev/null || true
    elif sudo -n true 2>/dev/null; then
        sudo mandb -q 2>/dev/null || true
    else
        mandb -q 2>/dev/null || true
    fi
fi

# ── Cleanup Virtual Environment ──────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -d "$SCRIPT_DIR/.venv" ]; then
    info "Removing virtual environment..."
    rm -rf "$SCRIPT_DIR/.venv"
    success "Removed $SCRIPT_DIR/.venv"
fi

if [ "$FOUND" = false ]; then
    error "spider command not found in any standard location"
fi

echo ""
echo -e "  ${GRN}${BLD}Uninstall complete.${RST}"
echo ""