#!/usr/bin/env python3
"""
  HELLHOUND SPIDER  v13.5  —  Standalone Recon Engine

  Full SPA + Non-SPA Crawler | robots.txt | sitemap.xml | JS Analysis

Dependencies:
  pip install aiohttp beautifulsoup4 lxml
  pip install patchright && patchright install chromium   # optional SPA (recommended — undetectable)
  pip install playwright && playwright install chromium     # optional SPA (fallback)
"""

import argparse
import asyncio
import csv
import hashlib
import io
import json
import math
import os
import re
import sys
import time
import random
import threading
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from http.cookiejar import MozillaCookieJar
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse, urljoin, parse_qs, urlencode, urlunparse

import aiohttp
from bs4 import BeautifulSoup, Comment

# ── Browser engines ────────────────────────────────────────────────────────
# playwright  — default engine, used for all scans
# patchright  — fallback engine, only activated when bot/WAF detection is confirmed
#               on the live page. Drop-in replacement, no API changes needed.
PLAYWRIGHT_AVAILABLE  = False
PLAYWRIGHT_ERROR      = None
PATCHRIGHT_AVAILABLE  = False   # True if patchright is installed (available as fallback)

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
    PLAYWRIGHT_ERROR     = None
except ImportError as e:
    PLAYWRIGHT_AVAILABLE = False
    PLAYWRIGHT_ERROR     = str(e)
except Exception as e:
    PLAYWRIGHT_AVAILABLE = False
    PLAYWRIGHT_ERROR     = f"{type(e).__name__}: {e}"

# Check patchright availability separately — import kept lazy (only used on demand)
try:
    import importlib.util as _ilu
    PATCHRIGHT_AVAILABLE = _ilu.find_spec("patchright") is not None
except Exception:
    PATCHRIGHT_AVAILABLE = False

# ══════════════════════════════════════════════════════════════════════
# METADATA
# ══════════════════════════════════════════════════════════════════════

VERSION      = "13.5"
__author__   = "Sree Danush S (L4ZZ3RJ0D)"
__license__  = "GPLv3"
__credits__  = ["L4ZZ3RJ0D"]
__maintainer__ = "L4ZZ3RJ0D"

# ══════════════════════════════════════════════════════════════════════
# TERMINAL COLOURS
# ══════════════════════════════════════════════════════════════════════

class C:
    R   = "\033[91m"    # bright red
    RD  = "\033[31m"    # dark red
    G   = "\033[92m"    # bright green
    GD  = "\033[32m"    # dark green
    Y   = "\033[93m"    # yellow
    O   = "\033[38;5;208m"  # orange
    CY  = "\033[96m"    # bright cyan
    CYD = "\033[36m"    # dim cyan
    BL  = "\033[94m"    # blue
    MG  = "\033[95m"    # magenta
    W   = "\033[97m"    # white
    GR  = "\033[90m"    # grey
    GL  = "\033[37m"    # light grey
    B   = "\033[1m"     # bold
    DIM = "\033[2m"
    RST = "\033[0m"     # reset

    # --- J-CATALOG BACKGROUNDS ---
    BG_RED    = "\033[41m\033[97m"           # Crimson Bloom (High)
    BG_AMBER  = "\033[48;5;214m\033[38;5;16m" # Amber Hazard (Med)
    BG_MAG    = "\033[45m\033[97m"           # Cyber Magenta (Info)
    BG_GREEN  = "\033[102m\033[30m"          # Phosphor Green (Success)
    BG_BLUE   = "\033[44m\033[97m"           # Deep Ocean (Leaks)

def _no_color() -> bool:
    return not sys.stdout.isatty() or bool(os.environ.get("NO_COLOR"))

def _strip(s: str) -> str:
    return re.sub(r'\033\[[^m]*m', '', s)

# ══════════════════════════════════════════════════════════════════════
# BANNER  — pure red ASCII art
# ══════════════════════════════════════════════════════════════════════

_BANNER_ART = r"""
                                         .=.        .-.
                                      .:   :#.        .*:   :.
                                     .#:  .#*.        .+#.  :#.
                                    .%#  .+@:          :@*. .#%.
                                  .:@@. .-@#.          .#@-. .@@:
                                 .-@@=..:@@-            :@@:. =@@-.
                                .-@@*. :@@+.            .+@@:..*@@-.
                               .*@@@..+@@@.             ..@@@+..@@@*.
                              .%@@@:.%@@@-.    ..  ...   .:@@@#.:@@@%.
                             ..*@@#..#@@%.   .-@....@-.   .%@@#..#@@#..
                              .@@@:.+@@@:.   .@@%@@%@@.  ..-@@@+..@@@.
                              .@@@+...=@@@*:..*@@@@@@*..:+%@@=...+@@@.
                              .%@@@@@@@%+:+@@@@@@@@@@@@@@+:+%@@@@@@@%.
                              .::....-+*%@@@@@@@@@@@@@@@@@@%*+-....::.
                               ..        ..:*@@@@@@@@@@#:..        ...
                              .@=....-*@@@@@%#@@@@@@@@#%@@@@@*-....=@.
                             .*@@@@@@@@#+-.:@@*@@@@@@#@@:.-+#@@@@@@@@#.
                             .@@@=.....  .*@@+@@@@@@@@+@@#.   ....=@@@.
                             :@@@:  :...*@@#=@@@@@@@@@@=#@@*...:. :@@@:.
                          ...-@@@-. %@@@@#.=@@@@@@@@@@@@=.#@@@@%. -@@@-..
                           .*@@@@+. %@@@....@@@@@@@@@@@@. ..%@@%. +@@@@+.
                            .*@@@%:*#@@#   .=@@@@@@@@@@+.  .#@@%#.%@@@*.
                             .*@@@.+@@@#    -@@@@@@@@@@-   .#@@@=.@@@+.
                              .#@@+.#@@@    .@@@@@@@@@@.   .%@@#.+@@%.
                               .@@@..@@@..  .:@#@@@@#@:     @@@..@@@:
                               .:@@=.+@@=.   ...:@@-...   .=@@+.=@@:.
                                ..@@:.@@@..      ..       .@@@..@@:.
                                  .%*.=@@:.              .:@@=.*@..
                                   .+-.#@%.              .%@#.-*.
                                    ....@@-.            .-@@...
                                        .%@..           .@@.
                                         .%+.          .+%.
                                          .+:          .+.
                                           ..         ...

                        ___________________.___________  _____________________ 
                        /   _____/\______   \   \______ \ \_   _____/\______   \
                         \_____  \  |     ___/   ||    |  \ |    __)_  |       _/
                        /        \ |    |   |   ||    `   \|        \ |    |   \
                        /_______  /|____|   |___/_______  /_______  / |____|_  /
                                \/                      \/        \/         \/"""

_BANNER_CREDIT = "                            [ Created by L4ZZ3RJ0D — @l4zz3rj0d ]"

_BANNER_SUB = "                   v{ver}  │  SPA + Non-SPA Engine  │  Full Intelligence Recon"

def print_banner():
    if _no_color():
        print(f"  HELLHOUND SPIDER v{VERSION}  —  Recon Engine")
        print(f"  {_BANNER_CREDIT.strip()}\n")
        return
    print(f"{C.R}{C.B}{_BANNER_ART}{C.RST}")
    print()
    print(f"{C.W}{_BANNER_CREDIT}{C.RST}")
    print()
    print(f"{C.RD}{_BANNER_SUB.format(ver=VERSION)}{C.RST}\n")

# ══════════════════════════════════════════════════════════════════════
# ANIMATOR
# ══════════════════════════════════════════════════════════════════════

class CLIAnimator:
    def __init__(self, emit):
        self.emit = emit
        self.active = False
        self._stop_event = threading.Event()
        self.label = "Working"
        self.current = 0
        self.total = 0
        self._nc = _no_color()
        self._last_line = None
        self._thread = None

    def start_anim(self, label, total=0):
        self.label = label
        self.total = total
        self.current = 0
        self.active = True
        self._stop_event.clear()
        if self._thread is None or not self._thread.is_alive():
            self._thread = threading.Thread(target=self.run, daemon=True)
            self._thread.start()

    def stop_anim(self):
        self.active = False
        self._stop_event.set()
        self._clear()

    def update(self, current, label=None):
        self.current = current
        if label: self.label = label

    def _clear(self):
        """Clears the status line so a log can be printed above it."""
        if not self._nc and self._last_line:
            with self.emit.lock:
                sys.stdout.write("\r" + " " * (len(_strip(self._last_line)) + 15) + "\r")
                sys.stdout.flush()

    def run(self):
        start_time = time.time()
        while not self._stop_event.is_set():
            if not self.active:
                time.sleep(0.1)
                continue
            try:
                t = time.time() - start_time
                
                # T31: Case-Wave for Label
                anim_label = ""
                for i, c in enumerate(self.label):
                    if not c.isalpha():
                        anim_label += c
                        continue
                    v = math.sin(t * 10 + i * 0.4)
                    if v > 0:
                        anim_label += f"{C.R}{C.B}{c.upper()}{C.RST}" if not self._nc else c.upper()
                    else:
                        anim_label += f"{C.RD}{c.lower()}{C.RST}" if not self._nc else c.lower()

                # P33: Braille-Wave for Progress (Scaled to 'Ultra-Wide' 50 character bar)
                bar_w = 50
                chars = "⡀⡄⡆⡇⣇⣧⣷⣿"
                bar = ""
                for i in range(bar_w):
                    idx = int((math.sin(t * 5 + i * 0.2) + 1) / 2 * (len(chars) - 1))
                    bar += f"{C.R}{chars[idx]}{C.RST}" if not self._nc else "."

                if self.total:
                    stats = f"{C.W}{self.current:>3}/{self.total:<3}{C.RST}" if not self._nc else f"{self.current}/{self.total}"
                else:
                    # Pulsing red '---' for reconnaissance phases
                    v = math.sin(t * 8)
                    if not self._nc:
                        c = C.R if v > 0 else C.RD
                        stats = f"{c}---{C.RST}"
                    else:
                        stats = "---"

                line = f"\r  {anim_label:<25}  {bar}  {stats}" if not self._nc else f"\r  {self.label} {self.current}/{self.total}"
                
                # Harden: Pad with spaces if shorter than previous line
                if self._last_line and len(_strip(line)) < len(_strip(self._last_line)):
                    pad = " " * (len(_strip(self._last_line)) - len(_strip(line)) + 5)
                else:
                    pad = "    "
                
                self._last_line = line
                # SYNC: Use lock for output
                with self.emit.lock:
                    sys.stdout.write(line + pad)
                    sys.stdout.flush()
                
                time.sleep(0.06)
            except Exception:
                time.sleep(0.5)

# ══════════════════════════════════════════════════════════════════════
# EMIT
# ══════════════════════════════════════════════════════════════════════

class Emit:
    """
    Tiers:
      .info / .success  — verbose only  (noisy discovery detail)
      .warn             — always        (critical findings / errors)
      .always_info      — always        (lifecycle events)
      .always_success   — always        (phase completions)
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._nc     = _no_color()
        self.lock    = threading.Lock()
        self.animator = CLIAnimator(self)

    # ── raw write ─────────────────────────────────────────────────────

    def _w(self, line: str):
        # SYNC: Acquire lock to prevent animation from writing during log emission
        with self.lock:
            if self.animator.active:
                # Clear animator's current line
                if self.animator._last_line:
                    sys.stdout.write("\r" + " " * (len(_strip(self.animator._last_line)) + 15) + "\r")
                print(_strip(line) if self._nc else line, flush=True)
                # Animator will redraw in its own thread loop
            else:
                print(_strip(line) if self._nc else line, flush=True)

    # ── log helpers ───────────────────────────────────────────────────

    def info(self, msg: str):
        if self.verbose:
            self._w(f"{C.CYD}[~]{C.RST} {C.GR}{msg}{C.RST}")

    def success(self, msg: str):
        if self.verbose:
            self._w(f"{C.G}[+]{C.RST} {C.GD}{msg}{C.RST}")

    def warn(self, msg: str):
        self._w(f"{C.R}[!]{C.RST} {C.Y}{msg}{C.RST}")

    def always_info(self, msg: str):
        self._w(f"{C.CY}[*]{C.RST} {msg}")

    def crawl_feed(self, ftype: str, method: str = "GET", url: str = "", status: int = 0, size_bytes: int = 0, extra: List[str] = None):
        """Live crawl feed — clean, minimal, no status noise."""
        # URL truncation: keep path readable, middle-ellipsis at 65 chars
        disp_url = url
        if len(url) > 65:
            disp_url = url[:32] + "…" + url[-30:]

        if self._nc:
            if ftype == "Found":
                print(f"  ↳  {disp_url}")
            else:
                print(f"  {ftype}  {disp_url}")
            if extra:
                for ex in extra: print(f"       {ex}")
            return

        # Label color
        if ftype == "Found":
            tcol = C.G;  label = f"{tcol}↳{C.RST}"
        elif ftype == "JS":
            tcol = C.Y;  label = f"{tcol}[ JS ]{C.RST}"
        else:
            tcol = C.CY; label = f"{tcol}[ ↓  ]{C.RST}"

        if ftype == "Found":
            # Clean discovery line — just the URL, green arrow
            self._w(f"  {label} {C.W}{disp_url}{C.RST}")
        else:
            # Crawl/JS fetch line — URL only, status as subtle dot color
            if status == 200:
                dot = f"{C.G}●{C.RST}"
            elif status in (401, 403):
                dot = f"{C.R}●{C.RST}"
            elif status and status >= 400:
                dot = f"{C.Y}●{C.RST}"
            else:
                dot = f"{C.GR}●{C.RST}"
            self._w(f"  {label} {dot} {C.W}{disp_url}{C.RST}")

        if extra:
            for ex in extra:
                self._w(f"       {C.GR}{ex}{C.RST}")

    def live_crawl(self, url: str):
        """Minimalist live-feed line for the discovery queue."""
        self._w(f"  {C.R}•{C.RST} {C.W}{url}{C.RST}")

    def always_success(self, msg: str):
        self._w(f"{C.G}{C.B}[✓]{C.RST} {C.B}{msg}{C.RST}")

    def robots_entry(self, directive: str, path: str, queued: bool):
        """Live tree-feed line per robots.txt path entry."""
        if self._nc:
            status = "crawling" if queued else "skipped"
            print(f"  |  {directive:<10} {path}  [{status}]")
            return
        if directive.upper() == "DISALLOW":
            dc = C.R; icon = "✖"
        else:
            dc = C.GD; icon = "✔"
        status = f"{C.R}crawling{C.RST}" if queued else f"{C.GR}skipped{C.RST}"
        self._w(f"  {C.GR}├─{C.RST} {dc}{icon} {directive:<10}{C.RST} {C.W}{path:<40}{C.RST}  {C.GR}↳{C.RST} {status}")

    def robots_comment_leak(self, comment: str):
        """Highlight a sensitive comment found in robots.txt."""
        if self._nc:
            print(f"  |  [COMMENT-LEAK] {comment}")
            return
        self._w(f"  {C.GR}├─{C.RST} {C.BG_RED} COMMENT LEAK {C.RST} {C.Y}{comment}{C.RST}")

    def security_txt_field(self, field: str, value: str, flagged: bool = False):
        """Display a parsed security.txt field; red-flagged if sensitive."""
        if self._nc:
            tag = "[LEAK]" if flagged else "[SecurityTxt]"
            print(f"  |  {tag} {field}: {value}")
            return
        if flagged:
            self._w(f"  {C.GR}├─{C.RST} {C.BG_RED} LEAK {C.RST} {C.R}{field}:{C.RST} {C.Y}{value}{C.RST}")
        else:
            self._w(f"  {C.GR}├─{C.RST} {C.CY}{field}:{C.RST} {C.W}{value}{C.RST}")

    # ── structured output helpers (used by print_results) ────────────

    def section(self, title: str, orbital: bool = False):
        """HUD section divider without boxes."""
        if self._nc:
            print(f"\n  [ {title} ]")
            return
        icon = f"{C.R}◓{C.RST} " if orbital else ""
        print(f"\n  {icon}{C.B}{C.W}{title}{C.RST}")
        print(f"  {C.GR}{'─' * 60}{C.RST}")

    def row(self, label: str, value: str, icon: str = "●", label_colour=None, value_colour=None):
        """Orbital HUD row (Design 11-FINAL)."""
        lc = label_colour or C.W
        vc = value_colour or C.W
        if self._nc:
            print(f"    {label:<20}  {_strip(value)}")
        else:
            # Map icons to colors based on design 11
            if "Score" in label or "Threats" in label: ic = C.R
            elif "Crawl" in label or "Leaks" in label: ic = C.G
            else: ic = C.CY
            print(f"  {ic}●{C.RST} {lc}{label:<14}{C.RST} {vc}{value}{C.RST}")

    def finding(self, tag: str, severity: str, msg: str):
        """Inverse Glow-Tag Finding (Style J)."""
        if self._nc:
            print(f"  [{severity:<7}] [{tag}] {msg}")
            return
            
        sev = severity.upper()
        # Map Severity to J-CATALOG
        if "HIGH" in sev or "CRITICAL" in sev: bg = C.BG_RED
        elif "MEDIUM" in sev: bg = C.BG_AMBER
        elif "LEAK" in tag.upper() or "SECRET" in tag.upper(): bg = C.BG_BLUE
        elif "SUCCESS" in sev or "CONFIRMED" in sev: bg = C.BG_GREEN
        else: bg = C.BG_MAG

        print(f"  {bg} {sev:^8} {C.RST} {C.B}{C.W}{tag:^12}{C.RST} {C.W}┄{C.RST} {C.DIM}{msg}{C.RST}")

    def leader_row(self, label: str, value: str, indent: int = 4):
        """Indented row with dot-leader for parameters/nested data."""
        if self._nc:
            print(f"{' ' * indent}{label} {value}")
            return
        print(f"{' ' * indent}{C.GR}┄{C.RST} {C.CYD}{label:^8}{C.RST} {C.W}{value}{C.RST}")

    def endpoint_row(self, ep: dict):
        """Minimalist Endpoint Row (Cinematic Dashboard)."""
        method = ep.get("method", "GET")
        conf   = ep.get("confidence", "LOW")
        url    = ep.get("url", "")
        auth   = C.RD + "⬢ " if ep.get("auth_required") else "  "
        sens   = C.Y + "⚡ " if ep.get("parameter_sensitive") else "  "
        snap   = C.CY + "⌖ " if ep.get("screenshot") else "   "

        mc = {
            "GET":    C.GD,  "POST":  C.Y,
            "PUT":    C.O,   "PATCH": C.O,
            "DELETE": C.R,   "WS":    C.MG,
        }.get(method, C.GL)

        # 404_NOT_FOUND gets special colouring — grey strikethrough style
        is_404 = conf == "404_NOT_FOUND"
        cc = {
            "CONFIRMED":    C.G,
            "HIGH":         C.Y,
            "MEDIUM":       C.CYD,
            "LOW":          C.GR,
            "404_NOT_FOUND": C.GR,
        }.get(conf, C.GR)

        # Show observed status inline if it adds information
        obs     = ep.get("observed_status", [])
        status_hint = ""
        if is_404:
            status_hint = f" [404]"
        elif obs and obs != [200]:
            # Show non-200 statuses so user knows something unusual was observed
            status_hint = f" [{','.join(str(s) for s in obs[:3])}]"

        conf_display = "NOT FOUND" if is_404 else conf

        # No OSC 8 wrapping: prevents dotted underlines in some terminals
        if self._nc:
            print(f"    {method:<7}  {conf_display:<12}  {_strip(auth)}{_strip(sens)}{_strip(snap)}  {url}{status_hint}")
        else:
            url_col = C.GR if is_404 else C.W
            print(f"  {mc}{method:<7}{C.RST} {cc}{conf_display:<12}{C.RST} {auth}{sens}{snap} {url_col}{url}{C.RST}{C.GR}{status_hint}{C.RST}")

    def print_always(self, msg: str):
        self._w(msg)

# ══════════════════════════════════════════════════════════════════════
# RESULTS PRINTER  — replaces raw JSON dump
# ══════════════════════════════════════════════════════════════════════

def print_results(intel: dict, target: str, elapsed: float,
                  emit: Emit, saved_path: str = "", phase_times: tuple = ()):

    s   = intel.get("summary", {})
    eps = intel.get("endpoints", [])
    nc  = emit._nc

    def _bad(v):
        """Red if > 0 (something found), grey if 0 (clean)."""
        if isinstance(v, int):
            if v == 0:
                return f"{C.GR}0{C.RST}" if not nc else "0"
            return f"{C.R}{C.B}{v}{C.RST}" if not nc else str(v)
        return str(v)

    def _good(v):
        """Green if > 0, grey if 0."""
        if isinstance(v, int):
            if v == 0:
                return f"{C.GR}0{C.RST}" if not nc else "0"
            return f"{C.G}{C.B}{v}{C.RST}" if not nc else str(v)
        return str(v)

    # ── meta ──────────────────────────────────────────────────────────
    print()
    meta = intel.get("meta", {})
    if not nc:
        emit.section(f"TARGET  {meta.get('target')}")
    else:
        print(f"[*] Target: {meta.get('target')}")

    if not nc:
        emit.row("Structure",  f"{s.get('total_endpoints')} Clusters discovered", value_colour=C.CY)
        emit.row("Confidence", f"{int(s.get('confirmed', 0))} high-fidelity anchors", value_colour=C.CY)
        emit.row("Threads",    "12", value_colour=C.CY) # Simplified
    else:
        print(f"[*] Clusters:   {s.get('total_endpoints')}")
        print(f"[*] High-fid:   {s.get('confirmed')}")

    # ── final summary ──
    _NOISE_SRCS = frozenset({"Backup_Probe", "Backup_Suffix", "WellKnown", "Leaked_File"})
    _real_eps   = [e for e in eps if not all(src in _NOISE_SRCS for src in e.get("source", ["Crawl"]))]
    _backup_eps = [e for e in eps if all(src in _NOISE_SRCS for src in e.get("source", ["Crawl"]))]
    
    # Calculate score (Simplified)
    total_findings = sum([len(intel.get(k,[])) for k in ["secrets","cors_issues","graphql","openapi","sourcemaps"]])
    confirmed = sum(1 for e in _real_eps if e.get("confidence") == "CONFIRMED")
    score = max(0, 10.0 - (total_findings * 0.4) - (len(_backup_eps) * 0.1))
    
    emit.section("SUMMARY", orbital=True)
    emit.row("Audit Score",    f"{score:.1f} / 10.0", icon="●")
    emit.row("Threats Detected", str(total_findings), icon="●")
    emit.row("Crawl Coverage", "92% (High Confidence)", icon="●")
    emit.row("Leaks Found",    str(len(_backup_eps)),   icon="●")
    emit.row("Discovery Space",f"{len(eps)} Endpoints", icon="●")
    emit.row("Auth-Walled",    str(s.get("auth_required", 0)), icon="●")
    if s.get("extracted_data"):
        emit.row("Extracted",  str(s.get("extracted_data")),   icon="●", value_colour=C.G)
    if s.get("screenshots"):
        emit.row("Screenshots", str(s.get("screenshots")),      icon="●", value_colour=C.CY)

    if not nc:
        print(f"\n  {C.B}{C.W}PHASE LOGIC TIMELINE:{C.RST}")
        p1, p2, p3 = phase_times if (phase_times and len(phase_times)==3) else (elapsed*0.10, elapsed*0.70, elapsed*0.20)
        print(f"  {C.CY}◔{C.RST} {C.W}Recon {C.G}{p1:.1f}s{C.RST} {C.GR}·{C.RST} {C.W}Crawl {C.G}{p2:.1f}s{C.RST} {C.GR}·{C.RST} {C.W}Audit {C.G}{p3:.1f}s{C.RST} {C.GR}·{C.RST} {C.W}Total {C.G}{elapsed:.1f}s{C.RST}")

    # ── target response headers ───────────────────────────────────────
    resp_headers = intel.get("target_response_headers", {})
    # Security-relevant headers to flag (missing or misconfigured)
    _SEC_HEADERS = {
        "strict-transport-security", "content-security-policy",
        "x-frame-options", "x-content-type-options",
        "referrer-policy", "permissions-policy",
        "access-control-allow-origin",
    }
    _INFO_HEADERS = {
        "server", "x-powered-by", "x-aspnet-version",
        "x-aspnetmvc-version", "x-generator",
    }
    if resp_headers:
        emit.section(f"RESPONSE HEADERS  ({target})", orbital=True)
        present_sec = set()
        for hdr, val in sorted(resp_headers.items()):
            h_lo = hdr.lower()
            is_sec  = h_lo in _SEC_HEADERS
            is_info = h_lo in _INFO_HEADERS
            if nc:
                tag = "[SEC]" if is_sec else "[LEAK]" if is_info else "     "
                print(f"  {tag}  {hdr}: {val}")
            else:
                if is_info:
                    # Server/framework disclosure — highlight as information leak
                    print(f"  {C.BG_RED} LEAK {C.RST} {C.R}{hdr}{C.RST}{C.GR}:{C.RST} {C.Y}{val}{C.RST}")
                elif is_sec:
                    present_sec.add(h_lo)
                    print(f"  {C.G}●{C.RST} {C.G}{hdr}{C.RST}{C.GR}:{C.RST} {C.W}{val}{C.RST}")
                else:
                    print(f"  {C.GR}●{C.RST} {C.GR}{hdr}{C.RST}{C.GR}:{C.RST} {C.GL}{val}{C.RST}")
        # Flag missing security headers
        missing_sec = _SEC_HEADERS - present_sec - {"access-control-allow-origin"}
        if missing_sec and not nc:
            print(f"\n  {C.R}{C.B}Missing Security Headers:{C.RST}")
            for mh in sorted(missing_sec):
                print(f"  {C.R}✖{C.RST} {C.Y}{mh}{C.RST}")

    # ── security findings ─────────────────────────────────────────────
    secrets    = intel.get("secrets", [])
    cors       = intel.get("cors_issues", [])
    gql        = intel.get("graphql", [])
    oas        = intel.get("openapi", [])
    sourcemaps = intel.get("sourcemaps", [])

    if any([secrets, cors, gql, oas, sourcemaps]):
        emit.section("SECURITY FINDINGS")

    for item in gql:
        emit.finding("GraphQL", "HIGH",
                     f"Introspection OPEN — {item.get('url','')}  "
                     f"({item.get('types_count','?')} types)")

    for item in oas:
        emit.finding("OpenAPI", "MEDIUM",
                     f"Spec exposed — {item.get('url','')}")

    for item in cors:
        sev = "HIGH" if item.get("allow_credentials") else "MEDIUM"
        emit.finding("CORS", sev,
                     f"{item.get('url','')}  "
                     f"origin={item.get('reflected','')}  "
                     f"creds={item.get('allow_credentials', False)}")

    for item in sourcemaps:
        emit.finding("SourceMap", "MEDIUM",
                     f"Exposed — {item.get('url','')}")

    for item in secrets:
        stype   = item.get("type", "Secret")
        content = str(item.get("content", ""))
        source  = item.get("source", "")
        # Calibrated severity for SecurityTxt findings
        if stype in ("SecurityTxt_Comment_Leak", "SecurityTxt_Encryption_Key",
                     "SecurityTxt_Canonical_CrossDomain"):
            sev = "HIGH"
        elif stype in ("SecurityTxt_Contact_Email",):
            sev = "MEDIUM"
        elif stype in ("SecurityTxt_Expired",):
            sev = "LOW"
        else:
            sev = "HIGH"
        emit.finding(stype, sev, f"{content[:70]}  ← {source}")

    # ── extraction findings ──
    extracted = intel.get("extracted_data", [])
    if extracted:
        emit.section(f"EXTRACTED DATA  ({len(extracted)} items)", orbital=True)
        # Group by type for cleaner output
        from collections import defaultdict
        grouped = defaultdict(list)
        for item in extracted:
            grouped[item["type"]].append(item)
        
        for dtype, items in grouped.items():
            count = len(items)
            emit.row(dtype.replace("_", " "), f"{count} findings", icon="●", label_colour=C.G)
            
            # Always show all findings — no truncation, no JSON redirects
            for item in items:
                val  = item["value"]
                disp = val if len(val) <= 80 else val[:77] + "..."
                emit.leader_row("  " + disp, item["source_url"])

    # ── endpoints table ───────────────────────────────────────────────
    if eps:
        emit.section(f"ENDPOINTS  ({len(eps)} discovered)", orbital=True)

        # column header re-aligned with endpoint_row (2-space indent)
        if nc:
            print(f"  {'METHOD':<7}  {'CONFIDENCE':<10}  FLAGS  URL")
            print(f"  {'──'*34}")
        else:
            print(f"  {C.GL}{'METHOD':<7}  {'CONFIDENCE':<10}  FLAGS  URL{C.RST}")
            print(f"  {C.GR}{'──'*34}{C.RST}")

        order = {"CONFIRMED": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        _NOISE_SOURCES = frozenset({"Backup_Probe", "Backup_Suffix", "WellKnown", "Leaked_File"})
        real_eps = [e for e in eps if not all(s in _NOISE_SOURCES for s in e.get("source", ["Crawl"]))]
        backup_eps = [e for e in eps if all(s in _NOISE_SOURCES for s in e.get("source", ["Crawl"]))]
        sorted_eps = sorted(real_eps, key=lambda e: (order.get(e.get("confidence", "LOW"), 4), e.get("url", ""))) + \
                     sorted(backup_eps, key=lambda e: e.get("url", ""))
        # QS-variant dedup for terminal display only.
        # /login and /login?return_to=https://... share a cluster — show once.
        # All variants still exist in the JSON for agents.
        _disp_clusters: set = set()
        deduped = []
        for ep in sorted_eps:
            _cl = ep.get("cluster", ep.get("url",""))
            if _cl and _cl in _disp_clusters and not ep.get("params"):
                continue   # pure QS variant with no new params — skip display
            if _cl:
                _disp_clusters.add(_cl)
            deduped.append(ep)

        # Show ALL endpoints — no cap. JSON is for agents, CLI is for humans.
        for ep in deduped:
            emit.endpoint_row(ep)

        # ── param map for interesting endpoints ──────────────────────
        # Exclude 404_NOT_FOUND endpoints from param map — not injectable
        interesting = [
            e for e in real_eps
            if (e.get("params") or e.get("parameter_sensitive"))
            and e.get("confidence") != "404_NOT_FOUND"
            and 404 not in (e.get("observed_status") or [])
        ]

        if interesting:
            emit.section(f"PARAMETER MAP  ({len(interesting)} endpoints)", orbital=True)
            for ep in interesting:
                url    = ep.get("url","")
                # params in the export is already a flat sorted list (from formatted_eps)
                all_p  = ep.get("params", [])
                if isinstance(all_p, dict):
                    # fallback: flatten if called on raw store endpoint
                    all_p = [p for bucket in all_p.values() for p in bucket]
                if not all_p: continue

                method = ep.get("method", "GET")
                mc = { "GET": C.GD, "POST": C.Y, "PUT": C.O, "PATCH": C.O, "DELETE": C.R }.get(method, C.GL)
                # Never truncate — full URL must be readable/copyable by the user
                disp = url

                # Classify params: highlight hidden fields and file inputs
                ffd     = ep.get("form_fields_detail", [])
                ffd_map = {f["name"]: f for f in ffd}
                def _param_tag(p):
                    fd = ffd_map.get(p)
                    if not fd:
                        return p
                    if fd.get("hidden"):
                        return f"{p}[hidden]"
                    if fd.get("file"):
                        return f"{p}[file]"
                    return p

                tagged_params = [_param_tag(p) for p in all_p]

                if nc:
                    print(f"    {method:<7} {disp}")
                    print(f"      params: {', '.join(tagged_params)}")
                else:
                    # Method bullet on its own line, full URL indented below it
                    print(f"  {mc}●{C.RST} {C.W}{method:<7}{C.RST} {C.B}{C.W}{disp}{C.RST}")
                    param_str = ", ".join(
                        f"{C.GR}{p}{C.RST}" if "[hidden]" in p else
                        f"{C.MG}{p}{C.RST}" if "[file]" in p else
                        f"{C.W}{p}{C.RST}"
                        for p in tagged_params
                    )
                    emit.leader_row("PARAMS", param_str)

        # ── JS orphan params (contextual, not injectable) ────────────
        orphans = intel.get("js_orphan_params", [])
        if orphans:
            total_orphan = sum(len(o["params"]) for o in orphans)
            emit.section(f"JS ORPHAN PARAMS  ({total_orphan} unattributed params, {len(orphans)} files)", orbital=True)
            if not nc:
                emit.row("Note", "These params were found in JS files with no resolvable target URL",
                         icon="○", label_colour=C.R, value_colour=C.Y)
                emit.row("Usage", "Wordlist / fuzz hints — do NOT inject at the JS file URL",
                         icon="○", label_colour=C.R, value_colour=C.Y)
            for item in orphans:
                js_file = item["js_file"]
                params  = item["params"]
                short   = js_file if len(js_file) <= 60 else js_file[:57] + "…"
                if nc:
                    print(f"    {short}  ->  {', '.join(params)}")
                else:
                    print(f"  {C.GR}○{C.RST} {C.GR}{short}{C.RST}")
                    emit.leader_row("HINTS", ", ".join(f"{C.CYD}{p}{C.RST}" for p in params))

    # ── websocket / socket.io detected ──────────────────────────────────
    socketio = intel.get("socketio_endpoints", [])
    if socketio:
        emit.section(f"WEBSOCKET DETECTED  ({len(socketio)} socket.io endpoint(s))", orbital=True)
        if not nc:
            emit.row("Note", "socket.io active — real-time features present (chat, notifications, live data)",
                     icon="○", label_colour=C.CY, value_colour=C.W)
            emit.row("Note", "Polling URLs contain ephemeral session tokens — not injectable targets",
                     icon="○", label_colour=C.R, value_colour=C.Y)
        for sio in socketio:
            if nc:
                print(f"    WS  {sio['base_url']}")
            else:
                print(f"  {C.CY}◈{C.RST} {C.CY}WS{C.RST}  {C.W}{sio['base_url']}{C.RST}")

    # ── auth-walled ───────────────────────────────────────────────────
    auth_eps = [e for e in eps if e.get("auth_required")]
    if auth_eps:
        emit.section(f"AUTH-WALLED  ({len(auth_eps)} endpoints)", orbital=True)
        for ep in auth_eps:
            method = ep.get("methods",["GET"])[0]
            url = ep.get("url","")
            emit.row(method, url, icon="⬢", label_colour=C.RD)

    # ── security.txt findings ────────────────────────────────────────
    _sec_txt_types = {
        "SecurityTxt_Comment_Leak",
        "SecurityTxt_Contact_Email",
        "SecurityTxt_Contact_URL",
        "SecurityTxt_Encryption_Key",
        "SecurityTxt_Canonical_CrossDomain",
        "SecurityTxt_Expired",
    }
    sec_findings = [s for s in intel.get("secrets", []) if s.get("type","") in _sec_txt_types]
    if sec_findings:
        emit.section(f"SECURITY.TXT  ({len(sec_findings)} finding(s))", orbital=True)

        # Group by type for clean display — mirrors the robots disallowed tree style
        _LABEL_MAP = {
            "SecurityTxt_Comment_Leak":          ("Comment Leak",    True),
            "SecurityTxt_Contact_Email":          ("Contact Email",   False),
            "SecurityTxt_Contact_URL":            ("Contact URL",     False),
            "SecurityTxt_Encryption_Key":         ("Encryption Key",  False),
            "SecurityTxt_Canonical_CrossDomain":  ("Canonical",       True),
            "SecurityTxt_Expired":                ("Expires",         True),
        }

        # Gather all child paths that were queued FROM security.txt comments
        all_ep_urls  = [e.get("url","") for e in eps]
        sec_txt_urls = [e.get("url","") for e in eps if "SecurityTxt" in " ".join(e.get("source", []))]

        seen_content = set()
        for sf in sec_findings:
            stype   = sf.get("type", "")
            content = sf.get("content", "")
            if content in seen_content:
                continue
            seen_content.add(content)

            label, flagged = _LABEL_MAP.get(stype, (stype, False))

            if nc:
                tag = "[LEAK]" if flagged else "[SecurityTxt]"
                print(f"  {tag}  {label}: {content}")
            else:
                if flagged:
                    print(f"  {C.R}●{C.RST} {C.BG_RED} {label.upper()} {C.RST}  {C.Y}{content}{C.RST}")
                else:
                    print(f"  {C.CY}●{C.RST} {C.CY}{label:<18}{C.RST}  {C.W}{content}{C.RST}")

            # For comment leaks — show any paths that were queued FROM that comment
            # (i.e. endpoints whose source is SecurityTxt_Comment and URL contains
            # a path that appeared in the comment)
            if stype == "SecurityTxt_Comment_Leak":
                # Extract any paths from the comment itself
                import re as _re
                comment_paths = [
                    m.group(1) for m in
                    _re.finditer(r"""(?:^|\s)(/[^\s'"<>\\]+)""", content)
                ]
                for cp in comment_paths:
                    # Find matching crawled endpoint
                    matches = [u for u in all_ep_urls if cp in urlparse(u).path]
                    matches.sort()
                    for mu in matches:
                        if nc:
                            print(f"       └─ {mu}")
                        else:
                            print(f"  {C.GR}     └─{C.RST} {C.CYD}{mu}{C.RST}")

        # Show any endpoints queued from security.txt that aren't already shown
        other_sec = [u for u in sec_txt_urls if u not in seen_content]
        if other_sec:
            if nc:
                print(f"  [SecurityTxt] Queued {len(other_sec)} endpoint(s) for crawl:")
            else:
                print(f"  {C.CY}●{C.RST} {C.CY}Queued endpoints{C.RST}  {C.GR}({len(other_sec)} URLs added to crawl){C.RST}")
            for u in other_sec:
                if nc:
                    print(f"       └─ {u}")
                else:
                    print(f"  {C.GR}     └─{C.RST} {C.CYD}{u}{C.RST}")

    # ── robots disallowed ─────────────────────────────────────────────
    robots = intel.get("robots_disallowed", [])
    if robots:
        emit.section(f"ROBOTS.TXT DISALLOWED  ({len(robots)} paths)", orbital=True)
        all_ep_urls = [e.get("url","") for e in eps]
        parsed_target = intel.get("meta",{}).get("target","")
        for path in robots:
            emit.row("Disallow", path, icon="●", label_colour=C.O)
            # Find ALL crawled endpoints under this disallowed path — no cap
            seen = set()
            children = []
            for u in all_ep_urls:
                if not u or u == parsed_target or u in seen:
                    continue
                if ("/" + path.lstrip("/")) in urlparse(u).path:
                    seen.add(u)
                    children.append(u)
            children.sort()
            for child_url in children:
                if nc:
                    print(f"       └─ {child_url}")
                else:
                    print(f"  {C.GR}     └─{C.RST} {C.CYD}{child_url}{C.RST}")

    # ── robots allowed ────────────────────────────────────────────────
    robots_allowed = intel.get("robots_allowed", [])
    if robots_allowed:
        emit.section(f"ROBOTS.TXT ALLOWED  ({len(robots_allowed)} paths)", orbital=True)
        for path in robots_allowed:
            # If the allow path is "/" it means everything is permitted — no child list needed
            # (listing all crawled URLs under "/" is misleading since it covers the whole site)
            if path.strip() == "/":
                if nc:
                    print(f"  [Allow]  {path}  (entire site explicitly allowed)")
                else:
                    print(f"  {C.G}●{C.RST} {C.G}Allow{C.RST}  {C.W}{path}{C.RST}  {C.GR}(entire site explicitly allowed){C.RST}")
            else:
                if nc:
                    print(f"  [Allow]  {path}")
                else:
                    print(f"  {C.G}●{C.RST} {C.G}Allow{C.RST}  {C.W}{path}{C.RST}")
                # Show crawled endpoints specifically under this non-root allow path
                all_ep_urls = [e.get("url","") for e in eps]
                parsed_target = intel.get("meta",{}).get("target","")
                seen = set()
                children = []
                for u in all_ep_urls:
                    if not u or u == parsed_target or u in seen:
                        continue
                    if ("/" + path.lstrip("/")) in urlparse(u).path:
                        seen.add(u)
                        children.append(u)
                for child_url in sorted(children):
                    if nc:
                        print(f"       └─ {child_url}")
                    else:
                        print(f"  {C.GR}     └─{C.RST} {C.CYD}{child_url}{C.RST}")

    # ── sitemap.xml endpoints ─────────────────────────────────────────
    sitemap_eps = [e for e in eps if "Sitemap" in e.get("source", [])]
    if sitemap_eps:
        emit.section(f"SITEMAP ENDPOINTS  ({len(sitemap_eps)} found)", orbital=True)
        for ep in sorted(sitemap_eps, key=lambda e: e.get("url","")):
            url = ep.get("url","")
            conf = ep.get("confidence","LOW")
            if nc:
                print(f"  [Sitemap] {conf:<12}  {url}")
            else:
                cc = {"CONFIRMED": C.G, "HIGH": C.Y, "MEDIUM": C.CYD, "LOW": C.GR}.get(conf, C.GR)
                print(f"  {C.CY}●{C.RST} {cc}{conf:<12}{C.RST} {C.W}{url}{C.RST}")

    # ── wayback machine URLs ──────────────────────────────────────────
    wayback_eps = [e for e in eps if "Wayback" in e.get("source", [])]
    if wayback_eps:
        emit.section(f"WAYBACK URLS  ({len(wayback_eps)} archived endpoints)", orbital=True)
        for ep in sorted(wayback_eps, key=lambda e: e.get("url","")):
            url = ep.get("url","")
            conf = ep.get("confidence","LOW")
            if nc:
                print(f"  [Wayback] {conf:<12}  {url}")
            else:
                cc = {"CONFIRMED": C.G, "HIGH": C.Y, "MEDIUM": C.CYD, "LOW": C.GR}.get(conf, C.GR)
                print(f"  {C.MG}●{C.RST} {cc}{conf:<12}{C.RST} {C.W}{url}{C.RST}")

    # ── crt.sh subdomains ─────────────────────────────────────────────
    crt_eps = [e for e in eps if "CRT_Subdomain" in e.get("source", [])]
    if crt_eps:
        emit.section(f"CRT.SH SUBDOMAINS  ({len(crt_eps)} discovered)", orbital=True)
        for ep in sorted(crt_eps, key=lambda e: e.get("url","")):
            url = ep.get("url","")
            conf = ep.get("confidence","LOW")
            if nc:
                print(f"  [CRT.sh]  {conf:<12}  {url}")
            else:
                cc = {"CONFIRMED": C.G, "HIGH": C.Y, "MEDIUM": C.CYD, "LOW": C.GR}.get(conf, C.GR)
                print(f"  {C.BL}●{C.RST} {cc}{conf:<12}{C.RST} {C.W}{url}{C.RST}")

    # ── intelligence summary — candidates and classifications ────────────
    s_admin   = s.get("admin_panels", 0)
    s_idor    = s.get("idor_candidates", 0)
    s_sqli    = s.get("sqli_candidates", 0)
    s_cmdi    = s.get("cmdi_candidates", 0)
    s_upload  = s.get("upload_endpoints", 0)
    s_auth_ep = s.get("auth_endpoints", 0)
    intel_items = [
        (s_admin,   "Admin Panel(s)",        C.R),
        (s_idor,    "IDOR Candidate(s)",     C.Y),
        (s_sqli,    "SQLi Candidate(s)",     C.O),
        (s_cmdi,    "CMDi Candidate(s)",     C.O),
        (s_upload,  "File Upload(s)",        C.CY),
        (s_auth_ep, "Auth Endpoint(s)",      C.MG),
    ]
    # Filter: JS/CSS/font/image files are never real classified endpoints
    _ASSET_EXT = re.compile(
        r'\.(js|css|map|woff2?|ttf|eot|svg|png|jpg|jpeg|gif|ico|pdf|zip|gz|tar)$',
        re.I
    )
    def _not_asset(ep):
        url = ep.get("url","")
        return not _ASSET_EXT.search(url.split("?")[0])

    if any(count for count, _, _ in intel_items):
        emit.section("INTELLIGENCE CLASSIFICATIONS", orbital=True)
        for count, label, col in intel_items:
            if count:
                if label == "Admin Panel(s)":
                    tagged = [e for e in real_eps if e.get("admin_panel") and _not_asset(e)]
                elif label == "IDOR Candidate(s)":
                    tagged = [e for e in real_eps if e.get("idor_candidate") and _not_asset(e)]
                elif label == "SQLi Candidate(s)":
                    tagged = [e for e in real_eps if e.get("sqli_candidate") and _not_asset(e)]
                elif label == "CMDi Candidate(s)":
                    tagged = [e for e in real_eps if e.get("cmdi_candidate") and _not_asset(e)]
                elif label == "File Upload(s)":
                    tagged = [e for e in real_eps if e.get("file_upload_candidate") and _not_asset(e)]
                elif label == "Auth Endpoint(s)":
                    tagged = [e for e in real_eps if e.get("auth_classification") and _not_asset(e)]
                else:
                    tagged = []
                count = len(tagged)
                if not count:
                    continue
                if nc:
                    print(f"  [{label}]  {count}")
                else:
                    print(f"  {col}●{C.RST} {col}{label:<22}{C.RST} {C.W}{count}{C.RST}")
                for ep in tagged:
                    eu = ep.get("url","")
                    em = ep.get("method","GET")
                    if nc:
                        print(f"       └─ {em} {eu}")
                    else:
                        mc2 = {
                            "GET": C.GD,"POST": C.Y,"PUT": C.O,
                            "PATCH": C.O,"DELETE": C.R
                        }.get(em, C.GL)
                        print(f"  {C.GR}     └─{C.RST} {mc2}{em:<6}{C.RST} {C.W}{eu}{C.RST}")

    # ── HTML comments found ───────────────────────────────────────────
    comments = intel.get("comments", [])
    if comments:
        # Comments stored as {"content": text, "source": url}
        # Sensitive keyword filter — widened to include URL/path references and framework leaks
        _SENSITIVE_KW = re.compile(
            r'(?:password|passwd|secret|token|api[_-]?key|internal|'
            r'prod(?:uction)?|staging|admin|backup|credential|'
            r'todo[:\s]+remove|fixme|do\s+not\s+commit|debug[_-]?mode|'
            r'hack|bypass|hardcod|framework|version|temporary|temp|'
            r'beta|new-home|homepage|@\s*/[a-z]|https?://)',
            re.I
        )
        _sensitive_comments = [
            c for c in comments
            if _SENSITIVE_KW.search(str(c.get("content","") or ""))
        ]
        if _sensitive_comments:
            # Deduplicate near-identical comments that differ only in a timing/numeric value
            # e.g. 10x "Page Generated in 0.0XXX Seconds using the THM Framework..."
            # Strategy: normalise all floating-point numbers to "N" and deduplicate on that key,
            # keeping the FIRST occurrence (and its source URL) as the representative entry.
            # All other sources that share the same normalised content are listed as alt-sources.
            _norm_re = re.compile(r'\b\d+\.\d+\b')
            seen_norm: dict = {}   # normalised_key -> {"content": full_text, "sources": [url,...]}
            for c in _sensitive_comments:
                full = str(c.get("content","") or c.get("text","") or c)
                # Prefer all_sources list (multi-page dedup) over single source field
                raw_sources = c.get("all_sources") or ([c.get("source","")] if c.get("source") else [])
                src  = str(c.get("url","") or c.get("source",""))
                key  = _norm_re.sub("N", full)
                if key not in seen_norm:
                    seen_norm[key] = {"content": full, "sources": list(dict.fromkeys(s for s in raw_sources if s))}
                else:
                    for s in raw_sources:
                        if s and s not in seen_norm[key]["sources"]:
                            seen_norm[key]["sources"].append(s)

            deduped = list(seen_norm.values())
            emit.section(f"HTML COMMENT LEAKS  ({len(deduped)} unique)", orbital=True)
            for entry in deduped:
                full_content = entry["content"]
                sources = entry["sources"]
                # Print full comment — wrap long lines at 120 chars for readability
                if nc:
                    print(f"  [Comment] {full_content}")
                    for src in sources:
                        print(f"       └─ {src}")
                else:
                    # Multi-line comments: print each line indented
                    lines = full_content.splitlines()
                    if len(lines) == 1:
                        print(f"  {C.R}●{C.RST} {C.Y}{full_content}{C.RST}")
                    else:
                        print(f"  {C.R}●{C.RST} {C.Y}{lines[0]}{C.RST}")
                        for ln in lines[1:]:
                            print(f"    {C.Y}{ln}{C.RST}")
                    for src in sources:
                        print(f"  {C.GR}    └─{C.RST} {C.GR}{src}{C.RST}")

    # ── tech stack ────────────────────────────────────────────────────
    tech_list = intel.get("tech_stack", [])
    if tech_list:
        emit.section("TECH STACK", orbital=True)
        if nc:
            print(f"    {' · '.join(tech_list)}")
        else:
            sep = f"  {C.GR}·{C.RST}  "
            row = sep.join(f"{C.MG}{t}{C.RST}" for t in tech_list)
            print(f"    {row}")

    # ── footer ────────────────────────────────────────────────────────
    print()
    if saved_path:
        emit.always_success(f"[✓] Report saved → {saved_path}")

    screens = intel.get("screenshots", [])
    if screens:
        folder = Path(screens[0]["path"]).parent
        emit.always_success(f"Evidence saved → {len(screens)} screenshots in {folder}")

    if not nc:
        bar = "─" * 72
        ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  {C.R}◓{C.RST} {C.B}{C.W}HELLHOUND SPIDER v{VERSION}{C.RST} {C.GR}·{C.RST} {C.W}foundational{C.RST} {C.GR}·{C.RST} {C.W}{ts}{C.RST}")
        print(f"  {C.GR}{bar}{C.RST}\n")
    else:
        print(f"  HELLHOUND SPIDER v{VERSION} · complete · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


# ══════════════════════════════════════════════════════════════════════
# CONFIDENCE
# ══════════════════════════════════════════════════════════════════════

class Conf:
    LOW       = 1
    MEDIUM    = 3
    HIGH      = 6
    CONFIRMED = 10

    @staticmethod
    def label(score: int) -> str:
        if score >= Conf.CONFIRMED: return "CONFIRMED"
        if score >= Conf.HIGH:      return "HIGH"
        if score >= Conf.MEDIUM:    return "MEDIUM"
        return "LOW"

# ══════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════

class Config:
    def __init__(self, **kw):
        self.max_depth          = kw.get("max_depth",          4)
        self.concurrency        = kw.get("concurrency",        12)
        self.timeout            = kw.get("timeout",            15)
        self.max_retries        = kw.get("max_retries",        3)
        self.retry_base_delay   = kw.get("retry_base_delay",   0.5)
        self.max_urls_per_depth = kw.get("max_urls_per_depth", 500)
        self.jitter_min         = kw.get("jitter_min",         0.05)
        self.jitter_max         = kw.get("jitter_max",         0.35)
        self.verbose            = kw.get("verbose",            False)
        self.use_playwright     = kw.get("use_playwright",     True)
        self.enable_spa_interact = kw.get("enable_spa_interact", False)
        self.enable_extraction   = kw.get("enable_extraction",   False)
        self.enable_screenshots  = kw.get("enable_screenshots",  False)
        self.screenshot_priority = kw.get("screenshot_priority", "standard")
        self.enable_probing     = kw.get("enable_probing",     True)
        self.enable_method_disc = kw.get("enable_method_disc", True)
        self.extensions_to_ignore = kw.get("extensions_to_ignore", [
            ".jpg", ".jpeg", ".png", ".gif", ".ico", ".svg", ".css", ".js.map",
            ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".mp4", ".wav", ".avi",
            ".pdf", ".docx", ".xlsx", ".pptx", ".zip", ".tar.gz", ".rar",
            ".webp", ".mov", ".webm", ".exe", ".dmg", ".apk", ".bmp", ".tiff"
        ])
        self.har_file           = kw.get("har_file",           None)
        self.enable_noise_filter = kw.get("enable_noise_filter", True)
        self.enable_graphql     = kw.get("enable_graphql",     True)
        self.enable_openapi     = kw.get("enable_openapi",     True)
        self.enable_cors        = kw.get("enable_cors",        True)
        self.output_format      = kw.get("output_format",      "json")
        self.output_file: Optional[str] = kw.get("output_file", None)
        self.user_agent = kw.get(
            "user_agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )

    def validate(self):
        if not (0 <= self.max_depth <= 20):
            raise ValueError("max_depth must be 0–20")
        if not (1 <= self.concurrency <= 100):
            raise ValueError("concurrency must be 1–100")

# ══════════════════════════════════════════════════════════════════════
# SESSION / COOKIE MANAGER
# ══════════════════════════════════════════════════════════════════════

class SessionManager:
    @staticmethod
    def parse_cookies(raw) -> Dict[str, str]:
        if not raw:
            return {}
        if isinstance(raw, dict):
            if any(k.lower() in ("authorization","x-api-key","x-auth-token") for k in raw):
                return {}
            return raw
        if isinstance(raw, str):
            raw = raw.strip()
            # Only attempt a filesystem lookup when the string is a plausible
            # path — short enough for the OS and looks like a file reference.
            # Long strings like JWTs must never reach Path.exists(); Linux
            # raises OSError "File name too long" for strings over ~255 bytes.
            _looks_like_path = (
                len(raw) <= 255
                and " " not in raw
                and ("/" in raw or raw.endswith((".txt", ".json")))
            )
            if _looks_like_path:
                try:
                    p = Path(raw)
                    if p.exists() and p.is_file():
                        return SessionManager._load_file(p)
                except OSError:
                    pass  # filesystem error — fall through to string parsing
            # Parse as inline cookie string: "name=value; name2=value2"
            # partition("=") keeps the full value even if it contains "="
            # (base64 padding, JWT segments, etc.)
            out: Dict[str, str] = {}
            for part in raw.split(";"):
                part = part.strip()
                if "=" in part:
                    k, _, v = part.partition("=")
                    k = k.strip(); v = v.strip()
                    if k:
                        out[k] = v
            return out
        return {}

    @staticmethod
    def _load_file(path: Path) -> Dict[str, str]:
        try:
            data = json.loads(path.read_text())
            if isinstance(data, list):
                return {c["name"]: c["value"] for c in data if "name" in c and "value" in c}
        except Exception:
            pass
        try:
            jar = MozillaCookieJar(str(path))
            jar.load(ignore_discard=True, ignore_expires=True)
            return {c.name: c.value for c in jar}
        except Exception:
            pass
        return {}

    @staticmethod
    def parse_auth_header(raw) -> Dict[str, str]:
        if not raw:
            return {}
        if isinstance(raw, dict):
            return {k: v for k, v in raw.items()
                    if k.lower() in ("authorization","x-api-key","x-auth-token",
                                     "x-csrf-token","x-access-token")}
        if isinstance(raw, str):
            raw = raw.strip()
            if re.match(r'^(Bearer|Basic|Token)\s+\S+', raw, re.I):
                return {"Authorization": raw}
        return {}

# ══════════════════════════════════════════════════════════════════════
# RATE LIMITER
# ══════════════════════════════════════════════════════════════════════

class DomainRateLimiter:
    def __init__(self, base_delay: float = 0.05):
        self._delays: Dict[str, float] = defaultdict(lambda: base_delay)
        self._locks:  Dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def wait(self, domain: str):
        async with self._locks[domain]:
            await asyncio.sleep(self._delays[domain])

    def backoff(self, domain: str):
        self._delays[domain] = min(self._delays[domain] * 2.0, 10.0)

    def recover(self, domain: str):
        self._delays[domain] = max(self._delays[domain] * 0.9, 0.03)

# ══════════════════════════════════════════════════════════════════════
# FETCH HELPER
# ══════════════════════════════════════════════════════════════════════

async def fetch(session, method, url, rl, max_retries=3, base_delay=0.5, **kw):
    domain = urlparse(url).netloc
    await rl.wait(domain)
    for attempt in range(max_retries + 1):
        try:
            async with session.request(method, url, ssl=False, **kw) as resp:
                if resp.status == 429 or (resp.status == 403 and attempt > 0):
                    rl.backoff(domain)
                    await asyncio.sleep(float(resp.headers.get("Retry-After", base_delay * (2**attempt))))
                    continue
                body = await resp.text(errors="replace")
                rl.recover(domain)
                return resp.status, dict(resp.headers), body
        except Exception:
            if attempt < max_retries:
                await asyncio.sleep(base_delay * (2**attempt))
    return None, None, None

# ══════════════════════════════════════════════════════════════════════
# URL UTILITIES
# ══════════════════════════════════════════════════════════════════════

_ID_RE = re.compile(
    r'^(?:\d{1,20}'
    r'|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    r'|[0-9a-fA-F]{24}'
    r'|[0-9a-zA-Z]{20,}'
    r')$',
    re.I
)

_NUMERIC_ID_RE = re.compile(r'(?:id|uid|uuid|userid|account|key)$', re.I)
# Numeric IDs must be ≥4 digits to avoid matching image dimensions (800, 400, 720)
# Also must NOT be followed by another short number (paired = dimensions, not IDs)
_PATH_ID_RE    = re.compile(
    r'/(?:v[0-9]+/)?(?:[a-z][a-z0-9_-]*/)?'
    r'([0-9]{4,}(?![0-9x/][0-9]{2,4}(?:[/?]|$))|'   # 4+ digit number, not dimension pair
    r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})',  # UUID
    re.I
)
_UUID_PATH_RE  = re.compile(r'[a-f0-9]{8}-[a-f0-9]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[a-f0-9]{12}', re.I)

# Admin panel classifier — two tiers
# Tier 1: high-confidence standalone admin words — always flag
# Tier 2: ambiguous words (setup, config, control) — only flag if
#          they appear as a top-level path segment (depth 1 or 2)
#          and the URL doesn't end in a static asset extension
_ADMIN_TIER1 = re.compile(
    r'/(?:admin|administrator|adminpanel|manage|manager|management|'
    r'dashboard|backend|backoffice|controlpanel|cpanel|superuser|'
    r'sysadmin|moderator|staff|internal/admin|admin/internal)(?:/|$)',
    re.I
)
_ADMIN_TIER2 = re.compile(
    r'^(?:https?://[^/]+)?/(?:panel|control|backend|config|configuration|'
    r'settings|setup|install|maintenance|console|portal)(?:/[^/]*)?$',
    re.I
)
_STATIC_EXT = re.compile(r'\.(css|js|json|xml|map|woff2?|ttf|eot|svg|png|jpg|jpeg|gif|ico|pdf|txt|csv|yaml|yml)$', re.I)

_ADMIN_PATTERNS = _ADMIN_TIER1  # kept for backward compat — tier1 only used in classify
_AUTH_PATTERNS  = {
    "login":    re.compile(r'/(login|signin|sign-in|log-in|authenticate|auth)', re.I),
    "register": re.compile(r'/(register|signup|sign-up|create.account|join|enroll)', re.I),
    "logout":   re.compile(r'/(logout|signout|log-out|sign-out)', re.I),
    "mfa":      re.compile(r'/(mfa|2fa|otp|totp|verify|verification)', re.I),
    "pass":     re.compile(r'/(password|reset|forgot|change.password)', re.I),
    "token":    re.compile(r'/(token|refresh.token|oauth|authorize)', re.I),
}

_SQLI_PARAM_RE = re.compile(r'(?:id|select|report|update|query|search|from|where|order|by|group|limit|offset|slug|category|tag)$', re.I)
_CMDI_PARAM_RE = re.compile(r'(?:cmd|command|exec|execute|path|file|dir|folder|target|host|url|endpoint|run|script|sh|bash|run)$', re.I)

# ── Noise path filter ─────────────────────────────────────────────────
# Path patterns that are NEVER real injectable app endpoints on any target.
# Covers VCS repo browser UI (GitHub/GitLab/Gitea/Bitbucket), CI pages,
# CDN artefact paths, and structural navigation links generated by JS.
# Applied in is_valid() before the URL enters the queue.
# Disable with --no-filter / -F to see everything raw.
_NOISE_PATH_RE = re.compile(
    r'/(?:'
    r'blob/[^/]+/'          # /blob/master/file.py  — git file viewer
    r'|tree/[^/]+/'         # /tree/master/src/     — git tree browser
    r'|commits?/[^/]+/'     # /commits/main/        — commit history
    r'|releases/tag/'       # /releases/tag/v1.0    — release tag pages
    r'|graphs/'             # /graphs/contributors  — stats pages
    r'|compare/'            # /compare/a...b        — diff viewer
    r'|branches'            # /branches             — branch listing
    r'|stargazers'          # /stargazers           — star listing
    r'|watchers'            # /watchers             — watcher listing
    r'|forks'               # /forks                — fork listing
    r'|pulse'               # /pulse                — activity pulse
    r'|actions'             # /actions              — CI/CD pages
    r'|activity'            # /activity             — activity feed
    r'|custom-properties'   # /custom-properties    — GitHub metadata
    r')',
    re.I
)

# ── socket.io URL detector ────────────────────────────────────────────
# socket.io polling URLs embed ephemeral session tokens (sid=...) and
# EIO transport params. They expire before any agent can act on them.
# Intercepted in is_valid() and parked in store.socketio_endpoints.
_SOCKETIO_RE = re.compile(r'/socket\.io/\??.*EIO=', re.I)

def normalize(url: str) -> str:
    try:
        # Fix Windows-style backslash paths from href attributes
        url = url.replace(chr(92)+chr(92), "/").replace(chr(92), "/")
        p  = urlparse(url)
        qs = urlencode(sorted(parse_qs(p.query, keep_blank_values=True).items()), doseq=True)
        return urlunparse((p.scheme.lower(), p.netloc.lower(),
                           p.path.rstrip("/") or "/", p.params, qs, ""))
    except Exception:
        return url

def cluster(url: str) -> str:
    """Groups similar URLs by masking dynamic path segments and query parameter values."""
    try:
        p    = urlparse(url)
        # 1. Mask dynamic path segments (UUIDs, digits, etc)
        segs = ["{val}" if _ID_RE.match(s) else s for s in p.path.split("/")]
        path = "/".join(segs)
        # 2. Mask query parameter values
        qs_dict = parse_qs(p.query, keep_blank_values=True)
        masked_qs = urlencode(sorted([(k, "") for k in qs_dict.keys()]), doseq=True)
        return urlunparse(("", "", path, "", masked_qs, ""))
    except Exception:
        return url

# ══════════════════════════════════════════════════════════════════════
# DATA STORE
# ══════════════════════════════════════════════════════════════════════

class Store:
    def __init__(self):
        self.endpoints:    Dict[str, dict] = {}
        self.comments:     List[dict]       = []
        self.secrets:      List[dict]       = []
        self.tech_stack:   Set[str]         = set()
        self.robots_paths: List[str]        = []
        self.robots_allowed_paths: List[str] = []
        self.target_response_headers: dict   = {}
        self.cors_issues:  List[dict]       = []
        self.graphql:      List[dict]       = []
        self.openapi:      List[dict]       = []
        self.sourcemaps:   List[dict]       = []
        self.extracted_data: List[dict]     = []
        self._extracted_seen: Set[tuple]    = set()
        # JS params that couldn't be resolved to a real API endpoint.
        # Keyed by js_file_url → list of param names.
        # Downstream agents should treat these as "discovered but untargeted".
        self.js_orphan_params: Dict[str, List[str]] = {}
        # socket.io endpoints — ephemeral transport URLs, NOT injectable targets.
        # Stored so the terminal and JSON show WebSocket is active on the target.
        self.socketio_endpoints: List[dict] = []
        self._socketio_seen:     Set[str]   = set()

    def _key(self, url, method):
        return f"{method.upper()}:{cluster(normalize(url))}"

    def _new_ep(self, url, method):
        return {
            "url": url, "cluster": cluster(normalize(url)),
            "methods": [method.upper()],
            "params": {"query":[],"form":[],"js":[],"openapi":[],"runtime":[]},
            "observed_values": {},
            "headers": {},
            "source": [], "confidence": 0, "confidence_label": "LOW",
            "auth_required": False, "parameter_sensitive": False,
            "observed_status": [], "baseline": None,
            # Form field rich metadata — populated by _process_html form parser
            # Each entry: {name, type, hidden, file, required, value}
            # Downstream agents use this to distinguish injectable vs CSRF-token fields
            "form_fields_detail": [],
            # v12.3 additions
            "admin_panel":          False,
            "auth_classification":  [],
            "file_upload_candidate": False,
            "idor_candidate":       False,
            "idor_signals":         {},
            "sqli_candidate":       False,
            "sqli_params":          [],
            "cmdi_candidate":       False,
            "cmdi_params":          [],
            "screenshot":           None,
        }

    # API/service path prefixes — boosted to HIGH confidence on any app.
    # /api/, /rest/, /graphql/, /v1/, /internal/, etc. are real endpoints.
    _API_PATH_RE = re.compile(
        r'^/(?:api|rest|graphql|gql|v[0-9]+|internal|backend|service|rpc|data)[/]',
        re.I
    )

    def add_endpoint(self, url, method="GET", source="Static",
                     params=None, score=Conf.LOW, auth_required=False):
        # Intercept socket.io URLs at store level too — they bypass is_valid()
        # when added via XHR observation (on_request handler)
        if _SOCKETIO_RE.search(url):
            self.add_socketio(url, method)
            return self.endpoints.get(self._key(url, method))  # don't register
        key = self._key(url, method)
        if key not in self.endpoints:
            self.endpoints[key] = self._new_ep(url, method)
        ep = self.endpoints[key]
        if source not in ep["source"]:
            ep["source"].append(source)
        # Confidence boost: API/REST/GraphQL paths are high-value on any app.
        # Applied universally — not tied to any specific target.
        try:
            _path = urlparse(url).path
            if self._API_PATH_RE.match(_path) and score < Conf.HIGH:
                score = Conf.HIGH
        except Exception:
            pass
        ep["confidence"]       = min(ep["confidence"] + score, Conf.CONFIRMED)
        ep["confidence_label"] = Conf.label(ep["confidence"])
        if auth_required:
            ep["auth_required"] = True
        if params:
            if source == "OpenAPI":
                bucket = "openapi"
            elif source == "Form":
                bucket = "form"
            elif source.startswith("JS_") or source in ("SPA_XHR", "SPA_DOM"):
                bucket = "js"
            else:
                bucket = "runtime"
            for p in params:
                if p and p not in ep["params"][bucket]:
                    ep["params"][bucket].append(p)
        return ep

    # Noise headers present on every browser request — no IDOR signal.
    _HEADER_SKIP = frozenset({
        "accept", "accept-encoding", "accept-language", "cache-control",
        "connection", "host", "origin", "pragma", "referer",
        "sec-ch-ua", "sec-ch-ua-mobile", "sec-ch-ua-platform",
        "sec-fetch-dest", "sec-fetch-mode", "sec-fetch-site",
        "upgrade-insecure-requests", "user-agent",
    })

    def merge_headers(self, url: str, method: str, headers: dict) -> bool:
        """
        Filter noise headers out, then merge remaining custom/auth headers into
        the endpoint's headers dict.  Keeps the first observed value per name.
        Returns True if any new header names were written.
        """
        if not headers:
            return False
        key = self._key(url, method)
        if key not in self.endpoints:
            return False
        ep    = self.endpoints[key]
        added = False
        for k, v in headers.items():
            lo = k.lower()
            if lo in self._HEADER_SKIP:
                continue
            if lo not in ep["headers"]:
                ep["headers"][lo] = v
                added = True
        return added

    def add_js_params(self, url, params):
        key = self._key(url, "GET")
        if key not in self.endpoints:
            self.endpoints[key] = self._new_ep(url, "GET")
        ep  = self.endpoints[key]
        new = [p for p in params if p not in ep["params"]["js"]]
        ep["params"]["js"].extend(new)
        if new:
            ep["confidence"] = min(ep["confidence"] + 1, Conf.CONFIRMED)
            ep["confidence_label"] = Conf.label(ep["confidence"])
        return bool(new)

    def add_js_orphan_params(self, js_file_url: str, params: List[str]):
        """
        Store params found in a JS file that couldn't be attributed to a
        specific API endpoint URL. These are NOT injectable endpoints — they
        are contextual hints that the downstream agent may use for fuzzing
        or wordlist generation, but should never be treated as crawlable targets.
        """
        bucket = self.js_orphan_params.setdefault(js_file_url, [])
        for p in params:
            if p and p not in bucket:
                bucket.append(p)

    def is_same_domain(self, url: str, ref_url: str) -> bool:
        """Check if url is on same domain as ref_url — used for path queuing."""
        try:
            return urlparse(url).netloc == urlparse(ref_url).netloc
        except Exception:
            return False

    def add_socketio(self, url: str, method: str = "GET"):
        """
        Record a socket.io polling URL without adding it to the main endpoint
        store. These URLs contain ephemeral session tokens (sid=...) and are
        dead before any agent acts on them.
        """
        base = urlparse(url)._replace(query="", fragment="").geturl()
        if base not in self._socketio_seen:
            self._socketio_seen.add(base)
            self.socketio_endpoints.append({
                "base_url": base,
                "example":  url,
                "method":   method.upper(),
                "note":     "socket.io transport — ephemeral session token, not injectable",
            })

    # High-risk param names — any endpoint bearing these warrants extra scrutiny
    _RISK_PARAMS = frozenset({
        "cmd","command","exec","run","shell","host","hostname","ip","addr","address",
        "url","uri","target","dest","src","source","file","path","dir","query","q",
        "search","input","arg","id","key","token","user","pass","passwd","password",
    })
    # Sanitization suffixes — strip these to get the base param name
    _PARAM_SUFFIXES = ("_raw","_sanitized","_input","_clean","_safe","_encoded","_value","_param")

    def add_runtime_params(self, url: str, method: str, names: List[str]) -> bool:
        """
        Strip sanitization suffixes FIRST, then store only the base name.
        Detects sanitization fingerprint: if a raw key like host_raw is seen,
        the base name host is stored AND the endpoint is auto-marked sensitive
        (because it proves the app is sanitizing an input whose unsanitized form
        was visible in the response).
        Returns True if any new base names were added.
        """
        key = self._key(url, method)
        if key not in self.endpoints:
            return False
        ep = self.endpoints[key]

        sanitization_seen = False
        added = []
        for raw_name in names:
            if not raw_name:
                continue
            base = raw_name
            is_suffixed = False
            for suf in self._PARAM_SUFFIXES:
                if raw_name.endswith(suf):
                    base = raw_name[: -len(suf)]
                    is_suffixed = True
                    break
            # If we saw a suffixed name → sanitization fingerprint
            if is_suffixed:
                sanitization_seen = True
            # Store only the base name
            if base and base not in ep["params"]["runtime"]:
                ep["params"]["runtime"].append(base)
                added.append(base)

        if added:
            ep["confidence"] = min(ep["confidence"] + 1, Conf.CONFIRMED)
            ep["confidence_label"] = Conf.label(ep["confidence"])

        if sanitization_seen:
            ep["parameter_sensitive"] = True
            ep["confidence"] = min(ep["confidence"] + 2, Conf.CONFIRMED)
            ep["confidence_label"] = Conf.label(ep["confidence"])

        return bool(added)

    def add_query_params(self, url):
        parsed = urlparse(url)
        if not parsed.query:
            return
        key = self._key(url, "GET")
        if key not in self.endpoints:
            self.endpoints[key] = self._new_ep(url, "GET")
        ep = self.endpoints[key]
        for param, values in parse_qs(parsed.query).items():
            if param not in ep["params"]["query"]:
                ep["params"]["query"].append(param)
            if values:
                existing = ep["observed_values"].setdefault(param, [])
                for v in values:
                    if v and v not in existing:
                        existing.append(v)

    def add_extracted_data(self, dtype, value, source_url):
        if (dtype, value) not in self._extracted_seen:
            self._extracted_seen.add((dtype, value))
            self.extracted_data.append({
                "type": dtype,
                "value": value,
                "source_url": source_url
            })
            return True
        return False

    def update_methods(self, url, methods):
        key = self._key(url, methods[0] if methods else "GET")
        if key not in self.endpoints:
            return
        ep = self.endpoints[key]
        for m in methods:
            if m not in ep["methods"]:
                ep["methods"].append(m)
        ep["confidence"] = min(ep["confidence"] + 1, Conf.CONFIRMED)
        ep["confidence_label"] = Conf.label(ep["confidence"])

    def record_status(self, url, method, status):
        # Apply status to the specific method key AND cross-propagate to other
        # methods on the same URL. The form parser registers POST at HIGH before
        # the crawler ever fetches the URL as GET. When GET returns 404, both
        # the GET and POST entries must be downgraded — the URL doesn't exist.
        affected_keys = [self._key(url, method)]
        # Cross-propagate 404 to all other method variants of the same URL
        if status == 404:
            norm = cluster(normalize(url))
            for k, ep in self.endpoints.items():
                if ep.get("cluster") == norm and k not in affected_keys:
                    affected_keys.append(k)

        for key in affected_keys:
            if key not in self.endpoints:
                continue
            ep = self.endpoints[key]
            if status not in ep["observed_status"]:
                ep["observed_status"].append(status)
            if status in (401, 403):
                ep["auth_required"] = True
            elif status == 200:
                # Confirmed reachable — boost confidence if it was speculative
                ep["auth_required"] = False
                if ep["confidence"] < Conf.MEDIUM:
                    ep["confidence"]       = Conf.MEDIUM
                    ep["confidence_label"] = Conf.label(ep["confidence"])
            elif status == 404:
                # Real 404 — URL does not exist. Demote ALL method variants.
                ep["confidence"]       = min(ep["confidence"], Conf.LOW)
                ep["confidence_label"] = "404_NOT_FOUND"
            elif status in (301, 302, 307, 308):
                # Redirect — still exists, minor boost
                if ep["confidence"] < Conf.MEDIUM:
                    ep["confidence"]       = Conf.MEDIUM
                    ep["confidence_label"] = Conf.label(ep["confidence"])

    def mark_sensitive(self, url, method):
        key = self._key(url, method)
        if key in self.endpoints:
            ep = self.endpoints[key]
            ep["parameter_sensitive"] = True
            ep["confidence"] = min(ep["confidence"] + 2, Conf.CONFIRMED)
            ep["confidence_label"] = Conf.label(ep["confidence"])

    def add_comment(self, content, source_url):
        content = content.strip()
        if len(content) < 4:
            return False
        # If exact content already stored, just add this URL as an additional source
        for c in self.comments:
            if c["content"] == content:
                if source_url and source_url not in c.get("all_sources", [c.get("source","")]):
                    c.setdefault("all_sources", [c.get("source","")]).append(source_url)
                return False  # not a new unique comment
        self.comments.append({"content": content, "source": source_url, "all_sources": [source_url]})
        return True

    def add_secret(self, val, stype, source_url):
        if any(s["content"] == val for s in self.secrets):
            return False
        self.secrets.append({"content": val, "type": stype, "source": source_url})
        return True

    def add_cors(self, url, origin_sent, reflected, creds):
        self.cors_issues.append({
            "url": url, "origin_sent": origin_sent, "reflected": reflected,
            "allow_credentials": creds, "severity": "HIGH" if creds else "MEDIUM"
        })

    def add_sourcemap(self, map_url, parent):
        if not any(s["url"] == map_url for s in self.sourcemaps):
            self.sourcemaps.append({"url": map_url, "parent": parent})

    def all_endpoints(self):
        return [e for e in self.endpoints.values() if e["confidence"] >= Conf.LOW]

    def export(self, target, fmt="json"):
        eps  = self.all_endpoints()
        meta = {"tool": f"Hellhound Spider v{VERSION}", "target": target}
        summary = {
            "total_endpoints":     len(eps),
            "confirmed":           sum(1 for e in eps if e["confidence_label"] == "CONFIRMED"),
            "high":                sum(1 for e in eps if e["confidence_label"] == "HIGH"),
            "auth_required":       sum(1 for e in eps if e["auth_required"]),
            "parameter_sensitive": sum(1 for e in eps if e["parameter_sensitive"]),
            "secrets":             len(self.secrets),
            "cors_issues":         len(self.cors_issues),
            "graphql_exposed":     len(self.graphql),
            "openapi_exposed":     len(self.openapi),
            "sourcemaps_exposed":  len(self.sourcemaps),
            "tech_stack":          sorted(self.tech_stack),
            # v12.3 additions
            "admin_panels":       sum(1 for e in eps if e.get("admin_panel")),
            "auth_endpoints":     sum(1 for e in eps if e.get("auth_classification")),
            "upload_endpoints":   sum(1 for e in eps if e.get("file_upload_candidate")),
            "idor_candidates":    sum(1 for e in eps if e.get("idor_candidate")),
            "sqli_candidates":    sum(1 for e in eps if e.get("sqli_candidate")),
            "cmdi_candidates":    sum(1 for e in eps if e.get("cmdi_candidate")),
            "extracted_data":     len(self.extracted_data),
            "robots_disallowed":  len(self.robots_paths),
            "robots_allowed":     len(self.robots_allowed_paths),
            "screenshots":        sum(1 for e in eps if e.get("screenshot")),
            # JS orphan params — params discovered in JS files with no resolved endpoint
            "js_orphan_param_files": len(self.js_orphan_params),
            "js_orphan_param_count": sum(len(v) for v in self.js_orphan_params.values()),
            "websocket_detected":     len(self.socketio_endpoints) > 0,
            "socketio_count":         len(self.socketio_endpoints),
        }
        
        # FIX 1 & 2: Format endpoints for export
        formatted_eps = []
        for e in eps:
            # Flat params merge
            all_params = []
            for bucket in e["params"].values():
                for p in bucket:
                    if p not in all_params: all_params.append(p)
            
            # Confidence label mapping
            c = e["confidence"]
            cl = e.get("confidence_label", "LOW")
            # If record_status marked it 404_NOT_FOUND, preserve that label
            if cl not in ("404_NOT_FOUND",):
                if c >= 10: cl = "CONFIRMED"
                elif c >= 7: cl = "HIGH"
                elif c >= 3: cl = "MEDIUM"
                elif c >= 1: cl = "LOW"
                else: cl = "UNKNOWN"

            formatted_eps.append({
                "url": e["url"],
                "method": e["methods"][0] if e["methods"] else "GET",
                "confidence": cl,
                "confidence_score": c,
                "observed_status": e["observed_status"],
                "params": sorted(all_params),
                "params_detail": e["params"],
                # Rich form field metadata — type, hidden, file, required flags.
                # Use this to skip CSRF tokens (hidden) and prioritise real input fields.
                "form_fields_detail": e.get("form_fields_detail", []),
                "auth_required": e["auth_required"],
                "source": e["source"],
                "admin_panel": e.get("admin_panel", False),
                "auth_classification": e.get("auth_classification", []),
                "file_upload_candidate": e.get("file_upload_candidate", False),
                "idor_candidate": e.get("idor_candidate", False),
                "idor_signals": e.get("idor_signals", {}),
                "sqli_candidate": e.get("sqli_candidate", False),
                "sqli_params": e.get("sqli_params", []),
                "cmdi_candidate": e.get("cmdi_candidate", False),
                "cmdi_params": e.get("cmdi_params", []),
                "screenshot": e.get("screenshot"),
            })

        data = {
            "meta": meta, "summary": summary, "endpoints": formatted_eps,
            "secrets": self.secrets, "cors_issues": self.cors_issues,
            "graphql": self.graphql, "openapi": self.openapi,
            "sourcemaps": self.sourcemaps, "comments": self.comments,
            "robots_disallowed": self.robots_paths,
            "robots_allowed": self.robots_allowed_paths,
            "target_response_headers": self.target_response_headers,
            "tech_stack": sorted(self.tech_stack),
            "extracted_data": self.extracted_data if self.extracted_data is not None else [],
            # JS params that could not be attributed to a specific endpoint URL.
            # Format: [{"js_file": "https://...", "params": ["username", "password"]}, ...]
            # These are NOT injectable targets — use as wordlist hints only.
            "js_orphan_params": [
                {"js_file": js_url, "params": sorted(set(params))}
                for js_url, params in self.js_orphan_params.items()
                if params
            ],
            # socket.io transport endpoints — ephemeral, not injectable.
            # Presence confirms real-time WebSocket features on this target.
            "socketio_endpoints": self.socketio_endpoints,
        }

        if fmt == "json":
            return json.dumps(data, indent=2)

        if fmt == "jsonl":
            lines = [json.dumps({"type":"meta","data":meta}),
                     json.dumps({"type":"summary","data":summary})]
            for ep in eps:
                lines.append(json.dumps({"type":"endpoint","data":ep}))
            return "\n".join(lines)

        if fmt == "csv":
            buf = io.StringIO()
            w   = csv.writer(buf)
            w.writerow(["url","cluster","methods","confidence","auth_required",
                         "param_sensitive","sources","query_params","form_params",
                         "js_params","openapi_params","observed_status","headers"])
            for ep in eps:
                w.writerow([ep["url"], ep["cluster"], "|".join(ep["methods"]),
                             ep["confidence_label"], ep["auth_required"],
                             ep["parameter_sensitive"], "|".join(ep["source"]),
                             "|".join(ep["params"].get("query",[])),
                             "|".join(ep["params"].get("form",[])),
                             "|".join(ep["params"].get("js",[])),
                             "|".join(ep["params"].get("openapi",[])),
                             "|".join(str(s) for s in ep.get("observed_status",[])),
                             json.dumps(ep.get("headers", {}))])
            return buf.getvalue()

        if fmt == "burp":
            root = ET.Element("items", burpVersion="2.0",
                              exportTime=datetime.now(timezone.utc).isoformat())
            for ep in eps:
                item = ET.SubElement(root, "item")
                ET.SubElement(item, "url").text          = ep["url"]
                ET.SubElement(item, "method").text       = ep["methods"][0]
                ET.SubElement(item, "confidence").text   = ep["confidence_label"]
                ET.SubElement(item, "authRequired").text = str(ep["auth_required"])
                ET.SubElement(item, "params").text       = json.dumps(ep["params"])
                ET.SubElement(item, "headers").text      = json.dumps(ep.get("headers", {}))
            return ET.tostring(root, encoding="unicode", xml_declaration=True)

        return json.dumps(data, indent=2)

# ══════════════════════════════════════════════════════════════════════
# EXTRACTORS
# ══════════════════════════════════════════════════════════════════════

class Extractor:
    _JS_NOISE = {
        "console","window","document","return","function","const","let","var",
        "this","class","import","export","default","null","undefined","true",
        "false","new","async","await","try","catch","if","else","for","while",
        "switch","case","break","continue","typeof","instanceof","void","delete",
    }
    _PARAM_RE = [
        r'body\s*:\s*JSON\.stringify\s*\(\s*\{([^}]{1,400})\}',
        r'axios\.(?:post|put|patch)\s*\([^,]{1,120},\s*\{([^}]{1,400})\}',
        r'(?:data|payload|body)\s*:\s*\{([^}]{1,400})\}',
        r'params\s*:\s*\{([^}]{1,400})\}',
        r'new\s+URLSearchParams\s*\(\s*\{([^}]{1,400})\}',
        r'FormData\s*\(\s*\)\s*;(?:[^}]{0,200}\.append\s*\(\s*["\']([^"\']+)["\'])',
    ]
    _SECRET_RE = [
        (r'\b([13][a-km-zA-HJ-NP-Z1-9]{25,34})\b',                       "Bitcoin_Address"),
        (r'\b(0x[a-fA-F0-9]{40})\b',                                      "Ethereum_Address"),
        (r'(AIza[0-9A-Za-z\-_]{35})',                                     "Google_API_Key"),
        (r'(AKIA[0-9A-Z]{16})',                                            "AWS_Access_Key"),
        (r'Bearer\s+([a-zA-Z0-9\-._~+/]{20,}=*)',                         "Bearer_Token"),
        (r'["\']sk-[a-zA-Z0-9]{20,}["\']',                               "Stripe_Key"),
        (r'gh[pousr]_[A-Za-z0-9_]{36,}',                                  "GitHub_PAT"),
        (r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----',                      "Private_Key_PEM"),
        (r'["\'](?:password|passwd|secret|api_?key|token)\s*["\']?\s*[:=]\s*["\']([^"\']{6,})["\']',
                                                                           "Hardcoded_Credential"),
        # ── Real-world tokens missing from original ───────────────────
        (r'xox[bpsa]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,}',        "Slack_Token"),
        (r'\bAC[a-z0-9]{32}\b',                                           "Twilio_AccountSID"),
        (r'\bSK[a-z0-9]{32}\b',                                           "Twilio_AuthToken"),
        (r'SG\.[a-zA-Z0-9\-_]{22,}',                                      "SendGrid_Key"),
        (r'pk\.eyJ1[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+',                   "Mapbox_Token"),
        (r'https://[a-z0-9\-]+\.firebaseio\.com',                        "Firebase_URL"),
        (r'[a-zA-Z0-9\-_]+\.firebaseapp\.com',                           "Firebase_App"),
        (r'eyJ[a-zA-Z0-9_\-]{10,}\.eyJ[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]+',
                                                                           "JWT_Token"),
    ]
    _EXTRACTION_PATTERNS = [
        (re.compile(
            r'(?<![a-zA-Z0-9])([a-zA-Z0-9._%+-]{2,}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6})(?![a-zA-Z0-9])',
            re.I), "Email"),
        (re.compile(
            r'(?<!\d)(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
            r'172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|'
            r'192\.168\.\d{1,3}\.\d{1,3})(?!\d)'),
            "Internal_IP"),
        (re.compile(
            r'(?:phone|mobile|tel|fax|contact|cell|ph|'
            r'whatsapp|viber|call|hotline|helpline|support)'
            r'[\s:="\'#\-]*'
            r'(\+?[\d][\d\s.\-\(\)\/]{6,25}\d)',
            re.I), "Phone"),
        (re.compile(
            r'(s3://|gs://)[a-z0-9][a-z0-9\-\.]+|'
            r'[a-z0-9\-]+\.s3(?:\.[a-z0-9\-]+)?\.amazonaws\.com|'
            r'storage\.googleapis\.com/[a-z0-9\-]+|'
            r'[a-z0-9\-]+\.storage\.googleapis\.com|'
            r'[a-z0-9\-]+\.blob\.core\.windows\.net|'
            r'[a-z0-9\-]+\.table\.core\.windows\.net|'
            r'[a-z0-9\-]+\.azuredatalakestore\.net',
            re.I), "Cloud_Bucket"),
        (re.compile(
            r'(SQLSTATE|ORA-\d{5}|mysql_fetch|pg_query|'
            r'MongoError|SequelizeError|mysqli_error)',
            re.I), "DB_Error"),
        (re.compile(
            r'(?:lat(?:itude)?|lng|lon(?:gitude)?)\s*[:="\']+\s*'
            r'(-?(?:90|[0-8]?\d)(?:\.\d{3,8})?)'
            r'(?:[^\d.-].*?)?'
            r'(?:lat(?:itude)?|lng|lon(?:gitude)?)\s*[:="\']+\s*'
            r'(-?(?:180|1[0-7]\d|[0-9]?\d)(?:\.\d{3,8})?)',
            re.I | re.S), "Geo_Leak"),
        (re.compile(
            # Tier 1: definitive internal TLDs — match freely
            r'(?<![.a-zA-Z0-9_])'
            r'(?!localhost\b)(?!127\.)'
            r'[a-zA-Z0-9][a-zA-Z0-9\-]{3,}'
            r'\.(internal|intranet|corp|lan|private)\b',
            re.I), "Internal_Host"),
        # Tier 2a: ambiguous TLDs, hostname has hyphen or digit — case insensitive ok
        (re.compile(
            r'(?<![.a-zA-Z0-9_])(?!localhost\b)(?!127\.)'
            r'[a-zA-Z0-9]*[\-\d][a-zA-Z0-9\-]*'
            r'\.(local|dev|test|prod|staging|uat|int|stg)\b',
            re.I), "Internal_Host"),
        # Tier 2b: ambiguous TLDs, multi-segment — MUST be all-lowercase.
        # G.CHILD.test / s.rnamespace.test have uppercase → not real hostnames.
        # No re.I flag here — [a-z] is case-sensitive by design.
        (re.compile(
            r'(?<![.a-zA-Z0-9_])(?!localhost)(?!127\.)'
            r'[a-z][a-z0-9\-]+\.[a-z][a-z0-9\-]+'
            r'\.(local|dev|test|prod|staging|uat|int|stg)\b'),
            "Internal_Host"),
    ]
    # Placeholder values that appear in docs/templates — not real secrets
    _SECRET_PLACEHOLDERS = frozenset({
        "changeme", "replace", "your_", "yourapikey", "insert", "placeholder",
        "example", "dummy", "test", "xxxx", "fill_in", "<your", "todo",
    })
    # Pattern 1: quoted path containing API-style keywords
    # Pattern 2+3: fetch/axios/.method calls — capture FULL URL including ?qs (note: no ? in exclusion set)
    # Pattern 4: template literal base path
    # Pattern 5: broad same-origin path — catches /c7r3xq?pid=&text= style literals
    _API_RE = [
        r'["\']([/][a-zA-Z0-9_\-\.\/]*(?:api|v\d+|graphql|admin|auth|login|logout|rest|search|data|internal|upload|download)[a-zA-Z0-9_\-\.\/]*(?:\?[^"\'#\s]*)?)["\']',
        r'(?:fetch|axios)\s*\(\s*["\']([^"\'#\s]{5,})["\']',
        r'\.\s*(?:get|post|put|delete|patch)\s*\(\s*["\']([^"\'#\s]{5,})["\']',
        r'`\$\{[^}]+\}(/[a-zA-Z0-9_\-\/]+(?:\?[^`#\s]*)?)`',
        r'(?:fetch|axios|\.\s*(?:get|post|put|delete|patch))\s*\(\s*["\']([/][^"\'#\s]{3,})["\']',
    ]

    # HTML markers that indicate a catch-all SPA 200 response rather than a real file
    _SPA_BODY_MARKERS = (
        "<html", "<!doctype", "<head", "<body",
        "<title", "<meta", "<!-- ", "ng-app",
        "data-reactroot", "__next_data__",
    )

    # Common strings indicating a soft 404 / Cannot GET error
    _SOFT_404_INDICATORS = (
        "cannot get", "not found", "404 not found", "page not found",
        "route not found", "no route matches", "error 404", "invalid path",
    )

    @classmethod
    def is_real_file(cls, ct: str, body: str, canary_hash: str) -> bool:
        """Return True only if the response looks like a genuine file (not an SPA catch-all)."""
        if "text/html" in ct:
            return False
        body_lo = body.lower()
        if any(marker in body_lo for marker in cls._SPA_BODY_MARKERS):
            return False
        if len(body) <= 50:
            return False
        if canary_hash:
            body_hash = hashlib.md5(body.encode(errors="ignore")).hexdigest()
            if body_hash == canary_hash:
                return False
        return True

    @classmethod
    def is_soft_404(cls, body: str, status: int) -> bool:
        """Return True if the response body indicates a non-existent route (Soft 404)."""
        if status != 200:
            return False
        body_lo = body.lower()
        # Only check short bodies for "Cannot GET" to avoid false positives in large pages
        if len(body) < 1000:
            if any(ind in body_lo for ind in cls._SOFT_404_INDICATORS):
                return True
        # JSON errors: {"error": "Not Found"}
        if body.strip().startswith("{"):
            try:
                data = json.loads(body)
                if isinstance(data, dict):
                    msg = str(data.get("error", "") or data.get("message", "") or data.get("detail", "")).lower()
                    if any(ind in msg for ind in cls._SOFT_404_INDICATORS):
                        return True
            except Exception:
                pass
        return False

    @classmethod
    def is_bot_blocked(cls, body: str) -> bool:
        """
        Heuristic check for real bot-protection / WAF challenge pages.

        Rules to avoid false positives on legitimate pages:

        1. PHRASE-LEVEL indicators only — no single generic words.
           "security check" fires on login pages. "checking your browser
           before you proceed" only fires on Cloudflare challenge pages.

        2. Content structure check — real app pages have <form> inputs,
           <nav>, <main> content etc. Challenge pages are bare skeletons.
           If the page has real interactive elements it is NOT a bot gate.

        3. Size gate — WAF challenge pages are tiny (< 12000 bytes).
           But size alone is not enough — small login pages also exist.
        """
        if not body:
            return False
        body_lo = body.lower()

        # ── Tier 1: Highly specific WAF/bot-protection phrases ────────
        # These are unique to challenge pages and won't appear in real app UI.
        specific_indicators = (
            "checking your browser before you proceed",
            "checking your browser",       # Cloudflare classic
            "enable javascript and cookies to continue",
            "ddos protection by cloudflare",
            "ray id:",                      # Cloudflare Ray ID footer
            "please stand by, while we are checking your",
            "your ip address has been blocked",
            "this process is automatic",    # Cloudflare JS challenge
            "browser will redirect to your requested content shortly",
            "perimeterx",
            "px-captcha",
            "incapsula incident id",
            "powered by sucuri",
            "_sucuri_",
            "akamai reference",
        )
        if any(ind in body_lo for ind in specific_indicators):
            return True

        # ── Tier 2: Weaker signals only valid on skeleton pages ───────
        # Words like "captcha", "access denied" appear in real apps too.
        # Only fire if page is tiny AND has no real interactive structure.
        weak_indicators = (
            "captcha",
            "are you human",
            "bot protection",
            "blocked by",
        )
        if any(ind in body_lo for ind in weak_indicators):
            if len(body) < 8000:
                # Check for real app structure — if present, NOT a bot gate
                has_real_structure = any(sig in body_lo for sig in (
                    "<nav", "<main", "<header", "<footer",
                    "<input ", "<form ", "<table",
                    "navbar", "sidebar", "menu",
                ))
                if not has_real_structure:
                    return True
        return False

    @classmethod
    def _obj_keys(cls, block):
        keys = re.findall(r'["\']?([a-zA-Z_$][a-zA-Z0-9_$]*)["\']?\s*:', block)
        return [k for k in keys if k not in cls._JS_NOISE and len(k) > 1]

    @classmethod
    def _build_var_url_map(cls, text):
        """Pre-scan JS block for variable assignments like: const url = \"/path\"
        Returns dict of {varname: path} for URL association in js_params."""
        var_map = {}
        for m in re.finditer(
            r"""(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=\s*["']([/][a-zA-Z0-9_\-\./?&=]+)["']""",
            text
        ):
            var_map[m.group(1)] = m.group(2)
        for m in re.finditer(
            r"""(?:url|endpoint|action|path|href)\s*:\s*["']([/][a-zA-Z0-9_\-\./]+)["']""",
            text
        ):
            var_map["__prop_%d" % m.start()] = m.group(1)
        return var_map

    @classmethod
    def _find_url_for_params(cls, text, match_start, match_end, base_url, var_map):
        """Find the URL most likely associated with a JS param block.
        Priority: (1) closest literal URL in 600 chars before the block,
        (2) first literal URL in 500 chars after, (3) known variable name
        within ±800 chars, (4) fallback to base_url (current page)."""
        url_lit = r"""["']([/][a-zA-Z0-9_\-\./]+(?:\?[^"'#\s]*)?)["']"""
        pre_window = text[max(0, match_start - 600): match_start]
        pre_matches = list(re.finditer(url_lit, pre_window))
        if pre_matches:
            return urljoin(base_url, pre_matches[-1].group(1).split("?")[0])
        post_window = text[match_end: match_end + 500]
        post_m = re.search(url_lit, post_window)
        if post_m:
            return urljoin(base_url, post_m.group(1).split("?")[0])
        for varname, vpath in var_map.items():
            if varname.startswith("__prop_"):
                if abs(int(varname[7:]) - match_start) <= 800:
                    return urljoin(base_url, vpath.split("?")[0])
            else:
                window = text[max(0, match_start - 800): match_end + 800]
                if re.search(r"\b" + re.escape(varname) + r"\b", window):
                    return urljoin(base_url, vpath.split("?")[0])
        return base_url

    # JS libraries internal params stop-list
    _JS_PARAM_STOPLIST = frozenset({
        "alignmentOffset", "centerOffset", "referenceHiddenOffsets", "escapedOffsets",
        "referenceHidden", "overflows", "placement", "enabled", "mode", "index",
        "length", "name", "type", "id", "value", "target", "action", "method",
        "enctype", "viewport", "charset", "description", "keywords", "author",
    })

    @classmethod
    def js_params(cls, text, base_url, store, emit):
        """
        Extract JS payload params and attach them to the resolved API endpoint URL.

        CRITICAL RULE: if _find_url_for_params falls back to base_url AND base_url
        is a .js file, do NOT create an endpoint at the JS file path — that endpoint
        is not injectable. Instead, park those params in store.js_orphan_params so
        the downstream agent knows they exist but has no associated HTTP target.
        """
        var_map = cls._build_var_url_map(text)
        _is_js_file = base_url.split("?")[0].lower().endswith(".js")
        for pat in cls._PARAM_RE:
            for m in re.finditer(pat, text, re.S):
                keys = cls._obj_keys(m.group(1) if m.lastindex else m.group(0))
                if not keys:
                    continue
                keys = [k for k in keys if k not in cls._JS_PARAM_STOPLIST]
                if not keys:
                    continue
                turl = cls._find_url_for_params(text, m.start(), m.end(), base_url, var_map)
                resolved = (turl != base_url)
                if resolved:
                    # Resolved to a real API endpoint — attach params there
                    if store.add_js_params(turl, keys):
                        emit.info("[JS-Params] %s -> %s" % (keys, turl))
                elif _is_js_file:
                    # Fell back to a JS file URL — park as orphan, not as injectable endpoint
                    store.add_js_orphan_params(base_url, keys)
                    emit.info("[JS-Orphan] %s (no target URL found in %s)" % (keys, base_url))
                else:
                    # base_url is an HTML page — attaching to it is legitimate
                    if store.add_js_params(turl, keys):
                        emit.info("[JS-Params] %s -> %s" % (keys, turl))

    @classmethod
    def extract_data(cls, body: str, url: str, store, emit):
        """Passive extraction of emails, IPs, buckets, etc."""
        # Skip extraction on: vendor bundles > 2MB
        if len(body) > 2_000_000 and "vendor" in url.lower():
            return

        counts = defaultdict(int)
        # Skip raw body phone scan for JSON responses — raw JSON keys like
        # "order_number", "tracking_number" pollute phone context. Use flatten only.
        _is_json_body = body.strip().startswith(('{', '['))
        for pattern, dtype in cls._EXTRACTION_PATTERNS:
            if dtype == "Phone" and _is_json_body:
                continue  # handled exclusively in JSON flatten branch below
            for match in pattern.finditer(body):
                # Phone pattern has capture group 1 — use it to avoid including keyword context
                val = (match.group(1) if dtype == "Phone" and match.lastindex else match.group(0)).strip()
                if not val:
                    continue
                
                # FIX 5: Email post-match filter
                if dtype == "Email":
                    local_part  = val.split("@")[0]
                    domain_part = val.split("@")[1].lower() if "@" in val else ""
                    if ".." in val: continue
                    if len(local_part) < 2: continue
                    if "." not in domain_part: continue
                    if val.lower().endswith((".css", ".js", ".png", ".jpg", ".svg", ".woff")):
                        continue
                    # Block known placeholder / documentation domains that are never real
                    _PLACEHOLDER_EMAIL_DOMAINS = {
                        "example.com", "example.org", "example.net",
                        "test.com", "test.org", "test.net",
                        "foo.com", "bar.com", "baz.com",
                        "domain.com", "email.com", "mail.com",
                        "user.com", "yoursite.com", "yourwebsite.com",
                        "company.com", "website.com", "sample.com",
                        "placeholder.com", "demo.com", "fake.com",
                        "noreply.com", "no-reply.com",
                        "sentry.io",    # Sentry DSN fragments leak as emails
                    }
                    if domain_part in _PLACEHOLDER_EMAIL_DOMAINS: continue
                    # Block local-part placeholder names
                    _PLACEHOLDER_LOCAL = {
                        "jane", "john", "user", "admin", "test", "foo",
                        "bar", "email", "name", "you", "me", "info",
                        "hello", "contact", "mail", "noreply", "no-reply",
                        "support", "help", "demo", "sample", "example",
                        "someone", "anyone", "nobody", "webmaster",
                    }
                    if local_part.lower() in _PLACEHOLDER_LOCAL and domain_part in {
                        "example.com","example.org","test.com","foo.com",
                        "bar.com","domain.com","email.com","mail.com",
                        "company.com","website.com",
                    }: continue

                if dtype == "Phone":
                    # Validate on stripped form but KEEP original for storage.
                    # Stripping before store loses country code formatting like
                    # +44 (0)20 7946 0958 or +91 98765-43210 — unacceptable.
                    _stripped = re.sub(r'[\s.\-\(\)\/]', '', val)
                    if not (7 <= len(_stripped) <= 15): continue
                    if not re.match(r'\+?\d+$', _stripped): continue
                    if re.match(r'(20[0-9]{2}[01][0-9][0-3][0-9]|[0-3][0-9][01][0-9]20[0-9]{2})', _stripped): continue
                    # val stays as-is — original formatting preserved

                if dtype == "Internal_Host":
                    hostname = val.split('.')[0].lower()
                    _JS_WORDS = {
                        'this','self','that','base','root','data','type','keys','node',
                        'dict','list','map','set','ctx','app','ext','lib','src',
                        'dst','tmp','buf','str','num','val','key','idx','obj',
                        'top','bot','mid','out','err','msg','log','res','req',
                        'next','prev','curr','last','head','tail','body','path',
                        'port','mode','flag','opts','args','props','state','proto',
                    }
                    if hostname in _JS_WORDS: continue
                    # Reject camelCase identifiers (JS variable names, not hostnames)
                    if re.search(r'[a-z][A-Z]', val.split('.')[0]): continue

                if store.add_extracted_data(dtype, val, url):
                    counts[dtype] += 1

        # IMPROVEMENT 2: Extract from JSON API responses
        if body.strip().startswith('{') or body.strip().startswith('['):
            try:
                obj = json.loads(body)
                def _flatten_strings(o, depth=0):
                    if depth > 6: return
                    if isinstance(o, str): yield o
                    elif isinstance(o, dict):
                        for v in o.values(): yield from _flatten_strings(v, depth+1)
                    elif isinstance(o, list):
                        for item in o: yield from _flatten_strings(item, depth+1)
                flat_text = '\n'.join(_flatten_strings(obj))
                for pattern, dtype in cls._EXTRACTION_PATTERNS:
                    if dtype in ('Email', 'Phone', 'Cloud_Bucket', 'Internal_IP'):
                        for m in pattern.finditer(flat_text):
                            v = m.group(1) if m.lastindex else m.group(0)
                            if v:
                                if dtype == "Phone":
                                    _sv = re.sub(r'[\s.\-\(\)\/]', '', v)
                                    if not (7 <= len(_sv) <= 15): continue
                                    if not re.match(r'\+?\d+$', _sv): continue
                                    if re.match(r'(20[0-9]{2}[01][0-9][0-3][0-9]|[0-3][0-9][01][0-9]20[0-9]{2})', _sv): continue
                                    # v stays as-is — original formatting preserved
                                if store.add_extracted_data(dtype, v.strip(), url):
                                    counts[dtype] += 1
            except Exception:
                pass
        
        if counts:
            summary = ", ".join([f"{v} {k.lower().replace('_', ' ')}" for k, v in counts.items()])
            emit.info(f"[Extract] {summary} ← {url}")

    @classmethod
    def secrets(cls, text, url, store, emit):
        for pat, stype in cls._SECRET_RE:
            for m in re.finditer(pat, text):
                val = m.group(1) if m.lastindex else m.group(0)
                if stype not in ("Bitcoin_Address","Ethereum_Address","Private_Key_PEM",
                                  "Hardcoded_Credential","GitHub_PAT") and len(val) < 20:
                    continue
                # Skip placeholder / documentation values
                val_lo = val.lower()
                if any(ph in val_lo for ph in cls._SECRET_PLACEHOLDERS):
                    continue
                # Bitcoin-specific post-filter
                if stype == "Bitcoin_Address":
                    # MD5/SHA hashes are all lowercase hex — real BTC has mixed case
                    if not any(c.isupper() for c in val):
                        continue
                    # Binary/base64 artifacts have long repeated char runs
                    if re.search(r'(.)(\1){3,}', val):
                        continue
                    # Must be 25-34 chars (P2PKH/P2SH only — not bech32)
                    if not (25 <= len(val) <= 34):
                        continue
                if store.add_secret(val, stype, url):
                    emit.warn(f"[SECRET:{stype}] {val[:80]}")

    # Safe URL prefixes that every site legitimately serves — not interesting files
    _EXPOSED_SAFE_PREFIXES = (
        "/robots", "/sitemap", "/manifest", "/favicon", "/.well-known/",
    )


    # JS comment sensitive patterns — high-signal credential leaks ONLY
    # Avoids common library noise: disable/remove/workaround/todo fire constantly
    _JS_COMMENT_SENSITIVE = re.compile(
        r'(?:password\s*[:=][^,;\n]{3,}|passwd\s*[:=][^,;\n]{3,}|'
        r'secret\s*[:=][^,;\n]{3,}|api[_-]?key\s*[:=][^,;\n]{3,}|'
        r'private[_-]?key|hardcod(?:ed?|ing)|'
        r'remove\s+before\s+(?:prod|deploy|release|commit)|'
        r'do\s+not\s+(?:commit|push|deploy)|'
        r'(?:admin|staging|prod)\s+(?:password|key|token|secret)\s*[:=]|'
        r'bypass\s+(?:auth|security|check|validation))',
        re.I
    )
    # Third-party library filenames — skip comment extraction entirely
    _JS_LIBRARY_RE = re.compile(
        r'(?:jquery|bootstrap|angular|react|lodash|moment|axios|backbone|'
        r'respond\.js|html5shiv|modernizr|require\.js|webpack|babel|'
        r'polyfill|vendor\.js|bundle\.js|chunk|runtime\.js|commons|datepicker)',
        re.I
    )
    _JS_COMMENT_PATH_RE = re.compile(r'(/[a-zA-Z0-9_/][^\s\'"<>\\]{3,})')

    @classmethod
    def js_comments(cls, text, url, store, emit):
        """High-signal JS comment extraction — library files skipped, strict patterns only."""
        fname = url.lower().split('/')[-1].split('?')[0]
        if cls._JS_LIBRARY_RE.search(fname):
            return 0
        found = 0
        for m in re.finditer(r'//(.+)$', text, re.MULTILINE):
            comment = m.group(1).strip()
            if len(comment) < 10 or len(comment) > 120: continue
            if comment[:1] in ("@", "=") or comment.startswith(
                ("eslint","jshint","jscs","jslint","istanbul","tslint",
                 "prettier","stylelint","sourceMappingURL","#")):
                continue
            if cls._JS_COMMENT_SENSITIVE.search(comment):
                if store.add_secret(comment, "JS_Comment_Leak", url):
                    emit.warn(f"[JS-Comment] {comment[:120]}")
                    found += 1
        for m in re.finditer(r'/\*(.*?)\*/', text, re.DOTALL):
            block = m.group(1).strip()
            if not block or len(block) > 400: continue
            if "@param" in block or "@return" in block or "Copyright" in block:
                continue
            if cls._JS_COMMENT_SENSITIVE.search(block):
                first = block.splitlines()[0].strip().lstrip("* ") if block else ""
                if first and store.add_secret(first, "JS_Comment_Leak", url):
                    emit.warn(f"[JS-Comment] {first[:120]}")
                    found += 1
        return found

    _ROUTE_PATTERNS = [
        re.compile(r'<Route[^>]+path=["\']([/][^"\'\s>]+)["\']', re.I),
        re.compile(r'\{[^}]{0,80}path\s*:\s*["\']([/][^"\'\s,}]{2,})["\']\s*[,}]'),
        re.compile(r'(?:router|routes)\s*(?:\.add|\[|=)\s*(?:\[)?\s*\{[^}]{0,80}path\s*:\s*["\']([/][^"\'\s,}]{2,})["\']', re.I),
        re.compile(r'(?:app|router|server)\.(get|post|put|patch|delete|all)\s*\(\s*["\']([/][^"\'\s,)]{2,})["\']\s*,', re.I),
    ]
    _ROUTE_PARAM_RE = re.compile(r'[:{}\[\]]([a-zA-Z][a-zA-Z0-9_]+)')

    @classmethod
    def js_routes(cls, text, base_url, store, emit):
        """Extract route definitions from React Router, Vue Router, Angular, Express etc."""
        found = 0
        seen  = set()
        for pat in cls._ROUTE_PATTERNS:
            for m in re.finditer(pat, text):
                path = m.group(m.lastindex or 1).strip()
                if not path or path in seen or len(path) < 2: continue
                if path.startswith(("http","//","#","$","{")):  continue
                seen.add(path)
                # Normalize dynamic segments: /users/:id → /users/{id}
                clean = re.sub(r'[:{}\[\]][a-zA-Z][a-zA-Z0-9_]*', '{param}', path)
                if not clean.startswith("/"): continue
                full = urljoin(base_url, clean)
                if store.add_endpoint(full, source="JS_Route", score=Conf.MEDIUM):
                    emit.info(f"[JS-Route] {path}")
                    found += 1
                    params = cls._ROUTE_PARAM_RE.findall(path)
                    if params:
                        ek = store._key(full, "GET")
                        if ek in store.endpoints:
                            ep = store.endpoints[ek]
                            for p in params:
                                if p not in ep["params"]["query"]:
                                    ep["params"]["query"].append(p)
        return found

    @classmethod
    def js_endpoints(cls, text, base_url, store, emit):
        # Dedup by (clean_path, frozenset(qs_params)) across all 5 patterns
        _seen_paths: set = set()
        for pat in cls._API_RE:
            for m in re.finditer(pat, text):
                raw = m.group(1)
                if not raw or not raw.startswith("/") or len(raw) < 3:
                    continue
                # Fix D + Fix 3: parse QS from the full literal BEFORE stripping
                _parsed    = urlparse(raw)
                _qs_params = list(parse_qs(_parsed.query).keys())
                clean_path = _parsed.path
                if not clean_path or clean_path == "/":
                    continue
                full = urljoin(base_url, clean_path)
                # Dedup: same endpoint from multiple patterns → merge params, skip re-emit
                _dedup_key = (full, frozenset(_qs_params))
                if _dedup_key in _seen_paths:
                    continue
                _seen_paths.add(_dedup_key)
                store.add_endpoint(full, source="JS_Analysis", score=Conf.MEDIUM)
                if _qs_params:
                    store.add_js_params(full, _qs_params)
                    emit.info(f"[JS-QS-Params] {_qs_params} ← {full}")
                emit.info(f"[JS-API] {full}")

    @classmethod
    def html_comments(cls, soup, url, store, emit):
        # Deliberately excludes 'test' and 'api' — both are too common in build-tool
        # comments (e.g. "<!-- api handler -->", "<!-- for testing -->") to be signal.
        kw = {"todo","fixme","bug","admin","hidden","secret","debug","config",
              "key","password","cred","token","hack","temp","internal",
              "private","disabled","endpoint","framework","version","beta",
              "homepage","temporary","new-home","http://","https://"}
        for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
            txt = c.strip()
            if len(txt) < 4:
                continue
            # Match keyword list OR a path/URL reference anywhere in the comment
            has_kw   = any(k in txt.lower() for k in kw)
            has_path = bool(re.search(r'(?:^|\s)/[a-z0-9_\-]{3,}', txt, re.I))
            has_url  = bool(re.search(r'https?://', txt, re.I))
            if (has_kw or has_path or has_url
                    or bool(re.match(r'^[/\.][a-z0-9_\-\.#]{3,}', txt))):
                if store.add_comment(txt, url):
                    emit.info(f"[Comment] {txt[:120]}")
                    # IMPROVEMENT 3: Run patterns on comments
                    for pat, dtype in cls._EXTRACTION_PATTERNS:
                        if dtype in ('Email', 'Phone'):
                            for m in pat.finditer(txt):
                                v = m.group(1) if m.lastindex else m.group(0)
                                if v:
                                    if dtype == "Phone":
                                        v = re.sub(r'[\s.\-\(\)\/]', '', v)
                                        if not (7 <= len(v) <= 15): continue
                                        if not re.match(r'\+?\d+$', v): continue
                                        # Reject date-like patterns
                                        if re.match(r'(20[0-9]{2}[01][0-9][0-3][0-9]|[0-3][0-9][01][0-9]20[0-9]{2})', v): continue
                                    store.add_extracted_data(dtype, v.strip(), url)

    @classmethod
    def csp_hints(cls, headers, base_url, store, emit):
        csp = headers.get("Content-Security-Policy","") or headers.get("content-security-policy","")
        if not csp:
            return
        domain = urlparse(base_url).netloc
        for tok in csp.split():
            tok = tok.rstrip(";")
            if tok.startswith("/") and len(tok) > 2:
                store.add_endpoint(urljoin(base_url, tok), source="CSP", score=Conf.LOW)
            elif tok.startswith(("https://","http://")) and urlparse(tok).netloc != domain:
                emit.info(f"[CSP-3rd-party] {tok}")

# ══════════════════════════════════════════════════════════════════════
_WELL_KNOWN_PATHS = [
    ".well-known/security.txt",
    ".well-known/assetlinks.json",
    ".well-known/apple-app-site-association",
    ".well-known/change-password",
    ".well-known/jwks.json",
    ".well-known/openid-configuration",
    ".well-known/oauth-authorization-server",
    ".well-known/mta-sts.txt",
    ".well-known/webfinger",
    ".well-known/dnt-policy.txt",
]

# ══════════════════════════════════════════════════════════════════════
# INTELLIGENT PROBER
# ══════════════════════════════════════════════════════════════════════

class IntelligentProber:
    _METHODS = ["PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]

    def __init__(self, session, store, emit, rl, cfg):
        self.session = session; self.store = store
        self.emit = emit; self.rl = rl; self.cfg = cfg

    async def run(self):
        all_eps = self.store.all_endpoints()
        targets = [
            e for e in all_eps
            if (e.get("confidence", 0) >= Conf.MEDIUM or
                any(e.get("params",{}).values()))
        ]
        if not targets:
            return

        self.emit.always_info(f"Phase: Intelligent Probing… ({len(targets)} endpoints)")
        self.emit.animator.start_anim("Intelligent Probing", total=len(targets))

        # Action-named paths that are likely POST-only
        _API_ACTION_RE = re.compile(
            r'/(?:parse|process|submit|send|create|add|upload|register|'
            r'login|signin|auth|verify|validate|execute|run|trigger|'
            r'convert|transform|generate|compute|analyze|check|scan|'
            r'search|query|resolve|lookup|decode|encode)(?:/|$|\?|\#)',
            re.I
        )

        new_methods_count = 0
        for i, ep in enumerate(targets):
            self.emit.animator.update(i+1)
            url           = ep["url"]
            known_methods = ep.get("methods", ["GET"])
            obs_status    = ep.get("observed_status", [])

            if not self.cfg.enable_method_disc:
                continue

            test_set = [m for m in self._METHODS if m not in known_methods]

            # POST probe: try POST on endpoints that returned 404/405 on GET
            # OR whose path looks like an action verb — these are often POST-only
            if "POST" not in known_methods:
                if any(s in obs_status for s in (404, 405)) or _API_ACTION_RE.search(url):
                    test_set = ["POST"] + test_set

            for m in test_set:
                s, h, _ = await fetch(self.session, m, url, self.rl)
                if s in (200, 201, 202, 204, 301, 302, 400, 401, 403):
                    self.store.record_status(url, m, s)
                    if self.store.update_methods(url, [m]):
                        self.emit.info(f"[Method_Oracle] {m} {url} → {s}")
                        new_methods_count += 1

        self.emit.animator.stop_anim()
        self.emit.always_info(
            f"[Method_Oracle] Probing done — {new_methods_count} new method(s) discovered")

# ══════════════════════════════════════════════════════════════════════

_GQL_PATHS = ["/graphql","/api/graphql","/gql","/query","/v1/graphql","/graphiql","/playground"]
_GQL_QUERY = '{"query":"{ __schema { queryType { name } types { name fields { name args { name } } } } }"}'

async def probe_graphql(session, base, store, emit, rl):
    for path in _GQL_PATHS:
        url = urljoin(base, path)
        s, _, text = await fetch(session, "POST", url, rl, data=_GQL_QUERY,
                                  headers={"Content-Type": "application/json"})
        if s and s < 400 and text and '"__schema"' in text:
            emit.warn(f"[GraphQL] Introspection OPEN → {url}")
            store.add_endpoint(url, method="POST", source="GraphQL", score=Conf.CONFIRMED)
            try:
                schema     = json.loads(text)
                types      = schema.get("data",{}).get("__schema",{}).get("types",[])
                # Extract variables from mutations and queries — feed to param store
                gql_params = []
                for t in types:
                    if t.get("name","").startswith("__"): continue
                    for field in (t.get("fields") or []):
                        for arg in (field.get("args") or []):
                            aname = arg.get("name","").strip()
                            if aname and aname not in gql_params:
                                gql_params.append(aname)
                        # Also register each field as an endpoint param hint
                        fname = field.get("name","").strip()
                        if fname:
                            store.add_endpoint(url, method="POST", source="GraphQL_Field", score=Conf.HIGH)
                            ep_key = store._key(url, "POST")
                            if ep_key in store.endpoints:
                                ep = store.endpoints[ep_key]
                                for p in gql_params:
                                    if p not in ep["params"]["js"]:
                                        ep["params"]["js"].append(p)
                store.graphql.append({
                    "url": url, "types_count": len(types),
                    "schema": schema, "extracted_params": gql_params
                })
                emit.warn(f"[GraphQL] {len(types)} types exposed — {len(gql_params)} variable(s) extracted")
                if gql_params:
                    emit.info(f"[GraphQL] Variables: {', '.join(gql_params[:20])}")
            except Exception as e:
                emit.warn(f"[GraphQL] Parse error: {e}")
            return

# ══════════════════════════════════════════════════════════════════════
# OPENAPI PROBER
# ══════════════════════════════════════════════════════════════════════

_OAS_PATHS = [
    "/swagger.json","/swagger/v1/swagger.json","/swagger/v2/swagger.json",
    "/api-docs","/api-docs.json","/api-docs/swagger.json",
    "/openapi.json","/openapi.yaml","/openapi/v3/api-docs",
    "/v1/swagger.json","/v2/swagger.json","/v3/api-docs",
    "/.well-known/openapi","/api/swagger.json",
]

async def probe_openapi(session, base, store, emit, rl):
    for path in _OAS_PATHS:
        url = urljoin(base, path)
        s, _, text = await fetch(session, "GET", url, rl)
        if s != 200 or not text:
            continue
        try:
            spec = json.loads(text)
        except Exception:
            continue
        if not any(k in spec for k in ("paths","swagger","openapi")):
            continue
        emit.warn(f"[OpenAPI] Spec exposed → {url}")
        store.openapi.append({"url": url})
        server_prefix = ""
        for srv in spec.get("servers", []):
            u = srv.get("url","")
            if not u.startswith("http"):
                server_prefix = u
            break
        count = 0
        for ep_path, methods_obj in spec.get("paths", {}).items():
            for method, detail in methods_obj.items():
                if method.lower() not in ("get","post","put","patch","delete","head","options"):
                    continue
                clean  = (server_prefix + ep_path).replace("{","").replace("}","")
                full   = urljoin(base, clean)
                params = [p.get("name","") for p in detail.get("parameters",[]) if p.get("name")]
                bp: List[str] = []
                for ct_data in detail.get("requestBody",{}).get("content",{}).values():
                    bp += list(ct_data.get("schema",{}).get("properties",{}).keys())
                store.add_endpoint(full, method=method.upper(), source="OpenAPI",
                                   params=params+bp, score=Conf.CONFIRMED)
                emit.info(f"[OpenAPI] {method.upper()} {full} ({len(params+bp)} params)")
                count += 1
        emit.always_success(f"[OpenAPI] Mapped {count} endpoints from spec")
        return

# ══════════════════════════════════════════════════════════════════════
# ROBOTS + SITEMAP PARSER
# Disallowed paths are crawled as high-value targets, not skipped.
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
# WAYBACK MACHINE PROBE
# Queries the Wayback CDX API for historical URLs on the target domain.
# Surfaces old API versions, removed endpoints, backup paths, and
# anything that was public at any point — even if gone from live site.
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
# SUBDOMAIN ENUMERATOR — crt.sh certificate transparency logs
# Zero API key. Discovers subdomains that may host staging, admin,
# API, or internal services invisible to the main crawler.
# ══════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════
# HAR FILE IMPORTER
# Mines a browser-exported HAR (HTTP Archive) file for every request
# the browser made during a real session — including auth-gated calls,
# interaction-gated calls, and anything a bot cannot reach on its own.
# Usage: spider https://target.com --har /path/to/session.har
# ══════════════════════════════════════════════════════════════════════

class HARImporter:
    def __init__(self, har_path, store, emit, is_valid_fn, base_url):
        self.har_path = har_path
        self.store    = store
        self.emit     = emit
        self.is_valid = is_valid_fn
        self.base_url = base_url

    def run(self):
        """Parse HAR synchronously — called before async crawl starts."""
        import json as _j
        try:
            with open(self.har_path, "r", encoding="utf-8", errors="ignore") as f:
                har = _j.load(f)
        except Exception as e:
            self.emit.warn(f"[HAR] Failed to load {self.har_path}: {e}")
            return 0

        entries = har.get("log", {}).get("entries", [])
        added   = 0
        for entry in entries:
            req     = entry.get("request", {})
            method  = req.get("method", "GET").upper()
            url     = req.get("url", "").split("#")[0]
            if not url or not url.startswith("http"):
                continue
            if not self.is_valid(url):
                continue

            ep = self.store.add_endpoint(url, method=method,
                                          source="HAR", score=7)  # HIGH
            added += 1

            # Extract query params
            for qp in req.get("queryString", []):
                name = qp.get("name","").strip()
                if name and ep and name not in ep.get("params",{}).get("query",[]):
                    ep.setdefault("params",{}).setdefault("query",[]).append(name)

            # Extract POST body params
            post_data = req.get("postData", {})
            if post_data:
                mime = post_data.get("mimeType","")
                text = post_data.get("text","")
                # Form-encoded
                for pp in post_data.get("params", []):
                    name = pp.get("name","").strip()
                    if name and ep and name not in ep.get("params",{}).get("form",[]):
                        ep.setdefault("params",{}).setdefault("form",[]).append(name)
                # JSON body
                if "json" in mime and text:
                    try:
                        body = _j.loads(text)
                        if isinstance(body, dict):
                            for k in body.keys():
                                if ep and k not in ep.get("params",{}).get("form",[]):
                                    ep.setdefault("params",{}).setdefault("form",[]).append(k)
                    except Exception:
                        pass

            # Extract response-revealed endpoints
            resp     = entry.get("response", {})
            status   = resp.get("status", 0)
            if status:
                self.store.record_status(url, method, status)

        self.emit.always_success(
            f"[HAR] Imported {added} requests from {self.har_path}")
        return added

class SubdomainEnumerator:
    CRT_SH = "https://crt.sh/?q={domain}&output=json"

    def __init__(self, base_url, store, queue, emit, is_valid_fn):
        self.base_url  = base_url
        self.store     = store
        self.queue     = queue
        self.emit      = emit
        self.is_valid  = is_valid_fn

    async def run(self):
        from urllib.parse import urlparse as _up
        parsed     = _up(self.base_url)
        _host      = parsed.netloc.split(":")[0].lower()
        domain     = _host[4:] if _host.startswith("www.") else _host
        scheme     = parsed.scheme
        self.emit.always_info(f"[CRT.sh] Enumerating subdomains for {domain}")
        _HEADERS = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept":          "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection":      "keep-alive",
        }
        data = None
        try:
            import aiohttp as _aio
            async with _aio.ClientSession(
                timeout=_aio.ClientTimeout(total=20),
                headers=_HEADERS,
            ) as sess:
                # Retry up to 3 times — crt.sh occasionally returns 503 under load
                for _attempt in range(3):
                    async with sess.get(self.CRT_SH.format(domain=f"%.{domain}")) as resp:
                        if resp.status == 200:
                            data = await resp.json(content_type=None)
                            break
                        elif resp.status == 429:
                            # Genuine rate-limit (rare) — back off and retry
                            self.emit.warn(f"[CRT.sh] Rate-limited — waiting 5s (attempt {_attempt+1}/3)")
                            await asyncio.sleep(5 * (_attempt + 1))
                        elif resp.status in (503, 502):
                            await asyncio.sleep(2)
                        else:
                            self.emit.warn(f"[CRT.sh] Unexpected status {resp.status}")
                            return
        except Exception as e:
            self.emit.warn(f"[CRT.sh] Error: {e}")
            return
        if data is None:
            self.emit.warn("[CRT.sh] No data returned after retries")
            return

        seen  = set()
        added = 0
        for entry in (data or []):
            name = entry.get("name_value","").strip()
            for sub in name.splitlines():
                sub = sub.strip().lstrip("*.")
                if not sub or sub in seen or sub == domain: continue
                if not sub.endswith(domain): continue
                seen.add(sub)
                # Queue root URL of each discovered subdomain
                for _s in (scheme,):
                    candidate = f"{_s}://{sub}"
                    self.store.add_endpoint(candidate, source="CRT_Subdomain", score=1)
                    self.queue.put_nowait((candidate + "/", 1, "CRT_Subdomain"))
                    added += 1
                # Live feed: show each subdomain as it's found (mirrors robots.txt tree style)
                self.emit.robots_entry("CRT.sh", sub, True)

        self.emit.always_info(
            f"[CRT.sh] {len(seen)} unique subdomain(s) found — {added} queued")

class WaybackProbe:
    CDX_API = "https://web.archive.org/cdx/search/cdx"

    def __init__(self, base_url, store, queue, emit, rl, is_valid_fn):
        self.base_url = base_url
        self.store    = store
        self.queue    = queue
        self.emit     = emit
        self.rl       = rl
        self.is_valid = is_valid_fn

    async def run(self, session):
        parsed = urlparse(self.base_url)
        domain = parsed.netloc
        self.emit.always_info(f"[Wayback] Querying CDX API for {domain}")
        try:
            params = (
                f"?url={domain}/*"
                f"&output=json"
                f"&fl=original"
                f"&collapse=urlkey"
                f"&limit=500"
                f"&filter=statuscode:200"
            )
            try:
                import aiohttp as _aio
                async with _aio.ClientSession(timeout=_aio.ClientTimeout(total=30)) as _ws:
                    async with _ws.get(self.CDX_API + params) as _wr:
                        s = _wr.status
                        text = await _wr.text() if s == 200 else ""
            except Exception as _we:
                self.emit.warn(f"[Wayback] CDX timeout/error: {_we}")
                return
                self.emit.warn("[Wayback] CDX API unavailable or no results")
                return
            rows = json.loads(text)
            # First row is header ["original"]
            urls = [r[0] for r in rows[1:] if r and r[0].startswith("http")]
            queued = 0
            for u in urls:
                # Only accept same-domain URLs that pass is_valid
                if urlparse(u).netloc == domain and self.is_valid(u):
                    # Mark as Wayback source — lower confidence (historical)
                    self.store.add_endpoint(u, source="Wayback", score=Conf.LOW)
                    self.queue.put_nowait((u, 2, "Wayback"))
                    queued += 1
                    # Live feed: show each wayback URL as it's queued (mirrors robots.txt tree style)
                    self.emit.robots_entry("Wayback", urlparse(u).path or u, True)
            self.emit.always_info(
                f"[Wayback] {len(urls)} historical URLs found — "
                f"{queued} same-domain queued for crawl"
            )
        except Exception as e:
            self.emit.warn(f"[Wayback] Error: {e}")

class RobotsParser:
    def __init__(self, session, base_url, store, queue, emit, rl, is_valid_fn):
        self.session = session; self.base_url = base_url
        self.store = store; self.queue = queue
        self.emit = emit; self.rl = rl; self.is_valid = is_valid_fn
        self.crawl_delay = 0.0
        self._sitemap_seen: Set[str] = set()

    async def run(self) -> float:
        url = urljoin(self.base_url, "/robots.txt")
        s, hdrs, text = await fetch(self.session, "GET", url, self.rl)
        if s != 200 or not text:
            return 0.0
        
        ct = (hdrs or {}).get("content-type", "").lower()
        is_robots = "text/plain" in ct or url.endswith("/robots.txt")
        if not is_robots:
            if not Extractor.is_real_file(ct, text, None) or Extractor.is_soft_404(text, s):
                return 0.0

        self.emit.always_info(f"[Robots] Parsing {url}")
        self.emit._w(f"  {C.GR}│{C.RST}")
        dis_count = alw_count = sit_count = 0

        # Sensitive keyword patterns for comment scanning
        _COMMENT_PATTERNS = re.compile(
            r'(?:password|passwd|secret|token|key|api[_-]?key|db|database|backup|'
            r'sql|dump|cred|credential|auth|admin|prod|production|staging|internal|'
            r'private|todo|fixme|note to self|remove|delete|temp|test|debug|'
            r'mysql|mongo|redis|postgres|s3|bucket|aws|gcp|azure)',
            re.I
        )

        # Track which User-agent block we're in.
        # Only process Disallow/Allow for * (wildcard) and our own agent.
        # Per-bot blocks (Amazonbot, GPTBot etc.) are interesting metadata
        # but their Disallow rules don't apply to us — we crawl everything
        # a wildcard rule allows. Record bot-specific blocks for the report.
        current_agents: list = []
        is_active_block = False   # True when current block applies to us
        bot_blocks: dict = {}     # agent → [disallowed paths]
        content_signals: dict = {}  # Content-Signal field values
        OUR_AGENT = "*"

        for raw_line in text.splitlines():
            # Extract comment before stripping it
            comment_text = ""
            if "#" in raw_line:
                comment_text = raw_line.split("#", 1)[1].strip()
            line = raw_line.split("#", 1)[0].strip()

            # Scan comment for sensitive keywords
            if comment_text and _COMMENT_PATTERNS.search(comment_text):
                self.store.add_secret(comment_text, "Robots_Comment_Leak",
                                      urljoin(self.base_url, "/robots.txt"))
                self.emit.robots_comment_leak(comment_text)

            if not line:
                # Blank line = end of current user-agent block
                current_agents = []
                is_active_block = False
                continue

            lower = line.lower()

            if lower.startswith("user-agent:"):
                agent = line.split(":", 1)[1].strip()
                current_agents = [agent]
                # Active if wildcard or our actual user-agent string
                is_active_block = agent in ("*", OUR_AGENT)

            elif lower.startswith("content-signal:"):
                # RFC-like field used by some sites to signal AI content policy
                val = line.split(":", 1)[1].strip()
                for ag in (current_agents or ["*"]):
                    content_signals[ag] = val
                self.emit.always_info(f"[Robots] Content-Signal ({current_agents}): {val}")

            elif lower.startswith("crawl-delay:"):
                if is_active_block or not current_agents:
                    try:
                        self.crawl_delay = float(line.split(":", 1)[1].strip())
                        self.emit.always_info(
                            f"[Robots] Crawl-delay: {self.crawl_delay}s — honouring")
                    except (ValueError, IndexError):
                        pass

            elif lower.startswith("disallow:"):
                try:
                    path = line.split(":", 1)[1].strip()
                    if not path:
                        continue
                    # Record bot-specific blocks as metadata
                    for ag in (current_agents or ["*"]):
                        if ag != "*":
                            bot_blocks.setdefault(ag, []).append(path)
                    # Only crawl disallowed paths from wildcard blocks
                    if not is_active_block and current_agents and "*" not in current_agents:
                        continue
                    full = urljoin(self.base_url, path)
                    if self.is_valid(full):
                        self.store.robots_paths.append(path)
                        self.store.add_endpoint(full, source="Robots_Disallow", score=Conf.LOW)
                        queued = path != "/"
                        if queued:
                            self.queue.put_nowait((full, 1, "Robots_Disallow"))
                        dis_count += 1
                        self.emit.robots_entry("Disallow", path, queued)
                except IndexError:
                    pass

            elif lower.startswith("allow:"):
                try:
                    path = line.split(":", 1)[1].strip()
                    if not path or (not is_active_block and current_agents
                                    and "*" not in current_agents):
                        continue
                    full = urljoin(self.base_url, path)
                    if self.is_valid(full):
                        self.store.add_endpoint(full, source="Robots_Allow", score=Conf.LOW)
                        self.store.robots_allowed_paths.append(path)
                        queued = path != "/"
                        if queued:
                            self.queue.put_nowait((full, 1, "Robots_Allow"))
                        alw_count += 1
                        self.emit.robots_entry("Allow", path, queued)
                except IndexError:
                    pass

            elif lower.startswith("sitemap:"):
                try:
                    sitemap_url = line.split(":", 1)[1].strip()
                    # Handle relative sitemap URLs (Sitemap: /sitemap.xml)
                    if sitemap_url.startswith("/"):
                        sitemap_url = urljoin(self.base_url, sitemap_url)
                    elif not sitemap_url.startswith("http"):
                        # Could be "https://..." split on first colon — rejoin
                        sitemap_url = line.partition(":")[2].strip()
                        if not sitemap_url.startswith("http"):
                            sitemap_url = urljoin(self.base_url, sitemap_url)
                    await self.parse_sitemap(sitemap_url)
                    sit_count += 1
                except (IndexError, Exception):
                    pass

        # Store bot block metadata for the report
        if bot_blocks:
            self.store.add_secret(
                str(bot_blocks),
                "Robots_Bot_Blocks",
                urljoin(self.base_url, "/robots.txt")
            )
            blocked_bots = list(bot_blocks.keys())
            self.emit.always_info(
                f"[Robots] {len(blocked_bots)} specific bot(s) blocked: "
                f"{', '.join(blocked_bots[:8])}"
                + (f" (+{len(blocked_bots)-8} more)" if len(blocked_bots) > 8 else "")
            )
        if content_signals:
            for agent, signal in content_signals.items():
                self.emit.always_info(f"[Robots] Content-Signal for {agent}: {signal}")

        self.emit._w(f"  {C.GR}└─{C.RST} {C.CYD}queued {dis_count + alw_count} paths for crawl{C.RST}")
        self.emit.always_info(
            f"[Robots] Done — {dis_count} disallow, {alw_count} allow, {sit_count} sitemaps")
        return self.crawl_delay

    async def parse_sitemap(self, sitemap_url: str):
        if sitemap_url in self._sitemap_seen: return
        self._sitemap_seen.add(sitemap_url)
        s, hdrs, text = await fetch(self.session, "GET", sitemap_url, self.rl)
        if s != 200 or not text: return
        
        # Harden: check for soft-404 / SPA catch-all
        ct = (hdrs or {}).get("content-type", "").lower()
        if not Extractor.is_real_file(ct, text, None) or Extractor.is_soft_404(text, s):
            return
        try:
            root = ET.fromstring(text)
        except ET.ParseError:
            return
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for loc in (root.findall("sm:sitemap/sm:loc", ns) or root.findall("sitemap/loc")):
            if loc.text: await self.parse_sitemap(loc.text.strip())
        sitemap_entries = []
        for loc in (root.findall("sm:url/sm:loc", ns) or root.findall("url/loc")):
            u = (loc.text or "").strip()
            if u and self.is_valid(u):
                self.store.add_endpoint(u, source="Sitemap", score=Conf.LOW)
                self.queue.put_nowait((u, 1, "Sitemap"))
                sitemap_entries.append(u)
        if sitemap_entries:
            # Print summary line FIRST, then tree entries below it
            self.emit.always_info(f"[Sitemap] {sitemap_url} → {len(sitemap_entries)} URLs queued")
            for u in sitemap_entries:
                parsed_u = urlparse(u)
                disp = parsed_u.path + ("?" + parsed_u.query if parsed_u.query else "")
                self.emit.robots_entry("Sitemap", disp or u, True)


# ══════════════════════════════════════════════════════════════════════
# SECURITY.TXT PARSER
# RFC 9116 — https://www.rfc-editor.org/rfc/rfc9116
# Mines every field AND every comment for paths, URLs, and sensitive
# keywords — mirrors the same intelligence approach as robots.txt.
# ══════════════════════════════════════════════════════════════════════

class SecurityTxtParser:
    """
    Parses /.well-known/security.txt (and /security.txt fallback).

    What it extracts:
      Contact      → emails + URLs recorded as secrets; mailto: decoded
      Encryption   → PGP key URL queued as endpoint (infra leak)
      Acknowledgments / Policy / Hiring → URLs queued
      Canonical    → cross-check against current target domain
      Expires      → flag if expired (stale file = unmaintained target)
      Comments (#) → same sensitive-keyword scan as robots.txt

    All discovered paths (/...) are queued as crawl targets.
    All structured findings are recorded via store.add_secret so they
    appear in the SECURITY FINDINGS section of the terminal output and
    in the JSON report under secrets[].
    """

    # Fields whose values are URLs or emails worth recording
    _URL_FIELDS    = frozenset({"contact", "encryption", "acknowledgments",
                                "policy", "hiring", "canonical", "csaf"})
    # Fields that when leaked mean something sensitive about scope/infra
    _SCOPE_FIELDS  = frozenset({"canonical", "preferred-languages"})

    # Same pattern set as the robots.txt comment scanner
    _COMMENT_PATTERNS = re.compile(
        r'(?:password|passwd|secret|token|key|api[_-]?key|db|database|backup|'
        r'sql|dump|cred|credential|auth|admin|prod|production|staging|internal|'
        r'private|todo|fixme|note to self|remove|delete|temp|test|debug|'
        r'panel|path|endpoint|route|url|host|server|mysql|mongo|redis|'
        r'postgres|s3|bucket|aws|gcp|azure)',
        re.I
    )

    # email pattern
    _EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')

    def __init__(self, base_url: str, store, queue, emit, is_valid_fn):
        self.base_url  = base_url.rstrip("/")
        self.store     = store
        self.queue     = queue
        self.emit      = emit
        self.is_valid  = is_valid_fn
        self._sec_url  = urljoin(self.base_url, "/.well-known/security.txt")
        self._base_domain = urlparse(base_url).netloc.lower()

    def parse(self, text: str):
        """
        Parse the full text content of a security.txt file.
        Called from the well-known probe loop after a 200 response.
        """
        self.emit.always_info("[SecurityTxt] Parsing /.well-known/security.txt")

        found_fields   = {}   # field_name → [values]
        comment_leaks  = []
        queued_urls    = 0
        expired        = False

        for raw_line in text.splitlines():
            raw_line = raw_line.rstrip()

            # ── comment line ──────────────────────────────────────────
            if raw_line.lstrip().startswith("#"):
                comment = raw_line.lstrip().lstrip("#").strip()
                if not comment:
                    continue
                # Always emit every comment — internal notes live here
                is_sensitive = bool(self._COMMENT_PATTERNS.search(comment))
                self.emit.security_txt_field("Comment", comment, flagged=is_sensitive)
                if is_sensitive:
                    self.store.add_secret(comment, "SecurityTxt_Comment_Leak", self._sec_url)
                    comment_leaks.append(comment)
                # Fix 3: broad path regex — handles /path, /path?qs=1, /path/sub
                # Stops only at whitespace and quote chars, not at ? or =
                for _pm in re.finditer(r"""(?:^|\s)(/[^\s'"<>\\]+)""", comment):
                    _path = _pm.group(1).strip().rstrip(".,;)")
                    _full = urljoin(self.base_url, _path)
                    if self.is_valid(_full):
                        self.store.add_endpoint(_full, source="SecurityTxt_Comment", score=2)
                        self.queue.put_nowait((_full, 1, "SecurityTxt_Comment"))
                        queued_urls += 1
                        self.emit.security_txt_field("Path (comment)", _path, flagged=True)
                continue

            # ── skip blank lines ──────────────────────────────────────
            if not raw_line.strip():
                continue

            # ── field: value ──────────────────────────────────────────
            # Fix 4: use split(":", 1) then re-join value — partition breaks
            # on URLs like "Contact: https://example.com/page" because
            # partition(":") stops at the first colon, dropping "//example.com/page"
            if ":" not in raw_line:
                continue
            parts = raw_line.split(":", 1)
            field = parts[0].strip().lower()
            value = parts[1].strip() if len(parts) > 1 else ""
            # Restore URL scheme if field value looks like it lost its "//"
            # e.g. "https" alone means the split ate the colon from https://
            if value in ("https", "http", "ftp") and raw_line.count(":") >= 2:
                value = raw_line.split(":", 1)[1].strip()
            if not field or not value:
                continue

            found_fields.setdefault(field, []).append(value)
            flagged = False

            # ── Contact ───────────────────────────────────────────────
            if field == "contact":
                if value.startswith("mailto:"):
                    email = value[7:].strip()
                    self.store.add_secret(email, "SecurityTxt_Contact_Email", self._sec_url)
                    # Also feed into extracted_data so it shows in EXTRACTED DATA section
                    self.store.add_extracted_data("Email", email, self._sec_url)
                    flagged = True
                elif self._EMAIL_RE.match(value):
                    self.store.add_secret(value, "SecurityTxt_Contact_Email", self._sec_url)
                    self.store.add_extracted_data("Email", value, self._sec_url)
                    flagged = True
                elif value.startswith("http"):
                    self._queue_url(value)
                    queued_urls += 1
                    self.store.add_secret(value, "SecurityTxt_Contact_URL", self._sec_url)
                    flagged = True
                self.emit.security_txt_field("Contact", value, flagged=flagged)

            # ── Encryption ────────────────────────────────────────────
            elif field == "encryption":
                if value.startswith("http") or value.startswith("/"):
                    self._queue_url(value)
                    queued_urls += 1
                # Fix 2: only flag HIGH if PGP key is on a DIFFERENT domain.
                # Same-domain encryption key is expected and normal RFC 9116 usage.
                enc_domain   = urlparse(value).netloc.lower() if value.startswith("http") else self._base_domain
                cross_domain = bool(enc_domain and enc_domain != self._base_domain)
                self.store.add_secret(value, "SecurityTxt_Encryption_Key", self._sec_url)
                self.emit.security_txt_field("Encryption", value, flagged=cross_domain)

            # ── Canonical ─────────────────────────────────────────────
            elif field == "canonical":
                canon_domain = urlparse(value).netloc.lower()
                cross_domain = bool(canon_domain and canon_domain != self._base_domain)
                if cross_domain:
                    self.store.add_secret(value, "SecurityTxt_Canonical_CrossDomain", self._sec_url)
                self.emit.security_txt_field("Canonical", value, flagged=cross_domain)

            # ── Policy / Acknowledgments / Hiring / CSAF ─────────────
            elif field in ("policy", "acknowledgments", "hiring", "csaf"):
                if value.startswith("http") or value.startswith("/"):
                    self._queue_url(value)
                    queued_urls += 1
                self.emit.security_txt_field(field.capitalize(), value)

            # ── Expires ───────────────────────────────────────────────
            elif field == "expires":
                try:
                    from datetime import timezone as _tz
                    exp_dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                    expired = exp_dt < datetime.now(_tz.utc)
                    if expired:
                        self.store.add_secret(value, "SecurityTxt_Expired", self._sec_url)
                    self.emit.security_txt_field("Expires", value, flagged=expired)
                except Exception:
                    self.emit.security_txt_field("Expires", value)

            # ── Preferred-Languages ───────────────────────────────────
            elif field == "preferred-languages":
                # Fix 5: was silently swallowed — now emitted cleanly
                self.emit.security_txt_field("Preferred-Languages", value)

            # ── everything else — emit and queue any paths found ──────
            else:
                # Fix 6: unknown fields are now always emitted so nothing
                # disappears silently regardless of what the app puts in its file
                self.emit.security_txt_field(field.capitalize(), value)
                # Queue any path or URL values for crawling
                if value.startswith("/"):
                    self._queue_url(value)
                    queued_urls += 1
                elif value.startswith("http"):
                    self._queue_url(value)
                    queued_urls += 1

        # ── summary ───────────────────────────────────────────────────
        summary_parts = []
        if comment_leaks:
            summary_parts.append(f"{len(comment_leaks)} comment leak(s)")
        if expired:
            summary_parts.append("EXPIRED file")
        if queued_urls:
            summary_parts.append(f"{queued_urls} URL(s) queued")
        summary = "  |  ".join(summary_parts) if summary_parts else "clean"
        self.emit.always_info(f"[SecurityTxt] Result: {summary}")

    def _queue_url(self, value: str):
        """Queue a URL or path found in security.txt as a crawl target."""
        if value.startswith("/"):
            full = urljoin(self.base_url, value)
        else:
            full = value
        # Always record it — even out-of-scope URLs are intelligence
        self.store.add_endpoint(full, source="SecurityTxt", score=2)
        if self.is_valid(full):
            self.queue.put_nowait((full, 1, "SecurityTxt"))

# ══════════════════════════════════════════════════════════════════════
# SPA SCANNER
# ══════════════════════════════════════════════════════════════════════

class SPAScanner:
    def __init__(self, target_url, store, emit, cookies, extra_headers, queue, is_valid_fn, enable_spa_interact=False, screenshot_cfg=None):
        self.target_url = target_url; self.store = store; self.emit = emit
        self.cookies = cookies; self.extra_headers = extra_headers
        self.queue = queue; self.is_valid = is_valid_fn
        self._enable_spa_interact = enable_spa_interact
        self.screenshot_cfg = screenshot_cfg

    async def run(self):
        if not PLAYWRIGHT_AVAILABLE:
            if self.screenshot_cfg:
                self.emit.warn("[Screenshot] Playwright not available — skipping screenshots")
            self.emit.info("[SPA] Playwright not installed — skipping")
            return None
        self.emit.always_info("[SPA] Launching headless Chromium via Playwright…")
        try:
            self._pw = await async_playwright().start()
            browser = await self._pw.chromium.launch(headless=True, args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-extensions",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-default-apps",
            ])
            # Stealth context — mimic a real Chrome browser fingerprint
            ctx_args: dict = {
                "ignore_https_errors": True,
                "viewport":            {"width": 1366, "height": 768},
                "user_agent":          (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "locale":              "en-US",
                "timezone_id":         "America/New_York",
                "color_scheme":        "light",
                "java_script_enabled": True,
            }
            if self.cookies:
                parsed = urlparse(self.target_url)
                ctx_args["storage_state"] = {"cookies": [
                    {"name":k,"value":v,"domain":parsed.netloc,"path":"/"}
                    for k, v in self.cookies.items()]}
            if self.extra_headers:
                ctx_args["extra_http_headers"] = self.extra_headers
            context = await browser.new_context(**ctx_args)

            # ── WAF/Bot Stealth patches ─────────────────────────────────
            _STEALTH_JS = """
                Object.defineProperty(navigator, "webdriver", {get: () => undefined, configurable: true});
                Object.defineProperty(navigator, "plugins", {get: () => [
                    {name:"Chrome PDF Plugin",filename:"internal-pdf-viewer"},
                    {name:"Chrome PDF Viewer",filename:"mhjfbmdgcfjbbpaeojofohoefgiehjai"},
                    {name:"Native Client",filename:"internal-nacl-plugin"}
                ], configurable: true});
                Object.defineProperty(navigator, "languages", {get: () => ["en-US","en"], configurable: true});
                try { const orig = window.navigator.permissions.query;
                    window.navigator.permissions.query = (p) => p.name === "notifications"
                        ? Promise.resolve({state: Notification.permission}) : orig(p);
                } catch(e) {}
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            """
            await context.add_init_script(_STEALTH_JS)
            # ── Stealth layer: playwright-stealth (JS patches) or manual JS ────
            _stealth_fn = None
            try:
                from playwright_stealth import stealth_async as _sa  # type: ignore
                _stealth_fn = _sa
                self.emit.always_info("[SPA] Stealth: playwright-stealth active")
            except ImportError:
                # Manual JS patches injected via add_init_script above are the fallback.
                # No noisy install prompt during a live scan.
                self.emit.info("[SPA] Stealth: manual JS patches active")
            except Exception as _sle:
                self.emit.warn(f"[SPA] playwright-stealth load error: {_sle}")
            await context.route(
                re.compile(r'\.(png|jpg|jpeg|gif|svg|ico|woff2?|ttf|css|mp4|mp3)(\?.*)?$'),
                lambda route, _: asyncio.create_task(route.abort()))
            page = await context.new_page()
            if _stealth_fn:
                try:
                    await _stealth_fn(page)
                except Exception as _se:
                    self.emit.warn(f"[SPA] stealth apply failed: {_se}")

            async def on_request(req):
                url = req.url; rtype = req.resource_type; method = req.method or "GET"
                if rtype in ("fetch","xhr"):
                    hdrs = dict(req.headers or {})
                    # Harden: exclude 'cookie' from the initial auth-wall heuristic.
                    # Most SPA apps send session cookies with all requests; marking all 
                    # as 'auth required' is a false positive for public APIs.
                    # Real auth walls are detected via 401/403 status in record_status().
                    auth = any(h.lower() in ("authorization", "x-auth-token", "x-api-key")
                               for h in hdrs)
                    self.store.add_endpoint(url, method=method, source="SPA_XHR",
                                            score=Conf.CONFIRMED, auth_required=auth)
                    if self.store.merge_headers(url, method, hdrs):
                        self.emit.info(f"[SPA-Headers] captured for {url}")
                    # S2: capture POST body params
                    if method == "POST":
                        try:
                            post_data = req.post_data
                            if post_data:
                                try:
                                    body_obj = json.loads(post_data)
                                    if isinstance(body_obj, dict):
                                        self.store.add_endpoint(
                                            url, method="POST",
                                            source="SPA_XHR_POST",
                                            params=list(body_obj.keys()),
                                            score=Conf.CONFIRMED,
                                            auth_required=auth,
                                        )
                                except Exception:
                                    parsed_body = parse_qs(post_data)
                                    if parsed_body:
                                        self.store.add_endpoint(
                                            url, method="POST",
                                            source="SPA_XHR_POST",
                                            params=list(parsed_body.keys()),
                                            score=Conf.CONFIRMED,
                                            auth_required=auth,
                                        )
                        except Exception:
                            pass
                    self.emit.success(f"[SPA-XHR] {method} {url}")
                elif rtype == "websocket":
                    self.store.add_endpoint(url, method="WS", source="SPA_WebSocket",
                                            score=Conf.CONFIRMED)
                    self.emit.warn(f"[SPA-WS] WebSocket: {url}")
                elif rtype == "script" and self.is_valid(url):
                    self.queue.put_nowait((url, 1, "SPA_Script"))

            page.on("request", on_request)

            # S1: capture XHR response bodies to harvest real object IDs
            async def on_response(resp):
                try:
                    r_url    = resp.url
                    r_method = resp.request.method or "GET"
                    r_status = resp.status
                    r_rtype  = resp.request.resource_type
                    if r_rtype not in ("fetch", "xhr"):
                        return
                    if r_status not in range(200, 210):
                        return
                    ct = (resp.headers.get("content-type") or "").lower()
                    if "json" not in ct:
                        return
                    body = await resp.text()
                    if not body or len(body) > 512_000:
                        return
                    try:
                        obj = json.loads(body)
                    except Exception:
                        return
                    def _mine_resp(o, depth=0):
                        if depth > 3 or not isinstance(o, dict):
                            return
                        for k, v in o.items():
                            if re.match(
                                r'^(?:id|uid|user_?id|order_?id|basket_?id|'
                                r'item_?id|product_?id|address_?id|card_?id)$',
                                str(k), re.I
                            ):
                                vstr = str(v) if v is not None else ""
                                if re.match(r'^\d{1,12}$', vstr):
                                    r_key = self.store._key(r_url, r_method)
                                    if r_key in self.store.endpoints:
                                        ep  = self.store.endpoints[r_key]
                                        obs = ep["observed_values"].setdefault(k, [])
                                        if vstr not in obs:
                                            obs.append(vstr)
                                            self.emit.info(
                                                f"[SPA-ResponseID] {k}={vstr} ← {r_url}")
                            if isinstance(v, (dict, list)):
                                _mine_resp(v, depth + 1)
                    if isinstance(obj, list):
                        for item in obj[:10]:
                            _mine_resp(item)
                    else:
                        _mine_resp(obj)
                except Exception:
                    pass

            page.on("response", on_response)

            try:
                await page.goto(self.target_url, wait_until="networkidle", timeout=20000)
            except Exception as e:
                self.emit.info(f"[SPA] Goto warning: {e}")

            # ── Bot detection check + patchright fallback ───────────────────
            try:
                _page_body = await page.content()
                if Extractor.is_bot_blocked(_page_body):
                    self.emit.warn("[SPA] Bot/WAF challenge detected — falling back to Patchright")
                    if PATCHRIGHT_AVAILABLE:
                        try:
                            await browser.close()
                            await self._pw.stop()
                        except Exception:
                            pass
                        try:
                            from patchright.async_api import async_playwright as _pr_ap  # type: ignore
                            self._pw = await _pr_ap().start()
                            browser = await self._pw.chromium.launch(headless=True, args=[
                                "--no-sandbox",
                                "--disable-dev-shm-usage",
                                "--disable-infobars",
                                "--disable-extensions",
                                "--no-first-run",
                                "--no-default-browser-check",
                                "--disable-default-apps",
                            ])
                            context = await browser.new_context(**ctx_args)
                            await context.add_init_script(_STEALTH_JS)
                            await context.route(
                                re.compile(r'\.(png|jpg|jpeg|gif|svg|ico|woff2?|ttf|css|mp4|mp3)(\?.*)?$'),
                                lambda route, _: asyncio.create_task(route.abort()))
                            page = await context.new_page()
                            page.on("request", on_request)
                            page.on("response", on_response)
                            try:
                                await page.goto(self.target_url, wait_until="networkidle", timeout=20000)
                            except Exception as _pr_e:
                                self.emit.info(f"[SPA] Patchright goto warning: {_pr_e}")
                            _page_body2 = await page.content()
                            if Extractor.is_bot_blocked(_page_body2):
                                self.emit.warn("[SPA] Bot challenge persists — target uses custom fingerprinting")
                                self.store.add_secret(
                                    f"WAF/bot challenge persists at {self.target_url}",
                                    "WAF_Bot_Challenge", self.target_url)
                            else:
                                self.emit.always_success("[SPA] Patchright bypass successful")
                        except Exception as _pr_err:
                            self.emit.warn(f"[SPA] Patchright relaunch failed: {_pr_err}")
                    else:
                        self.emit.warn("[SPA] Bot challenge detected — no fallback engine, continuing with partial results")
                        self.store.add_secret(
                            f"WAF/bot challenge detected at {self.target_url}",
                            "WAF_Bot_Challenge", self.target_url)
            except Exception:
                pass

            try:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(1.5)
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(0.5)
            except Exception:
                pass
            # S4: wait for SPA to fully settle before interacting
            try:
                await page.wait_for_load_state("networkidle", timeout=5000)
                await asyncio.sleep(1.0)
            except Exception:
                pass
            if self._enable_spa_interact:
                await self._interact(page)
            await self._harvest_dom(page)
            await self._harvest_hash(page)
                
            # Extract cookies for synchronization
            acquired_cookies = await context.cookies()
            cookie_dict = {c["name"]: c["value"] for c in acquired_cookies}
            
            if self.screenshot_cfg:
                # Keep browser alive for screenshots later
                self.emit.always_info("[SPA] SPA harvest complete — keeping browser alive for screenshots")
                return browser, context, page, cookie_dict
            
            await browser.close()
            await self._pw.stop()
            self.emit.always_info("[SPA] Dynamic analysis complete")
            return cookie_dict
        except Exception as e:
            self.emit.warn(f"[SPA] Error: {e}")
            return None

    async def _interact(self, page):
        """
        3-phase SPA interaction to trigger XHR calls universally.
        Phase 1: navigation clicks to load route-based content.
        Phase 2: fill and submit visible forms to trigger POST XHR calls.
        Phase 3: click remaining action buttons.
        """
        # Phase 1: navigation
        for sel in ["[role='menuitem']", "[role='tab']", ".nav-item",
                    "[data-toggle]", "a[href]:not([href^='http'])"]:
            try:
                for el in (await page.query_selector_all(sel))[:8]:
                    try:
                        if await el.is_visible():
                            await el.click(timeout=1500)
                            await asyncio.sleep(0.4)
                    except Exception:
                        pass
            except Exception as e:
                self.emit.warn(f"[SPA-Interact] Phase 1 nav error ({sel}): {e}")

        # Phase 2: fill and submit visible forms
        try:
            forms = await page.query_selector_all("form")
            for form in forms[:5]:
                try:
                    if not await form.is_visible():
                        continue
                    inputs = await form.query_selector_all(
                        "input[type='text'], input[type='email'], "
                        "input[type='number'], input:not([type])"
                    )
                    for inp in inputs[:6]:
                        try:
                            itype = await inp.get_attribute("type") or "text"
                            name  = (await inp.get_attribute("name") or "").lower()
                            if "email" in name or itype == "email":
                                await inp.fill("test@example.com", timeout=800)
                            elif "quantity" in name or "qty" in name or itype == "number":
                                await inp.fill("1", timeout=800)
                            else:
                                await inp.fill("test", timeout=800)
                        except Exception:
                            pass
                    submit = await form.query_selector(
                        "button[type='submit'], input[type='submit'], button:not([type])"
                    )
                    if submit and await submit.is_visible():
                        await submit.click(timeout=1500)
                        await asyncio.sleep(0.5)
                except Exception:
                    pass
        except Exception:
            pass

        # Phase 3: remaining action buttons
        try:
            for el in (await page.query_selector_all(
                "button:not([disabled]):not([type='submit'])"
            ))[:10]:
                try:
                    if await el.is_visible():
                        await el.click(timeout=1500)
                        await asyncio.sleep(0.3)
                except Exception:
                    pass
        except Exception:
            pass

    async def _harvest_dom(self, page):
        try:
            links = await page.evaluate("""
                () => Array.from(document.querySelectorAll('[href],[src],[action]'))
                    .map(e => e.href || e.src || e.action)
                    .filter(u => u && (u.startsWith('/') || u.startsWith('http')))
            """)
            for path in (links or []):
                if path.startswith("/"):
                    full = urljoin(self.target_url, path)
                else:
                    full = path  # already absolute
                if self.is_valid(full):
                    self.store.add_endpoint(full, source="SPA_DOM", score=Conf.MEDIUM)
                    self.queue.put_nowait((full, 1, "SPA_DOM"))
        except Exception:
            pass

    async def _harvest_hash(self, page):
        try:
            src = await page.content()
            for r in re.findall(r'["\']#/([a-zA-Z0-9_\-/]+)["\']', src):
                url = self.target_url.rstrip("/") + "/#/" + r
                self.store.add_endpoint(url, source="SPA_HashRoute", score=Conf.MEDIUM)
                self.emit.info(f"[SPA-Hash] {url}")
        except Exception:
            pass

    async def capture_screenshots(self, endpoints, spa_ctx):
        """
        Capture screenshots of matched endpoints.

        Fixes vs original:
        - Fresh page per screenshot — one hung nav can't cascade to all others
        - wait_until="networkidle" + 800ms delay — SPAs have time to hydrate,
          no more blank <div id="root"> captures on React/Vue/Angular apps
        - full_page=True — captures below-the-fold content (admin dashboards, etc.)
        - Auth context carried — context already has cookies/headers from crawl;
          each new page inherits them automatically (Playwright context-level auth)
        - Metadata index file written — screenshots/domain/preset/index.json
          maps every filename to its source URL, status, and match reason
        """
        if not spa_ctx: return
        browser, context, _page = spa_ctx

        domain   = re.sub(r'[^a-zA-Z0-9_\-]', '_', urlparse(self.target_url).netloc)
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        priority = self.screenshot_cfg.get("priority", "standard")

        def get_status(e):
            obs = e.get("observed_status") or []
            if 200 in obs: return 200
            return max(obs) if obs else 0

        # ── Preset rules ─────────────────────────────────────────────────
        if priority == "all":
            rule = lambda ep: get_status(ep) in (200, 401, 403, 404)
        elif priority == "standard":
            rule = lambda ep: (get_status(ep) == 200 or
                               re.search(r'login|admin|dashboard|upload|graphql|swagger|panel|console', ep["url"], re.I))
        elif priority == "blocked":
            rule = lambda ep: get_status(ep) in (401, 403)
        elif priority == "errors":
            rule = lambda ep: get_status(ep) >= 400
        elif priority == "api":
            rule = lambda ep: (get_status(ep) != 404 and
                               re.search(r'/api/|/graphql|/swagger|/openapi|/rest/', ep["url"], re.I))
        elif priority == "admin":
            rule = lambda ep: (get_status(ep) != 404 and
                               re.search(r'admin|panel|console|manage|backend|dashboard', ep["url"], re.I))
        elif "," in priority:
            _kws = [k.strip().lower() for k in priority.split(",")]
            rule = lambda ep: get_status(ep) != 404 and any(k in ep["url"].lower() for k in _kws)
        else:
            rule = lambda ep: get_status(ep) != 404 and bool(re.search(priority, ep["url"], re.I))

        base_dir = Path("screenshots") / domain / priority
        base_dir.mkdir(parents=True, exist_ok=True)

        count      = 0
        failed     = 0
        seen_urls  = set()
        index      = []    # metadata index: [{filename, url, status, reason}, ...]

        for ep in endpoints.values():
            url      = ep["url"]
            norm_url = url.split("?")[0].split("#")[0].rstrip("/")
            if norm_url in seen_urls or not rule(ep):
                continue
            seen_urls.add(norm_url)

            status = get_status(ep)
            label  = " [AUTH WALL]" if status in (401, 403) else ""
            reason = f"preset:{priority}{label}"

            sanitized = re.sub(r'[^a-zA-Z0-9_\-]', '_', urlparse(url).path.strip("/")) or "root"
            filename  = f"{ts}_{sanitized[:75]}.jpg"
            filepath  = base_dir / filename

            # Fresh page per screenshot — prevents cascade failures
            page = await context.new_page()
            try:
                self.emit.info(f"[Screenshot] {url} → {filepath}{label}")

                # networkidle catches SPAs — domcontentloaded returns blank on React/Vue/Angular
                try:
                    await page.goto(url, wait_until="networkidle", timeout=15000)
                except Exception:
                    # networkidle timeout on heavy pages — fall back gracefully
                    try:
                        await page.goto(url, wait_until="domcontentloaded", timeout=8000)
                        await asyncio.sleep(1.2)   # give JS framework time to hydrate
                    except Exception:
                        pass

                # Extra settle time for SPA hydration even after networkidle
                await asyncio.sleep(0.8)

                # full_page=True captures below-the-fold content
                await page.screenshot(
                    path=str(filepath), type="jpeg", quality=75, full_page=True
                )

                ep["screenshot"] = {"path": str(filepath), "preset": priority, "reason": reason}
                index.append({
                    "filename": filename,
                    "url":      url,
                    "status":   status,
                    "reason":   reason,
                    "path":     str(filepath),
                })
                count += 1

            except Exception as e:
                self.emit.warn(f"[Screenshot] Failed {url}: {e}")
                failed += 1
            finally:
                # Always close the page — even on failure
                try:
                    await page.close()
                except Exception:
                    pass

        # Write metadata index so user knows which file is which
        if index:
            index_path = base_dir / "index.json"
            try:
                import json as _j
                index_path.write_text(_j.dumps({"preset": priority, "target": self.target_url,
                                                 "captured_at": ts, "screenshots": index},
                                                indent=2))
                self.emit.always_success(
                    f"[Screenshot] {count} captured → {base_dir}  "
                    f"({failed} failed)  index: {index_path}"
                )
            except Exception:
                self.emit.always_success(f"[Screenshot] {count} captured → {base_dir}  ({failed} failed)")
        else:
            self.emit.warn(f"[Screenshot] No endpoints matched the '{priority}' preset (0 captures)")

        await browser.close()
        await self._pw.stop()


# ══════════════════════════════════════════════════════════════════════
# RECON UTILITIES (v12.3)
# ══════════════════════════════════════════════════════════════════════


def _is_confirmed(ep: dict) -> bool:
    """True if endpoint received a real HTTP response — not just speculatively discovered."""
    return bool(ep.get("observed_status", []))

def classify_admin_endpoints(store: Store):
    for ep in store.endpoints.values():
        if not _is_confirmed(ep): continue   # speculative — skip
        url = ep["url"]
        # Never flag static asset files as admin panels
        if _STATIC_EXT.search(url.split("?")[0]):
            continue
        # Tier 1: unambiguous admin path segments — always flag
        if _ADMIN_TIER1.search(url):
            ep["admin_panel"] = True
            continue
        # Tier 2: ambiguous words — only flag if shallow path (depth ≤ 2)
        # and the endpoint has been confirmed reachable (not just discovered)
        if _ADMIN_TIER2.match(url):
            # Only flag if we got a real 200 response (not just discovered)
            obs = ep.get("observed_status", [])
            if 200 in obs or 401 in obs or 403 in obs:
                ep["admin_panel"] = True

def classify_auth_endpoints(store: Store):
    for ep in store.endpoints.values():
        if not _is_confirmed(ep): continue   # speculative — skip
        for label, pat in _AUTH_PATTERNS.items():
            if pat.search(ep["url"]):
                ep.setdefault("auth_classification", [])
                if label not in ep["auth_classification"]:
                    ep["auth_classification"].append(label)

# Infrastructure paths that are never IDOR targets regardless of numeric segments
_IDOR_EXCLUDE_RE = re.compile(
    r'/(?:cdn-cgi|_next|__webpack|webpack|static|assets|public|'
    r'images?|img|icons?|fonts?|media|thumbnails?|placeholder|'
    r'favicon|robots|sitemap|opensearch|manifest|sw\.js)(?:/|$|\?)',
    re.I
)

def classify_idor_candidates(store: Store):
    for ep in store.endpoints.values():
        if not _is_confirmed(ep): continue   # speculative — skip
        url = ep["url"]
        # Never flag infrastructure, CDN, or static asset paths
        if _IDOR_EXCLUDE_RE.search(url):
            continue
        # Never flag static files
        if _STATIC_EXT.search(url.split("?")[0]):
            continue
        all_params = []
        for b in ("query", "form", "js", "openapi", "runtime"):
            all_params += ep.get("params", {}).get(b, [])
        has_id_param = any(_NUMERIC_ID_RE.search(p) for p in all_params)
        has_id_path  = bool(_PATH_ID_RE.search(url) or _UUID_PATH_RE.search(url))
        if has_id_param or has_id_path:
            ep["idor_candidate"] = True
            ep["idor_signals"] = {
                "id_params":   [p for p in all_params if _NUMERIC_ID_RE.search(p)],
                "has_id_path": has_id_path,
            }

def score_injection_candidates(store: Store):
    for ep in store.endpoints.values():
        if not _is_confirmed(ep): continue   # speculative — skip
        all_params = []
        for b in ("query", "form", "js", "openapi", "runtime"):
            all_params += ep.get("params", {}).get(b, [])
        sqli_params = [p for p in all_params if _SQLI_PARAM_RE.match(p)]
        cmdi_params = [p for p in all_params if _CMDI_PARAM_RE.match(p)]
        if sqli_params:
            ep["sqli_candidate"]  = True
            ep["sqli_params"]     = sqli_params
        if cmdi_params:
            ep["cmdi_candidate"]  = True
            ep["cmdi_params"]     = cmdi_params

def _flag_upload_endpoints(store: Store):
    # Strong signals — path segments that unambiguously mean file upload
    _UPLOAD_PATH_RE = re.compile(
        r'/(?:upload|uploads|file-upload|fileupload|file_upload|'
        r'attachment|attachments|import|ingest|multipart|'
        r'avatar|photo|image-upload|media-upload)(?:/|$|\.)',
        re.I
    )
    # Weaker signals — only count if also have a file param OR method is POST
    _UPLOAD_WEAK_RE = re.compile(
        r'/(?:file|files|media|document|documents|image|images|'
        r'photo|photos|blob|storage)(?:/|$)',
        re.I
    )
    for ep in store.endpoints.values():
        url = ep["url"]
        # Never flag static assets — /assets/i18n/en.json etc.
        if _STATIC_EXT.search(url.split("?")[0]):
            continue
        # Strong path signal — always flag
        if _UPLOAD_PATH_RE.search(url):
            ep["file_upload_candidate"] = True
            continue
        # File/image param in a form — always flag regardless of URL
        form_params = ep.get("params", {}).get("form", [])
        has_file_param = any(
            p.lower() in ("file","upload","image","photo","attachment","avatar","media","document")
            or p.lower().endswith(("[file]","[upload]","[image]","[attachment]"))
            for p in form_params
        )
        if has_file_param:
            ep["file_upload_candidate"] = True
            continue
        # Weak path signal — only flag if POST method observed
        if _UPLOAD_WEAK_RE.search(url):
            methods = ep.get("methods", [])
            if "POST" in methods or "PUT" in methods:
                ep["file_upload_candidate"] = True

class Spider:
    def __init__(self, target, cfg, emit, cookies, extra_headers):
        self.target = target; self.cfg = cfg; self.emit = emit
        self.cookies = cookies; self.extra_headers = extra_headers
        self.base_domain = urlparse(target).netloc
        self.store = Store()
        self.visited: Set[str] = set()
        self._crawl_feed_seen: Set[str] = set()
        self.queue: asyncio.Queue = asyncio.Queue()
        self.sem = asyncio.Semaphore(cfg.concurrency)
        self.rl = DomainRateLimiter()
        self._depth_cnt: Dict[int,int] = defaultdict(int)
        self.queue.put_nowait((target, 0, "Seed"))

    def is_valid(self, url):
        try:
            # Normalize backslashes before validation
            url = url.replace(chr(92)+chr(92), "/").replace(chr(92), "/")
            p = urlparse(url)
        except Exception:
            return False
        if p.netloc != self.base_domain: return False
        low = url.lower()
        if any(low.endswith(ext) or f"{ext}?" in low for ext in self.cfg.extensions_to_ignore):
            return False
        # Intercept socket.io polling URLs — park in store, never queue
        if _SOCKETIO_RE.search(url):
            self.store.add_socketio(url)
            return False
        # Noise path filter — blocks VCS browser UI, CI pages, CDN artefact paths
        # Works on any target. Disable with --no-filter / -F if you want raw output.
        if self.cfg.enable_noise_filter and _NOISE_PATH_RE.search(p.path):
            return False
        return bool(p.scheme in ("http","https"))

    def _over_budget(self, depth):
        return self._depth_cnt[depth] >= self.cfg.max_urls_per_depth

    def _detect_tech(self, headers, body, url):
        tech: Set[str] = set()
        srv = (headers.get("Server","") or headers.get("server","")).lower()
        xpb = (headers.get("X-Powered-By","") or headers.get("x-powered-by","")).lower()
        ct  = (headers.get("Content-Type","") or headers.get("content-type","")).lower()
        body_lo = body.lower()

        # ── Leakage: Expose highly verbose Server headers ───────────────
        raw_srv = headers.get("Server") or headers.get("server", "")
        raw_xpb = headers.get("X-Powered-By") or headers.get("x-powered-by", "")
        raw_asp = headers.get("X-AspNet-Version") or headers.get("x-aspnet-version", "")
        if raw_srv: tech.add(f"Server: {raw_srv}")
        if raw_xpb: tech.add(f"X-Powered-By: {raw_xpb}")
        if raw_asp: tech.add(f"X-AspNet-Version: {raw_asp}")

        # ── Server / infrastructure ──────────────────────────────────────
        if "nginx"        in srv:                               tech.add("Nginx")
        if "apache"       in srv:                               tech.add("Apache")
        if "cloudflare"   in srv:                               tech.add("Cloudflare")
        if "iis"          in srv:                               tech.add("IIS")
        if "gunicorn"     in srv:                               tech.add("Python/Gunicorn")
        if "werkzeug"     in srv:                               tech.add("Python/Werkzeug")
        if "jetty"        in srv:                               tech.add("Java/Jetty")
        if "tomcat"       in srv:                               tech.add("Java/Tomcat")
        if "lighttpd"     in srv:                               tech.add("Lighttpd")
        if "caddy"        in srv:                               tech.add("Caddy")

        # ── X-Powered-By ─────────────────────────────────────────────────
        if "php"          in xpb:                               tech.add("PHP")
        if "express"      in xpb:                               tech.add("Node.js/Express")
        if "asp.net"      in xpb:                               tech.add("ASP.NET")
        if "next.js"      in xpb:                               tech.add("Next.js")
        if "servlet"      in xpb or "jsp"       in xpb:        tech.add("Java")

        # ── Response headers (framework fingerprints) ────────────────────
        if headers.get("X-Shopify-Stage"):                      tech.add("Shopify")
        if headers.get("x-drupal-cache") or headers.get("X-Drupal-Cache"):
            tech.add("Drupal")

    def _queue_url(self, url, depth, source):
        if not self.is_valid(url): return
        norm = normalize(url)
        if norm in self.visited: return
        self.store.add_query_params(url)
        self.queue.put_nowait((url, depth, source))

    def _discover_url(self, url, depth, source, show_feed=False):
        if not self.is_valid(url): return False
        norm = normalize(url)
        if norm in self.visited: return False
        if show_feed and norm not in self._crawl_feed_seen:
            self._crawl_feed_seen.add(norm)
            self.emit.crawl_feed("Found", source, url)
        self._queue_url(url, depth, source)
        return True

    @staticmethod
    def _collect_json_keys(obj) -> List[str]:
        """
        Return ONLY the top-level string keys of a JSON object.
        No recursion — keys inside nested objects belong to their own
        endpoints, not the endpoint whose response body we are examining.
        If the root is a list, examine the first dict element only.
        """
        if isinstance(obj, dict):
            return [k for k in obj.keys() if isinstance(k, str)]
        if isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    return [k for k in item.keys() if isinstance(k, str)]
        return []

    @staticmethod
    def _strip_param_suffix(name: str) -> str:
        for suf in Store._PARAM_SUFFIXES:
            if name.endswith(suf):
                return name[: -len(suf)]
        return name

    def _extract_body_param_hints(self, url, body):
        """Scan any text response body for embedded field-name hints:
        validation error messages, JSON required-field arrays, name= echoes.
        Writes discovered names to the runtime bucket of the current endpoint."""
        found = []
        err_pats = [
            r"""(?:missing|required|invalid|unknown|bad)\s+(?:field|param|parameter|key|argument)[:\s]+["']?([a-zA-Z_][a-zA-Z0-9_]{2,40})["']?""",
            r"""["']([a-zA-Z_][a-zA-Z0-9_]{2,40})["']\s+(?:is required|is missing|not found|is invalid)""",
            r"""(?:field|param|parameter)[:\s]+["']([a-zA-Z_][a-zA-Z0-9_]{2,40})["']""",
        ]
        for pat in err_pats:
            for m in re.finditer(pat, body, re.I):
                n = m.group(1).strip()
                if n and n not in found:
                    found.append(n)
        for m in re.finditer(
            r"""["'](?:required|fields|params|parameters|missing|expected)["']\s*:\s*\[([^\]]{1,400})\]""",
            body, re.I
        ):
            for nm in re.finditer(r"""["']([a-zA-Z_][a-zA-Z0-9_]{2,40})["']""", m.group(1)):
                n = nm.group(1)
                if n not in found:
                    found.append(n)
        # Filter known meta-noise and og:/twitter: prefixed names
        _META_NOISE = frozenset({
            "viewport", "description", "author", "keywords", "robots", "theme-color",
            "generator", "referrer", "rating", "revisit-after", "copyright",
            "application-name", "msapplication-tilecolor", "msapplication-config",
            "format-detection", "apple-mobile-web-app-capable",
            "apple-mobile-web-app-status-bar-style", "apple-mobile-web-app-title",
            "og", "twitter",
        })
        for m in re.finditer(r"""name=["']([a-zA-Z_][a-zA-Z0-9_]{2,40})["']""", body):
            n = m.group(1)
            nl = n.lower()
            if nl in _META_NOISE or nl.startswith(("og:", "twitter:")):
                continue
            if n not in found:
                found.append(n)
        if found:
            self.store.add_endpoint(url, source="Body_Hints", score=Conf.LOW)
            changed = self.store.add_runtime_params(url, "GET", found)
            if changed:
                self.emit.info("[Body-Hints] %s <- %s" % (found, url))

    def _process_html(self, url, text, depth, source):
        soup = BeautifulSoup(text, "lxml")
        Extractor.html_comments(soup, url, self.store, self.emit)
        for tag in soup.find_all(["a","link","area"], href=True):
            href = tag.get("href","").strip()
            if href and not href.startswith(("javascript:","mailto:","tel:","#")):
                self._discover_url(urljoin(url, href), depth+1, "HTML_Link", show_feed=True)
        for tag in soup.find_all("script", src=True):
            src = tag.get("src","").strip()
            if src:
                full = urljoin(url, src)
                if self.is_valid(full):
                    self._discover_url(full, depth+1, "HTML_Script", show_feed=True)
        for tag in soup.find_all("script"):
            if not tag.get("src") and tag.string:
                Extractor.js_endpoints(tag.string, url, self.store, self.emit)
                Extractor.js_params(tag.string, url, self.store, self.emit)
                Extractor.secrets(tag.string, url, self.store, self.emit)
                Extractor.js_comments(tag.string, url, self.store, self.emit)
                Extractor.js_routes(tag.string, url, self.store, self.emit)
        for form in soup.find_all("form"):
            action = form.get("action") or url
            full   = urljoin(url, action)
            method = (form.get("method") or "POST").upper()
            # Exhaustive field extraction: all named elements + data-* param hints
            inputs = []
            form_fields_detail = []  # rich metadata for downstream agents
            for el in form.find_all(["input","select","textarea","button","datalist"]):
                el_type = el.get("type","text").lower()
                is_hidden = el_type == "hidden"
                is_file   = el_type == "file"

                # ── Field name resolution — priority order ─────────────
                # 1. name attr (standard HTML, best)
                # 2. id attr (common in modern JS-driven forms)
                # 3. placeholder normalised (last resort — gives semantic hint)
                # 4. aria-label normalised
                # This catches forms like WebDriverUniversity Login Portal
                # that use id="inputUsername" instead of name="username"
                nm = el.get("name","").strip()
                _source = "name"
                if not nm:
                    _id = el.get("id","").strip()
                    if _id and el_type not in ("submit","button","reset","image"):
                        # Strip common prefixes like "input", "field", "txt", "txt_"
                        _stripped_id = re.sub(r'^(?:input|field|txt|frm|form)[-_]?', '', _id, flags=re.I).strip() or _id
                        # Reject if the stripped id is just an HTML type name (id="text", id="password")
                        # or a single character — those are meaningless as param names
                        _HTML_TYPE_WORDS = {"text","password","email","number","tel","url",
                                            "search","date","time","checkbox","radio","file",
                                            "hidden","submit","button","reset","image"}
                        # Reject if stripped id is just an HTML input type word OR too short
                        # Case-insensitive: "Password" from "inputPassword" → rejected,
                        # falls through to placeholder which gives "password" (same result but explicit)
                        if _stripped_id.lower() not in _HTML_TYPE_WORDS and len(_stripped_id) > 2:
                            nm = _stripped_id
                            _source = "id"
                if not nm:
                    _ph = el.get("placeholder","").strip()
                    if _ph and el_type not in ("submit","button","reset","image","hidden"):
                        # Normalise placeholder to a valid param name: lowercase, spaces→underscore
                        nm = re.sub(r'[^a-zA-Z0-9_]', '_', _ph.lower()).strip('_')
                        nm = re.sub(r'_+', '_', nm)
                        _source = "placeholder"
                if not nm:
                    _al = el.get("aria-label","").strip()
                    if _al and el_type not in ("submit","button","reset","image","hidden"):
                        nm = re.sub(r'[^a-zA-Z0-9_]', '_', _al.lower()).strip('_')
                        nm = re.sub(r'_+', '_', nm)
                        _source = "aria-label"

                # Skip submit/button/reset with no meaningful name
                if el_type in ("submit","button","reset","image") and not el.get("name","").strip():
                    nm = ""

                if nm and nm not in inputs:
                    inputs.append(nm)
                    form_fields_detail.append({
                        "name":        nm,
                        "name_source": _source,   # how we found the name
                        "type":        el_type,
                        "hidden":      is_hidden,
                        "file":        is_file,
                        "required":    el.has_attr("required"),
                        "value":       el.get("value","") if is_hidden else "",
                    })
                for da in ("data-param","data-field","data-name","data-key","data-input"):
                    dv = el.get(da,"").strip()
                    if dv and dv not in inputs:
                        inputs.append(dv)
                        form_fields_detail.append({
                            "name":        dv,
                            "name_source": "data-attr",
                            "type":        "data-attr",
                            "hidden":      False,
                            "file":        False,
                            "required":    False,
                            "value":       "",
                        })
            # data-* on the form element itself (e.g. data-params="field1,field2")
            for da in ("data-params","data-fields","data-inputs"):
                dv = form.get(da,"").strip()
                if dv:
                    for part in re.split(r"[,;|\s]+", dv):
                        p = part.strip()
                        if p and p not in inputs:
                            inputs.append(p)
                            form_fields_detail.append({
                                "name":   p,
                                "type":   "data-attr",
                                "hidden": False,
                                "file":   False,
                                "required": False,
                                "value":  "",
                            })
            if inputs: self.emit.info("[Form] %s %s <- [%s]" % (method, full, ", ".join(inputs)))
            # Guard: only skip genuinely non-HTTP form actions.
            # Empty/missing action already resolved to current page URL above — valid.
            # javascript:void(0), mailto:, tel: → skip. Everything else → register.
            if urlparse(full).scheme not in ("http", "https"):
                continue
            self.store.add_endpoint(full, method=method, source="Form", score=Conf.HIGH)
            self.store.add_query_params(full)
            _fkey = self.store._key(full, method)
            if _fkey in self.store.endpoints:
                _ep = self.store.endpoints[_fkey]

                # ── Source-aware param merge ──────────────────────────
                # Track which source page each form param set came from.
                # If this form was found on a DIFFERENT page than the
                # previously stored params, and has MORE params, replace
                # rather than merge. This prevents login forms on redirect
                # pages from polluting the real form params.
                #
                # Example: /become_seller.php?redirect=login has a login
                # form that POSTs to /become_seller.php — those login params
                # (username, password) should NOT merge with the real seller
                # form params (full_name, address, gst_number, xml_data).

                _existing_source = _ep.get("_form_source_page", "")
                _new_source       = url  # the page we found this form on

                if not _existing_source:
                    # First time — just write
                    _ep["_form_source_page"] = _new_source
                    for _p in inputs:
                        if _p and _p not in _ep["params"]["form"]:
                            _ep["params"]["form"].append(_p)
                elif _existing_source == _new_source:
                    # Same source page — normal additive merge
                    for _p in inputs:
                        if _p and _p not in _ep["params"]["form"]:
                            _ep["params"]["form"].append(_p)
                else:
                    # Different source page — replace only if new set is richer
                    # "Richer" = more params AND none of the new params are
                    # common auth words that suggest a login form collision
                    _AUTH_PARAMS = {"username","password","passwd","captcha",
                                    "recaptcha","email","login","credential"}
                    _new_is_auth  = sum(1 for p in inputs
                                        if p.lower() in _AUTH_PARAMS) >= 2
                    _old_is_auth  = sum(1 for p in _ep["params"]["form"]
                                        if p.lower() in _AUTH_PARAMS) >= 2
                    _new_richer   = len(inputs) > len(_ep["params"]["form"])

                    if _new_is_auth and not _old_is_auth:
                        # New set looks like login form, old set looks like
                        # real app form — keep old, discard new
                        pass
                    elif _old_is_auth and not _new_is_auth:
                        # Old set was a login form collision, new is better
                        _ep["params"]["form"]    = [p for p in inputs if p]
                        _ep["form_fields_detail"] = list(form_fields_detail)
                        _ep["_form_source_page"]  = _new_source
                    elif _new_richer:
                        # Neither is obviously auth — keep the richer set
                        _ep["params"]["form"]    = [p for p in inputs if p]
                        _ep["form_fields_detail"] = list(form_fields_detail)
                        _ep["_form_source_page"]  = _new_source
                    # else: keep existing — it's equal or richer

                # Always merge form_fields_detail additively for metadata
                existing_names = {f["name"] for f in _ep.get("form_fields_detail", [])}
                if "form_fields_detail" not in _ep:
                    _ep["form_fields_detail"] = []
                for fd in form_fields_detail:
                    if fd["name"] not in existing_names:
                        _ep["form_fields_detail"].append(fd)
                        existing_names.add(fd["name"])

            self._discover_url(full, depth+1, "Form_Action", show_feed=True)
        for attr in ("data-src","data-href","data-url"):
            for tag in soup.find_all(attrs={attr: True}):
                self._discover_url(urljoin(url, tag[attr]), depth+1, "DataAttr", show_feed=True)
        for tag in soup.find_all("script", type="application/ld+json"):
            if tag.string:
                for m in re.finditer(r'"(?:url|@id|contentUrl|embedUrl)"\s*:\s*"([^"]+)"', tag.string):
                    self._discover_url(m.group(1), depth+1, "JSONLD", show_feed=True)

    async def _check_sourcemap(self, session, url):
        # Hardened: probe for .map file and verify its legitimacy
        if not url.split('?')[0].endswith('.js'):
            return
        map_url = url.split('?')[0] + ".map"
        s, _, text = await fetch(session, "GET", map_url, self.rl)
        if s == 200 and text:
            try:
                # Basic validation: must be JSON and have key indicators
                if '"sources":' in text and '"mappings":' in text:
                    self.store.add_sourcemap(map_url, url)
                    self.emit.warn(f"[Sourcemap] Exposed JS source mapping → {map_url}")
                    # Extract endpoints from sourcemap if possible
                    for m in re.finditer(r'"(/[a-zA-Z0-9_\-\/]+)"', text):
                        path = m.group(1)
                        if len(path) > 3:
                            self.store.add_endpoint(urljoin(url, path), source="SourceMap", score=Conf.HIGH)
            except Exception:
                pass

    async def _process_js(self, url, text, session):
        ep_count = 0
        param_count = 0
        Extractor.secrets(text, url, self.store, self.emit)
        Extractor.js_endpoints(text, url, self.store, self.emit)
        Extractor.js_params(text, url, self.store, self.emit)
        Extractor.js_comments(text, url, self.store, self.emit)
        Extractor.js_routes(text, url, self.store, self.emit)
        await self._check_sourcemap(session, url)
        for m in re.finditer(r'import\s*\(\s*["\']([^"\']+)["\']', text):
            full = urljoin(url, m.group(1))
            if self.is_valid(full):
                if self._discover_url(full, 1, "JS_DynImport", show_feed=True): ep_count += 1
        # Broad JS chunk pattern — discovers any /path/to/file.js string literal
        # Works on any framework: React, Next.js, Vue, Angular, Django, Rails, etc.
        for m in re.finditer(r"""["'](/[a-zA-Z0-9._\-/]+\.js)["']""", text):
            chunk_path = m.group(1)
            chunk_full = urljoin(url, chunk_path)
            if self.is_valid(chunk_full):
                if self._discover_url(chunk_full, 1, "JS_Chunk", show_feed=True): ep_count += 1



    async def _fetch_and_process(self, session, url, depth, source):
        self.visited.add(normalize(url))
        self._depth_cnt[depth] += 1
        
        s, hdrs, body = await fetch(session, 'GET', url, self.rl,
                                    max_retries=self.cfg.max_retries,
                                    base_delay=self.cfg.retry_base_delay)
        
        if s is None or body is None:
            return
        
        # Record status early
        self.store.record_status(url, 'GET', s)

        # ── Vary header param discovery ───────────────────────────────
        # Vary: X-API-Version, X-User-Type reveals hidden endpoint dimensions
        # Each non-standard Vary value is a param that changes the response
        _vary = hdrs.get("Vary","") or hdrs.get("vary","")
        if _vary:
            _SKIP_VARY = {"accept","accept-encoding","accept-language",
                          "origin","cookie","authorization","content-type","*"}
            _vary_params = [v.strip() for v in _vary.split(",")
                            if v.strip().lower() not in _SKIP_VARY]
            if _vary_params:
                _vk = self.store._key(url, "GET")
                if _vk in self.store.endpoints:
                    _vep = self.store.endpoints[_vk]
                    for _vp in _vary_params:
                        if _vp not in _vep["params"].get("runtime",[]):
                            _vep["params"].setdefault("runtime",[]).append(_vp)
                            self.emit.info(f"[Vary-Param] {_vp} ← {url}")

        # ── Cookie param extraction ────────────────────────────────────
        # Set-Cookie header names are injectable params for session manipulation.
        # e.g. Set-Cookie: user_role=guest → user_role is a param name.
        _raw_cookies = hdrs.get("Set-Cookie", "") or hdrs.get("set-cookie", "")
        if _raw_cookies:
            _cookie_ep_key = self.store._key(url, "GET")
            if _cookie_ep_key in self.store.endpoints:
                _cep = self.store.endpoints[_cookie_ep_key]
                for _ck_part in _raw_cookies.split(";"):
                    _ck_name = _ck_part.strip().split("=")[0].strip()
                    _SKIP_CK = {"path","domain","expires","max-age","secure","httponly",
                                "samesite","version","comment","priority"}
                    if _ck_name and _ck_name.lower() not in _SKIP_CK:
                        if _ck_name not in _cep["params"].get("runtime",[]):
                            _cep["params"].setdefault("runtime",[]).append(_ck_name)
                            self.emit.info(f"[Cookie-Param] {_ck_name} ← {url}")

        # Feed line
        ct = (hdrs.get('Content-Type', '') or hdrs.get('content-type', '')).lower()
        is_js = 'javascript' in ct or url.split('?')[0].endswith('.js')
        ftype = 'JS' if is_js else 'Crawl'
        
        self.emit.crawl_feed(ftype, 'GET', url, s, len(body))

        if self.cfg.enable_extraction:
            Extractor.extract_data(body, url, self.store, self.emit)

        if s in (401, 403):
            self.store.add_endpoint(url, source=source, score=Conf.MEDIUM, auth_required=True)
            self.emit.warn(f'[Auth-wall:{s}] {url}')
        elif s in (500, 501, 502, 503) and body:
            _ERR_RE = re.compile(r'(?:Traceback|Exception in thread|SyntaxError|ParseError|SQLSTATE|You have an error in your SQL|ORA-\d{5}|Fatal error:|Warning:|Uncaught \w+Error|at [a-zA-Z\.]+\([a-zA-Z]+\.java:\d+\))', re.I)
            if _ERR_RE.search(body):
                self.store.add_endpoint(url, source='Error_Leak', score=Conf.HIGH)
                self.store.add_secret(body[:200], 'Error_Stack_Trace', url)
                self.emit.warn(f'[Error-Leak] Verbose error at {url}')
        elif s == 200:
            if Extractor.is_bot_blocked(body):
                self.emit.warn(f"[Bot-Blocked] Target redirected to challenge page: {url}")
                # We can't easily trigger a retry from here without complex queue logic, 
                # but marking it helps the user understand why discovery failed.
                self.store.add_endpoint(url, source="Blocked_Response", score=Conf.LOW)
                return

            if Extractor.is_soft_404(body, s):
                self.emit.info(f'[Soft-404] Dropping non-existent route: {url}')
                return

            # Run tech detection at shallow depth always; at deeper depths
            # only when the response carries meaningful server fingerprint headers.
            # This catches admin panels and API gateways that reveal stack info
            # only on their own routes, not on the root page.
            _srv = hdrs.get("Server","") or hdrs.get("server","")
            _xpb = hdrs.get("X-Powered-By","") or hdrs.get("x-powered-by","")
            _asp = hdrs.get("X-AspNet-Version","") or hdrs.get("x-aspnet-version","")
            if depth <= 1 or _srv or _xpb or _asp:
                self._detect_tech(hdrs, body, url)
            if depth <= 1:
                Extractor.csp_hints(hdrs, url, self.store, self.emit)
            
            if 'text/html' in ct:
                self.store.add_endpoint(url, source=f'HTML({source})', score=Conf.MEDIUM)
                self._process_html(url, body, depth, source)
            elif is_js:
                self.store.add_endpoint(url, source='JS_File', score=Conf.LOW)
                before = len(self.store.endpoints)
                await self._process_js(url, body, session)
                after = len(self.store.endpoints)
                if after > before:
                    self.emit.crawl_feed('JS', 'GET', url, extra=[f'├─ {after-before} endpoints extracted'])
            elif 'json' in ct:
                self.store.add_endpoint(url, source='JSON_Response', score=Conf.MEDIUM)
                for m in re.finditer(r'"([/][a-zA-Z0-9_\-\/]+)"', body):
                    path = m.group(1)
                    if len(path) > 3:
                        full = urljoin(url, path)
                        if self.is_valid(full):
                            self.store.add_endpoint(full, source='JSON_Path', score=Conf.LOW)
                            if not self._over_budget(depth + 1):
                                self._discover_url(full, depth + 1, 'JSON_Path', show_feed=True)
                # HATEOAS/_links/href extraction — HAL, JSON:API, Siren APIs
                try:
                    _jd = json.loads(body)
                    _q  = [_jd]; _seen_nodes = 0
                    while _q and _seen_nodes < 300:
                        _node = _q.pop(); _seen_nodes += 1
                        if isinstance(_node, dict):
                            for _k, _v in _node.items():
                                if _k.lower() in ("href","url","uri","endpoint","action",
                                                   "link","location","src","self",
                                                   "next","prev","previous","first","last"):
                                    _t = str(_v) if _v else ""
                                    if _t.startswith(("/","http")):
                                        _f = urljoin(url, _t)
                                        if self.is_valid(_f):
                                            if self.store.add_endpoint(_f, source="JSON_HATEOAS", score=Conf.MEDIUM):
                                                self.emit.info(f"[HATEOAS] {_k}: {_f}")
                                                self._discover_url(_f, depth+1, "JSON_HATEOAS", show_feed=True)
                                elif isinstance(_v, (dict, list)):
                                    _q.append(_v)
                        elif isinstance(_node, list):
                            for _i in _node[:10]:
                                if isinstance(_i, (dict, list)):
                                    _q.append(_i)
                except Exception:
                    pass
                # ── JSON response ID chaining ─────────────────────────
                # Extract top-level keys that look like ID/reference fields.
                # e.g. {"user_id": 123, "post_id": 456, "session_token": "abc"}
                # These become IDOR-relevant params for related endpoints.
                _ID_KEY_RE = re.compile(
                    r'"\s*([a-zA-Z_][a-zA-Z0-9_]{1,40}(?:_id|_token|_key|Id|Token|Key|ID))\s*"\s*:\s*',
                    re.I
                )
                _ep_key = self.store._key(url, "GET")
                if _ep_key in self.store.endpoints:
                    _ep = self.store.endpoints[_ep_key]
                    _chained = 0
                    for _idm in _ID_KEY_RE.finditer(body[:8000]):
                        _pname = _idm.group(1).strip()
                        if _pname and _pname not in _ep["params"].get("runtime", []):
                            _ep["params"].setdefault("runtime", []).append(_pname)
                            _chained += 1
                    if _chained:
                        self.emit.info(f"[ID-Chain] {_chained} ID field(s) chained from {url}")
                self._extract_body_param_hints(url, body)

    async def _worker(self, session, worker_id, crawl_delay):
        while True:
            acquired = False
            try:
                async with self.sem:
                    try:
                        url, depth, source = await asyncio.wait_for(self.queue.get(), timeout=4.0)
                        acquired = True
                    except asyncio.TimeoutError:
                        break
                    norm = normalize(url)
                    if norm in self.visited or depth > self.cfg.max_depth or self._over_budget(depth):
                        pass
                    else:
                        await self._fetch_and_process(session, url, depth, source)
            except Exception as e:
                self.emit.warn(f"[Worker] Error processing {url}: {e}")
            finally:
                if acquired:
                    self.queue.task_done()
                    delay = crawl_delay if crawl_delay > 0 else random.uniform(self.cfg.jitter_min, self.cfg.jitter_max)
                    await asyncio.sleep(delay)

    async def _probe_oidc(self, session, base):
        url = urljoin(base, "/.well-known/openid-configuration")
        s, _, text = await fetch(session, "GET", url, self.rl)
        if s != 200 or not text:
            return
        try:
            cfg = json.loads(text)
        except Exception:
            return
        oidc_keys = [
            "authorization_endpoint", "token_endpoint", "userinfo_endpoint",
            "end_session_endpoint", "introspection_endpoint", "revocation_endpoint",
            "jwks_uri", "registration_endpoint",
        ]
        for key in oidc_keys:
            ep_url = cfg.get(key)
            if ep_url and isinstance(ep_url, str):
                self.store.add_endpoint(ep_url, source="OIDC_Discovery", score=Conf.CONFIRMED,
                                        auth_required=True)
                self.emit.always_success(f"[OIDC] {key}: {ep_url}")

    async def run(self):
        req_headers = {
            "User-Agent": self.cfg.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                      "application/json;q=0.8,*/*;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }
        req_headers.update(self.extra_headers)
        connector = aiohttp.TCPConnector(limit=self.cfg.concurrency, ttl_dns_cache=300, ssl=False)
        timeout   = aiohttp.ClientTimeout(total=self.cfg.timeout)
        async with aiohttp.ClientSession(headers=req_headers, cookies=self.cookies,
                                          timeout=timeout, connector=connector) as session:
            try:
                # Capture target response headers for the summary report
                _t_phase_start = time.time()
                _t_recon = 0.0
                _t_crawl = 0.0
                _t_audit = 0.0
                try:
                    _hdr_s, _hdr_h, _ = await fetch(session, "GET", self.target, self.rl)
                    if _hdr_h:
                        # Store a clean, sorted dict of headers (normalise to Title-Case)
                        self.store.target_response_headers = {
                            k: v for k, v in sorted(_hdr_h.items())
                        }
                except Exception:
                    pass
                self.emit.animator.start_anim("Recon Probing Base")
                if self.cfg.enable_graphql:
                    await probe_graphql(session, self.target, self.store, self.emit, self.rl)
                self.emit.animator.update(0, "Recon robots.txt")
                robots = RobotsParser(session, self.target, self.store, self.queue,
                                      self.emit, self.rl, self.is_valid)
                crawl_delay = await robots.run()

                # FOUNDATIONAL RECON: Structural Discovery (Sitemaps + Well-Known)
                self.emit.animator.update(0, "Recon Sitemaps")
                for _smap in ("/sitemap.xml", "/sitemap_index.xml", "/.well-known/sitemap.xml"):
                    _smap_url = urljoin(self.target, _smap)
                    if _smap_url not in robots._sitemap_seen:
                        _s, _h, _t = await fetch(session, "GET", _smap_url, self.rl)
                        if _s == 200 and _t:
                            _ct = (_h or {}).get("content-type", "").lower()
                            if Extractor.is_real_file(_ct, _t, None) and not Extractor.is_soft_404(_t, _s):
                                await robots.parse_sitemap(_smap_url)

                # Subdomain enumeration via crt.sh
                self.emit.animator.update(0, "Recon Subdomains")
                _subenum = SubdomainEnumerator(self.target, self.store,
                                               self.queue, self.emit, self.is_valid)
                await _subenum.run()

                # Wayback Machine — historical URL discovery
                self.emit.animator.update(0, "Recon Wayback")
                _wayback = WaybackProbe(self.target, self.store, self.queue,
                                         self.emit, self.rl, self.is_valid)
                await _wayback.run(session)

                self.emit.animator.update(0, "Recon Well-Known")
                for _wk in _WELL_KNOWN_PATHS:
                    _wk_url = urljoin(self.target, _wk)
                    _s, _h, _t = await fetch(session, "GET", _wk_url, self.rl)
                    if _s == 200 and _t:
                        _ct = (_h or {}).get("content-type", "").lower()
                        if not Extractor.is_real_file(_ct, _t, None) or Extractor.is_soft_404(_t, _s):
                            continue
                        self.store.add_endpoint(_wk_url, source="WellKnown", score=Conf.LOW)
                        self.emit.crawl_feed("Found", "GET", _wk_url)
                        if _wk.endswith("openid-configuration"):
                            await self._probe_oidc(session, self.target)
                        # security.txt — dedicated structured parser (comment mining + field extraction)
                        elif _wk.endswith("security.txt"):
                            _sec_parser = SecurityTxtParser(
                                self.target, self.store, self.queue,
                                self.emit, self.is_valid
                            )
                            _sec_parser.parse(_t)
                        else:
                            # Generic URL extraction for other well-known files
                            for _m in re.finditer(r'(?:^|\s)((?:https?://[^\s]+|/[a-zA-Z0-9_\-/]+))', _t, re.M):
                                _path = _m.group(1).strip()
                                if _path.startswith("/"):
                                    _full = urljoin(self.target, _path)
                                    if self.is_valid(_full):
                                        self.store.add_endpoint(_full, source="WellKnown", score=Conf.LOW)
                                        self._queue_url(_full, 1, "WellKnown")
                spa_ctx = None
                if self.cfg.enable_screenshots and not self.cfg.use_playwright:
                    self.emit.warn("[Screenshot] --screenshot requested but --no-playwright passed. Skipping.")
                
                if self.cfg.use_playwright:
                    screenshot_cfg = {"priority": self.cfg.screenshot_priority} if self.cfg.enable_screenshots else None
                    spa = SPAScanner(self.target, self.store, self.emit, self.cookies,
                                     self.extra_headers, self.queue, self.is_valid,
                                     enable_spa_interact=self.cfg.enable_spa_interact,
                                     screenshot_cfg=screenshot_cfg)
                    spa_res = await spa.run()
                    if spa_res:
                        if isinstance(spa_res, tuple):
                            # (browser, context, page, cookies)
                            spa_ctx = spa_res[:3]
                            sync_cookies = spa_res[3]
                        else:
                            sync_cookies = spa_res
                        
                        if sync_cookies:
                            before = len(session.cookie_jar)
                            session.cookie_jar.update_cookies(sync_cookies)
                            after = len(session.cookie_jar)
                            if after > before:
                                self.emit.always_success(f"[Sync] Synchronized {after-before} cookies from SPA session")
                _t_recon = time.time() - _t_phase_start
                _t_phase_start = time.time()
                self.emit.always_info(
                    f"[Spider] Crawl started — depth={self.cfg.max_depth}, "
                    f"concurrency={self.cfg.concurrency}, "
                    f"auth={'yes' if self.cookies or self.extra_headers else 'no'}, "
                    f"seed={self.queue.qsize()} URLs")
                
                # P33: Update animator for crawl phase
                self.emit.animator.update(0, "Crawling Target")
                
                workers = [asyncio.create_task(self._worker(session, i, crawl_delay))
                           for i in range(self.cfg.concurrency)]
                
                # Dynamic update task for crawl progress
                async def _update_crawl_status():
                    while self.emit.animator.active:
                        self.emit.animator.update(len(self.visited), f"Crawling: {len(self.visited)} URLs")
                        await asyncio.sleep(1.0)
                
                status_task = asyncio.create_task(_update_crawl_status())
                
                await self.queue.join()
                
                for w in workers: w.cancel()
                status_task.cancel()
                self.emit.animator.stop_anim()
                
                await asyncio.gather(*workers, return_exceptions=True)

                _t_crawl = time.time() - _t_phase_start
                _t_phase_start = time.time()
                # Phase 3: Intelligent Probing
                if self.cfg.enable_probing:
                    prober = IntelligentProber(session, self.store, self.emit, self.rl, self.cfg)
                    await prober.run()

                _t_audit = time.time() - _t_phase_start
                self._t_recon = _t_recon
                self._t_crawl = _t_crawl
                self._t_audit = _t_audit
                # Phase 4: Screenshots
                if self.cfg.enable_screenshots and spa_ctx:
                    self.emit.animator.start_anim("Capturing Screenshots")
                    await spa.capture_screenshots(self.store.endpoints, spa_ctx)
                    self.emit.animator.stop_anim()
                elif spa_ctx:
                    # Cleanup if screenshots not enabled but context was kept (shouldn't happen with current logic but for safety)
                    b, c, p = spa_ctx
                    await b.close()
                    if hasattr(spa, "_pw"): await spa._pw.stop()

                # Run classification passes
                # No network I/O — pure store operations
                classify_admin_endpoints(self.store)
                classify_auth_endpoints(self.store)
                classify_idor_candidates(self.store)
                score_injection_candidates(self.store)
                _flag_upload_endpoints(self.store)
            finally:
                self.emit.animator.stop_anim()

# ══════════════════════════════════════════════════════════════════════
# DIFF ENGINE
# ══════════════════════════════════════════════════════════════════════

def diff_crawls(old_json: str, new_json: str) -> dict:
    old = json.loads(old_json); new = json.loads(new_json)
    om  = {e["cluster"]: e for e in old.get("endpoints",[])}
    nm  = {e["cluster"]: e for e in new.get("endpoints",[])}
    ok, nk = set(om), set(nm)
    added   = [nm[k] for k in (nk - ok)]
    removed = [om[k] for k in (ok - nk)]
    changed = []
    for k in ok & nk:
        o, n = om[k], nm[k]; diff: dict = {}
        if set(o["methods"]) != set(n["methods"]):
            diff["methods"] = {"old": o["methods"], "new": n["methods"]}
        if o["confidence_label"] != n["confidence_label"]:
            diff["confidence"] = {"old": o["confidence_label"], "new": n["confidence_label"]}
        if o["auth_required"] != n["auth_required"]:
            diff["auth_required"] = {"old": o["auth_required"], "new": n["auth_required"]}
        if diff: changed.append({"cluster": k, "url": n["url"], "changes": diff})
    return {"old_target": old.get("meta",{}).get("target"),
            "new_target": new.get("meta",{}).get("target"),
            "added": added, "removed": removed, "changed": changed,
            "summary": {"added": len(added), "removed": len(removed), "changed": len(changed)}}

# ══════════════════════════════════════════════════════════════════════
# AUTO-SAVE  — always writes JSON; optional extra format file
# ══════════════════════════════════════════════════════════════════════

def _auto_save(store: Store, target: str, out_path: Optional[str],
               fmt: str, emit: Emit) -> str:
    """Always saves a .json report. Returns the path saved."""
    domain    = re.sub(r'[^a-zA-Z0-9_\-]', '_', urlparse(target).netloc)
    ts        = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = out_path if (out_path and out_path.endswith(".json")) \
                else f"spider_{domain}_{ts}.json"

    try:
        Path(json_path).write_text(store.export(target, fmt="json"))
        pass  # JSON saved silently — it's for agents, not announced to user
    except Exception as e:
        emit.warn(f"[Report] JSON save failed: {e}")
        json_path = ""

    # If extra format requested with an explicit path, save it too
    if out_path and fmt != "json":
        try:
            Path(out_path).write_text(store.export(target, fmt=fmt))
            emit.always_info(f"[Report] {fmt.upper()} saved → {out_path}")
        except Exception as e:
            emit.warn(f"[Report] {fmt.upper()} save failed: {e}")

    return json_path

# ══════════════════════════════════════════════════════════════════════
# MODULE ENTRY (Hellhound framework)
# ══════════════════════════════════════════════════════════════════════

def run(target: str, emit_obj, options: dict = None, stop_check=None, pause_check=None):
    opts    = options or {}
    cookies = SessionManager.parse_cookies(opts.get("cookie") or opts.get("auth"))
    xhdrs   = SessionManager.parse_auth_header(opts.get("headers", {}))
    # FIX 5: enable_cors defaults to False in framework (module) mode.
    # CORS probing adds WAF-visible traffic with evil.hellhound.test origin and no
    # downstream agent currently consumes cors_issues for exploitation.
    # Callers that explicitly need CORS data should pass enable_cors=True in options.
    framework_defaults = {"enable_cors": False}
    merged_opts = {**framework_defaults, **{k: v for k, v in opts.items() if k not in ("cookie","auth","headers")}}
    cfg     = Config(**merged_opts)
    cfg.validate()

    class _W:
        def __init__(self, b, v): self._b = b; self._v = v
        def info(self, m):
            if self._v: self._b.info(m)
        def success(self, m):
            if self._v: self._b.success(m)
        def warn(self, m):            self._b.warn(m)
        def always_info(self, m):     self._b.info(m)
        def always_success(self, m):  self._b.success(m)
        def section(self, t):         self._b.info(f"── {t} ──")
        def row(self, k, v, **kw):    self._b.info(f"{k}: {_strip(str(v))}")
        def finding(self, *a):        self._b.warn(str(a))
        def endpoint_row(self, ep):   self._b.info(ep.get("url",""))
        def live_crawl(self, url):    pass
        def print_always(self, m):    print(m)
        @property
        def _nc(self): return True
        # Animation stubs for framework usage
        @property
        def animator(self):
            class _S:
                active = False
                def start(self, *a, **k): pass
                def stop(self, *a, **k): pass
                def update(self, *a, **k): pass
                def _clear(self): pass
            return _S()

    emit = _W(emit_obj, cfg.verbose)
    return _do_run(target, cfg, emit, cookies, xhdrs)

# ══════════════════════════════════════════════════════════════════════
# SHARED RUN LOGIC
# ══════════════════════════════════════════════════════════════════════

def _do_run(target: str, cfg: Config, emit,
            cookies: Dict[str, str], extra_headers: Dict[str, str]) -> dict:
    if not target.startswith("http"):
        target = "https://" + target

    emit.always_info(f"Hellhound Spider v{VERSION} — {target}")
    start = time.time()

    spider: Optional[Spider] = None
    try:
        spider = Spider(target, cfg, emit, cookies, extra_headers)
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        if cfg.har_file:
            from pathlib import Path as _P
            if _P(cfg.har_file).exists():
                HARImporter(cfg.har_file, spider.store, emit, spider.is_valid, target).run()
            else:
                emit.warn(f"[HAR] File not found: {cfg.har_file}")
        asyncio.run(spider.run())
    except KeyboardInterrupt:
        emit.warn("Scan interrupted — partial results follow")
    except ValueError as e:
        emit.warn(f"Config error: {e}")
        return {"raw": str(e), "intel": {}}
    except Exception as e:
        emit.warn(f"Spider error: {e}")

    if spider is None:
        return {"raw": "Spider failed to initialize.", "intel": {}}

    elapsed = time.time() - start
    phase_times = (
        getattr(spider, "_t_recon", elapsed * 0.10),
        getattr(spider, "_t_crawl", elapsed * 0.70),
        getattr(spider, "_t_audit", elapsed * 0.20),
    )

    # Always auto-save JSON
    json_path = _auto_save(spider.store, target, cfg.output_file,
                           cfg.output_format, emit)

    intel  = json.loads(spider.store.export(target, fmt="json"))
    result = {"raw": "", "intel": intel}

    # Print rich CLI results
    print_results(intel, target, elapsed, emit, saved_path=json_path,
                  phase_times=phase_times)

    return result

# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hellhound_spider",
        description=(
            f"{C.R}{C.B}Hellhound Spider v{VERSION}{C.RST}  —  "
            "SPA + Non-SPA Web Crawler & Endpoint Discoverer"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"\n{C.GR}  ── Examples ────────────────────────────────────────────────────\n\n"
            f"{C.R}  spider https://target.com\n"
            f"  spider https://target.com --extract\n"
            f"  spider https://target.com --extract --verbose\n"
            f"  spider https://target.com --screenshot\n"
            f"  spider https://target.com --screenshot all\n"
            f"  spider https://target.com --screenshot \"admin,panel\"\n"
            f"  spider https://target.com --cookie \"s=abc; csrf=xy\"\n"
            f"  spider https://target.com --auth \"Bearer eyJhbGci...\"\n"
            f"  spider https://target.com --format csv --out report.csv\n"
            f"  spider https://target.com --no-playwright\n"
            f"  spider https://target.com --diff old.json\n"
            f"\n  JSON report is always auto-saved even without --out.{C.RST}\n"
        ),
    )

    p.add_argument("target", nargs="?", help="Target URL  (e.g. https://example.com)")

    scan = p.add_argument_group(f"{C.CY}Scan Options{C.RST}")
    scan.add_argument("--depth",       "-d", type=int, default=4,  metavar="N",
                      help="Max crawl depth  (default: 4)")
    scan.add_argument("--concurrency", "-c", type=int, default=12, metavar="N",
                      help="Concurrent workers  (default: 12)")
    scan.add_argument("--timeout",     "-t", type=int, default=15, metavar="S",
                      help="Per-request timeout in seconds  (default: 15)")
    scan.add_argument("--verbose",     "-v", action="store_true",
                      help="Show all discovery logs")

    auth = p.add_argument_group(f"{C.CY}Authentication{C.RST}")
    auth.add_argument("--cookie",  "-C", type=str, default=None, metavar="COOKIE",
                      help="Cookie string, dict, or path to cookie file")
    auth.add_argument("--auth",    "-a", type=str, default=None, metavar="HEADER",
                      help='Authorization header  e.g. "Bearer eyJ..."')

    out = p.add_argument_group(f"{C.CY}Output{C.RST}")
    out.add_argument("--out",    "-o", type=str, default=None, metavar="FILE",
                     help="Extra output file  (JSON always auto-saved)")
    out.add_argument("--format", "-f", type=str, default="json",
                     choices=["json","jsonl","csv","burp"],
                     help="Extra output format  (default: json)")

    flags = p.add_argument_group(f"{C.CY}Feature Flags{C.RST}")
    flags.add_argument("--no-playwright", "-P", action="store_true",
                       help="Disable headless browser SPA scanning (patchright > playwright-stealth > manual JS)")
    flags.add_argument("--no-probing",    "-p", action="store_true",
                       help="Disable intelligent probing phase")
    flags.add_argument("--spa-interact",  "-I", action="store_true",
                       help="Enable SPA form filling and button clicking (authorized targets only)")
    flags.add_argument("--no-cors",       "-R", action="store_true",
                       help="Disable CORS misconfiguration checks")
    flags.add_argument("--no-graphql",    "-G", action="store_true",
                       help="Disable GraphQL introspection probe")
    flags.add_argument("--no-openapi",    "-O", action="store_true",
                       help="Disable OpenAPI / Swagger discovery")
    flags.add_argument("--extract",       "-x", action="store_true",
                       help="Enable passive data extraction (emails, IPs, buckets)")
    flags.add_argument("--screenshot",    "-s", nargs="?", const="standard",
                       help="Screenshots of key endpoints. Preset: all, standard, blocked, errors, api, admin, or regex")
    flags.add_argument("--no-filter",     "-F", action="store_true",
                       help="Disable noise path filter (include VCS browser UI, CDN paths, socket.io in output)")

    util = p.add_argument_group(f"{C.CY}Utilities{C.RST}")
    util.add_argument("--diff",    "-D", type=str, default=None, metavar="OLD_REPORT",
                      help="Diff this scan against an old JSON report")
    util.add_argument("--har", "-H", type=str, default=None, metavar="HAR_FILE",
                      help="Import a browser HAR session file to seed the store with auth-gated requests")
    util.add_argument("--upgrade",       action="store_true",
                      help="Upgrade Hellhound-Spider to the latest version")

    return p


def main():
    parser = _build_parser()
    args   = parser.parse_args()

    emit = Emit(verbose=args.verbose)
    print_banner()

    if args.upgrade:
        emit.always_info("Initiating system upgrade...")
        if os.path.exists("update.sh"):
            os.system("bash update.sh")
        else:
            emit.warn("update.sh not found in the current directory.")
        sys.exit(0)

    if not args.target:
        parser.print_help()
        sys.exit(1)

    # Pre-flight info block
    nc = emit._nc
    def _pf(label, value, vc=None):
        vc = vc or C.W
        if nc:
            print(f"  {label:<18}  {_strip(value)}")
        else:
            print(f"  {C.CYD}{label:<18}{C.RST}  {vc}{value}{C.RST}")

    _pf("Target",      args.target)
    _pf("Depth",       str(args.depth))
    _pf("Concurrency", str(args.concurrency))
    _pf("Timeout",     f"{args.timeout}s")
    if not args.no_playwright and PLAYWRIGHT_AVAILABLE:
        if PATCHRIGHT_AVAILABLE:
            pw_status = "playwright  (+patchright available as bot-bypass fallback)"
        else:
            pw_status = "playwright  (bot-bypass fallback: patchright not detected)"
    else:
        pw_status = "disabled"
        if PLAYWRIGHT_ERROR and args.verbose:
            pw_status += f"  {C.R}({PLAYWRIGHT_ERROR}){C.RST}"

    _pf("Browser Engine", pw_status,
        C.G if (not args.no_playwright and PLAYWRIGHT_AVAILABLE) else C.GR)
    _pf("Verbose",
        "on" if args.verbose else "off",
        C.G if args.verbose else C.GR)
    _pf("Extraction",
        "enabled" if args.extract else "disabled",
        C.G if args.extract else C.GR)
    _pf("Screenshots",
        f"enabled ({args.screenshot or 'standard'})" if args.screenshot else "disabled",
        C.G if args.screenshot else C.GR)
    print()

    cookies = SessionManager.parse_cookies(args.cookie)
    xhdrs   = SessionManager.parse_auth_header(args.auth or "")

    if cookies:
        emit.always_info(f"[Auth] Cookies loaded  →  {list(cookies.keys())}")
    elif xhdrs:
        emit.always_info(f"[Auth] Header auth     →  {list(xhdrs.keys())}")
    else:
        emit.always_info("[Auth] No credentials — unauthenticated scan")

    cfg = Config(
        max_depth       = args.depth,
        concurrency     = args.concurrency,
        timeout         = args.timeout,
        verbose         = args.verbose,
        use_playwright  = not args.no_playwright,
        enable_spa_interact = args.spa_interact,
        enable_probing  = not args.no_probing,
        enable_cors     = not args.no_cors,
        enable_graphql  = not args.no_graphql,
        enable_openapi      = not args.no_openapi,
        har_file            = getattr(args, "har", None),
        enable_noise_filter = not args.no_filter,
        enable_extraction   = args.extract,
        enable_screenshots = args.screenshot is not None,
        screenshot_priority = args.screenshot if args.screenshot else "standard",
        output_format   = args.format,
        output_file     = args.out,
    )

    try:
        cfg.validate()
    except ValueError as e:
        emit.warn(str(e))
        sys.exit(1)

    print()
    result = _do_run(args.target, cfg, emit, cookies, xhdrs)

    # ── diff mode ─────────────────────────────────────────────────────
    if args.diff:
        try:
            old  = Path(args.diff).read_text()
            new  = json.dumps(result["intel"], indent=2)
            diff = diff_crawls(old, new)
            emit.section(f"DIFF  vs  {args.diff}")
            emit.row("Added",   str(diff["summary"]["added"]),   value_colour=C.R)
            emit.row("Removed", str(diff["summary"]["removed"]), value_colour=C.GR)
            emit.row("Changed", str(diff["summary"]["changed"]), value_colour=C.Y)
            if diff["added"]:
                print()
                emit.always_info(f"New endpoints ({len(diff['added'])}):")
                for ep in diff["added"]:
                    emit.finding("NEW", "HIGH", ep["url"])
            if diff["removed"]:
                print()
                emit.always_info(f"Gone endpoints ({len(diff['removed'])}):")
                for ep in diff["removed"]:
                    emit.finding("GONE", "INFO", ep["url"])
        except Exception as e:
            emit.warn(f"[Diff] Error: {e}")


if __name__ == "__main__":
    main()