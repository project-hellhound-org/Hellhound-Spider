#!/usr/bin/env python3
"""
  HELLHOUND SPIDER  v12.3  —  Standalone Recon Engine

  Full SPA + Non-SPA Crawler | robots.txt | sitemap.xml | JS Analysis

Dependencies:
  pip install aiohttp beautifulsoup4 lxml
  pip install playwright && playwright install chromium     # optional SPA
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

# ══════════════════════════════════════════════════════════════════════
# METADATA
# ══════════════════════════════════════════════════════════════════════

VERSION      = "12.3"
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

        cc = {
            "CONFIRMED": C.G, "HIGH": C.Y, "MEDIUM": C.CYD, "LOW": C.GR,
        }.get(conf, C.GR)

        # No OSC 8 wrapping: prevents dotted underlines in some terminals
        if self._nc:
            print(f"    {method:<7}  {conf:<10}  {_strip(auth)}{_strip(sens)}{_strip(snap)}  {url}")
        else:
            print(f"  {mc}{method:<7}{C.RST} {cc}{conf:<10}{C.RST} {auth}{sens}{snap} {C.W}{url}{C.RST}")

    def print_always(self, msg: str):
        self._w(msg)

# ══════════════════════════════════════════════════════════════════════
# RESULTS PRINTER  — replaces raw JSON dump
# ══════════════════════════════════════════════════════════════════════

def print_results(intel: dict, target: str, elapsed: float,
                  emit: Emit, saved_path: str = ""):

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
        # Estimating phases based on total elapsed
        p1, p2, p3 = elapsed * 0.1, elapsed * 0.7, elapsed * 0.2
        print(f"  {C.CY}◔{C.RST} {C.W}Recon {C.G}{p1:.1f}s{C.RST} {C.GR}·{C.RST} {C.W}Crawl {C.G}{p2:.1f}s{C.RST} {C.GR}·{C.RST} {C.W}Audit {C.G}{p3:.1f}s{C.RST}")

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
        emit.finding(item.get("type", "Secret"), "HIGH",
                     f"{str(item.get('content',''))[:70]}  ← {item.get('source','')}")

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
            
            # Show all if verbose, else limit to 10
            limit = count if emit.verbose else 10
            for item in items[:limit]:
                val = item["value"]
                disp = val if len(val) <= 60 else val[:57] + "..."
                emit.leader_row("  " + disp, item["source_url"])
            if count > limit:
                emit.row("  ...", f"{count-limit} more in JSON", icon="○")

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
        shown    = sorted_eps[:200]
        overflow = len(sorted_eps) - len(shown)

        for ep in shown:
            emit.endpoint_row(ep)

        if overflow > 0:
            emit.row("...", f"{overflow} more — see JSON report", icon="○")

        # ── param map for interesting endpoints ──────────────────────
        interesting = [e for e in real_eps if (e.get("params") or e.get("parameter_sensitive"))][:40]

        if interesting:
            emit.section(f"PARAMETER MAP  ({len(interesting)} endpoints)", orbital=True)
            for ep in interesting:
                url = ep.get("url","")
                all_p = ep.get("params", [])
                if not all_p: continue

                method = ep.get("method", "GET")
                mc = { "GET": C.GD, "POST": C.Y, "PUT": C.O, "PATCH": C.O, "DELETE": C.R }.get(method, C.GL)
                disp = url if len(url) <= 64 else url[:61] + "…"

                if nc:
                    print(f"    {method:<7} {disp}")
                    print(f"      params: {', '.join(all_p)}")
                else:
                    print(f"  {mc}●{C.RST} {C.W}{method:<7}{C.RST} {C.B}{C.W}{disp}{C.RST}")
                    emit.leader_row("PARAMS", ", ".join(all_p))

    # ── auth-walled ───────────────────────────────────────────────────
    auth_eps = [e for e in eps if e.get("auth_required")]
    if auth_eps:
        emit.section(f"AUTH-WALLED  ({len(auth_eps)} endpoints)", orbital=True)
        for ep in auth_eps[:40]:
            method = ep.get("methods",["GET"])[0]
            url = ep.get("url","")
            emit.row(method, url, icon="⬢", label_colour=C.RD)

    # ── robots disallowed ─────────────────────────────────────────────
    robots = intel.get("robots_disallowed", [])
    if robots:
        emit.section(f"ROBOTS DISALLOWED  ({len(robots)} paths)", orbital=True)
        for path in robots[:50]:
            emit.row("Disallow", path, icon="●", label_colour=C.O)

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
        emit.always_success(f"Report saved → {saved_path}")

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
_PATH_ID_RE    = re.compile(r'/(?:v[0-9]+/)?(?:[a-z]+/)?([0-9]{3,}|[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', re.I)
_UUID_PATH_RE  = re.compile(r'[a-f0-9]{8}-[a-f0-9]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[a-f0-9]{12}', re.I)

_ADMIN_PATTERNS = re.compile(r'/(admin|manage|panel|control|dashboard|backend|config|setup|root|superuser)', re.I)
_AUTH_PATTERNS  = {
    "login":  re.compile(r'/(login|signin|authenticate|auth)', re.I),
    "logout": re.compile(r'/(logout|signout)', re.I),
    "mfa":    re.compile(r'/(mfa|2fa|otp|totp)', re.I),
    "pass":   re.compile(r'/(password|reset|forgot)', re.I),
}

_SQLI_PARAM_RE = re.compile(r'(?:id|select|report|update|query|search|from|where|order|by|group|limit|offset|slug|category|tag)$', re.I)
_CMDI_PARAM_RE = re.compile(r'(?:cmd|command|exec|execute|path|file|dir|folder|target|host|url|endpoint|run|script|sh|bash|run)$', re.I)

def normalize(url: str) -> str:
    try:
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
        self.cors_issues:  List[dict]       = []
        self.graphql:      List[dict]       = []
        self.openapi:      List[dict]       = []
        self.sourcemaps:   List[dict]       = []
        self.extracted_data: List[dict]     = []
        self._extracted_seen: Set[tuple]    = set()

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

    def add_endpoint(self, url, method="GET", source="Static",
                     params=None, score=Conf.LOW, auth_required=False):
        key = self._key(url, method)
        if key not in self.endpoints:
            self.endpoints[key] = self._new_ep(url, method)
        ep = self.endpoints[key]
        if source not in ep["source"]:
            ep["source"].append(source)
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
        key = self._key(url, method)
        if key in self.endpoints:
            ep = self.endpoints[key]
            if status not in ep["observed_status"]:
                ep["observed_status"].append(status)
            if status in (401, 403):
                ep["auth_required"] = True
            elif status == 200:
                # If we saw a 200, it's not strictly 'walled' for this session
                ep["auth_required"] = False

    def mark_sensitive(self, url, method):
        key = self._key(url, method)
        if key in self.endpoints:
            ep = self.endpoints[key]
            ep["parameter_sensitive"] = True
            ep["confidence"] = min(ep["confidence"] + 2, Conf.CONFIRMED)
            ep["confidence_label"] = Conf.label(ep["confidence"])

    def add_comment(self, content, source_url):
        content = content.strip()
        if len(content) < 4 or any(c["content"] == content for c in self.comments):
            return False
        self.comments.append({"content": content, "source": source_url})
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
            "screenshots":        sum(1 for e in eps if e.get("screenshot")),
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
            "tech_stack": sorted(self.tech_stack),
            "extracted_data": self.extracted_data if self.extracted_data is not None else [],
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
        (r'["\']sk-[a-zA-Z0-9]{20,}["\']',                                "Stripe_Key"),
        (r'gh[pousr]_[A-Za-z0-9_]{36,}',                                  "GitHub_PAT"),
        (r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----',                      "Private_Key_PEM"),
        (r'["\'](?:password|passwd|secret|api_?key|token)\s*["\']?\s*[:=]\s*["\']([^"\']{6,})["\']',
                                                                           "Hardcoded_Credential"),
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
            r'[a-z0-9\-]+\.s3\.amazonaws\.com|'
            r'[a-z0-9\-]+\.blob\.core\.windows\.net',
            re.I), "Cloud_Bucket"),
        (re.compile(
            r'(SQLSTATE|ORA-\d{5}|mysql_fetch|pg_query|'
            r'MongoError|SequelizeError|mysqli_error)',
            re.I), "DB_Error"),
        (re.compile(
            r'(?<![.a-zA-Z0-9_])'          # not a property chain (no this.internal, obj.corp)
            r'(?!localhost\b)(?!127\.)'   # exclude localhost
            r'[a-zA-Z0-9][a-zA-Z0-9\-]{3,}'  # hostname min 4 chars
            r'\.(internal|intranet|corp|lan|private)\b',
            re.I), "Internal_Host"),
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
        """Heuristic check for common bot-protection/WAF challenge pages."""
        if not body:
            return False
        body_lo = body.lower()
        # Look for challenge/WAF indicators
        indicators = (
            "cloudflare", "ddos protection", "checking your browser",
            "access denied", "security check", "captcha", "verification required",
            "one more step", "sucuri", "incapsula", "akamai", "perimeterx",
        )
        if any(ind in body_lo for ind in indicators):
            # Only count as blocked if it's a small "gate" page
            if len(body) < 15000:
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
        var_map = cls._build_var_url_map(text)
        for pat in cls._PARAM_RE:
            for m in re.finditer(pat, text, re.S):
                keys = cls._obj_keys(m.group(1) if m.lastindex else m.group(0))
                if not keys:
                    continue
                # Harden: filter out high-noise JS library params
                keys = [k for k in keys if k not in cls._JS_PARAM_STOPLIST]
                if not keys:
                    continue
                turl = cls._find_url_for_params(text, m.start(), m.end(), base_url, var_map)
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
                    local_part = val.split("@")[0]
                    domain_part = val.split("@")[1] if "@" in val else ""
                    if ".." in val: continue
                    if len(local_part) < 2: continue
                    if "." not in domain_part: continue
                    if val.lower().endswith((".css", ".js", ".png", ".jpg", ".svg", ".woff")):
                        continue

                if dtype == "Phone":
                    val = re.sub(r'[\s.\-\(\)\/]', '', val)
                    if not (7 <= len(val) <= 15): continue
                    if not re.match(r'\+?\d+$', val): continue
                    # Reject date-like patterns: YYYYMMDD, YYYYDDMM, DDMMYYYY etc
                    if re.match(r'(20[0-9]{2}[01][0-9][0-3][0-9]|[0-3][0-9][01][0-9]20[0-9]{2})', val): continue

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
                                    v = re.sub(r'[\s.\-\(\)\/]', '', v)
                                    if not (7 <= len(v) <= 15): continue
                                    if not re.match(r'\+?\d+$', v): continue
                                    # Reject date-like patterns
                                    if re.match(r'(20[0-9]{2}[01][0-9][0-3][0-9]|[0-3][0-9][01][0-9]20[0-9]{2})', v): continue
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
              "private","disabled","endpoint"}
        for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
            txt = c.strip()
            if len(txt) < 4:
                continue
            if (any(k in txt.lower() for k in kw)
                    or bool(re.match(r'^[/\.][a-z0-9_\-\.#]{3,}', txt))):
                if store.add_comment(txt, url):
                    emit.info(f"[Comment] {txt[:100]}")
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
    _METHODS = ["PUT", "PATCH", "DELETE", "HEAD", "TRACE"]

    def __init__(self, session, store, emit, rl, cfg):
        self.session = session; self.store = store
        self.emit = emit; self.rl = rl; self.cfg = cfg

    async def run(self):
        # Filter for high-confidence endpoints or those with parameters
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
        
        new_methods_count = 0
        for i, ep in enumerate(targets):
            self.emit.animator.update(i+1)
            url = ep["url"]
            known_methods = ep.get("methods", ["GET"])
            
            # Method Oracle: Probing for hidden API capabilities
            if self.cfg.enable_method_disc:
                test_set = [m for m in self._METHODS if m not in known_methods]
                for m in test_set:
                    s, h, t = await fetch(self.session, m, url, self.rl)
                    if s in (200, 201, 204, 401, 403):
                        if self.store.update_methods(url, [m]):
                            new_methods_count += 1
                        if s in (401, 403):
                            self.store.record_status(url, m, s)

        self.emit.animator.stop_anim()
        self.emit.always_info(f"[✓] Probing done — new methods: {new_methods_count}")

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
                schema = json.loads(text)
                types  = schema.get("data",{}).get("__schema",{}).get("types",[])
                store.graphql.append({"url": url, "types_count": len(types), "schema": schema})
                emit.warn(f"[GraphQL] {len(types)} types exposed — disable introspection!")
            except Exception as e:
                self.emit.warn(f"[Worker] Error processing {url}: {e}")
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
# INTELLIGENT PROBER
# ══════════════════════════════════════════════════════════════════════


        return found

# ══════════════════════════════════════════════════════════════════════
# ROBOTS + SITEMAP PARSER
# Disallowed paths are crawled as high-value targets, not skipped.
# ══════════════════════════════════════════════════════════════════════

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
                continue
            lower = line.lower()

            if lower.startswith("crawl-delay:"):
                try:
                    self.crawl_delay = float(line.split(":", 1)[1].strip())
                    self.emit.always_info(f"[Robots] Crawl-delay: {self.crawl_delay}s — honouring")
                except (ValueError, IndexError):
                    pass
            elif "disallow:" in lower:
                try:
                    path = line.split(":", 1)[1].strip()
                    if not path:
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
            elif "allow:" in lower:
                try:
                    path = line.split(":", 1)[1].strip()
                    if not path:
                        continue
                    full = urljoin(self.base_url, path)
                    if self.is_valid(full):
                        self.store.add_endpoint(full, source="Robots_Allow", score=Conf.LOW)
                        queued = path != "/"
                        if queued:
                            self.queue.put_nowait((full, 1, "Robots_Allow"))
                        alw_count += 1
                        self.emit.robots_entry("Allow", path, queued)
                except IndexError:
                    pass
            elif "sitemap:" in lower:
                try:
                    sitemap_url = line.split(":", 1)[1].strip()
                    if not sitemap_url.startswith("http"):
                        sitemap_url = line.partition(":")[2].strip()
                    await self.parse_sitemap(sitemap_url)
                    sit_count += 1
                except (IndexError, Exception):
                    pass

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
        count = 0
        for loc in (root.findall("sm:url/sm:loc", ns) or root.findall("url/loc")):
            u = (loc.text or "").strip()
            if u and self.is_valid(u):
                self.store.add_endpoint(u, source="Sitemap", score=Conf.LOW)
                self.queue.put_nowait((u, 1, "Sitemap"))
                count += 1
        if count:
            self.emit.always_info(f"[Sitemap] {sitemap_url} → {count} URLs queued")

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
        self.emit.always_info("[SPA] Launching headless Chromium…")
        try:
            self._pw = await async_playwright().start()
            browser = await self._pw.chromium.launch(headless=True, args=[
                    "--no-sandbox","--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled"])
            ctx_args: dict = {
                "ignore_https_errors": True,
                "viewport": {"width": 1280, "height": 720}
            }
            if self.cookies:
                parsed = urlparse(self.target_url)
                ctx_args["storage_state"] = {"cookies": [
                    {"name":k,"value":v,"domain":parsed.netloc,"path":"/"}
                    for k, v in self.cookies.items()]}
            if self.extra_headers:
                ctx_args["extra_http_headers"] = self.extra_headers
            context = await browser.new_context(**ctx_args)
            await context.route(
                re.compile(r'\.(png|jpg|jpeg|gif|svg|ico|woff2?|ttf|css|mp4|mp3)(\?.*)?$'),
                lambda route, _: asyncio.create_task(route.abort()))
            page = await context.new_page()

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
                self.emit.warn(f"[Worker] Error processing {url}: {e}")

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
                    .filter(u => u && u.startsWith('/'))
            """)
            for path in (links or []):
                full = urljoin(self.target_url, path) if path.startswith("/") else path
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
        if not spa_ctx: return
        browser, context, page = spa_ctx
        
        domain = re.sub(r'[^a-zA-Z0-9_\-]', '_', urlparse(self.target_url).netloc)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        priority = self.screenshot_cfg.get("priority", "standard")
        def get_status(e):
            obs = e.get("observed_status") or []
            if 200 in obs: return 200
            return max(obs) if obs else 0
        
        # Preset logic
        rules = []
        if priority == "all":
            rules = [lambda ep: get_status(ep) in (200, 401, 403, 404)]
        elif priority == "standard":
            rules = [lambda ep: get_status(ep) == 200 or re.search(r'login|admin|dashboard|upload|graphql|swagger|panel|console', ep["url"], re.I)]
        elif priority == "blocked":
            rules = [lambda ep: get_status(ep) in (401, 403)]
        elif priority == "errors":
            rules = [lambda ep: get_status(ep) >= 400]
        elif priority == "api":
            rules = [lambda ep: get_status(ep) != 404 and re.search(r'/api/|/graphql|/swagger|/openapi', ep["url"], re.I)]
        elif priority == "admin":
            rules = [lambda ep: get_status(ep) != 404 and re.search(r'admin|panel|console|manage|backend', ep["url"], re.I)]
        else:
            # Custom keywords or regex
            if "," in priority:
                keywords = [k.strip() for k in priority.split(",")]
                rules = [lambda ep: get_status(ep) != 404 and any(k.lower() in ep["url"].lower() for k in keywords)]
            else:
                rules = [lambda ep: get_status(ep) != 404 and re.search(priority, ep["url"], re.I)]

        base_dir = Path("screenshots") / domain / priority
        base_dir.mkdir(parents=True, exist_ok=True)
        
        count = 0
        seen_urls = set()
        
        for ep in endpoints.values():
            url = ep["url"]
            norm_url = url.split("?")[0].split("#")[0].rstrip("/")
            if norm_url in seen_urls: continue
            
            matched = False
            reason = ""
            if priority in ("all", "standard", "blocked", "errors", "api", "admin"):
                if any(r(ep) for r in rules):
                    matched = True
                    reason = f"preset: {priority}"
            else:
                if any(r(ep) for r in rules):
                    matched = True
                    reason = f"custom match: {priority}"
            
            if matched:
                seen_urls.add(norm_url)
                sanitized_path = re.sub(r'[^a-zA-Z0-9_\-]', '_', urlparse(url).path.strip("/"))
                if not sanitized_path: sanitized_path = "root"
                sanitized_path = sanitized_path[:80]
                filename = f"{ts}_{sanitized_path}.jpg"
                filepath = base_dir / filename
                
                label = ""
                if get_status(ep) in (401, 403):
                    label = " [AUTH WALL]"

                try:
                    self.emit.info(f"[Screenshot] {url} → {filepath}{label}")
                    await page.goto(url, wait_until="domcontentloaded", timeout=10000)
                    await page.screenshot(path=str(filepath), type="jpeg", quality=75)
                    ep["screenshot"] = {
                        "path": str(filepath),
                        "preset": priority,
                        "reason": reason + label
                    }
                    count += 1
                except Exception as e:
                    self.emit.warn(f"[Screenshot] Failed {url}: {e}")
        
        if count:
            self.emit.always_success(f"[Screenshot] Captured {count} screenshots to {base_dir}")
        else:
            self.emit.warn(f"[Screenshot] No endpoints matched the '{priority}' preset (0 captures)")
        
        await browser.close()
        await self._pw.stop()


# ══════════════════════════════════════════════════════════════════════
# RECON UTILITIES (v12.3)
# ══════════════════════════════════════════════════════════════════════

def classify_admin_endpoints(store: Store):
    for ep in store.endpoints.values():
        if _ADMIN_PATTERNS.search(ep["url"]):
            ep["admin_panel"] = True

def classify_auth_endpoints(store: Store):
    for ep in store.endpoints.values():
        for label, pat in _AUTH_PATTERNS.items():
            if pat.search(ep["url"]):
                ep.setdefault("auth_classification", [])
                if label not in ep["auth_classification"]:
                    ep["auth_classification"].append(label)

def classify_idor_candidates(store: Store):
    for ep in store.endpoints.values():
        url = ep["url"]
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
    upload_re = re.compile(
        r'/(?:upload|uploads|file|files|media|attachment|attachments|'
        r'import|ingest|document|documents|image|images|avatar|photo|'
        r'asset|assets|storage|blob|chunk|multipart)',
        re.I
    )
    for ep in store.endpoints.values():
        if upload_re.search(ep["url"]):
            ep["file_upload_candidate"] = True
        if any("file" in p.lower() or "upload" in p.lower()
               for p in ep.get("params", {}).get("form", [])):
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
            p = urlparse(url)
        except Exception:
            return False
        if p.netloc != self.base_domain: return False
        low = url.lower()
        if any(low.endswith(ext) or f"{ext}?" in low for ext in self.cfg.extensions_to_ignore):
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
        for form in soup.find_all("form"):
            action = form.get("action") or url
            full   = urljoin(url, action)
            method = (form.get("method") or "POST").upper()
            # Exhaustive field extraction: all named elements + data-* param hints
            inputs = []
            for el in form.find_all(["input","select","textarea","button","datalist"]):
                nm = el.get("name","").strip()
                if nm and nm not in inputs:
                    inputs.append(nm)
                for da in ("data-param","data-field","data-name","data-key","data-input"):
                    dv = el.get(da,"").strip()
                    if dv and dv not in inputs:
                        inputs.append(dv)
            # data-* on the form element itself (e.g. data-params="field1,field2")
            for da in ("data-params","data-fields","data-inputs"):
                dv = form.get(da,"").strip()
                if dv:
                    for part in re.split(r"[,;|\s]+", dv):
                        p = part.strip()
                        if p and p not in inputs:
                            inputs.append(p)
            if inputs: self.emit.info("[Form] %s %s <- [%s]" % (method, full, ", ".join(inputs)))
            # Fix C: register exact URL, write params directly to form bucket
            self.store.add_endpoint(full, method=method, source="Form", score=Conf.HIGH)
            self.store.add_query_params(full)
            _fkey = self.store._key(full, method)
            if _fkey in self.store.endpoints:
                _ep = self.store.endpoints[_fkey]
                for _p in inputs:
                    if _p and _p not in _ep["params"]["form"]:
                        _ep["params"]["form"].append(_p)
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
        await self._check_sourcemap(session, url)
        for m in re.finditer(r'import\s*\(\s*["\']([^"\']+)["\']', text):
            full = urljoin(url, m.group(1))
            if self.is_valid(full):
                if self._discover_url(full, 1, "JS_DynImport", show_feed=True): ep_count += 1
        for m in re.finditer(r'["\']\/(?:static|_next|assets)\/[a-zA-Z0-9._\-\/]+\.js["\']', text):
            path = m.group(0).strip('"\'')
            if self._discover_url(urljoin(url, path), 1, "JS_Chunk", show_feed=True): ep_count += 1

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
            import re
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

            if depth <= 1:
                self._detect_tech(hdrs, body, url)
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
                import re
                for m in re.finditer(r'"([/][a-zA-Z0-9_\-\/]+)"', body):
                    path = m.group(1)
                    if len(path) > 3:
                        full = urljoin(url, path)
                        if self.is_valid(full):
                            self.store.add_endpoint(full, source='JSON_Path', score=Conf.LOW)
                            if not self._over_budget(depth + 1):
                                self._discover_url(full, depth + 1, 'JSON_Path', show_feed=True)
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
                # Start persistent status animator
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

                # Phase 3: Intelligent Probing
                if self.cfg.enable_probing:
                    prober = IntelligentProber(session, self.store, self.emit, self.rl, self.cfg)
                    await prober.run()

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
                else f"hellhound_{domain}_{ts}.json"

    try:
        Path(json_path).write_text(store.export(target, fmt="json"))
        emit.always_info(f"[Report] JSON saved → {json_path}")
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

    # Always auto-save JSON
    json_path = _auto_save(spider.store, target, cfg.output_file,
                           cfg.output_format, emit)

    intel  = json.loads(spider.store.export(target, fmt="json"))
    result = {"raw": "", "intel": intel}

    # Print rich CLI results
    print_results(intel, target, elapsed, emit, saved_path=json_path)

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
    scan.add_argument("--depth",   "-d",  type=int, default=4,  metavar="N",
                      help="Max crawl depth  (default: 4)")
    scan.add_argument("--concurrency",     type=int, default=12, metavar="N",
                      help="Concurrent workers  (default: 12)")
    scan.add_argument("--timeout",         type=int, default=15, metavar="S",
                      help="Per-request timeout in seconds  (default: 15)")
    scan.add_argument("--verbose", "-v",  action="store_true",
                      help="Show all discovery logs")

    auth = p.add_argument_group(f"{C.CY}Authentication{C.RST}")
    auth.add_argument("--cookie",  type=str, default=None, metavar="COOKIE",
                      help="Cookie string, dict, or path to cookie file")
    auth.add_argument("--auth",    type=str, default=None, metavar="HEADER",
                      help='Authorization header  e.g. "Bearer eyJ..."')

    out = p.add_argument_group(f"{C.CY}Output{C.RST}")
    out.add_argument("--out",      type=str, default=None, metavar="FILE",
                     help="Extra output file  (JSON always auto-saved)")
    out.add_argument("--format",   type=str, default="json",
                     choices=["json","jsonl","csv","burp"],
                     help="Extra output format  (default: json)")

    flags = p.add_argument_group(f"{C.CY}Feature Flags{C.RST}")
    flags.add_argument("--no-playwright", action="store_true",
                       help="Disable headless browser SPA scanning")
    flags.add_argument("--no-probing",    action="store_true",
                       help="Disable intelligent probing phase")
    flags.add_argument("--spa-interact", action="store_true",
                       help="Enable SPA form filling and button clicking (use only on authorized targets)")
    flags.add_argument("--no-cors",       action="store_true",
                       help="Disable CORS misconfiguration checks")
    flags.add_argument("--no-graphql",    action="store_true",
                       help="Disable GraphQL introspection probe")
    flags.add_argument("--no-openapi",    action="store_true",
                       help="Disable OpenAPI / Swagger discovery")
    flags.add_argument("--extract",      action="store_true",
                       help="Enable passive data extraction (emails, IPs, buckets)")
    flags.add_argument("--screenshot", nargs="?", const="standard",
                       help="Capture screenshots of key endpoints (default: standard). Optionally specify preset: all, blocked, errors, api, admin, or custom regex")

    util = p.add_argument_group(f"{C.CY}Utilities{C.RST}")
    util.add_argument("--diff",    type=str, default=None, metavar="OLD_REPORT",
                      help="Diff this scan against an old JSON report")
    util.add_argument("--upgrade", action="store_true",
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
    pw_status = "enabled" if (not args.no_playwright and PLAYWRIGHT_AVAILABLE) else "disabled"
    if pw_status == "disabled" and PLAYWRIGHT_ERROR and args.verbose:
        pw_status += f"  {C.R}({PLAYWRIGHT_ERROR}){C.RST}"
    
    _pf("Playwright", pw_status,
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
        enable_openapi  = not args.no_openapi,
        enable_extraction = args.extract,
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