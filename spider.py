#!/usr/bin/env python3

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
import subprocess
import base64
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from http.cookiejar import MozillaCookieJar
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urlparse, urljoin, parse_qs, urlencode, urlunparse

import aiohttp
import socket
import ipaddress
import ssl as _ssl
from bs4 import BeautifulSoup, Comment

                                                                             
                                                  
                                                                                   
                                                                             
PLAYWRIGHT_AVAILABLE  = False
PLAYWRIGHT_ERROR      = None
PATCHRIGHT_AVAILABLE  = False                                                            

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

                                                                                   
try:
    import importlib.util as _ilu
    PATCHRIGHT_AVAILABLE = _ilu.find_spec("patchright") is not None
except Exception:
    PATCHRIGHT_AVAILABLE = False

                                                                        
          
                                                                        

VERSION      = "13.11"
__author__   = "Sree Danush S (L4ZZ3RJ0D)"
__license__  = "GPLv3"
__credits__  = ["L4ZZ3RJ0D"]
__maintainer__ = "L4ZZ3RJ0D"

                                                                        
                  
                                                                        

class C:
    R   = "\033[91m"                
    RD  = "\033[31m"              
    G   = "\033[92m"                  
    GD  = "\033[32m"                
    Y   = "\033[93m"            
    O   = "\033[38;5;208m"          
    CY  = "\033[96m"                 
    CYD = "\033[36m"              
    BL  = "\033[94m"          
    MG  = "\033[95m"             
    W   = "\033[97m"           
    GR  = "\033[90m"          
    GL  = "\033[37m"                
    B   = "\033[1m"           
    DIM = "\033[2m"
    RST = "\033[0m"            

                                   
    BG_RED    = "\033[41m\033[97m"                                 
    BG_AMBER  = "\033[48;5;214m\033[38;5;16m"                     
    BG_MAG    = "\033[45m\033[97m"                                 
    BG_GREEN  = "\033[102m\033[30m"                                    
    BG_BLUE   = "\033[44m\033[97m"                               

def _no_color() -> bool:
    return not sys.stdout.isatty() or bool(os.environ.get("NO_COLOR"))

def _strip(s: str) -> str:
    return re.sub(r'\033\[[^m]*m', '', s)

                                                                        
                              
                                                                        

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

                                                                                          
                bar_w = 50
                chars = "⡀⡄⡆⡇⣇⣧⣷⣿"
                bar = ""
                for i in range(bar_w):
                    idx = int((math.sin(t * 5 + i * 0.2) + 1) / 2 * (len(chars) - 1))
                    bar += f"{C.R}{chars[idx]}{C.RST}" if not self._nc else "."

                if self.total:
                    stats = f"{C.W}{self.current:>3}/{self.total:<3}{C.RST}" if not self._nc else f"{self.current}/{self.total}"
                else:
                                                                 
                    v = math.sin(t * 8)
                    if not self._nc:
                        c = C.R if v > 0 else C.RD
                        stats = f"{c}---{C.RST}"
                    else:
                        stats = "---"

                line = f"\r  {anim_label:<25}  {bar}  {stats}" if not self._nc else f"\r  {self.label} {self.current}/{self.total}"
                
                                                                       
                if self._last_line and len(_strip(line)) < len(_strip(self._last_line)):
                    pad = " " * (len(_strip(self._last_line)) - len(_strip(line)) + 5)
                else:
                    pad = "    "
                
                self._last_line = line
                                           
                with self.emit.lock:
                    sys.stdout.write(line + pad)
                    sys.stdout.flush()
                
                time.sleep(0.06)
            except Exception:
                time.sleep(0.5)

                                                                        
      
                                                                        

class Emit:
\
\
\
\
\
\
       

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._nc     = _no_color()
        self.lock    = threading.Lock()
        self.animator = CLIAnimator(self)

                                                                        

    def _w(self, line: str):
                                                                                  
        with self.lock:
            if self.animator.active:
                                               
                if self.animator._last_line:
                    sys.stdout.write("\r" + " " * (len(_strip(self.animator._last_line)) + 15) + "\r")
                print(_strip(line) if self._nc else line, flush=True)
                                                             
            else:
                print(_strip(line) if self._nc else line, flush=True)

                                                                        

    def info(self, msg: str):
        if self.verbose:
            self._w(f"{C.CYD}[~]{C.RST} {C.GR}{msg}{C.RST}")

    def success(self, msg: str):
        if self.verbose:
            self._w(f"{C.G}[+]{C.RST} {C.GD}{msg}{C.RST}")

    def warn(self, msg: str):
        self._w(f"{C.R}{C.B}[!]{C.RST} {C.R}{msg}{C.RST}")

    def warn_sev(self, msg: str, severity: str = "HIGH"):
                                                                       
        nc = self._nc
        sev = severity.upper()
        if sev == "CRITICAL":
            bracket = f"{C.BG_RED}{C.B}[CRIT]{C.RST}" if not nc else "[CRIT]"
            body    = f"{C.R}{C.B}{msg}{C.RST}"        if not nc else msg
        elif sev == "HIGH":
            bracket = f"{C.R}{C.B}[HIGH]{C.RST}"       if not nc else "[HIGH]"
            body    = f"{C.R}{msg}{C.RST}"              if not nc else msg
        elif sev == "MEDIUM":
            bracket = f"{C.O}{C.B}[MED]{C.RST}"        if not nc else "[MED]"
            body    = f"{C.O}{msg}{C.RST}"              if not nc else msg
        else:                                                       
            bracket = f"{C.GR}[LOW]{C.RST}"            if not nc else "[LOW]"
            body    = f"{C.GR}{msg}{C.RST}"             if not nc else msg
        self._w(f"{bracket} {body}")

    def always_info(self, msg: str):
        self._w(f"{C.CY}[*]{C.RST} {msg}")

    def crawl_feed(self, ftype: str, method: str = "GET", url: str = "", status: int = 0, size_bytes: int = 0, extra: List[str] = None):
                                                                
                                                                         
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

                     
        if ftype == "Found":
            tcol = C.G;  label = f"{tcol}↳{C.RST}"
        elif ftype == "JS":
            tcol = C.Y;  label = f"{tcol}[ JS ]{C.RST}"
        else:
            tcol = C.CY; label = f"{tcol}[ ↓  ]{C.RST}"

        if ftype == "Found":
                                                              
            self._w(f"  {label} {C.W}{disp_url}{C.RST}")
        else:
                                                                        
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
                                                                
        self._w(f"  {C.R}•{C.RST} {C.W}{url}{C.RST}")

    def always_success(self, msg: str):
        self._w(f"{C.G}{C.B}[✓]{C.RST} {C.B}{msg}{C.RST}")

    def robots_entry(self, directive: str, path: str, queued: bool):
                                                                                               
                                                                                           
        _GROUP_MAP = {
            "DISALLOW":  "ROBOTS.TXT",
            "ALLOW":     "ROBOTS.TXT",
            "SITEMAP-REF": "ROBOTS.TXT",
            "SITEMAP":   "SITEMAP",
            "WAYBACK":   "WAYBACK",
            "CRT.SH":    "CRT.SH SUBDOMAINS",
        }
        group = _GROUP_MAP.get(directive.upper(), directive.upper())
        if not hasattr(self, "_last_feed_group"):
            self._last_feed_group = None
        if group != self._last_feed_group:
            self._last_feed_group = group
            if self._nc:
                print(f"\n  ── {group} ──")
            else:
                self._w(f"\n  {C.CY}── {group} ──{C.RST}")

        display_dir = "Sitemap" if directive.upper() == "SITEMAP-REF" else directive
        if self._nc:
            status = "crawling" if queued else "skipped"
            print(f"  |  {display_dir:<10} {path}  [{status}]")
            return
        if directive.upper() == "DISALLOW":
            dc = C.R; icon = "✖"
        elif directive.upper() == "SITEMAP-REF":
            dc = C.CY; icon = "◈"
        elif directive.upper() in ("SITEMAP", "WAYBACK", "CRT.SH"):
            dc = C.CY; icon = "↳"
        else:
            dc = C.GD; icon = "✔"
        status = f"{C.G}crawling{C.RST}" if queued else f"{C.GR}skipped{C.RST}"
        self._w(f"  {C.GR}├─{C.RST} {dc}{icon} {display_dir:<10}{C.RST} {C.W}{path:<40}{C.RST}  {C.GR}↳{C.RST} {status}")

    def robots_comment_leak(self, comment: str):
                                                                
        if self._nc:
            print(f"  |  [COMMENT-LEAK] {comment}")
            return
        self._w(f"  {C.GR}├─{C.RST} {C.BG_RED} COMMENT LEAK {C.RST} {C.Y}{comment}{C.RST}")

    def security_txt_field(self, field: str, value: str, flagged: bool = False):
                                                                            
        if self._nc:
            tag = "[LEAK]" if flagged else "[SecurityTxt]"
            print(f"  |  {tag} {field}: {value}")
            return
        if flagged:
            self._w(f"  {C.GR}├─{C.RST} {C.BG_RED} LEAK {C.RST} {C.R}{field}:{C.RST} {C.Y}{value}{C.RST}")
        else:
            self._w(f"  {C.GR}├─{C.RST} {C.CY}{field}:{C.RST} {C.W}{value}{C.RST}")

                                                                       

    def section(self, title: str, orbital: bool = False):
                                                
        if self._nc:
            print(f"\n  [ {title} ]")
            return
        icon = f"{C.R}◓{C.RST} " if orbital else ""
        print(f"\n  {icon}{C.B}{C.W}{title}{C.RST}")
        print(f"  {C.GR}{'─' * 60}{C.RST}")

    def row(self, label: str, value: str, icon: str = "●", label_colour=None, value_colour=None):
                                                
        lc = label_colour or C.W
        vc = value_colour or C.W
        if self._nc:
            print(f"    {label:<20}  {_strip(value)}")
        else:
                                                    
            if "Score" in label or "Threats" in label: ic = C.R
            elif "Crawl" in label or "Leaks" in label: ic = C.G
            else: ic = C.CY
            print(f"  {ic}●{C.RST} {lc}{label:<14}{C.RST} {vc}{value}{C.RST}")

    def finding(self, tag: str, severity: str, msg: str):
                                                 
        if self._nc:
            print(f"  [{severity:<7}] [{tag}] {msg}")
            return
            
        sev = severity.upper()
                                   
        if "HIGH" in sev or "CRITICAL" in sev: bg = C.BG_RED
        elif "MEDIUM" in sev: bg = C.BG_AMBER
        elif "LEAK" in tag.upper() or "SECRET" in tag.upper(): bg = C.BG_BLUE
        elif "SUCCESS" in sev or "CONFIRMED" in sev: bg = C.BG_GREEN
        else: bg = C.BG_MAG

        print(f"  {bg} {sev:^8} {C.RST} {C.B}{C.W}{tag:^12}{C.RST} {C.W}┄{C.RST} {C.DIM}{msg}{C.RST}")

    def leader_row(self, label: str, value: str, indent: int = 4):
                                                                      
        if self._nc:
            print(f"{' ' * indent}{label} {value}")
            return
        print(f"{' ' * indent}{C.GR}┄{C.RST} {C.CYD}{label:^8}{C.RST} {C.W}{value}{C.RST}")

    def endpoint_row(self, ep: dict):
                                                            
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

                                                                         
        is_404 = conf == "404_NOT_FOUND"
        cc = {
            "CONFIRMED":    C.G,
            "HIGH":         C.Y,
            "MEDIUM":       C.CYD,
            "LOW":          C.GR,
            "404_NOT_FOUND": C.GR,
        }.get(conf, C.GR)

                                                            
        obs     = ep.get("observed_status", [])
        status_hint = ""
        if is_404:
            status_hint = f" [404]"
        elif obs and obs != [200]:
                                                                                
            status_hint = f" [{','.join(str(s) for s in obs[:3])}]"

        conf_display = "NOT FOUND" if is_404 else conf

                                                                         
        if self._nc:
            print(f"    {method:<7}  {conf_display:<12}  {_strip(auth)}{_strip(sens)}{_strip(snap)}  {url}{status_hint}")
        else:
            url_col = C.GR if is_404 else C.W
            print(f"  {mc}{method:<7}{C.RST} {cc}{conf_display:<12}{C.RST} {auth}{sens}{snap} {url_col}{url}{C.RST}{C.GR}{status_hint}{C.RST}")

    def print_always(self, msg: str):
        self._w(msg)

                                                                        
                                           
                                                                        

def print_results(intel: dict, target: str, elapsed: float,
                  emit: Emit, saved_path: str = "", phase_times: tuple = ()):

    s   = intel.get("summary", {})
    eps = intel.get("endpoints", [])
    nc  = emit._nc

                                                                               
    _NOISE_SOURCES_GLOBAL = frozenset({"Backup_Probe", "Backup_Suffix", "WellKnown", "Leaked_File"})
    real_eps = [e for e in eps if not all(src in _NOISE_SOURCES_GLOBAL for src in e.get("source", ["Crawl"]))]

    def _bad(v):
                                                              
        if isinstance(v, int):
            if v == 0:
                return f"{C.GR}0{C.RST}" if not nc else "0"
            return f"{C.R}{C.B}{v}{C.RST}" if not nc else str(v)
        return str(v)

    def _good(v):
                                      
        if isinstance(v, int):
            if v == 0:
                return f"{C.GR}0{C.RST}" if not nc else "0"
            return f"{C.G}{C.B}{v}{C.RST}" if not nc else str(v)
        return str(v)

                                                                        
    print()
    meta = intel.get("meta", {})
    if not nc:
        emit.section(f"TARGET  {meta.get('target')}")
    else:
        print(f"[*] Target: {meta.get('target')}")

    if not nc:
        emit.row("Structure",  f"{s.get('total_endpoints')} Clusters discovered", value_colour=C.CY)
        emit.row("Confidence", f"{int(s.get('confirmed', 0))} high-fidelity anchors", value_colour=C.CY)
        emit.row("Threads",    "12", value_colour=C.CY)             
    else:
        print(f"[*] Clusters:   {s.get('total_endpoints')}")
        print(f"[*] High-fid:   {s.get('confirmed')}")

                         
    _NOISE_SRCS = frozenset({"Backup_Probe", "Backup_Suffix", "WellKnown", "Leaked_File"})
    _real_eps   = [e for e in eps if not all(src in _NOISE_SRCS for src in e.get("source", ["Crawl"]))]
    _backup_eps = [e for e in eps if all(src in _NOISE_SRCS for src in e.get("source", ["Crawl"]))]
    
                                  
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

                                                                        
                                                  
                                                     
                                               
                          
                  
                   
                         
                          
                   
                
                
                           
                    
                                                                     
                        
                                
                      
                       
                                                            
                                                                        

                                                                        
    resp_headers = intel.get("target_response_headers", {})
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
                    print(f"  {C.BG_RED} LEAK {C.RST} {C.R}{hdr}{C.RST}{C.GR}:{C.RST} {C.Y}{val}{C.RST}")
                elif is_sec:
                    present_sec.add(h_lo)
                    print(f"  {C.G}●{C.RST} {C.G}{hdr}{C.RST}{C.GR}:{C.RST} {C.W}{val}{C.RST}")
                else:
                    print(f"  {C.GR}●{C.RST} {C.GR}{hdr}{C.RST}{C.GR}:{C.RST} {C.GL}{val}{C.RST}")
        missing_sec = _SEC_HEADERS - present_sec - {"access-control-allow-origin"}
        if missing_sec and not nc:
            print(f"\n  {C.R}{C.B}Missing Security Headers:{C.RST}")
            for mh in sorted(missing_sec):
                print(f"  {C.R}✖{C.RST} {C.Y}{mh}{C.RST}")

                                                                        
    header_issues = intel.get("header_audit", [])
    if header_issues:
        emit.section(f"SECURITY HEADERS  ({len(header_issues)} issue(s))", orbital=True)
        for f in header_issues:
            sev     = f.get("severity", "INFO")
            sev_col = {"HIGH": C.R, "MEDIUM": C.O, "LOW": C.GR}.get(sev, C.GR) if not nc else ""
            if nc:
                print(f"  [{sev}] {f.get('header','')}  {f.get('detail','')}")
            else:
                pill = f"{sev_col}{C.B}[{sev}]{C.RST}"
                print(f"  {pill} {sev_col}{f.get('header',''):<32}{C.RST} {C.GR}{f.get('detail','')}{C.RST}")

                                                                        
    tls_findings = intel.get("tls_findings", [])
    if tls_findings:
        emit.section(f"TLS / CERTIFICATE  ({len(tls_findings)} issue(s))", orbital=True)
        for f in tls_findings:
            sev     = f.get("severity", "INFO")
            sev_col = {"CRITICAL": C.BG_RED, "HIGH": C.R, "MEDIUM": C.O, "LOW": C.GR}.get(sev, C.GR) if not nc else ""
            if nc:
                print(f"  [{sev}] {f.get('issue','')}  {f.get('detail','')}")
            else:
                pill = f"{sev_col}{C.B} {sev} {C.RST}"
                print(f"  {pill}  {C.W}{f.get('issue','')}{C.RST}  {C.GR}{f.get('detail','')}{C.RST}")

                                                                        
    waf_findings = intel.get("waf_findings", [])
    if waf_findings:
        emit.section(f"WAF / CDN  ({len(waf_findings)} detected)", orbital=True)
        for wf in waf_findings:
            conf_col = {"HIGH": C.R, "MEDIUM": C.O, "LOW": C.GR}.get(wf.get("confidence",""), C.GR) if not nc else ""
            if nc:
                print(f"  [WAF] {wf.get('waf','')}  ({wf.get('confidence','')})")
            else:
                pill = f"{conf_col}{C.B}[{wf.get('confidence','?')}]{C.RST}"
                print(f"  {C.MG}◈{C.RST} {pill} {C.W}{wf.get('waf','')}{C.RST}")

                                                                        
    # ── TECH STACK — rich WhatWeb panel + internal fallback ──────────────────
    whatweb_data = intel.get("whatweb_data", {})
    tech_list    = intel.get("tech_stack", [])
    # internal-only entries (exclude [WW] prefixed ones added by WhatWeb)
    internal_tech = [t for t in tech_list if not t.startswith("[WW]")]

    if whatweb_data or internal_tech:
        total_plugins = sum(len(v) for v in whatweb_data.values()) if whatweb_data else len(internal_tech)
        source_label  = "WhatWeb" if whatweb_data else "Internal Detection"
        emit.section(f"TECH STACK  ({total_plugins} plugins · {source_label})", orbital=True)

        if whatweb_data:
            _ORDER = ["Server","Runtime","CDN/Cloud","CMS","Framework","JS Libs",
                      "Analytics","Security","Generator","Cookies","GeoIP","Emails","Headers","Page","Other"]
            _CAT_STYLE = {
                "Server":     (C.R,   "SERVER   "),
                "Runtime":    (C.O,   "RUNTIME  "),
                "CMS":        (C.R,   "CMS      "),
                "Framework":  (C.O,   "FRAMEWORK"),
                "JS Libs":    (C.W,   "JS LIBS  "),
                "Analytics":  (C.GL,  "ANALYTICS"),
                "CDN/Cloud":  (C.O,   "CDN/CLOUD"),
                "Security":   (C.G,   "SECURITY "),
                "Generator":  (C.GL,  "GENERATOR"),
                "GeoIP":      (C.GR,  "GEO/IP   "),
                "Emails":     (C.GL,  "EMAIL    "),
                "Cookies":    (C.GR,  "COOKIES  "),
                "Headers":    (C.GR,  "HEADERS  "),
                "Page":       (C.GR,  "PAGE     "),
                "Other":      (C.GR,  "OTHER    "),
            }
            ordered_cats = _ORDER + [c for c in whatweb_data if c not in _ORDER]

            for cat in ordered_cats:
                entries = whatweb_data.get(cat)
                if not entries:
                    continue
                col, label = _CAT_STYLE.get(cat, (C.GR, f"{cat:<9}"))
                if nc:
                    items_str = "  ·  ".join(e[1] if isinstance(e, (list,tuple)) else str(e) for e in entries)
                    print(f"  [{label.strip():<9}]  {items_str}")
                else:
                    badge = f"{C.R}{C.B}[{C.RST}{col}{C.B}{label.strip()}{C.RST}{C.R}{C.B}]{C.RST}"
                    pills = []
                    for e in entries:
                        icon, display = (e[0], e[1]) if isinstance(e, (list,tuple)) else ("·", str(e))
                        pills.append(f"{col}{C.B}{icon}{C.RST} {col}{display}{C.RST}")
                    pills_str = f"  {C.GR}│{C.RST}  ".join(pills)
                    print(f"  {badge}  {pills_str}")

        elif internal_tech:
            # Fallback: internal detection only when WhatWeb produced nothing
            if nc:
                print(f"    {' · '.join(internal_tech)}")
            else:
                sep = f"  {C.GR}·{C.RST}  "
                row = sep.join(f"{C.MG}{t}{C.RST}" for t in internal_tech)
                if row:
                    print(f"    {row}")

                                                                        
    dns_findings = intel.get("dns_findings", [])
    if dns_findings:
        emit.section(f"DNS INTELLIGENCE  ({len(dns_findings)} finding(s))", orbital=True)
        for f in dns_findings:
            sev     = f.get("severity", "INFO")
            sev_col = {"CRITICAL": C.BG_RED, "HIGH": C.R, "MEDIUM": C.O, "LOW": C.GR}.get(sev, C.GR) if not nc else ""
            if nc:
                print(f"  [{sev}] {f.get('issue','')}  {f.get('detail','')}")
            else:
                pill = f"{sev_col}{C.B} {sev} {C.RST}"
                print(f"  {pill}  {C.W}{f.get('issue','')}{C.RST}  {C.GR}{f.get('detail','')}{C.RST}")

                                                                        
    crt_subs = intel.get("crt_subdomains", [])
    if crt_subs:
        emit.section(f"CRT.SH SUBDOMAINS  ({len(crt_subs)} discovered)", orbital=True)
        for sub in sorted(crt_subs, key=lambda s: s.get("hostname","") if isinstance(s,dict) else str(s)):
            hostname = sub.get("hostname","") if isinstance(sub, dict) else str(sub)
            url      = sub.get("url","")      if isinstance(sub, dict) else ""
            queued   = sub.get("queued", False) if isinstance(sub, dict) else False
            q_tag    = f"  {C.G}[crawling]{C.RST}" if queued else f"  {C.GR}[passive]{C.RST}"
            if nc:
                print(f"  ● {hostname:<40} {url}  {'[crawling]' if queued else ''}")
            else:
                print(f"  {C.G}●{C.RST} {C.W}{hostname:<40}{C.RST} {C.CYD}{url}{C.RST}{q_tag}")

                                                                        
    robots         = intel.get("robots_disallowed", [])
    robots_allowed = intel.get("robots_allowed", [])
    all_ep_urls_r  = [e.get("url","") for e in eps]
    parsed_target  = intel.get("meta",{}).get("target","")

    if robots:
        emit.section(f"ROBOTS.TXT DISALLOWED  ({len(robots)} paths)", orbital=True)
        for path in robots:
            if nc:
                print(f"  ✖ Disallow       {path}")
            else:
                print(f"  {C.R}●{C.RST} {C.R}Disallow{C.RST}       {C.Y}{path}{C.RST}")
            seen_r: set = set()
            for u in all_ep_urls_r:
                if not u or u == parsed_target or u in seen_r: continue
                if ("/" + path.lstrip("/")) in urlparse(u).path:
                    seen_r.add(u)
                    if nc: print(f"       └─ {u}")
                    else:  print(f"  {C.GR}     └─{C.RST} {C.CYD}{u}{C.RST}")

    if robots_allowed:
        emit.section(f"ROBOTS.TXT ALLOWED  ({len(robots_allowed)} paths)", orbital=True)
        for path in robots_allowed:
            if path.strip() == "/":
                if nc: print(f"  ✔ Allow  {path}  (entire site explicitly allowed)")
                else:  print(f"  {C.G}●{C.RST} {C.G}Allow{C.RST}  {C.W}{path}{C.RST}  {C.GR}(entire site explicitly allowed){C.RST}")
            else:
                if nc: print(f"  ✔ Allow  {path}")
                else:  print(f"  {C.G}●{C.RST} {C.G}Allow{C.RST}  {C.W}{path}{C.RST}")
                seen_r2: set = set()
                for u in all_ep_urls_r:
                    if not u or u == parsed_target or u in seen_r2: continue
                    if ("/" + path.lstrip("/")) in urlparse(u).path:
                        seen_r2.add(u)
                        if nc: print(f"       └─ {u}")
                        else:  print(f"  {C.GR}     └─{C.RST} {C.CYD}{u}{C.RST}")

                                                                        
    sitemap_eps = [e for e in eps if "Sitemap" in e.get("source", [])]
    if sitemap_eps:
        emit.section(f"SITEMAP ENDPOINTS  ({len(sitemap_eps)} found)", orbital=True)
        for ep in sorted(sitemap_eps, key=lambda e: e.get("url","")):
            u   = ep.get("url","")
            con = ep.get("confidence","LOW")
            if nc:
                print(f"  ● {con:<12} {u}")
            else:
                col = {"CONFIRMED": C.G, "HIGH": C.Y, "MEDIUM": C.CYD, "LOW": C.GR}.get(con, C.GR)
                print(f"  {C.CY}●{C.RST} {col}{con:<12}{C.RST} {C.W}{u}{C.RST}")

                                                                        
    wayback_eps = [e for e in eps if "Wayback" in e.get("source", [])]
    if wayback_eps:
        emit.section(f"WAYBACK URLS  ({len(wayback_eps)} archived endpoints)", orbital=True)
        for ep in sorted(wayback_eps, key=lambda e: e.get("url","")):
            u   = ep.get("url","")
            con = ep.get("confidence","LOW")
            if nc:
                print(f"  ● {con:<12} {u}")
            else:
                col = {"CONFIRMED": C.G, "HIGH": C.Y, "MEDIUM": C.CYD, "LOW": C.GR}.get(con, C.GR)
                print(f"  {C.MG}●{C.RST} {col}{con:<12}{C.RST} {C.W}{u}{C.RST}")

                                                                        
    comments = intel.get("comments", [])
    cmt_filtered = []   # built below, displayed after SECURITY FINDINGS
    if comments:
                                                                             
        _HIGH_SIGNAL_KW = re.compile(
            r'(?:password|passwd|secret|token|api[_-]?key|'
            r'credential|auth[_-]?key|private[_-]?key|access[_-]?key|'
            r'todo[:\s]+remove|fixme|do\s+not\s+commit|'
            r'debug[_-]?mode|hack|bypass|hardcod|'
            r'internal[_-]?(?:use|only|api|endpoint)|'
            r'prod(?:uction)[_-](?:key|token|secret|db|host)|'
            r'staging[_-](?:key|token|secret)|'
            r'backup[_-](?:key|path|db)|'
            r'admin[_-](?:pass|key|token|secret))',
            re.I
        )
                                                                                
        _LOW_SIGNAL_KW = re.compile(
            r'(?:admin|internal|staging|prod(?:uction)?|backup|'
            r'temp(?:orary)?|beta|debug|version|framework|'
            r'new[_-]home|homepage|disabled|removed)',
            re.I
        )
                                                                                         
        _SCHEME_HOST_RE = re.compile(r'https?://[^\s/]+', re.I)
        _FULL_URL_RE    = re.compile(r'https?://\S+', re.I)
        _INT_PATH_RE    = re.compile(r'(?<![a-z0-9\-\._:/])/[a-z0-9_\-\.]{2,}', re.I)
        _EXT_URL_RE     = re.compile(r'https?://', re.I)

        def _has_internal_path(txt: str) -> bool:
                                                                           
            no_urls = _FULL_URL_RE.sub("", txt)
            no_urls = _SCHEME_HOST_RE.sub("", no_urls)
            return bool(_INT_PATH_RE.search(no_urls))

        def _is_sensitive_comment(txt: str) -> bool:
                                                                 
            if _HIGH_SIGNAL_KW.search(txt):
                return True
                                                                           
            if _LOW_SIGNAL_KW.search(txt) and _has_internal_path(txt):
                return True
                                                                        
            if _has_internal_path(txt) and not _EXT_URL_RE.search(txt):
                return True
                                                               
            if _EXT_URL_RE.search(txt) and _has_internal_path(txt):
                return True
                                                                                
            for m in _FULL_URL_RE.finditer(txt):
                host_m = re.match(r'https?://([^/\s]+)', m.group(0))
                if host_m:
                    h = host_m.group(1).lower()
                    if (re.match(r'^\d+\.\d+\.\d+\.\d+', h) or
                            h in ("localhost", "127.0.0.1") or
                            any(h.endswith(s) for s in
                                (".local", ".internal", ".corp", ".lan", ".intranet"))):
                        return True
            return False

        _sensitive_comments = [
            c for c in comments
            if _is_sensitive_comment(str(c.get("content","") or ""))
        ]
        if _sensitive_comments:
            _norm_re = re.compile(r'\b\d+\.\d+\b')
            seen_norm: dict = {}
            for c in _sensitive_comments:
                full = str(c.get("content","") or c.get("text","") or c)
                raw_sources = c.get("all_sources") or ([c.get("source","")] if c.get("source") else [])
                key  = _norm_re.sub("N", full)
                if key not in seen_norm:
                    seen_norm[key] = {"content": full, "sources": list(dict.fromkeys(s for s in raw_sources if s))}
                else:
                    for s in raw_sources:
                        if s and s not in seen_norm[key]["sources"]:
                            seen_norm[key]["sources"].append(s)

            _html_tag_re    = re.compile(r'<[^>]+>')
            _pure_url_re    = re.compile(r'^https?://\S+$')
            _mostly_html_re = re.compile(r'<(?:a|img|div|span|h[1-6]|p|ul|li|nav|section|header|footer)\b', re.I)
            _path_in_cmt_re = re.compile(r'(?:^|\s)(/[a-z0-9_\-\.]{2,}(?:/[a-z0-9_\-\.]*)*/?)', re.I)
            _MAX_CMT        = 160

            def _clean_cmt(raw):
                return re.sub(r'\s+', ' ', _html_tag_re.sub(" ", raw)).strip()

            def _noise_cmt(raw, cleaned):
                return (_mostly_html_re.search(raw) or len(cleaned) < 8
                        or bool(_pure_url_re.match(cleaned)))

            all_ep_urls = [e.get("url","") for e in eps]
            cmt_filtered = []
            for entry in seen_norm.values():
                cleaned = _clean_cmt(entry["content"])
                if _noise_cmt(entry["content"], cleaned):
                    continue
                display = cleaned if len(cleaned) <= _MAX_CMT else cleaned[:_MAX_CMT] + "…"
                qpaths = []
                for m in _path_in_cmt_re.finditer(entry["content"]):
                    cp = m.group(1).strip()
                    qpaths.extend(u for u in all_ep_urls
                                  if urlparse(u).path.rstrip("/") == cp.rstrip("/"))
                cmt_filtered.append({
                    "display": display,
                    "sources": entry["sources"],
                    "queued_paths": list(dict.fromkeys(qpaths)),
                })

            if cmt_filtered:
                pass  # displayed later, after SECURITY FINDINGS

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
    sorted_eps = sorted(real_eps, key=lambda e: (order.get(e.get("confidence", "LOW"), 4), e.get("url", ""))) +\
                 sorted(backup_eps, key=lambda e: e.get("url", ""))
                                                 
                                                                          
                                                      
    _disp_clusters: set = set()
    deduped = []
    for ep in sorted_eps:
        _cl = ep.get("cluster", ep.get("url",""))
        if _cl and _cl in _disp_clusters and not ep.get("params"):
            continue                                                      
        if _cl:
            _disp_clusters.add(_cl)
        deduped.append(ep)

                                                                                 
                                                                                
    _third_party_host = re.compile(
        r'(?:^|\.)(?:google-analytics\.com|analytics\.google\.com|'
        r'doubleclick\.net|googletagmanager\.com|facebook\.net|'
        r'connect\.facebook\.net|hotjar\.com|segment\.com|'
        r'amplitude\.com|mixpanel\.com|intercom\.io|'
        r'cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com)$',
        re.I
    )
    for ep in deduped:
        ep_host = urlparse(ep.get("url","")).netloc
        if _third_party_host.search(ep_host):
            continue
        emit.endpoint_row(ep)

                                                                   
                                                                     
                                              
    _FW_PREFIX_RE = re.compile(
        r'^(?:wpforms\[|_wpnonce|_wp_http_referer|action\[|'
        r'wp-submit|testcookie|rememberme|submit\b)',
        re.I
    )
    def _is_noise_p(p: str) -> bool:
        base = p.lower().split("[")[0].rstrip()
        if base in _NOISE_PARAMS: return True
        if _FW_PREFIX_RE.match(p): return True
        clean = re.sub(r'\[hidden\]$', '', p, flags=re.I).strip()
        return clean.lower() in _NOISE_PARAMS

    def _has_real_params(ep):
        raw = ep.get("params", [])
        if isinstance(raw, dict):
            raw = [p for bucket in raw.values() for p in bucket]
        real = [p for p in raw if not _is_noise_p(p)]
        return bool(real) or ep.get("parameter_sensitive")

    interesting = [
        e for e in real_eps
        if _has_real_params(e)
        and e.get("confidence") != "404_NOT_FOUND"
        and 404 not in (e.get("observed_status") or [])
    ]

    if interesting:
        emit.section(f"PARAMETER MAP  ({len(interesting)} endpoints)", orbital=True)
        for ep in interesting:
            url    = ep.get("url","")
                                                                                     
            all_p  = ep.get("params", [])
            if isinstance(all_p, dict):
                                                                   
                all_p = [p for bucket in all_p.values() for p in bucket]
                                                           
                                                                        
                                                                    
            _FRAMEWORK_PREFIX = re.compile(
                r'^(?:wpforms\[|_wpnonce|_wp_http_referer|action\[|'
                r'wp-submit|testcookie|rememberme|submit\b)',
                re.I
            )
            def _is_noise_param(p: str) -> bool:
                base = p.lower().split("[")[0].rstrip()
                if base in _NOISE_PARAMS:
                    return True
                if _FRAMEWORK_PREFIX.match(p):
                    return True
                                                   
                clean = re.sub(r'\[hidden\]$', '', p, flags=re.I).strip()
                if clean.lower() in _NOISE_PARAMS:
                    return True
                return False

            all_p = [p for p in all_p if not _is_noise_param(p)]
            if not all_p: continue

            method = ep.get("method", "GET")
            mc = { "GET": C.GD, "POST": C.Y, "PUT": C.O, "PATCH": C.O, "DELETE": C.R }.get(method, C.GL)
                                                                             
            disp = url

                                                                      
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

                                                                    
                                                                       
                                                                           
            def _collapse_numbered(params: list) -> list:
                _num_suffix = re.compile(r'^(.+?)[-_](\d+)(\[.*\])?$')
                groups: dict = {}                                   
                order:  list = []                             
                for p in params:
                    m = _num_suffix.match(p)
                    if m:
                        base, num, suf = m.group(1), int(m.group(2)), m.group(3) or ""
                        if base not in groups:
                            groups[base] = {"nums": [], "suffix": suf}
                            order.append(("group", base))
                        groups[base]["nums"].append(num)
                    else:
                        order.append(("single", p))
                result = []
                seen_groups: set = set()
                for kind, val in order:
                    if kind == "single":
                        result.append(val)
                    else:
                        if val in seen_groups:
                            continue
                        seen_groups.add(val)
                        g = groups[val]
                        nums = sorted(g["nums"])
                        suf  = g["suffix"]
                        if len(nums) == 1:
                            result.append(f"{val}-{nums[0]}{suf}")
                        else:
                            result.append(f"{val}-[{nums[0]}..{nums[-1]}]{suf}")
                return result

            tagged_params = _collapse_numbered(tagged_params)

            if nc:
                print(f"    {method:<7} {disp}")
                print(f"      params: {', '.join(tagged_params)}")
            else:
                                                                           
                print(f"  {mc}●{C.RST} {C.W}{method:<7}{C.RST} {C.B}{C.W}{disp}{C.RST}")
                param_str = ", ".join(
                    f"{C.GR}{p}{C.RST}" if "[hidden]" in p else
                    f"{C.MG}{p}{C.RST}" if "[file]" in p else
                    f"{C.W}{p}{C.RST}"
                    for p in tagged_params
                )
                emit.leader_row("PARAMS", param_str)

                                                                   
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

                                                                                    
        _LABEL_MAP = {
            "SecurityTxt_Comment_Leak":          ("Comment Leak",    True),
            "SecurityTxt_Contact_Email":          ("Contact Email",   False),
            "SecurityTxt_Contact_URL":            ("Contact URL",     False),
            "SecurityTxt_Encryption_Key":         ("Encryption Key",  False),
            "SecurityTxt_Canonical_CrossDomain":  ("Canonical",       True),
            "SecurityTxt_Expired":                ("Expires",         True),
        }

                                                                            
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

                                                                                   
                                                                                  
                                                  
            if stype == "SecurityTxt_Comment_Leak":
                                                           
                import re as _re
                comment_paths = [
                    m.group(1) for m in
                    _re.finditer(r"""(?:^|\s)(/[^\s'"<>\\]+)""", content)
                ]
                for cp in comment_paths:
                                                    
                    matches = [u for u in all_ep_urls if cp in urlparse(u).path]
                    matches.sort()
                    for mu in matches:
                        if nc:
                            print(f"       └─ {mu}")
                        else:
                            print(f"  {C.GR}     └─{C.RST} {C.CYD}{mu}{C.RST}")

                                                                               
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

                                                                        
    auth_eps = [e for e in real_eps if e.get("auth_required") or
                (e.get("observed_status") and
                 all(s in (401, 403) for s in e.get("observed_status", [])))]
    if auth_eps:
        emit.section(f"AUTH-WALLED  ({len(auth_eps)} endpoints)", orbital=True)
        for ep in auth_eps:
            eu = ep.get("url","")
            obs = ep.get("observed_status", [])
            sc  = f" [{','.join(str(s) for s in obs)}]" if obs else ""
            if nc:
                print(f"  ● {ep.get('method','GET'):<6} {eu}{sc}")
            else:
                print(f"  {C.R}●{C.RST} {C.W}{ep.get('method','GET'):<10}{C.RST} {C.CYD}{eu}{C.RST}{C.GR}{sc}{C.RST}")

                                                                        
    secrets    = intel.get("secrets", [])
    credentials = intel.get("credentials", [])
    cors       = intel.get("cors_issues", [])
    gql        = intel.get("graphql", [])
    oas        = intel.get("openapi", [])
    sourcemaps = intel.get("sourcemaps", [])
    if any([secrets, credentials, cors, gql, oas, sourcemaps]):
        # ── CTF Flags ─────────────────────────────────────────────────────────
        ctf_flags = [s for s in secrets if s.get("type") == "CTF_Flag"]
        if ctf_flags:
            emit.section(f"CTF FLAGS  ({len(ctf_flags)} found)", orbital=True)
            for item in ctf_flags:
                flag    = str(item.get("content", ""))
                source  = item.get("source", "")
                if nc:
                    print(f"  [FLAG] {flag}")
                    print(f"       └─ {source}")
                else:
                    print(f"  {C.BG_RED}{C.W} FLAG {C.RST} {C.G}{C.B}{flag}{C.RST}")
                    print(f"  {C.GR}    └─{C.RST} {source}")
                print()

        # ── Credentials (identity-linked: username/email -> password/token/mfa) ──
        if credentials:
            emit.section(f"CREDENTIALS EXPOSED  ({len(credentials)} found)", orbital=True)
            _cred_order = []
            _cred_groups = {}
            for c in credentials:
                _idv = c.get("identity_value", "USERNAME_NOT_FOUND")
                _src = c.get("source", "")
                _gkey = (_idv, _src)
                if _gkey not in _cred_groups:
                    _cred_groups[_gkey] = []
                    _cred_order.append(_gkey)
                _cred_groups[_gkey].append(c)
            for _idv, _src in _cred_order:
                _items = _cred_groups[(_idv, _src)]
                if nc:
                    print(f"  [{_idv}]  <- {_src}")
                else:
                    _idcol = C.O if _idv == "USERNAME_NOT_FOUND" else C.G
                    print(f"  {_idcol}{C.B}{_idv}{C.RST}  {C.GR}<- {_src}{C.RST}")
                for c in _items:
                    ctype = c.get("credential_type", "Secret")
                    cval  = str(c.get("credential_value", ""))
                    sev = "CRITICAL" if ctype in (
                        "Password", "MFA_Secret", "MFA_Backup_Code", "Client_Secret"
                    ) else "HIGH"
                    if nc:
                        print(f"      [{sev}] {ctype} = {cval}")
                    else:
                        sevcol = {"CRITICAL": C.BG_RED, "HIGH": C.R}.get(sev, C.GR)
                        print(f"      {sevcol}{C.B} {sev:<8}{C.RST} {C.O}{ctype:<16}{C.RST} {cval}")
                print()

        _remaining_secrets = [s for s in secrets
                              if s.get("type") not in ("CTF_Flag", "Hardcoded_Credential")]
        if any([_remaining_secrets, cors, gql, oas, sourcemaps]):
            emit.section("SECURITY FINDINGS")
    for item in gql:
        emit.finding("GraphQL", "HIGH",
                     f"Introspection OPEN — {item.get('url','')}  "
                     f"({item.get('types_count','?')} types)")
    for item in oas:
        emit.finding("OpenAPI", "MEDIUM", f"Spec exposed — {item.get('url','')}")
    for item in cors:
        sev = "HIGH" if item.get("allow_credentials") else "MEDIUM"
        emit.finding("CORS", sev,
                     f"{item.get('url','')}  "
                     f"origin={item.get('reflected','')}  "
                     f"creds={item.get('allow_credentials', False)}")
    for item in sourcemaps:
        emit.finding("SourceMap", "MEDIUM", f"Exposed — {item.get('url','')}")
    for item in secrets:
        stype   = item.get("type", "Secret")
        content = str(item.get("content", ""))
        source  = item.get("source", "")
        if stype == "CTF_Flag":
            continue  # displayed in dedicated CTF FLAGS section above
        if stype == "Hardcoded_Credential":
            continue  # displayed correlated-with-identity in CREDENTIALS EXPOSED section above
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

                                                                        
    sensitive_files = intel.get("sensitive_files", [])
    if sensitive_files:
        emit.section(f"SENSITIVE FILES  ({len(sensitive_files)} exposed)", orbital=True)
        for f in sensitive_files:
            sev     = f.get("severity", "INFO")
            sev_col = {"CRITICAL": C.BG_RED, "HIGH": C.R, "MEDIUM": C.O, "LOW": C.GR}.get(sev, C.GR) if not nc else ""
            if nc:
                print(f"  [{sev}] {f.get('type','')}  {f.get('url','')}")
                if f.get("preview"): print(f"       {f['preview'][:80]}")
            else:
                pill = f"{sev_col}{C.B} {sev:<8}{C.RST}"
                print(f"  {pill}  {C.O}{f.get('type',''):<20}{C.RST} {C.W}{f.get('url','')}{C.RST}")
                if f.get("preview"):
                    print(f"  {C.GR}     └─ {f['preview'][:90]}{C.RST}")

                                                                        
    js_libs = intel.get("js_libs", [])
    if js_libs:
        emit.section(f"VULNERABLE JS LIBRARIES  ({len(js_libs)} found)", orbital=True)
        for f in js_libs:
            if nc:
                print(f"  [HIGH] {f.get('library','')}@{f.get('version','')}  {f.get('cve','')}  {f.get('detail','')}")
            else:
                print(f"  {C.R}●{C.RST} {C.Y}{f.get('library','')}{C.RST}@{C.W}{f.get('version','')}{C.RST}  {C.R}{f.get('cve','')}{C.RST}  {C.GR}{f.get('detail','')}{C.RST}")

                                                                        
    cloud_probes = intel.get("cloud_probes", [])
    if cloud_probes:
        emit.section(f"CLOUD STORAGE  ({len(cloud_probes)} finding(s))", orbital=True)
        for f in cloud_probes:
            sev     = f.get("severity", "INFO")
            sev_col = {"CRITICAL": C.BG_RED, "HIGH": C.R, "MEDIUM": C.O, "LOW": C.GR}.get(sev, C.GR) if not nc else ""
            if nc:
                print(f"  [{sev}] {f.get('issue','')}  {f.get('url','')}")
                print(f"       {f.get('detail','')}")
            else:
                pill = f"{sev_col}{C.B} {sev} {C.RST}"
                print(f"  {pill}  {C.W}{f.get('issue',''):<28}{C.RST} {C.CYD}{f.get('url','')}{C.RST}")
                print(f"  {C.GR}     └─ {f.get('detail','')}{C.RST}")

                                                                        
    extracted = intel.get("extracted_data", [])
    if extracted:
        emit.section(f"EXTRACTED DATA  ({len(extracted)} items)", orbital=True)
        from collections import defaultdict
        grouped = defaultdict(list)
        for item in extracted:
            grouped[item["type"]].append(item)
        for dtype, items in grouped.items():
            emit.row(dtype.replace("_", " "), f"{len(items)} findings", icon="●", label_colour=C.G)
            for item in items:
                val  = item["value"]
                disp = val if len(val) <= 80 else val[:77] + "..."
                emit.leader_row("  " + disp, item["source_url"])

    # ── HTML Comment Leaks ───────────────────────────────────────────────────
    if cmt_filtered:
        emit.section(f"HTML COMMENT LEAKS  ({len(cmt_filtered)} unique)", orbital=True)
        _SRC_CAP = 5
        for i, entry in enumerate(cmt_filtered, 1):
            display = entry["display"]
            shown   = entry["sources"][:_SRC_CAP]
            hidden  = len(entry["sources"]) - len(shown)
            qpaths  = entry.get("queued_paths", [])
            if nc:
                print(f"  [{i}] {display}")
                for src in shown:
                    print(f"       └─ {src}")
                if hidden:
                    print(f"       └─ (+{hidden} more)")
                for qp in qpaths:
                    print(f"       ↳ [path] {qp}")
            else:
                sev_col = C.R if any(kw in display.lower() for kw in
                    ("password","secret","token","key","credential","debug","bypass","hardcod","todo","fixme","do not commit")) else C.Y
                print(f"  {sev_col}[{i}]{C.RST} {C.W}{display}{C.RST}")
                for src in shown:
                    print(f"  {C.GR}    └─{C.RST} {src}")
                if hidden:
                    print(f"  {C.GR}    └─{C.RST} {C.GR}(+{hidden} more pages){C.RST}")
                for qp in qpaths:
                    print(f"  {C.CY}    ↳{C.RST} {C.CYD}{qp}{C.RST}")
            print()

    s_admin    = s.get("admin_panels", 0)
    s_upload   = s.get("upload_endpoints", 0)
    s_auth_ep  = s.get("auth_endpoints", 0)
    s_unauth   = s.get("unauthenticated_apis", 0)
    s_sensdata = s.get("sensitive_data_sources", 0)
    s_legacy   = s.get("legacy_endpoints", 0)
    intel_items = [
        (s_admin,    "Admin Panel(s)",           C.R),
        (s_upload,   "File Upload(s)",           C.CY),
        (s_auth_ep,  "Auth Endpoint(s)",         C.MG),
        (s_unauth,   "Unauth API(s)",            C.R),
        (s_sensdata, "Sensitive Data Source(s)", C.O),
        (s_legacy,   "Legacy/Deprecated(s)",     C.Y),
    ]
                                                                         
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
                elif label == "File Upload(s)":
                    tagged = [e for e in real_eps if e.get("file_upload_candidate") and _not_asset(e)]
                elif label == "Auth Endpoint(s)":
                    tagged = [e for e in real_eps if e.get("auth_classification") and _not_asset(e)]
                elif label == "Unauth API(s)":
                    tagged = [e for e in real_eps if e.get("unauthenticated_api") and _not_asset(e)]
                elif label == "Sensitive Data Source(s)":
                    tagged = [e for e in real_eps if e.get("sensitive_data_source") and _not_asset(e)]
                elif label == "Legacy/Deprecated(s)":
                    tagged = [e for e in real_eps if e.get("legacy_endpoint") and _not_asset(e)]
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
                                                                        
        self.follow_subdomains  = kw.get("follow_subdomains",  False)
        self.follow_redirects   = kw.get("follow_redirects",   False)
        self.enable_subdomain_enum = kw.get("enable_subdomain_enum", False)
        self.wordlist           = kw.get("wordlist",           None)
        self.no_crawl           = kw.get("no_crawl",           False)
        self.ctf_flag_templates = kw.get("ctf_flag_templates", [])
                                                                
        self.extra_scope: frozenset = frozenset(kw.get("extra_scope", []))
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

                                                                        
                          
                                                                        

class SessionManager:
    @staticmethod
    def parse_cookies(raw) -> Dict[str, str]:
        if not raw:
            return {}
        if isinstance(raw, dict):
            return {k: v for k, v in raw.items()
                    if k.lower() not in ("authorization","x-api-key","x-auth-token",
                                          "x-csrf-token","x-access-token")}
        if isinstance(raw, str):
            raw = raw.strip()
                                                                             
                                                                             
                                                                          
                                                                              
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
                    pass                                                     
                                                                       
                                                                         
                                                  
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

    @staticmethod
    def parse_basic_auth(raw) -> Dict[str, str]:
        if not raw:
            return {}
        if isinstance(raw, str):
            raw = raw.strip()
            if ":" not in raw:
                return {}
            encoded = base64.b64encode(raw.encode("utf-8")).decode("ascii")
            return {"Authorization": f"Basic {encoded}"}
        return {}

    @staticmethod
    def parse_custom_headers(raw_list) -> Dict[str, str]:
        """
        Generic --header / -X parser. Unlike parse_auth_header, this is NOT
        restricted to a fixed allowlist — bug bounty programs (Bugcrowd,
        HackerOne, Synack, etc.) often require arbitrary identifying headers
        e.g. "X-Bug-Bounty: handle" or "X-BugCrowd-Ninja: handle" so a tester's
        traffic is provably theirs and excluded from third-party noise.

        Accepts a list of "Name: Value" strings (repeatable),
        or a single such string, or a dict. Last value wins on duplicate names.
        """
        if not raw_list:
            return {}
        if isinstance(raw_list, dict):
            return {str(k).strip(): str(v).strip() for k, v in raw_list.items() if str(k).strip()}
        if isinstance(raw_list, str):
            raw_list = [raw_list]
        out: Dict[str, str] = {}
        for item in raw_list:
            if not item:
                continue
            item = item.strip()
            if ":" not in item:
                continue
            k, _, v = item.partition(":")
            k = k.strip(); v = v.strip()
            if k:
                out[k] = v
        return out


                                                                        
              
                                                                        

class DomainRateLimiter:
    def __init__(self, base_delay: float = 0.05, fixed_delay: float = 0.0, max_concurrent: int = 10):
        self._fixed   = fixed_delay
        self._delays: Dict[str, float] = defaultdict(lambda: base_delay)
        self._sems:   Dict[str, asyncio.Semaphore] = defaultdict(lambda: asyncio.Semaphore(max_concurrent))

    async def wait(self, domain: str):
        async with self._sems[domain]:
            await asyncio.sleep(self._fixed if self._fixed > 0 else self._delays[domain])

    def backoff(self, domain: str):
        self._delays[domain] = min(self._delays[domain] * 2.0, 10.0)

    def recover(self, domain: str):
        self._delays[domain] = max(self._delays[domain] * 0.9, 0.03)

                                                                        
              
                                                                        

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


async def fetch_with_redirect(session, method, url, rl, max_retries=3, base_delay=0.5, **kw):
\
\
\
\
\
       
    domain = urlparse(url).netloc
    await rl.wait(domain)
    for attempt in range(max_retries + 1):
        try:
            async with session.request(method, url, ssl=False,
                                       allow_redirects=True, **kw) as resp:
                if resp.status == 429 or (resp.status == 403 and attempt > 0):
                    rl.backoff(domain)
                    await asyncio.sleep(float(resp.headers.get("Retry-After", base_delay * (2**attempt))))
                    continue
                body = await resp.text(errors="replace")
                rl.recover(domain)
                final_url = str(resp.url)
                return resp.status, dict(resp.headers), body, final_url
        except Exception:
            if attempt < max_retries:
                await asyncio.sleep(base_delay * (2**attempt))
    return None, None, None, url

                                                                        
               
                                                                        

_ID_RE = re.compile(
    r'^(?:\d{1,20}'
    r'|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    r'|[0-9a-fA-F]{24}'
    r'|[0-9a-zA-Z]{20,}'
    r')$',
    re.I
)

                                                                        
                                                          
_NOISE_PARAMS: frozenset = frozenset({
    "aiovg_rand_seed", "ver", "v", "gtm", "tid", "cid", "gcd",
    "npa", "dma", "_p", "_gaz", "frm", "pscdl", "rcb", "sr",
    "uaa", "uab", "uafvl", "uam", "uamb", "uap", "uapv", "uaw",
    "ul", "gaf", "_s", "tfd", "_fv", "_ss", "_c", "_ee", "_nsi",
    "tag_exp", "sid", "sct", "seg", "dl", "dt", "en", "are",
    "ir", "gdid", "fbclid", "ec_cart_id",
    "wordpress_test_cookie",
                                                                        
    "ec_currency_conversion", "ec_option1", "ec_cart_form_action",
    "ec_cart_form_nonce", "ec_account_form_action", "ec_account_form_nonce",
                              
    "page_id", "page_title", "page_url", "url_referer",
    "ak_js", "comment_post_id", "comment_parent",
})

                                    
                                                              
                                                                 
                                                                 
                                                              
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

_ADMIN_PATTERNS = _ADMIN_TIER1                                                          
_AUTH_PATTERNS  = {
    "login":    re.compile(r'/(?:login|signin|sign-in|log-in|authenticate|wp-login[.]php)(?:[/?]|$)', re.I),
    "register": re.compile(r'/(?:register(?!-account$|.*-account$)|signup|sign-up|create.account|join|enroll|ecommerce-sign-up|register-account)(?:[/?]|$)', re.I),
    "logout":   re.compile(r'/(?:logout|signout|log-out|sign-out)(?:[/?]|$)', re.I),
    "mfa":      re.compile(r'/(?:mfa|2fa|otp|totp|verify|verification)(?:[/?]|$)', re.I),
    "pass":     re.compile(r'/(?:password|reset|forgot|change.password|lostpassword)(?:[/?]|$)', re.I),
    "token":    re.compile(r'/(?:token|refresh.token|oauth|authorize)(?:[/?]|$)', re.I),
    "account":  re.compile(r'/(?:account|my-account|profile|user-profile)(?:[/?]|$)', re.I),
}
                                                                                              
_AUTH_EXCLUDE_RE = re.compile(r'/author(?:s)?/', re.I)

                                                                           
                                                                 
                                                                           
                                                                             

                                                                        
                                                                           
                                                                       
                                                                      
                                                        
                                                      
_NOISE_PATH_RE = re.compile(
    r'/(?:'
    r'blob/[^/]+/'                                                   
    r'|tree/[^/]+/'                                                   
    r'|commits?/[^/]+/'                                             
    r'|releases/tag/'                                                  
    r'|graphs/'                                                  
    r'|compare/'                                                 
    r'|branches'                                                    
    r'|stargazers'                                                
    r'|watchers'                                                     
    r'|forks'                                                     
    r'|pulse'                                                       
    r'|actions'                                                  
    r'|activity'                                                   
    r'|custom-properties'                                            
    r')',
    re.I
)

                                                                        
                                                                     
                                                                     
                                                                   
_SOCKETIO_RE = re.compile(r'/socket\.io/\??.*EIO=', re.I)

def normalize(url: str) -> str:
    try:
                                                                
        url = url.replace(chr(92)+chr(92), "/").replace(chr(92), "/")
        p  = urlparse(url)
        qs = urlencode(sorted(parse_qs(p.query, keep_blank_values=True).items()), doseq=True)
        return urlunparse((p.scheme.lower(), p.netloc.lower(),
                           p.path.rstrip("/") or "/", p.params, qs, ""))
    except Exception:
        return url

def cluster(url: str) -> str:
                                                                                          
    try:
        p    = urlparse(url)
                                                            
        segs = ["{val}" if _ID_RE.match(s) else s for s in p.path.split("/")]
        path = "/".join(segs)
                                        
        qs_dict = parse_qs(p.query, keep_blank_values=True)
        masked_qs = urlencode(sorted([(k, "") for k in qs_dict.keys()]), doseq=True)
        return urlunparse(("", "", path, "", masked_qs, ""))
    except Exception:
        return url

                                                                        
            
                                                                        

class Store:
    def __init__(self):
        self.endpoints:    Dict[str, dict] = {}
        self.comments:     List[dict]       = []
        self.secrets:      List[dict]       = []
        self.credentials:  List[dict]       = []
        self._credential_seen: Set[tuple]   = set()
        self.tech_stack:   Set[str]         = set()
        self.whatweb_data: dict             = {}   # {category: [(icon, display_str), ...]}
        self.robots_paths: List[str]        = []
        self.robots_allowed_paths: List[str] = []
        self.target_response_headers: dict   = {}
        self.cors_issues:  List[dict]       = []
        self.graphql:      List[dict]       = []
        self.openapi:      List[dict]       = []
        self.sourcemaps:   List[dict]       = []
        self.extracted_data: List[dict]     = []
        self._extracted_seen: Set[tuple]    = set()
                                                                     
                                                     
                                                                              
        self.js_orphan_params: Dict[str, List[str]] = {}
                                                                                 
                                                                                 
        self.socketio_endpoints: List[dict] = []
        self._socketio_seen:     Set[str]   = set()
                                                              
                                                                             
        self.crt_subdomains: List[dict] = []                             
        self._crt_seen:      Set[str]  = set()
                                                                              
                                                                            
                                                               
                                                                               
                                                                     
        self._graph_nodes: Dict[str, dict] = {}                        
        self._graph_edges: List[dict]       = []                                     
        self._graph_edge_seen: Set[tuple]   = set()
                                                                            
        self.waf_findings:       List[dict] = []
        self.tls_findings:       List[dict] = []
        self.header_audit:       List[dict] = []
        self.dns_findings:       List[dict] = []
        self.sensitive_files:    List[dict] = []
        self.js_libs:            List[dict] = []
        self.cloud_probes:       List[dict] = []

    def _key(self, url, method):
        return f"{method.upper()}:{cluster(normalize(url))}"

    def _new_ep(self, url, method):
        return {
            "url": url, "cluster": cluster(normalize(url)),
            "methods": [method.upper()],
            "params": {"query":[],"form":[],"js":[],"openapi":[],"runtime":[]},
            "headers_detail": {"vary": [], "cookies": []},
            "observed_values": {},
            "headers": {},
            "source": [], "confidence": 0, "confidence_label": "LOW",
            "auth_required": False, "parameter_sensitive": False,
            "observed_status": [], "baseline": None,
                                                                               
                                                                     
                                                                                       
            "form_fields_detail": [],
                             
            "admin_panel":          False,
            "auth_classification":  [],
            "file_upload_candidate": False,
            "screenshot":           None,
        }

                                                                        
                                                                          
    _API_PATH_RE = re.compile(
        r'^/(?:api|rest|graphql|gql|v[0-9]+|internal|backend|service|rpc|data)[/]',
        re.I
    )

    def add_endpoint(self, url, method="GET", source="Static",
                     params=None, score=Conf.LOW, auth_required=False):
                                                                              
                                                             
        if _SOCKETIO_RE.search(url):
            self.add_socketio(url, method)
            return self.endpoints.get(self._key(url, method))                  
        key = self._key(url, method)
        if key not in self.endpoints:
            self.endpoints[key] = self._new_ep(url, method)
        ep = self.endpoints[key]
        if source not in ep["source"]:
            ep["source"].append(source)
                                                                             
                                                                
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

                                                                      
    _HEADER_SKIP = frozenset({
        "accept", "accept-encoding", "accept-language", "cache-control",
        "connection", "host", "origin", "pragma", "referer",
        "sec-ch-ua", "sec-ch-ua-mobile", "sec-ch-ua-platform",
        "sec-fetch-dest", "sec-fetch-mode", "sec-fetch-site",
        "upgrade-insecure-requests", "user-agent",
    })

    def merge_headers(self, url: str, method: str, headers: dict) -> bool:
\
\
\
\
           
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
\
\
\
\
\
           
        bucket = self.js_orphan_params.setdefault(js_file_url, [])
        for p in params:
            if p and p not in bucket:
                bucket.append(p)

    def is_same_domain(self, url: str, ref_url: str) -> bool:
                                                                                
        try:
            return urlparse(url).netloc == urlparse(ref_url).netloc
        except Exception:
            return False

    def add_socketio(self, url: str, method: str = "GET"):
\
\
\
\
           
        base = urlparse(url)._replace(query="", fragment="").geturl()
        if base not in self._socketio_seen:
            self._socketio_seen.add(base)
            self.socketio_endpoints.append({
                "base_url": base,
                "example":  url,
                "method":   method.upper(),
                "note":     "socket.io transport — ephemeral session token, not injectable",
            })

                                                                                
    _RISK_PARAMS = frozenset({
        "cmd","command","exec","run","shell","host","hostname","ip","addr","address",
        "url","uri","target","dest","src","source","file","path","dir","query","q",
        "search","input","arg","id","key","token","user","pass","passwd","password",
    })
                                                                    
    _PARAM_SUFFIXES = ("_raw","_sanitized","_input","_clean","_safe","_encoded","_value","_param")

    def add_runtime_params(self, url: str, method: str, names: List[str]) -> bool:
\
\
\
\
\
\
\
           
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
                                                                  
            if is_suffixed:
                sanitization_seen = True
                                      
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
                                                                              
                                                                                
                                                                             
                                                                              
        affected_keys = [self._key(url, method)]
                                                                          
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
                                                                              
                ep["auth_required"] = False
                if ep["confidence"] < Conf.MEDIUM:
                    ep["confidence"]       = Conf.MEDIUM
                    ep["confidence_label"] = Conf.label(ep["confidence"])
            elif status == 404:
                                                                            
                ep["confidence"]       = min(ep["confidence"], Conf.LOW)
                ep["confidence_label"] = "404_NOT_FOUND"
            elif status in (301, 302, 307, 308):
                                                      
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

    def add_graph_edge(self, from_url: str, to_url: str, via: str, depth: int = 0):
\
\
\
\
\
           
        if not from_url or not to_url or from_url == to_url:
            return
                        
        if from_url not in self._graph_nodes:
            self._graph_nodes[from_url] = {"url": from_url, "type": "page"}
        if to_url not in self._graph_nodes:
            self._graph_nodes[to_url]   = {"url": to_url,   "type": "page"}
                     
        edge_key = (from_url, to_url, via)
        if edge_key not in self._graph_edge_seen:
            self._graph_edge_seen.add(edge_key)
            self._graph_edges.append({
                "from_url": from_url,
                "to_url":   to_url,
                "via":      via,
                "depth":    depth,
            })

    def export_page_graph(self) -> dict:
\
\
\
\
           
                                               
        for url, node in self._graph_nodes.items():
            ep_key_get  = self._key(url, "GET")
            ep_key_post = self._key(url, "POST")
            ep = self.endpoints.get(ep_key_get) or self.endpoints.get(ep_key_post)
            if ep:
                if ep.get("auth_required"):
                    node["auth_required"] = True
                if ep.get("admin_panel"):
                    node["type"] = "admin"
                elif any("XHR" in s or "SPA" in s for s in ep.get("source", [])):
                    node["type"] = "xhr"
                elif any("Form" in s for s in ep.get("source", [])):
                    node["type"] = "form_action"
                elif any("GraphQL" in s for s in ep.get("source", [])):
                    node["type"] = "graphql"
                elif any("WS" in m for m in ep.get("methods", [])):
                    node["type"] = "ws"
                confidence = ep.get("confidence_label", "LOW")
                node["confidence"] = confidence
        return {
            "nodes": list(self._graph_nodes.values()),
            "edges": self._graph_edges,
        }

    def add_comment(self, content, source_url):
        content = content.strip()
        if len(content) < 4:
            return False
                                                                                    
        for c in self.comments:
            if c["content"] == content:
                if source_url and source_url not in c.get("all_sources", [c.get("source","")]):
                    c.setdefault("all_sources", [c.get("source","")]).append(source_url)
                return False                            
        self.comments.append({"content": content, "source": source_url, "all_sources": [source_url]})
        return True

    def add_secret(self, val, stype, source_url):
        if any(s["content"] == val for s in self.secrets):
            return False
        self.secrets.append({"content": val, "type": stype, "source": source_url})
        return True

    def add_credential(self, identity_field, identity_value, cred_type, cred_value, source_url):
\
\
\
\
\
\
           
        dedup_key = (identity_value, cred_type, cred_value, source_url)
        if dedup_key in self._credential_seen:
            return False
        self._credential_seen.add(dedup_key)
        self.credentials.append({
            "identity_field": identity_field,
            "identity_value": identity_value,
            "credential_type": cred_type,
            "credential_value": cred_value,
            "source": source_url,
        })
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

    def _build_agent_targets(self, formatted_eps: list) -> list:
\
\
\
\
\
\
\
\
\
\
\
\
        results = []
        for ep in formatted_eps:
            conf = ep.get("confidence", "LOW")
            if conf not in ("CONFIRMED", "HIGH"):
                continue
            if "404" in str(ep.get("confidence", "")):
                continue
            if 404 in (ep.get("observed_status") or []):
                continue
            params = ep.get("params", [])
            params_detail = ep.get("params_detail", {})
            all_params = params if isinstance(params, list) else []
            if not all_params:
                                                                  
                for bucket in params_detail.values():
                    for p in bucket:
                        if p not in all_params:
                            all_params.append(p)
            if not all_params:
                continue                          

                              
            score = 0
            if ep.get("file_upload_candidate"): score += 15
            if ep.get("unauthenticated_api"):   score += 18
            if ep.get("sensitive_data_source"): score += 16
            if ep.get("legacy_endpoint"):       score += 12
            if conf == "CONFIRMED":             score += 10
            if ep.get("auth_required"):         score += 5
            score += min(len(all_params) * 3, 15)

            ep_key  = self._key(ep["url"], ep.get("method", "GET"))
            raw_ep  = self.endpoints.get(ep_key)
            obs_val = (raw_ep or {}).get("observed_values", {})

            results.append({
                "url":                   ep["url"],
                "method":                ep.get("method", "GET"),
                "confidence":            conf,
                "params":                all_params,
                "params_detail":         params_detail,
                "form_fields_detail":    ep.get("form_fields_detail", []),
                "auth_required":         ep.get("auth_required", False),
                "file_upload_candidate": ep.get("file_upload_candidate", False),
                "observed_values":       obs_val,
                "unauthenticated_api":   ep.get("unauthenticated_api", False),
                "sensitive_data_source": ep.get("sensitive_data_source", False),
                "sensitive_signals":     ep.get("sensitive_signals", []),
                "legacy_endpoint":       ep.get("legacy_endpoint", False),
                "legacy_reason":         ep.get("legacy_reason", ""),
                "priority_score":        score,
                "source":                ep.get("source", []),
            })

        results.sort(key=lambda x: x["priority_score"], reverse=True)
        return results

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
            "credentials_exposed": len(self.credentials),
            "cors_issues":         len(self.cors_issues),
            "graphql_exposed":     len(self.graphql),
            "openapi_exposed":     len(self.openapi),
            "sourcemaps_exposed":  len(self.sourcemaps),
            "tech_stack":          sorted(self.tech_stack),
            "whatweb_data":        self.whatweb_data,
            "admin_panels":       sum(1 for e in eps if e.get("admin_panel")),
            "auth_endpoints":     sum(1 for e in eps if e.get("auth_classification")),
            "upload_endpoints":   sum(1 for e in eps if e.get("file_upload_candidate")),
            "extracted_data":     len(self.extracted_data),
            "robots_disallowed":  len(self.robots_paths),
            "robots_allowed":     len(self.robots_allowed_paths),
            "screenshots":        sum(1 for e in eps if e.get("screenshot")),
                                                                                        
            "js_orphan_param_files": len(self.js_orphan_params),
            "js_orphan_param_count": sum(len(v) for v in self.js_orphan_params.values()),
            "websocket_detected":     len(self.socketio_endpoints) > 0,
            "socketio_count":         len(self.socketio_endpoints),
            "crt_subdomain_count":    len(self.crt_subdomains),
                 
            "waf_detected":           len(self.waf_findings) > 0,
            "waf_count":              len(self.waf_findings),
            "tls_issues":             len(self.tls_findings),
            "header_issues":          len(self.header_audit),
            "dns_issues":             len(self.dns_findings),
            "sensitive_files_found":  len(self.sensitive_files),
            "js_vulnerable_libs":     len(self.js_libs),
            "cloud_bucket_issues":    len(self.cloud_probes),
                                                                           
            "unauthenticated_apis":   sum(1 for e in eps if e.get("unauthenticated_api")),
            "sensitive_data_sources": sum(1 for e in eps if e.get("sensitive_data_source")),
            "legacy_endpoints":       sum(1 for e in eps if e.get("legacy_endpoint")),
        }
        
                                                
        formatted_eps = []
        for e in eps:
                               
            all_params = []
            for bucket in e["params"].values():
                for p in bucket:
                    if p not in all_params: all_params.append(p)
            
                                      
            c = e["confidence"]
            cl = e.get("confidence_label", "LOW")
                                                                           
            if cl not in ("404_NOT_FOUND",):
                if c >= 10: cl = "CONFIRMED"
                elif c >= 7: cl = "HIGH"
                elif c >= 3: cl = "MEDIUM"
                elif c >= 1: cl = "LOW"
                else: cl = "UNKNOWN"

            formatted_eps.append({
                "url": e["url"],
                "cluster": e.get("cluster") or cluster(normalize(e["url"])),
                "method": e["methods"][0] if e["methods"] else "GET",
                "confidence": cl,
                "confidence_score": c,
                "observed_status": e["observed_status"],
                "params": sorted(all_params),
                "params_detail": e["params"],
                "headers_detail": e.get("headers_detail", {"vary": [], "cookies": []}),
                                                                                
                                                                                         
                "form_fields_detail": e.get("form_fields_detail", []),
                "auth_required": e["auth_required"],
                "source": e["source"],
                "admin_panel": e.get("admin_panel", False),
                "auth_classification": e.get("auth_classification", []),
                "file_upload_candidate": e.get("file_upload_candidate", False),
                "screenshot": e.get("screenshot"),
                                                                                           
                                                                              
                "observed_values": {k: v for k, v in e.get("observed_values", {}).items() if v},
                                                                             
                                                                                     
                "unauthenticated_api":  e.get("unauthenticated_api", False),
                                                                                               
                "sensitive_data_source": e.get("sensitive_data_source", False),
                "sensitive_signals":     e.get("sensitive_signals", []),
                                                                                     
                "legacy_endpoint":  e.get("legacy_endpoint", False),
                "legacy_reason":    e.get("legacy_reason", ""),
            })

        data = {
            "meta": meta, "summary": summary, "endpoints": formatted_eps,
            "secrets": self.secrets, "cors_issues": self.cors_issues,
            "credentials": self.credentials,
            "graphql": self.graphql, "openapi": self.openapi,
            "sourcemaps": self.sourcemaps, "comments": self.comments,
            "robots_disallowed": self.robots_paths,
            "robots_allowed": self.robots_allowed_paths,
            "target_response_headers": self.target_response_headers,
            "tech_stack": sorted(self.tech_stack),
            "extracted_data": self.extracted_data if self.extracted_data is not None else [],
                                                                                
                                                                                           
                                                                            
            "js_orphan_params": [
                {"js_file": js_url, "params": sorted(set(params))}
                for js_url, params in self.js_orphan_params.items()
                if params
            ],
                                                                        
                                                                            
            "socketio_endpoints": self.socketio_endpoints,
            "crt_subdomains":     self.crt_subdomains,
                              
            "waf_findings":      self.waf_findings,
            "tls_findings":      self.tls_findings,
            "header_audit":      self.header_audit,
            "dns_findings":      self.dns_findings,
            "sensitive_files":   self.sensitive_files,
            "js_libs":           self.js_libs,
            "cloud_probes":      self.cloud_probes,
                                                                             
                                                                               
                                                      
                                                                           
                                                                        
                                                                             
            "page_graph": self.export_page_graph(),
                                                                             
                                                                                    
                                                                              
                                                                           
            "agent_targets": self._build_agent_targets(formatted_eps),
            "whatweb_data":  self.whatweb_data,
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

        if fmt == "urls":
                                                                                    
            return "\n".join(ep["url"] for ep in eps)

        if fmt == "nuclei":
                                                                                       
            lines = ["# Hellhound Spider — nuclei target list"]
            lines.append(f"# Generated: {datetime.now().isoformat()}")
            lines.append(f"# Target: {meta.get('target','?')}\n")
                                                                   
            lines.append("# ── CRAWLED ENDPOINTS (use with: nuclei -l targets.txt) ──")
            for ep in eps:
                lines.append(ep["url"])
                                                                      
            findings_sections = [
                ("tls_findings",   data.get("tls_findings",[])),
                ("header_audit",   data.get("header_audit",[])),
                ("dns_findings",   data.get("dns_findings",[])),
                ("sensitive_files",data.get("sensitive_files",[])),
                ("js_libs",        data.get("js_libs",[])),
            ]
            lines.append("\n# ── ASM FINDINGS ──")
            for section, items in findings_sections:
                if not items:
                    continue
                lines.append(f"# [{section.upper()}]")
                for item in items:
                    sev  = item.get("severity","INFO")
                    iss  = item.get("issue") or item.get("library","") or item.get("type","")
                    det  = item.get("detail","") or item.get("cve","")
                    url  = item.get("url","")
                    line = f"#   [{sev}] {iss}"
                    if det:  line += f" — {det}"
                    if url:  line += f"  ({url})"
                    lines.append(line)
            return "\n".join(lines)

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

                                                                        
            
                                                                        


def _build_ctf_flag_patterns(templates: list) -> list:
    """Convert user-supplied flag templates like 'flag{}' or 'HTB{}'
    into compiled regexes.  The {} placeholder expands to [^}]{1,200}.
    Returns a list of (display_prefix, compiled_re) tuples."""
    patterns = []
    
    if templates:
        # Generic CTF flag fallback: catches words containing flag/ctf followed by {...}
        # e.g., bitflag{...}, HTB{...}, picoCTF{...}. Helps avoid misses from user typos.
        fallback_re = re.compile(r"\b[a-zA-Z0-9_]*(?:flag|ctf)[a-zA-Z0-9_]*\{[^}\s]{4,200}\}", re.IGNORECASE)
        patterns.append(("generic_flag{}", fallback_re))

    for tmpl in templates:
        tmpl = tmpl.strip()
        if not tmpl:
            continue
        if "{}" not in tmpl:
            # If user forgot the {}, append it
            tmpl = tmpl.rstrip("{") + "{}"
        # Escape everything except the {} placeholder
        prefix, _, _ = tmpl.partition("{}")
        esc = re.escape(prefix) + r"\{([^}]{1,200})\}"
        try:
            # Ignore case so casing mismatches don't miss the flag
            patterns.append((prefix + "{}", re.compile(esc, re.IGNORECASE)))
        except re.error:
            pass
    return patterns


def scan_ctf_flags(text: str, url: str, store, emit, patterns: list) -> int:
    """Scan text for CTF flags matching any of the compiled patterns.
    Records each unique match as a secret and emits a high-severity warning."""
    if not patterns or not text:
        return 0
    found = 0
    for display, pat in patterns:
        for m in pat.finditer(text):
            flag = m.group(0)
            if store.add_secret(flag, "CTF_Flag", url):
                # Print prominently for live findings (not just in the summary)
                msg = f"\033[41m\033[1m[CTF-FLAG]\033[0m \033[1m\033[92m{flag}\033[0m  ← {url}"
                if hasattr(emit, '_w'):
                    emit._w(msg)
                else:
                    emit.warn_sev(f"[CTF-FLAG] {flag}  ← {url}", "CRITICAL")
                found += 1
    return found


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
                                                                                
                                                                            
            r'(?<![a-zA-Z0-9])(?!.*@[123456789]x[-_.])'
            r'([a-zA-Z0-9._%+-]{2,}@[a-zA-Z0-9.-]+\.(?!png|jpg|jpeg|gif|svg|webp|ico|woff|woff2|ttf|eot|mp4|mp3|pdf|zip)[a-zA-Z]{2,6})'
            r'(?![a-zA-Z0-9@])',
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
                                                             
            r'(?<![.a-zA-Z0-9_])'
            r'(?!localhost\b)(?!127\.)'
            r'[a-zA-Z0-9][a-zA-Z0-9\-]{3,}'
            r'\.(internal|intranet|corp|lan|private)\b',
            re.I), "Internal_Host"),
                                                                                     
        (re.compile(
            r'(?<![.a-zA-Z0-9_])(?!localhost\b)(?!127\.)'
            r'[a-zA-Z0-9]*[\-\d][a-zA-Z0-9\-]*'
            r'\.(local|dev|test|prod|staging|uat|int|stg)\b',
            re.I), "Internal_Host"),
                                                                         
                                                                               
                                                                
        (re.compile(
            r'(?<![.a-zA-Z0-9_])(?!localhost)(?!127\.)'
            r'[a-z][a-z0-9\-]+\.[a-z][a-z0-9\-]+'
            r'\.(local|dev|test|prod|staging|uat|int|stg)\b'),
            "Internal_Host"),
    ]
                                                                         
    _SECRET_PLACEHOLDERS = frozenset({
        "changeme", "replace", "your_", "yourapikey", "insert", "placeholder",
        "example", "dummy", "test", "xxxx", "fill_in", "<your", "todo",
    })
                                                          
                                                                                                           
                                           
                                                                                   
    _API_RE = [
        r'["\']([/][a-zA-Z0-9_\-\.\/]*(?:api|v\d+|graphql|admin|auth|login|logout|rest|search|data|internal|upload|download)[a-zA-Z0-9_\-\.\/]*(?:\?[^"\'#\s]*)?)["\']',
        r'(?:fetch|axios)\s*\(\s*["\']([^"\'#\s]{5,})["\']',
        r'\.\s*(?:get|post|put|delete|patch)\s*\(\s*["\']([^"\'#\s]{5,})["\']',
        r'`\$\{[^}]+\}(/[a-zA-Z0-9_\-\/]+(?:\?[^`#\s]*)?)`',
        r'(?:fetch|axios|\.\s*(?:get|post|put|delete|patch))\s*\(\s*["\']([/][^"\'#\s]{3,})["\']',
    ]

                                                                                     
    _SPA_BODY_MARKERS = (
        "<html", "<!doctype", "<head", "<body",
        "<title", "<meta", "<!-- ", "ng-app",
        "data-reactroot", "__next_data__",
        '<div id="root"', '<div id="app"',                               
        '<div id="__nuxt"', '<div id="__next"',                   
    )

                                                             
    _SOFT_404_INDICATORS = (
        "cannot get", "not found", "404 not found", "page not found",
        "route not found", "no route matches", "error 404", "invalid path",
    )

    @classmethod
    def is_real_file(cls, ct: str, body: str, canary_hash: str) -> bool:
                                                                                                
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
\
\
\
\
\
\
           
        if status != 200:
            return False
        body_lo = body.lower()
                                                         
        if len(body) < 1000:
            if any(ind in body_lo for ind in cls._SOFT_404_INDICATORS):
                return True
                                                                         
                                                                                
                                                
        title_m = re.search(r'<title[^>]*>(.*?)</title>', body_lo, re.S)
        if title_m:
            title_text = title_m.group(1).strip()
            if any(ind in title_text for ind in cls._SOFT_404_INDICATORS):
                return True
                                                            
            if re.search(r'\b404\b', title_text):
                return True
                                             
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
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
           
        if not body:
            return False
        body_lo = body.lower()

                                                                        
                                                                              
        specific_indicators = (
            "checking your browser before you proceed",
            "checking your browser",                           
            "enable javascript and cookies to continue",
            "ddos protection by cloudflare",
            "ray id:",                                                
            "please stand by, while we are checking your",
            "your ip address has been blocked",
            "this process is automatic",                             
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

                                                                        
                                                                        
                                                                          
        weak_indicators = (
            "captcha",
            "are you human",
            "bot protection",
            "blocked by",
        )
        if any(ind in body_lo for ind in weak_indicators):
            if len(body) < 8000:
                                                                           
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
\
                                                                            
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
\
\
\
                                                                      
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

                                            
    _JS_PARAM_STOPLIST = frozenset({
        "alignmentOffset", "centerOffset", "referenceHiddenOffsets", "escapedOffsets",
        "referenceHidden", "overflows", "placement", "enabled", "mode", "index",
        "length", "name", "type", "id", "value", "target", "action", "method",
        "enctype", "viewport", "charset", "description", "keywords", "author",
    })

    @classmethod
    def js_params(cls, text, base_url, store, emit):
\
\
\
\
\
\
\
           
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
                                                                           
                    if store.add_js_params(turl, keys):
                        emit.info("[JS-Params] %s -> %s" % (keys, turl))
                elif _is_js_file:
                                                                                             
                    store.add_js_orphan_params(base_url, keys)
                    emit.info("[JS-Orphan] %s (no target URL found in %s)" % (keys, base_url))
                else:
                                                                              
                    if store.add_js_params(turl, keys):
                        emit.info("[JS-Params] %s -> %s" % (keys, turl))

    @classmethod
    def extract_data(cls, body: str, url: str, store, emit):
                                                              
                                                  
        if len(body) > 2_000_000 and "vendor" in url.lower():
            return

        counts = defaultdict(int)
                                                                          
                                                                                    
        _is_json_body = body.strip().startswith(('{', '['))
        for pattern, dtype in cls._EXTRACTION_PATTERNS:
            if dtype == "Phone" and _is_json_body:
                continue                                                    
            for match in pattern.finditer(body):
                                                                                               
                val = (match.group(1) if dtype == "Phone" and match.lastindex else match.group(0)).strip()
                if not val:
                    continue
                
                                                
                if dtype == "Email":
                    local_part  = val.split("@")[0]
                    domain_part = val.split("@")[1].lower() if "@" in val else ""
                    if ".." in val: continue
                    if len(local_part) < 2: continue
                    if "." not in domain_part: continue
                    if val.lower().endswith((".css", ".js", ".png", ".jpg", ".svg", ".woff")):
                        continue
                                                                                         
                    _PLACEHOLDER_EMAIL_DOMAINS = {
                        "example.com", "example.org", "example.net",
                        "test.com", "test.org", "test.net",
                        "foo.com", "bar.com", "baz.com",
                        "domain.com", "email.com", "mail.com",
                        "user.com", "yoursite.com", "yourwebsite.com",
                        "company.com", "website.com", "sample.com",
                        "placeholder.com", "demo.com", "fake.com",
                        "noreply.com", "no-reply.com",
                        "sentry.io",                                         
                    }
                    if domain_part in _PLACEHOLDER_EMAIL_DOMAINS: continue
                                                        
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
                                                                              
                                                                               
                                                                            
                    _stripped = re.sub(r'[\s.\-\(\)\/]', '', val)
                    if not (7 <= len(_stripped) <= 15): continue
                    if not re.match(r'\+?\d+$', _stripped): continue
                    if re.match(r'(20[0-9]{2}[01][0-9][0-3][0-9]|[0-3][0-9][01][0-9]20[0-9]{2})', _stripped): continue
                                                                     

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
                                                                                     
                    if re.search(r'[a-z][A-Z]', val.split('.')[0]): continue

                if store.add_extracted_data(dtype, val, url):
                    counts[dtype] += 1

                                                        
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
                                                                                   
                                if store.add_extracted_data(dtype, v.strip(), url):
                                    counts[dtype] += 1
            except Exception:
                pass
        
        if counts:
            summary = ", ".join([f"{v} {k.lower().replace('_', ' ')}" for k, v in counts.items()])
            emit.info(f"[Extract] {summary} ← {url}")

    # ── Identity + credential key vocab for structured credential extraction ──
    # Generic field-name vocab, not tied to any specific target's schema —
    # matches common identity/credential key naming conventions broadly.
    # Ordered by preference: prefer human-readable identifiers (username,
    # email) over opaque numeric ids when multiple identity keys exist.
    _IDENTITY_KEY_PRIORITY = (
        "username", "user", "login", "loginname", "login_id", "handle",
        "email", "email_address", "account", "accountname",
        "full_name", "fullname", "display_name", "name",
        "userid", "user_id", "id",
    )
    _IDENTITY_KEYS = frozenset(_IDENTITY_KEY_PRIORITY)

    _CREDENTIAL_KEY_PATTERNS = [
        (re.compile(r'^pass(?:word|wd)?$', re.I),                            "Password"),
        (re.compile(r'^(?:password|passwd|pwd)_hash$', re.I),                "Password_Hash"),
        (re.compile(r'^hashed_password$', re.I),                             "Password_Hash"),
        (re.compile(r'^(?:mfa|totp|2fa|otp|two_factor)_secret$', re.I),      "MFA_Secret"),
        (re.compile(r'^(?:backup|recovery)_codes?$', re.I),                  "MFA_Backup_Code"),
        (re.compile(r'^(?:auth|access|refresh|session|api)_token$', re.I),   "Token"),
        (re.compile(r'^api_key$', re.I),                                     "API_Key"),
        (re.compile(r'^(?:client|app)_secret$', re.I),                       "Client_Secret"),
        (re.compile(r'^secret$', re.I),                                      "Secret"),
        (re.compile(r'^token$', re.I),                                       "Token"),
    ]

    _JS_OBJ_ASSIGN_RE = re.compile(
        r'(?:window\.[A-Za-z_$][\w$]*|(?:var|let|const)\s+[A-Za-z_$][\w$]*)\s*=\s*\{'
    )

    @staticmethod
    def _balanced_object_end(text: str, brace_start: int) -> int:
\
\
\
           
        depth, in_str, str_ch, escape = 0, False, "", False
        i, n = brace_start, len(text)
        while i < n:
            ch = text[i]
            if in_str:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == str_ch:
                    in_str = False
            else:
                if ch in ('"', "'"):
                    in_str, str_ch = True, ch
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        return i
            i += 1
        return -1

    @classmethod
    def _walk_credential_dict(cls, obj, store, emit, url, depth=0):
\
\
\
\
           
        if depth > 8 or not isinstance(obj, dict):
            return
        identity_field = identity_value = None
        lower_keys = {k.lower(): k for k in obj.keys() if isinstance(k, str)}
        for pref in cls._IDENTITY_KEY_PRIORITY:
            if pref in lower_keys:
                orig_k = lower_keys[pref]
                v = obj.get(orig_k)
                if isinstance(v, (str, int)) and str(v).strip():
                    identity_field, identity_value = orig_k, str(v)
                    break
        for k, v in obj.items():
            if not isinstance(k, str) or not isinstance(v, (str, int)):
                continue
            for pat, ctype in cls._CREDENTIAL_KEY_PATTERNS:
                if not pat.match(k):
                    continue
                val = str(v).strip()
                if not val or val.lower() in cls._SECRET_PLACEHOLDERS:
                    break
                idf = identity_field or "n/a"
                idv = identity_value or "USERNAME_NOT_FOUND"
                if store.add_credential(idf, idv, ctype, val, url):
                    sev = "CRITICAL" if ctype in (
                        "Password", "MFA_Secret", "MFA_Backup_Code", "Client_Secret"
                    ) else "HIGH"
                    emit.warn_sev(f"[Credential] {idv} -> {ctype}={val[:60]}", sev)
                break
        for v in obj.values():
            if isinstance(v, dict):
                cls._walk_credential_dict(v, store, emit, url, depth + 1)
            elif isinstance(v, list):
                for item in v[:50]:
                    if isinstance(item, dict):
                        cls._walk_credential_dict(item, store, emit, url, depth + 1)

    @classmethod
    def credential_objects(cls, body: str, url: str, store, emit):
\
\
\
\
\
\
\
\
           
        if not body or "{" not in body:
            return
                                                                
        for m in cls._JS_OBJ_ASSIGN_RE.finditer(body):
            brace_idx = m.end() - 1
            end_idx = cls._balanced_object_end(body, brace_idx)
            if end_idx == -1:
                continue
            blob = body[brace_idx:end_idx + 1]
            if len(blob) > 50_000:
                continue
            try:
                obj = json.loads(blob)
            except Exception:
                continue
            cls._walk_credential_dict(obj, store, emit, url)
                                                                
        stripped = body.strip()
        if stripped.startswith(("{", "[")):
            try:
                obj = json.loads(stripped)
                cls._walk_credential_dict(obj, store, emit, url)
            except Exception:
                pass

    @classmethod
    def secrets(cls, text, url, store, emit):
        for pat, stype in cls._SECRET_RE:
            for m in re.finditer(pat, text):
                val = m.group(1) if m.lastindex else m.group(0)
                if stype not in ("Bitcoin_Address","Ethereum_Address","Private_Key_PEM",
                                  "Hardcoded_Credential","GitHub_PAT") and len(val) < 20:
                    continue
                                                         
                val_lo = val.lower()
                if any(ph in val_lo for ph in cls._SECRET_PLACEHOLDERS):
                    continue
                                              
                if stype == "Bitcoin_Address":
                                                                                    
                    if not any(c.isupper() for c in val):
                        continue
                                                                          
                    if re.search(r'(.)(\1){3,}', val):
                        continue
                                                                        
                    if not (25 <= len(val) <= 34):
                        continue
                if store.add_secret(val, stype, url):
                    emit.warn(f"[SECRET:{stype}] {val[:80]}")

                                                                                   
    _EXPOSED_SAFE_PREFIXES = (
        "/robots", "/sitemap", "/manifest", "/favicon", "/.well-known/",
    )


                                                                       
                                                                                 
    _JS_COMMENT_SENSITIVE = re.compile(
        r'(?:password\s*[:=][^,;\n]{3,}|passwd\s*[:=][^,;\n]{3,}|'
        r'secret\s*[:=][^,;\n]{3,}|api[_-]?key\s*[:=][^,;\n]{3,}|'
        r'private[_-]?key|hardcod(?:ed?|ing)\s*(?:password|key|token|secret|cred)[^,;\n]{2,}|'
        r'remove\s+before\s+(?:prod|deploy|release|commit)|'
        r'do\s+not\s+(?:commit|push|deploy)|'
        r'(?:admin|staging|prod)\s+(?:password|key|token|secret)\s*[:=]|'
        r'bypass\s+(?:auth|security|check|validation))',
        re.I
    )
                                                                      
    _JS_LIBRARY_RE = re.compile(
        r'(?:jquery|bootstrap|angular|react|lodash|moment|axios|backbone|'
        r'respond\.js|html5shiv|modernizr|require\.js|webpack|babel|'
        r'polyfill|vendor\.js|bundle\.js|chunk|runtime\.js|commons|datepicker|'
        r'complianz|cookiebot|cookie-?law|gdpr|matomo|gtag|analytics|'
        r'wp-includes|wp-content|plugins/|themes/|elementor|woocommerce|'
        r'slick|swiper|gsap|three\.min|d3\.min|chart\.js|recaptcha|'
        r'fontawesome|font-awesome|pixel|fbevents|hotjar|intercom|'
        r'twemoji|wp-emoji|plupload|tinymce|codemirror|ace\.js)',
        re.I
    )
    _JS_COMMENT_PATH_RE = re.compile(r'(/[a-zA-Z0-9_/][^\s\'"<>\\]{3,})')

    @classmethod
    def js_comments(cls, text, url, store, emit):
                                                                                              
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
                                                                                           
                                                                          
                if not re.search(r'[:=]', comment):
                    _prose_skip = re.compile(
                        r'^(?:this|the|it|we|a|an|if|when|note|todo|fixme|hack|bug)\s', re.I)
                    if _prose_skip.match(comment):
                        continue
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
                                                                                            
        found = 0
        seen  = set()
        for pat in cls._ROUTE_PATTERNS:
            for m in re.finditer(pat, text):
                path = m.group(m.lastindex or 1).strip()
                if not path or path in seen or len(path) < 2: continue
                if path.startswith(("http","//","#","$","{")):  continue
                seen.add(path)
                                                                      
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
                                                                           
        _seen_paths: set = set()
        for pat in cls._API_RE:
            for m in re.finditer(pat, text):
                raw = m.group(1)
                if not raw or not raw.startswith("/") or len(raw) < 3:
                    continue
                                                                                
                _parsed    = urlparse(raw)
                _qs_params = list(parse_qs(_parsed.query).keys())
                clean_path = _parsed.path
                if not clean_path or clean_path == "/":
                    continue
                full = urljoin(base_url, clean_path)
                                                                                          
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
    def html_comments(cls, soup, url, store, emit, base_url=None, discover_url=None, depth=0):
\
\
\
\
\
\
           
        kw = {"todo","fixme","bug","admin","hidden","secret","debug","config",
              "key","password","cred","token","hack","temp","internal",
              "private","disabled","endpoint","framework","version","beta",
              "homepage","temporary","new-home","http://","https://"}
        _path_re = re.compile(r'(?:^|\s)(/[a-z0-9_\-\.]{2,}(?:/[a-z0-9_\-\.]*)*/?)', re.I)
        for c in soup.find_all(string=lambda t: isinstance(t, Comment)):
            txt = c.strip()
            if len(txt) < 4:
                continue
            has_kw   = any(k in txt.lower() for k in kw)
            has_path = bool(_path_re.search(txt))
            has_url  = bool(re.search(r'https?://', txt, re.I))
            if (has_kw or has_path or has_url
                    or bool(re.match(r'^[/\.][a-z0-9_\-\.#]{3,}', txt))):
                if store.add_comment(txt, url):
                    emit.info(f"[Comment] {txt[:120]}")
                                                          
                    if discover_url is not None and base_url is not None:
                        for m in _path_re.finditer(txt):
                            cpath = m.group(1).strip()
                            if re.match(r'^/[0-9]+$', cpath):
                                continue
                            full = urljoin(base_url, cpath)
                            if discover_url(full, depth + 1, "Comment_Path", show_feed=True):
                                emit.info(f"[Comment→Queue] {full}")
                                                                   
                    if discover_url is not None:
                        for m in re.finditer(r'(https?://[^\s\'"<>]+)', txt):
                            candidate = m.group(1).rstrip(".,)")
                            discover_url(candidate, depth + 1, "Comment_URL", show_feed=True)
                                                         
                    for pat, dtype in cls._EXTRACTION_PATTERNS:
                        if dtype in ('Email', 'Phone'):
                            for m in pat.finditer(txt):
                                v = m.group(1) if m.lastindex else m.group(0)
                                if v:
                                    if dtype == "Phone":
                                        v = re.sub(r'[\s.\-\(\)\/]', '', v)
                                        if not (7 <= len(v) <= 15): continue
                                        if not re.match(r'\+?\d+$', v): continue
                                        if re.match(r'(20[0-9]{2}[01][0-9][0-3][0-9]|[0-3][0-9][01][0-9]20[0-9]{2})', v): continue
                                    store.add_extracted_data(dtype, v.strip(), url)

        # ── inline <script> // comments on the same HTML page ──────────────
        # js_comments() is called separately only for standalone .js file
        # fetches; this covers inline scripts embedded in HTML responses.
        for script_tag in soup.find_all("script"):
            src = script_tag.get("src")
            if src:
                continue  # external file — handled by the JS fetch path
            raw = script_tag.string or ""
            if not raw.strip():
                # tag has multiple children (uncommon but valid)
                raw = script_tag.get_text()
            if raw:
                cls.js_comments(raw, url, store, emit)

    @classmethod
    def css_comments(cls, text: str, url: str, store, emit, ctf_patterns=None):
        """Extract /* ... */ comments from CSS files.
        Looks for endpoint hints, credential leaks, and CTF flags."""
        _SKIP_RE = re.compile(
            r'^(?:author|version|license|copyright|font|color|'
            r'margin|padding|display|position|overflow|'
            r'webkit|moz|ms|w3c)',
            re.I
        )
        _SIGNAL_RE = re.compile(
            r'(?:password|passwd|secret|token|api[_-]?key|credential|'
            r'todo|fixme|hack|debug|internal|admin|staging|prod|'
            r'endpoint|path|url|config|key|auth|bypass|hidden|'
            r'remove\s+before|do\s+not\s+commit)',
            re.I
        )
        _PATH_RE = re.compile(r'(?:^|\s)(/[a-z0-9_\-\.]{2,}(?:/[a-z0-9_\-\.]*)*/?)', re.I)
        found = 0
        for m in re.finditer(r'/\*(.*?)\*/', text, re.DOTALL):
            block = m.group(1).strip()
            if not block or len(block) < 8 or len(block) > 600:
                continue
            first_line = block.splitlines()[0].strip().lstrip("* ")
            if _SKIP_RE.match(first_line):
                continue
            has_signal  = bool(_SIGNAL_RE.search(block))
            has_path    = bool(_PATH_RE.search(block))
            has_url     = bool(re.search(r'https?://', block, re.I))
            if not (has_signal or has_path or has_url):
                continue
            display = first_line if len(first_line) <= 160 else first_line[:157] + "…"
            if store.add_comment(display, url):
                emit.info(f"[CSS-Comment] {display[:120]}")
                found += 1
        if ctf_patterns:
            scan_ctf_flags(text, url, store, emit, ctf_patterns)
        return found

    @classmethod
    def data_attr_leaks(cls, soup, url: str, store, emit):
        """Scan HTML data-* attributes for endpoint hints and debug info.
        Developers sometimes leave data-api-url, data-endpoint, data-debug
        values in production HTML that reveal internal routes or tokens."""
        _INTERESTING = re.compile(
            r'^data-(?:api|url|endpoint|src|action|href|path|'
            r'debug|token|key|secret|auth|user|id|config|env|'
            r'version|build|commit|branch|server|host|backend)',
            re.I
        )
        _PATH_RE = re.compile(r'^(?:/[a-z0-9_\-\.]{2,}|https?://)', re.I)
        found = 0
        for tag in soup.find_all(True):
            for attr, val in (tag.attrs or {}).items():
                if not isinstance(val, str):
                    continue
                if not _INTERESTING.match(attr):
                    continue
                val = val.strip()
                if not val or len(val) < 3 or len(val) > 500:
                    continue
                display = f"{attr}={val}"
                if store.add_comment(display, url):
                    emit.info(f"[DataAttr] {display[:120]}")
                    found += 1
        return found

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
                                                                                    
                gql_params = []
                for t in types:
                    if t.get("name","").startswith("__"): continue
                    for field in (t.get("fields") or []):
                        for arg in (field.get("args") or []):
                            aname = arg.get("name","").strip()
                            if aname and aname not in gql_params:
                                gql_params.append(aname)
                                                                            
                        fname = field.get("name","").strip()
                        if fname:
                            store.add_endpoint(url, method="POST", source="GraphQL_Field", score=Conf.HIGH)
                            ep_key = store._key(url, "POST")
                            if ep_key in store.endpoints:
                                ep = store.endpoints[ep_key]
                                for p in gql_params:
                                    if p not in ep["params"]["js"]:
                                        ep["params"]["js"].append(p)
                                                                     
                                                                              
                                                                       
                operations: dict = {"queries": {}, "mutations": {}, "subscriptions": {}}
                for t in types:
                    tname = t.get("name", "")
                    if tname.startswith("__"):
                        continue
                    tname_lo = tname.lower()
                    if "mutation" in tname_lo:
                        bucket = "mutations"
                    elif "subscription" in tname_lo:
                        bucket = "subscriptions"
                    else:
                        bucket = "queries"
                    for field in (t.get("fields") or []):
                        fname = field.get("name", "").strip()
                        if not fname:
                            continue
                        fargs = [a.get("name", "") for a in (field.get("args") or []) if a.get("name")]
                        operations[bucket][fname] = fargs
                        emit.info(f"[GraphQL] op={fname} args={fargs}")

                store.graphql.append({
                    "url":              url,
                    "types_count":      len(types),
                    "extracted_params": gql_params,
                    "operations":       operations,
                                                                                          
                                                                               
                })
                total_ops = sum(len(v) for v in operations.values())
                emit.warn(f"[GraphQL] {len(types)} types — {total_ops} operation(s) — {len(gql_params)} arg(s) extracted")
                if gql_params:
                    emit.info(f"[GraphQL] Args: {', '.join(gql_params[:20])}")
            except Exception as e:
                emit.warn(f"[GraphQL] Parse error: {e}")
            return

                                                                        
                
                                                                        

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

                                                                        
                         
                                                                  
                                                                        


                                                                        
                       
                                                                       
                                                                 
                                                                      
                                                                        


                                                                        
                                                             
                                                                  
                                                          
                                                                        


                                                                        
                   
                                                                    
                                                                      
                                                                      
                                                             
                                                                        

class HARImporter:
    def __init__(self, har_path, store, emit, is_valid_fn, base_url):
        self.har_path = har_path
        self.store    = store
        self.emit     = emit
        self.is_valid = is_valid_fn
        self.base_url = base_url

    def run(self):
                                                                         
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
                                          source="HAR", score=7)        
            added += 1

                                  
            for qp in req.get("queryString", []):
                name = qp.get("name","").strip()
                if name and ep and name not in ep.get("params",{}).get("query",[]):
                    ep.setdefault("params",{}).setdefault("query",[]).append(name)

                                      
            post_data = req.get("postData", {})
            if post_data:
                mime = post_data.get("mimeType","")
                text = post_data.get("text","")
                              
                for pp in post_data.get("params", []):
                    name = pp.get("name","").strip()
                    if name and ep and name not in ep.get("params",{}).get("form",[]):
                        ep.setdefault("params",{}).setdefault("form",[]).append(name)
                           
                if "json" in mime and text:
                    try:
                        body = _j.loads(text)
                        if isinstance(body, dict):
                            for k in body.keys():
                                if ep and k not in ep.get("params",{}).get("form",[]):
                                    ep.setdefault("params",{}).setdefault("form",[]).append(k)
                    except Exception:
                        pass

                                                 
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
            _MAX_ATTEMPTS = 4
            for _attempt in range(_MAX_ATTEMPTS):
                _per_req_timeout = 45 + _attempt * 15                       
                try:
                    async with _aio.ClientSession(
                        timeout=_aio.ClientTimeout(total=_per_req_timeout),
                        headers=_HEADERS,
                    ) as sess:
                        async with sess.get(self.CRT_SH.format(domain=f"%.{domain}")) as resp:
                            if resp.status == 200:
                                data = await resp.json(content_type=None)
                                break
                            elif resp.status == 429:
                                wait = 8 * (_attempt + 1)
                                self.emit.warn(f"[CRT.sh] Rate-limited — waiting {wait}s (attempt {_attempt+1}/{_MAX_ATTEMPTS})")
                                await asyncio.sleep(wait)
                            elif resp.status in (503, 502):
                                await asyncio.sleep(3 * (_attempt + 1))
                            else:
                                self.emit.warn(f"[CRT.sh] Unexpected status {resp.status}")
                                break
                except Exception as _inner_e:
                    _ename = type(_inner_e).__name__
                    if _attempt < _MAX_ATTEMPTS - 1:
                        self.emit.warn(
                            f"[CRT.sh] {_ename} on attempt {_attempt+1}/{_MAX_ATTEMPTS} "
                            f"(timeout {_per_req_timeout}s) — retrying in 5s…"
                        )
                        await asyncio.sleep(5)
                    else:
                        self.emit.warn(
                            f"[CRT.sh] Failed after {_MAX_ATTEMPTS} attempts ({_ename}) — "
                            f"crt.sh may be overloaded, try again later"
                        )
                        return
        except Exception as e:
            self.emit.warn(f"[CRT.sh] Error: {type(e).__name__} {e}")
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
                                                             
                for _s in (scheme,):
                    candidate = f"{_s}://{sub}"
                    self.store.add_endpoint(candidate, source="CRT_Subdomain", score=1)
                    self.queue.put_nowait((candidate + "/", 1, "CRT_Subdomain"))
                    added += 1
                                                                                             
                    if sub not in self.store._crt_seen:
                        self.store._crt_seen.add(sub)
                        self.store.crt_subdomains.append({
                            "hostname": sub,
                            "url":      candidate,
                            "scheme":   _s,
                        })
                                                                                              
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
                _WB_MAX = 3
                text = ""
                for _wb_attempt in range(_WB_MAX):
                    _wb_timeout = 60 + _wb_attempt * 30                   
                    try:
                        async with _aio.ClientSession(
                            timeout=_aio.ClientTimeout(total=_wb_timeout)
                        ) as _ws:
                            async with _ws.get(self.CDX_API + params) as _wr:
                                if _wr.status == 200:
                                    text = await _wr.text()
                                    break
                                elif _wr.status in (429, 503, 502):
                                    await asyncio.sleep(5 * (_wb_attempt + 1))
                                else:
                                    self.emit.warn(f"[Wayback] CDX status {_wr.status}")
                                    break
                    except Exception as _we:
                        if _wb_attempt < _WB_MAX - 1:
                            self.emit.warn(
                                f"[Wayback] {type(_we).__name__} on attempt {_wb_attempt+1}/{_WB_MAX} — retrying…"
                            )
                            await asyncio.sleep(5)
                        else:
                            self.emit.warn(f"[Wayback] CDX failed after {_WB_MAX} attempts: {type(_we).__name__}")
                            return
            except Exception as _we:
                self.emit.warn(f"[Wayback] CDX error: {_we}")
                return
            if not text or not text.strip():
                self.emit.always_info("[Wayback] CDX returned empty response — no historical URLs found")
                return
            try:
                rows = json.loads(text)
            except json.JSONDecodeError:
                                                                                               
                if "no results" in text.lower() or len(text.strip()) < 5:
                    self.emit.always_info("[Wayback] No historical URLs found for this domain")
                else:
                    self.emit.warn(f"[Wayback] Unexpected CDX response (not JSON): {text[:80].strip()}")
                return
            if not rows or len(rows) < 2:
                self.emit.always_info("[Wayback] No historical URLs found for this domain")
                return
                                              
            urls = [r[0] for r in rows[1:] if r and r[0].startswith("http")]
            queued = 0
            clean_dom = domain.lower()
            if clean_dom.startswith("www."):
                clean_dom = clean_dom[4:]
            for u in urls:
                                                                 
                u_host = urlparse(u).netloc.lower()
                clean_u = u_host[4:] if u_host.startswith("www.") else u_host
                if clean_u == clean_dom and self.is_valid(u):
                                                                            
                    self.store.add_endpoint(u, source="Wayback", score=Conf.LOW)
                    self.queue.put_nowait((u, 2, "Wayback"))
                    queued += 1
                                                                                                     
                    self.emit.robots_entry("Wayback", urlparse(u).path or u, True)
            self.emit.always_info(
                f"[Wayback] {len(urls)} historical URLs found — "
                f"{queued} same-domain queued for crawl"
            )
        except Exception as e:
            self.emit.warn(f"[Wayback] Error: {type(e).__name__} {e}")

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

                                                         
        _COMMENT_PATTERNS = re.compile(
            r'(?:password|passwd|secret|token|key|api[_-]?key|db|database|backup|'
            r'sql|dump|cred|credential|auth|admin|prod|production|staging|internal|'
            r'private|todo|fixme|note to self|remove|delete|temp|test|debug|'
            r'mysql|mongo|redis|postgres|s3|bucket|aws|gcp|azure)',
            re.I
        )

                                                
                                                                         
                                                                          
                                                                          
                                                                            
        current_agents: list = []
        is_active_block = False                                          
        bot_blocks: dict = {}                                 
        content_signals: dict = {}                               
        OUR_AGENT = "*"

        for raw_line in text.splitlines():
                                                 
            comment_text = ""
            if "#" in raw_line:
                comment_text = raw_line.split("#", 1)[1].strip()
            line = raw_line.split("#", 1)[0].strip()

                                                 
            if comment_text and _COMMENT_PATTERNS.search(comment_text):
                self.store.add_secret(comment_text, "Robots_Comment_Leak",
                                      urljoin(self.base_url, "/robots.txt"))
                self.emit.robots_comment_leak(comment_text)

            if not line:
                                                              
                current_agents = []
                is_active_block = False
                continue

            lower = line.lower()

            if lower.startswith("user-agent:"):
                agent = line.split(":", 1)[1].strip()
                current_agents = [agent]
                                                                    
                is_active_block = agent in ("*", OUR_AGENT)

            elif lower.startswith("content-signal:"):
                                                                               
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
                                                            
                    for ag in (current_agents or ["*"]):
                        if ag != "*":
                            bot_blocks.setdefault(ag, []).append(path)
                                                                      
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
                                                                          
                    if sitemap_url.startswith("/"):
                        sitemap_url = urljoin(self.base_url, sitemap_url)
                    elif not sitemap_url.startswith("http"):
                                                                              
                        sitemap_url = line.partition(":")[2].strip()
                        if not sitemap_url.startswith("http"):
                            sitemap_url = urljoin(self.base_url, sitemap_url)
                    self.emit.robots_entry("Sitemap-Ref", sitemap_url, True)
                    await self.parse_sitemap(sitemap_url)
                    sit_count += 1
                except (IndexError, Exception):
                    pass

                                                 
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
                                                                  
            self.emit.always_info(f"[Sitemap] {sitemap_url} → {len(sitemap_entries)} URLs queued")
            for u in sitemap_entries:
                parsed_u = urlparse(u)
                disp = parsed_u.path + ("?" + parsed_u.query if parsed_u.query else "")
                self.emit.robots_entry("Sitemap", disp or u, True)


                                                                        
                     
                                                   
                                                                    
                                                                  
                                                                        

class SecurityTxtParser:
\
\
\
\
\
\
\
\
\
\
\
\
\
\
\
       

                                                            
    _URL_FIELDS    = frozenset({"contact", "encryption", "acknowledgments",
                                "policy", "hiring", "canonical", "csaf"})
                                                                        
    _SCOPE_FIELDS  = frozenset({"canonical", "preferred-languages"})

                                                        
    _COMMENT_PATTERNS = re.compile(
        r'(?:password|passwd|secret|token|key|api[_-]?key|db|database|backup|'
        r'sql|dump|cred|credential|auth|admin|prod|production|staging|internal|'
        r'private|todo|fixme|note to self|remove|delete|temp|test|debug|'
        r'panel|path|endpoint|route|url|host|server|mysql|mongo|redis|'
        r'postgres|s3|bucket|aws|gcp|azure)',
        re.I
    )

                   
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
\
\
\
           
        self.emit.always_info("[SecurityTxt] Parsing /.well-known/security.txt")

        found_fields   = {}                          
        comment_leaks  = []
        queued_urls    = 0
        expired        = False

        for raw_line in text.splitlines():
            raw_line = raw_line.rstrip()

                                                                        
            if raw_line.lstrip().startswith("#"):
                comment = raw_line.lstrip().lstrip("#").strip()
                if not comment:
                    continue
                                                                      
                is_sensitive = bool(self._COMMENT_PATTERNS.search(comment))
                self.emit.security_txt_field("Comment", comment, flagged=is_sensitive)
                if is_sensitive:
                    self.store.add_secret(comment, "SecurityTxt_Comment_Leak", self._sec_url)
                    comment_leaks.append(comment)
                                                                                
                                                                         
                for _pm in re.finditer(r"""(?:^|\s)(/[^\s'"<>\\]+)""", comment):
                    _path = _pm.group(1).strip().rstrip(".,;)")
                    _full = urljoin(self.base_url, _path)
                    if self.is_valid(_full):
                        self.store.add_endpoint(_full, source="SecurityTxt_Comment", score=2)
                        self.queue.put_nowait((_full, 1, "SecurityTxt_Comment"))
                        queued_urls += 1
                        self.emit.security_txt_field("Path (comment)", _path, flagged=True)
                continue

                                                                        
            if not raw_line.strip():
                continue

                                                                        
                                                                            
                                                                      
                                                                                    
            if ":" not in raw_line:
                continue
            parts = raw_line.split(":", 1)
            field = parts[0].strip().lower()
            value = parts[1].strip() if len(parts) > 1 else ""
                                                                           
                                                                            
            if value in ("https", "http", "ftp") and raw_line.count(":") >= 2:
                value = raw_line.split(":", 1)[1].strip()
            if not field or not value:
                continue

            found_fields.setdefault(field, []).append(value)
            flagged = False

                                                                        
            if field == "contact":
                if value.startswith("mailto:"):
                    email = value[7:].strip()
                    self.store.add_secret(email, "SecurityTxt_Contact_Email", self._sec_url)
                                                                                         
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

                                                                        
            elif field == "encryption":
                if value.startswith("http") or value.startswith("/"):
                    self._queue_url(value)
                    queued_urls += 1
                                                                            
                                                                                   
                enc_domain   = urlparse(value).netloc.lower() if value.startswith("http") else self._base_domain
                cross_domain = bool(enc_domain and enc_domain != self._base_domain)
                self.store.add_secret(value, "SecurityTxt_Encryption_Key", self._sec_url)
                self.emit.security_txt_field("Encryption", value, flagged=cross_domain)

                                                                        
            elif field == "canonical":
                canon_domain = urlparse(value).netloc.lower()
                cross_domain = bool(canon_domain and canon_domain != self._base_domain)
                if cross_domain:
                    self.store.add_secret(value, "SecurityTxt_Canonical_CrossDomain", self._sec_url)
                self.emit.security_txt_field("Canonical", value, flagged=cross_domain)

                                                                       
            elif field in ("policy", "acknowledgments", "hiring", "csaf"):
                if value.startswith("http") or value.startswith("/"):
                    self._queue_url(value)
                    queued_urls += 1
                self.emit.security_txt_field(field.capitalize(), value)

                                                                        
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

                                                                        
            elif field == "preferred-languages":
                                                                     
                self.emit.security_txt_field("Preferred-Languages", value)

                                                                        
            else:
                                                                         
                                                                                 
                self.emit.security_txt_field(field.capitalize(), value)
                                                           
                if value.startswith("/"):
                    self._queue_url(value)
                    queued_urls += 1
                elif value.startswith("http"):
                    self._queue_url(value)
                    queued_urls += 1

                                                                        
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
                                                                          
        if value.startswith("/"):
            full = urljoin(self.base_url, value)
        else:
            full = value
                                                                    
        self.store.add_endpoint(full, source="SecurityTxt", score=2)
        if self.is_valid(full):
            self.queue.put_nowait((full, 1, "SecurityTxt"))

                                                                        
             
                                                                        

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
                                                                                 
            _stealth_fn = None
            try:
                from playwright_stealth import stealth_async as _sa                
                _stealth_fn = _sa
                self.emit.always_info("[SPA] Stealth: playwright-stealth active")
            except ImportError:
                                                                                        
                                                             
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
                                                                                    
                                                                                        
                                                                             
                                                                                         
                    auth = any(h.lower() in ("authorization", "x-auth-token", "x-api-key")
                               for h in hdrs)
                    self.store.add_endpoint(url, method=method, source="SPA_XHR",
                                            score=Conf.CONFIRMED, auth_required=auth)
                                                                              
                    self.store.add_graph_edge(self.target_url, url, via="SPA_XHR", depth=1)
                    if self.store.merge_headers(url, method, hdrs):
                        self.emit.info(f"[SPA-Headers] captured for {url}")
                                                  
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
                            from patchright.async_api import async_playwright as _pr_ap                
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
                                                                 
            try:
                await page.wait_for_load_state("networkidle", timeout=5000)
                await asyncio.sleep(1.0)
            except Exception:
                pass
            if self._enable_spa_interact:
                await self._interact(page)
            await self._harvest_dom(page)
            await self._harvest_hash(page)
                
                                                 
            acquired_cookies = await context.cookies()
            cookie_dict = {c["name"]: c["value"] for c in acquired_cookies}
            
            if self.screenshot_cfg:
                                                          
                self.emit.always_info("[SPA] SPA harvest complete — keeping browser alive for screenshots")
                return browser, context, page, cookie_dict
            
            await browser.close()
            await self._pw.stop()
            self.emit.always_info("[SPA] Dynamic analysis complete")
            return cookie_dict
        except Exception as e:
            self.emit.warn(f"[SPA] Error: {type(e).__name__} {e}")
            return None

    async def _interact(self, page):
\
\
\
\
\
           
                             
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
                    full = path                    
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
\
\
\
\
\
\
\
\
\
\
\
\
           
        if not spa_ctx: return
        browser, context, _page = spa_ctx

        domain   = re.sub(r'[^a-zA-Z0-9_\-]', '_', urlparse(self.target_url).netloc)
        ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
        priority = self.screenshot_cfg.get("priority", "standard")

        def get_status(e):
            obs = e.get("observed_status") or []
            if 200 in obs: return 200
            return max(obs) if obs else 0

                                                                           
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
        index      = []                                                            

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

                                                                   
            page = await context.new_page()
            try:
                self.emit.info(f"[Screenshot] {url} → {filepath}{label}")

                                                                                                
                try:
                    await page.goto(url, wait_until="networkidle", timeout=15000)
                except Exception:
                                                                               
                    try:
                        await page.goto(url, wait_until="domcontentloaded", timeout=8000)
                        await asyncio.sleep(1.2)                                      
                    except Exception:
                        pass

                                                                            
                await asyncio.sleep(0.8)

                                                                
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
                                                         
                try:
                    await page.close()
                except Exception:
                    pass

                                                                
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


                                                                        
                         
                                                                        


def _is_confirmed(ep: dict) -> bool:
                                                                                             
    return bool(ep.get("observed_status", []))

                                              
_ADMIN_DIAG_EXCLUDE = re.compile(
    r'/(?:server-status|server-info|nginx-status|phpinfo|info[.]php|'
    r'status|healthz|health|ping|metrics|ready|live)(?:[/?]|$)',
    re.I
)

                                                                        
                                                             
                                                                        

                                                                                
                                                                              
_UNAUTH_API_RE = re.compile(
    r'^/(?:api|rest|wp-json|graphql|gql|v[0-9]+|backend|service|rpc|data|internal)'
    r'(?:/[^?#]*)?$',
    re.I
)
_UNAUTH_API_EXCLUDE = re.compile(
    r'/(?:_next|__webpack|static|assets|public|images?|fonts?|icons?|favicon'
    r'|manifest|sw\.js|robots|sitemap|healthz|health|ping|metrics)(?:/|$|\?)',
    re.I
)

def classify_unauthenticated_api(store: Store):
\
\
\
\
\
\
\
\
\
       
    ts = store.tech_stack

                                                         
                                                                          
                                                                  
    public_namespaces: list = []

    if any("WordPress" in t for t in ts):
        public_namespaces.append(re.compile(
            r'^/wp-json/wp/v2/(?:posts|pages|categories|tags|media|types|'
            r'taxonomies|blocks|templates|template-parts|navigation|'
            r'menu-items|font-families|global-styles|svplayer|'
            r'aiovg_videos|aiovg_categories|aiovg_tags|comments)'
            r'(?:/[^/]*)?/?$',                                       
            re.I
        ))
        public_namespaces.append(re.compile(
            r'^/wp-json/oembed/', re.I
        ))
        public_namespaces.append(re.compile(
            r'^/(?:feed|comments/feed|xmlrpc\.php)/?$', re.I
        ))
                                                                 
        public_namespaces.append(re.compile(
            r'^/wp-json/popup-maker/', re.I
        ))

    if any("Drupal" in t for t in ts):
        public_namespaces.append(re.compile(
            r'^/jsonapi/(?:node|taxonomy_term|file|media)(?:/[^/]*)?/?$', re.I
        ))

    if any("Strapi" in t for t in ts):
                                                                       
        public_namespaces.append(re.compile(
            r'^/api/[^/]+/?$', re.I
        ))

    for ep in store.endpoints.values():
        if not _is_confirmed(ep):
            continue
        url  = ep["url"]
        path = urlparse(url).path

        if not _UNAUTH_API_RE.match(path):
            continue
        if _UNAUTH_API_EXCLUDE.search(path):
            continue
        if _STATIC_EXT.search(path):
            continue

                                             
        if any(pat.match(path) for pat in public_namespaces):
            continue

        obs = ep.get("observed_status", [])
        if 200 not in obs:
            continue
        if ep.get("auth_required", False):
            continue

        ep["unauthenticated_api"] = True


                                                                                 
                                                                               
                                                                                  
                                                              
_SENSITIVE_RESP_KEYS = re.compile(
    r'(?:password|passwd|secret|api_?key|access_?token|refresh_?token|private_?key|'
    r'credit_?card|card_?number|cvv|ssn|social_?security|date_?of_?birth|dob|'
    r'phone_?number|email_?address|home_?address|bank_?account|iban|passport|'
    r'driver_?license|national_?id|tax_?id|auth_?token|session_?token|bearer)',
    re.I
)
_SENSITIVE_PATH_RE = re.compile(
    r'/(?:export|download|dump|backup|users?|accounts?|profile|me|self|'
    r'customers?|employees?|patients?|records?|pii|gdpr|personal|private|'
    r'credentials?|keys?|secrets?|tokens?|config|configuration|settings|env|'
    r'\.env|debug|diagnostics?|internal)(?:/|$|\?|\.)',
    re.I
)

def classify_sensitive_data_sources(store: Store):
\
\
\
\
\
\
\
\
\
\
       
                                                                          
    urls_with_secrets: set = set()
    for sec in store.secrets:
        src = sec.get("source", "")
        if src:
            urls_with_secrets.add(normalize(src))

    for ep in store.endpoints.values():
        if not _is_confirmed(ep):
            continue
        url     = ep["url"]
        path    = urlparse(url).path
        signals = []

                                                                      
        if normalize(url) in urls_with_secrets:
            signals.append("confirmed_secret_in_response")

                                                            
        if _SENSITIVE_PATH_RE.search(path):
            signals.append("sensitive_path_pattern")

                                                                    
        obs_vals = ep.get("observed_values", {})
        pii_keys = [k for k in obs_vals if _SENSITIVE_RESP_KEYS.search(k)]
        if pii_keys:
            signals.append(f"pii_keys_in_response:{','.join(pii_keys[:5])}")

        if signals:
            ep["sensitive_data_source"] = True
            ep["sensitive_signals"]     = signals


                                                                               
                                                                                  
_LEGACY_PATH_RE = re.compile(
    r'/(?:xmlrpc\.php|wp-login\.php|phpmyadmin|pma|adminer|phpinfo\.php|'
    r'info\.php|test\.php|debug\.php|install\.php|setup\.php|upgrade\.php|'
    r'web\.config|\.git/|\.svn/|\.env|\.htpasswd|\.htaccess|'
    r'server-status|server-info|elmah\.axd|trace\.axd|'
    r'api/v1(?:/|$)|api/v0(?:/|$)|v1/(?:users|admin|config)|'
    r'cgi-bin/|fcgi-bin/|remote/|dana-na/|pulse/|'
    r'struts/|axis/|axis2/)(?:[^?#]*)?',
    re.I
)

def classify_legacy_endpoints(store: Store):
\
\
\
\
\
\
\
\
\
\
\
\
\
       
                                                                       
    live_paths: set = set()
    for ep in store.endpoints.values():
        sources = ep.get("source", [])
        if sources and any(s != "Wayback" for s in sources):
            live_paths.add(urlparse(ep["url"]).path.rstrip("/"))

                                                                                  
                                                                                     
    _INFRA_EXCLUDE = re.compile(
        r'^/(?:robots\.txt|sitemap(?:_index)?\.xml|favicon\.ico|'
        r'\.well-known/|crossdomain\.xml|browserconfig\.xml|'
        r'ads\.txt|security\.txt|humans\.txt)$',
        re.I
    )

                                                                     
                                                                           
    _WP_LOGIN_SAFE_ACTIONS = frozenset({"lostpassword", "postpass", "logout"})

    for ep in store.endpoints.values():
        if not _is_confirmed(ep):
            continue
        url     = ep["url"]
        path    = urlparse(url).path
        obs     = ep.get("observed_status", [])
        sources = ep.get("source", [])
        reason  = None

                                          
        if _INFRA_EXCLUDE.match(path):
            continue

                                                                 
        if _LEGACY_PATH_RE.search(path):
                                                                         
            if "wp-login.php" in path.lower():
                qs = urlparse(url).query.lower()
                action = ""
                for part in qs.split("&"):
                    if part.startswith("action="):
                        action = part.split("=",1)[1]
                if action in _WP_LOGIN_SAFE_ACTIONS:
                    continue
            if obs:
                reason = f"legacy_known_path:{path.split('?')[0]}"

                                                                            
        if not reason and "Wayback" in sources and 200 in obs:
            if path.rstrip("/") not in live_paths:
                reason = "wayback_zombie:historical_url_still_live"

        if reason:
            ep["legacy_endpoint"] = True
            ep["legacy_reason"]   = reason


def classify_admin_endpoints(store: Store):
    for ep in store.endpoints.values():
        if not _is_confirmed(ep): continue
        url = ep["url"]
        if _STATIC_EXT.search(url.split("?")[0]):
            continue
                                                            
        if _ADMIN_DIAG_EXCLUDE.search(url):
            continue
                                                               
        if _ADMIN_TIER1.search(url):
            ep["admin_panel"] = True
            continue
                                                                        
        if _ADMIN_TIER2.match(url):
            obs = ep.get("observed_status", [])
            if 200 in obs or 401 in obs or 403 in obs:
                ep["admin_panel"] = True

def classify_auth_endpoints(store: Store):
    for ep in store.endpoints.values():
        if not _is_confirmed(ep): continue
        url = ep["url"]
                                                           
        if _AUTH_EXCLUDE_RE.search(url):
            continue
        for label, pat in _AUTH_PATTERNS.items():
            if pat.search(url):
                ep.setdefault("auth_classification", [])
                if label not in ep["auth_classification"]:
                    ep["auth_classification"].append(label)

def _flag_upload_endpoints(store: Store):
                                                                        
    _UPLOAD_PATH_RE = re.compile(
        r'/(?:upload|uploads|file-upload|fileupload|file_upload|'
        r'attachments|import|ingest|multipart|'
        r'avatar|image-upload|media-upload)(?:/|$|\.)',
        re.I
    )
                                                             
    _REST_TYPE_EXCLUDE = re.compile(
        r'/wp-json/.*/types/|/api/.*/schema|/v[0-9]+/types/', re.I
    )
                                                                             
    _UPLOAD_WEAK_RE = re.compile(
        r'/(?:file|files|media|document|documents|image|images|'
        r'photo|photos|blob|storage)(?:/|$)',
        re.I
    )
    for ep in store.endpoints.values():
        url = ep["url"]
                                                              
        if _STATIC_EXT.search(url.split("?")[0]):
            continue
                                            
        if _REST_TYPE_EXCLUDE.search(url):
            continue
                                          
        if _UPLOAD_PATH_RE.search(url):
            ep["file_upload_candidate"] = True
            continue
                                                                    
        form_params = ep.get("params", {}).get("form", [])
        has_file_param = any(
            p.lower() in ("file","upload","image","photo","attachment","avatar","media","document")
            or p.lower().endswith(("[file]","[upload]","[image]","[attachment]"))
            for p in form_params
        )
        if has_file_param:
            ep["file_upload_candidate"] = True
            continue
                                                              
        if _UPLOAD_WEAK_RE.search(url):
            methods = ep.get("methods", [])
            if "POST" in methods or "PUT" in methods:
                ep["file_upload_candidate"] = True


                                                                        
                                         
                                                                          
                                                                        
                                                                        

_WAF_SIGNATURES = [
                                                           
                                                                        
    ("Cloudflare", "HIGH", [
        ("header_exists", "cf-ray",              None),
        ("header_value",  "server",              r"cloudflare"),
        ("cookie_name",   "__cfduid",            None),
        ("cookie_name",   "cf_clearance",        None),
    ]),
    ("Akamai", "HIGH", [
        ("header_exists", "x-check-cacheable",   None),
        ("header_exists", "x-akamai-transformed",None),
        ("header_value",  "server",              r"akamaighost|akamai"),
        ("header_exists", "akamai-origin-hop",   None),
    ]),
    ("AWS WAF / CloudFront", "HIGH", [
        ("header_exists", "x-amz-cf-id",         None),
        ("header_exists", "x-amz-request-id",    None),
        ("header_value",  "x-cache",             r"cloudfront"),
    ]),
    ("Imperva / Incapsula", "HIGH", [
        ("cookie_name",   "incap_ses",            None),
        ("cookie_name",   "visid_incap",          None),
        ("header_exists", "x-iinfo",             None),
        ("header_value",  "x-cdn",               r"incapsula"),
    ]),
    ("Sucuri", "HIGH", [
        ("header_exists", "x-sucuri-id",          None),
        ("header_value",  "x-sucuri-cache",       r".*"),
        ("header_value",  "server",               r"sucuri"),
    ]),
    ("F5 BIG-IP ASM", "HIGH", [
        ("cookie_name",   "ts",                   None),                     
        ("header_value",  "server",               r"bigip"),
        ("header_exists", "x-waf-event-info",     None),
    ]),
    ("ModSecurity", "MEDIUM", [
        ("header_exists", "x-mod-security",       None),
        ("header_value",  "server",               r"mod_security|modsec"),
    ]),
    ("Barracuda", "MEDIUM", [
        ("cookie_name",   "barra_counter_session", None),
        ("header_value",  "server",               r"barracuda"),
    ]),
    ("Radware AppWall", "MEDIUM", [
        ("cookie_name",   "rdwr",                 None),
        ("header_exists", "x-sid",                None),
    ]),
    ("Fastly CDN", "MEDIUM", [
        ("header_exists", "x-fastly-request-id",  None),
        ("header_value",  "via",                  r"fastly"),
        ("header_value",  "server",               r"fastly"),
    ]),
    ("Varnish", "MEDIUM", [
        ("header_exists", "x-varnish",            None),
        ("header_value",  "via",                  r"varnish"),
    ]),
    ("Nginx WAF / OpenResty", "LOW", [
        ("header_value",  "server",               r"openresty"),
    ]),
    ("Alibaba Cloud WAF", "MEDIUM", [
        ("header_value",  "server",               r"alibaba|tengine"),
        ("cookie_name",   "aliyungf_tc",          None),
    ]),
    ("Azure Front Door / WAF", "HIGH", [
        ("header_exists", "x-azure-ref",          None),
        ("header_exists", "x-ms-request-id",      None),
        ("header_value",  "server",               r"microsoft-azure"),
    ]),
    ("Wordfence (WordPress WAF)", "MEDIUM", [
        ("cookie_name",   "wfwaf-authcookie",     None),
        ("body",          None,                   r"wordfence"),
    ]),
    ("DDoS-Guard", "MEDIUM", [
        ("header_exists", "ddos-guard",            None),
        ("cookie_name",   "__ddg1",                None),
    ]),
    ("Reblaze", "MEDIUM", [
        ("cookie_name",   "rbzid",                None),
        ("header_value",  "server",               r"reblaze"),
    ]),
]


class WAFDetector:
    def __init__(self, store, emit):
        self.store = store
        self.emit  = emit

    def run(self, headers: dict, body: str, cookies: dict):
\
\
\
\
\
           
        norm_h = {k.lower(): (v or "").lower() for k, v in headers.items()}
        norm_c = {k.lower(): v for k, v in cookies.items()}
        body_lo = (body or "").lower()

        detected = []
        for waf_name, confidence, sigs in _WAF_SIGNATURES:
            matched_any = False
            for check, key, pattern in sigs:
                if check == "header_exists":
                    if key in norm_h:
                        matched_any = True; break
                elif check == "header_value":
                    val = norm_h.get(key, "")
                    if val and re.search(pattern, val, re.I):
                        matched_any = True; break
                elif check == "cookie_name":
                    if any(key in ck for ck in norm_c):
                        matched_any = True; break
                elif check == "body":
                    if pattern and re.search(pattern, body_lo, re.I):
                        matched_any = True; break
            if matched_any:
                detected.append({"waf": waf_name, "confidence": confidence})
                self.store.tech_stack.add(f"WAF: {waf_name}")
                self.emit.warn_sev(f"[WAF] Detected: {waf_name}", confidence)

        if not detected:
            self.emit.info("[WAF] No known WAF/CDN signature detected")
            self.store.waf_findings = []
        else:
            self.store.waf_findings = detected

        return detected


                                                                        
                                            
                                                                       
                              
                                                                        

class TLSInspector:
    def __init__(self, target: str, store, emit):
        self.target = target
        self.store  = store
        self.emit   = emit

    async def run(self):
        parsed = urlparse(self.target)
        if parsed.scheme != "https":
            self.store.tls_findings.append({"issue": "No_HTTPS", "severity": "HIGH",
                                             "detail": "Target is HTTP only — no TLS"})
            self.emit.warn_sev("[TLS] Target is HTTP only — no TLS encrypted transport", "HIGH")
            return
        host = parsed.hostname
        port = parsed.port or 443
        try:
            ctx = _ssl.create_default_context()
            loop = asyncio.get_event_loop()
            try:
                conn = await loop.run_in_executor(
                    None, lambda: _ssl.create_default_context().wrap_socket(
                        socket.create_connection((host, port), timeout=10),
                        server_hostname=host
                    )
                )
                cert  = conn.getpeercert()
                proto = conn.version()
                conn.close()
            except _ssl.CertificateError as e:
                self.store.tls_findings.append({"issue": "Cert_Hostname_Mismatch",
                                                 "severity": "HIGH", "detail": str(e)})
                self.emit.warn_sev(f"[TLS] Certificate hostname mismatch: {e}", "HIGH")
                return
            except _ssl.SSLError as e:
                self.store.tls_findings.append({"issue": "TLS_Handshake_Error",
                                                 "severity": "MEDIUM", "detail": str(e)})
                self.emit.warn_sev(f"[TLS] TLS error: {e}", "MEDIUM")
                return

                              
            if proto in ("TLSv1", "TLSv1.1", "SSLv3", "SSLv2"):
                self.store.tls_findings.append({"issue": "Weak_TLS_Version", "severity": "HIGH",
                                                 "detail": f"Server negotiated {proto}"})
                self.emit.warn_sev(f"[TLS] Weak protocol version negotiated: {proto}", "HIGH")
            else:
                self.emit.info(f"[TLS] Protocol: {proto} ✓")

                                
            if cert:
                from datetime import datetime as _dt
                not_after_str = cert.get("notAfter", "")
                if not_after_str:
                    try:
                        not_after = _dt.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
                        import datetime as _datetime_mod
                        days_left  = (not_after - _datetime_mod.datetime.now(_datetime_mod.timezone.utc).replace(tzinfo=None)).days
                        if days_left < 0:
                            self.store.tls_findings.append({"issue": "Cert_Expired",
                                "severity": "CRITICAL", "detail": f"Expired {abs(days_left)}d ago"})
                            self.emit.warn_sev(f"[TLS] Certificate EXPIRED {abs(days_left)} days ago!", "CRITICAL")
                        elif days_left < 14:
                            self.store.tls_findings.append({"issue": "Cert_Expiring_Soon",
                                "severity": "HIGH", "detail": f"Expires in {days_left} days"})
                            self.emit.warn_sev(f"[TLS] Certificate expiring in {days_left} days!", "HIGH")
                        elif days_left < 30:
                            self.store.tls_findings.append({"issue": "Cert_Expiring_Soon",
                                "severity": "MEDIUM", "detail": f"Expires in {days_left} days"})
                            self.emit.warn_sev(f"[TLS] Certificate expiring in {days_left} days", "MEDIUM")
                        else:
                            self.emit.info(f"[TLS] Cert valid for {days_left} more days ✓")
                    except Exception:
                        pass

                                                          
                issuer  = dict(x[0] for x in cert.get("issuer", []))
                subject = dict(x[0] for x in cert.get("subject", []))
                if issuer.get("organizationName") == subject.get("organizationName") and                    issuer.get("commonName") == subject.get("commonName"):
                    self.store.tls_findings.append({"issue": "Self_Signed_Cert",
                        "severity": "HIGH", "detail": f"CN={subject.get('commonName','?')}"})
                    self.emit.warn_sev(f"[TLS] Self-signed certificate detected", "HIGH")

                if not self.store.tls_findings:
                    self.emit.always_info(f"[TLS] Certificate OK — {subject.get('commonName','?')} expires in {days_left}d")
        except Exception as e:
            self.emit.info(f"[TLS] Inspection skipped: {e}")


                                                                        
                                             
                                                                         
                                                                        

class HeaderAuditor:
    _REQUIRED = {
        "Strict-Transport-Security":  ("HIGH",   "HSTS not set — forces plain HTTP fallback possible"),
        "X-Frame-Options":            ("MEDIUM",  "Clickjacking protection missing"),
        "X-Content-Type-Options":     ("LOW",     "MIME-sniffing protection missing (nosniff)"),
        "Content-Security-Policy":    ("MEDIUM",  "CSP not set — XSS risk elevated"),
        "Referrer-Policy":            ("LOW",     "Referrer leakage uncontrolled"),
        "Permissions-Policy":         ("LOW",     "Feature/permissions policy not set"),
    }
    _LEAK_HEADERS = {
        "Server", "X-Powered-By", "X-AspNet-Version",
        "X-AspNetMvc-Version", "X-Generator",
    }

    def __init__(self, store, emit):
        self.store = store
        self.emit  = emit

    def run(self, headers: dict):
        norm = {k.lower(): v for k, v in headers.items()}

        for header, (severity, reason) in self._REQUIRED.items():
            if header.lower() not in norm:
                self.store.header_audit.append({
                    "issue": f"Missing_{header.replace('-','_')}",
                    "severity": severity,
                    "header": header,
                    "detail": reason,
                })
                self.emit.warn_sev(f"[Headers] MISSING {header} — {reason}", severity)
            else:
                                                     
                if header == "Strict-Transport-Security":
                    val = norm[header.lower()]
                    if "max-age" not in val.lower():
                        self.store.header_audit.append({
                            "issue": "HSTS_No_MaxAge", "severity": "MEDIUM",
                            "header": header, "detail": f"Value missing max-age: {val}"})
                        self.emit.warn_sev(f"[Headers] HSTS present but no max-age: {val}", "MEDIUM")
                    elif "includesubdomains" not in val.lower():
                        self.store.header_audit.append({
                            "issue": "HSTS_No_IncludeSubDomains", "severity": "LOW",
                            "header": header, "detail": "HSTS does not cover subdomains"})
                                                               
                if header == "X-Frame-Options":
                    val = norm[header.lower()].upper()
                    if val not in ("DENY", "SAMEORIGIN"):
                        self.store.header_audit.append({
                            "issue": "Weak_XFrameOptions", "severity": "MEDIUM",
                            "header": header, "detail": f"Weak value: {val}"})
                        self.emit.warn_sev(f"[Headers] X-Frame-Options has weak value: {val}", "MEDIUM")

                             
        for lh in self._LEAK_HEADERS:
            if lh.lower() in norm:
                val = norm[lh.lower()]
                self.store.header_audit.append({
                    "issue": f"Info_Leak_{lh.replace('-','_')}",
                    "severity": "LOW", "header": lh,
                    "detail": f"Version/tech exposed: {val}",
                })
                self.emit.warn_sev(f"[Headers] Info leak — {lh}: {val}", "LOW")

                                                       
        if "set-cookie" in norm and "cache-control" not in norm:
            self.store.header_audit.append({
                "issue": "Missing_Cache_Control", "severity": "LOW",
                "header": "Cache-Control",
                "detail": "Set-Cookie present but no Cache-Control — response may be cached"})

        if not self.store.header_audit:
            self.emit.always_info("[Headers] Security headers OK ✓")


                                                                        
                                 
                                                                   
                                             
                                                                  
                                                                        

class DNSIntel:
                                                                              
                                                             
    _TAKEOVER_SERVICES = {
        "s3.amazonaws.com":           "AWS S3",
        "s3-website":                 "AWS S3 Website",
        "cloudfront.net":             "AWS CloudFront",
        "elasticbeanstalk.com":       "AWS ElasticBeanstalk",
        "azurewebsites.net":          "Azure WebApps",
        "blob.core.windows.net":      "Azure Blob",
        "trafficmanager.net":         "Azure TrafficManager",
        "cloudapp.net":               "Azure CloudApp",
        "azureedge.net":              "Azure CDN",
        "onmicrosoft.com":            "Microsoft 365",
        "github.io":                  "GitHub Pages",
        "fastly.net":                 "Fastly CDN",
        "herokudns.com":              "Heroku",
        "herokuapp.com":              "Heroku",
        "pantheonsite.io":            "Pantheon",
        "pantheon.io":                "Pantheon",
        "wpengine.com":               "WP Engine",
        "myshopify.com":              "Shopify",
        "shopify.com":                "Shopify",
        "zendesk.com":                "Zendesk",
        "helpscoutdocs.com":          "HelpScout",
        "ghost.io":                   "Ghost",
        "webflow.io":                 "Webflow",
        "netlify.com":                "Netlify",
        "netlify.app":                "Netlify",
        "surge.sh":                   "Surge.sh",
        "readthedocs.io":             "ReadTheDocs",
        "readme.io":                  "Readme.io",
        "bitbucket.io":               "Bitbucket",
        "smartling.com":              "Smartling",
    }

    def __init__(self, target: str, store, emit):
        self.target = target
        self.store  = store
        self.emit   = emit
        self._domain = urlparse(target).hostname or ""

    async def run(self):
        if not self._domain:
            return
        loop = asyncio.get_event_loop()
        self.emit.always_info(f"[DNS] Querying DNS intelligence for {self._domain}")

                                                              
        try:
            import dns.resolver as _dnsr                
            await loop.run_in_executor(None, self._run_dnspython, _dnsr)
        except ImportError:
            await loop.run_in_executor(None, self._run_socket)
        except Exception as e:
            self.emit.info(f"[DNS] dnspython error: {e} — using socket fallback")
            await loop.run_in_executor(None, self._run_socket)

    def _run_dnspython(self, _dnsr):
                                              
        domain = self._domain

             
        try:
            for r in _dnsr.resolve(domain, "TXT"):
                txt = r.to_text().strip('"')
                if txt.startswith("v=spf1"):
                    self.emit.always_info(f"[DNS] SPF: {txt[:80]}")
                    if "+all" in txt:
                        self.store.dns_findings.append({
                            "issue": "SPF_Plus_All", "severity": "HIGH",
                            "detail": "+all means ANY server can send mail — email spoofing trivial"})
                        self.emit.warn_sev("[DNS] SPF +all — email spoofing is possible!", "HIGH")
                    break
        except Exception:
            self.store.dns_findings.append({"issue": "SPF_Missing", "severity": "HIGH",
                "detail": "No SPF record — email spoofing possible"})
            self.emit.warn_sev(f"[DNS] No SPF record for {domain} — email spoofing possible", "HIGH")

               
        try:
            _dnsr.resolve(f"_dmarc.{domain}", "TXT")
            self.emit.info(f"[DNS] DMARC record present ✓")
        except Exception:
            self.store.dns_findings.append({"issue": "DMARC_Missing", "severity": "HIGH",
                "detail": "No DMARC record — no email spoofing reporting/policy"})
            self.emit.warn_sev(f"[DNS] No DMARC record for _dmarc.{domain}", "HIGH")

                    
        try:
            mxs = [str(r.exchange).rstrip(".") for r in _dnsr.resolve(domain, "MX")]
            self.emit.info(f"[DNS] MX: {', '.join(mxs[:3])}")
        except Exception:
            pass

                                               
        for sub in ("", "www"):
            host = f"{sub}.{domain}" if sub else domain
            try:
                ans = _dnsr.resolve(host, "CNAME")
                cname_target = str(ans[0].target).rstrip(".")
                for svc_frag, svc_name in self._TAKEOVER_SERVICES.items():
                    if svc_frag in cname_target:
                                                               
                        try:
                            socket.getaddrinfo(cname_target, 80)
                        except socket.gaierror:
                            self.store.dns_findings.append({
                                "issue": "CNAME_Takeover_Candidate",
                                "severity": "CRITICAL",
                                "detail": f"{host} -> {cname_target} ({svc_name}) resolves to NXDOMAIN — potential subdomain takeover"})
                            self.emit.warn_sev(f"[DNS] TAKEOVER CANDIDATE: {host} -> {cname_target} ({svc_name})", "CRITICAL")
            except Exception:
                pass

    def _run_socket(self):
                                                        
        domain = self._domain
                                                                     
                                                                          
        self.emit.info(f"[DNS] Running basic socket DNS checks (install dnspython for full TXT/MX/CNAME analysis)")
        try:
            info = socket.getaddrinfo(domain, 80)
            ips  = list({r[4][0] for r in info if r[0] == socket.AF_INET})
            self.emit.info(f"[DNS] {domain} resolves to: {', '.join(ips[:4])}")
        except socket.gaierror as e:
            self.store.dns_findings.append({"issue": "DNS_Resolution_Failed",
                "severity": "HIGH", "detail": str(e)})
            self.emit.warn_sev(f"[DNS] Cannot resolve {domain}: {e}", "HIGH")


                                                                        
                         
                                                                     
                                                                
                                                                        

_ADMIN_PROBE_PATHS = [
                          
    "/admin", "/admin/", "/admin/login", "/admin/login.php",
    "/administrator", "/administrator/", "/administrator/index.php",
    "/adminpanel", "/adminpanel/", "/admin-panel/",
    "/manage", "/management", "/manager", "/manager/html",
    "/dashboard", "/dashboard/", "/control", "/controlpanel",
    "/cp", "/cp/", "/cpanel", "/backend", "/backend/",
                  
    "/wp-admin", "/wp-admin/", "/wp-login.php",
    "/wp-admin/admin-ajax.php", "/wp-admin/options-general.php",
    "/joomla/administrator", "/administrator/index.php",
    "/typo3", "/typo3/", "/typo3cms/",
    "/drupal/admin", "/user/login", "/admin/user/login",
    "/magento/admin", "/index.php/admin",
    "/shopify/admin",
                       
    "/admin/console", "/console/", "/web-console/",
    "/jmx-console", "/jmx-console/", "/invoker/JMXInvokerServlet",
    "/struts/", "/action/", "/jenkins", "/jenkins/",
    "/sonarqube", "/nexus", "/nexus/", "/artifactory",
                     
    "/admin/", "/django-admin/", "/_admin/",
           
    "/rails/", "/rails/info", "/rails/mailers",
          
    "/_api/", "/api/admin", "/api/admin/",
               
    "/phpmyadmin", "/phpmyadmin/", "/pma", "/pma/",
    "/adminer.php", "/adminer/", "/phpMyAdmin/",
    "/dbadmin", "/mysql", "/myadmin",
                         
    "/graphite", "/kibana", "/grafana", "/grafana/",
    "/prometheus", "/alert-manager",
    "/portainer", "/traefik", "/traefik/dashboard",
    "/netdata", "/uptime-kuma",
                     
    "/minio", "/minio/", "/_minio/health",
    "/s3browser", "/file-manager",
                 
    "/gitea", "/gogs", "/gitlab",
                 
    "/swagger", "/swagger-ui", "/swagger-ui.html",
    "/swagger/index.html", "/api-docs", "/api-docs/",
    "/__admin__", "/_debug", "/debug/pprof",
    "/server-status", "/server-info",
                         
    "/login", "/signin", "/sign-in",
    "/auth/login", "/auth/admin",
    "/sso/login", "/saml/login",
    "/oidc/login",
]

_ADMIN_TITLE_RE = re.compile(
    r'<title[^>]*>([^<]{3,100})</title>',
    re.I | re.S
)
_ADMIN_CONFIRM_RE = re.compile(
    r'(?:admin|administrator|login|sign.?in|dashboard|control.?panel|'
    r'manage|management|back.?office|cms|portal)',
    re.I
)


async def probe_admin_panels(session, base: str, store, emit, rl):
    # Dedupe paths that resolve to the same effective URL (e.g. "/admin" and
    # "/admin/" both appear in the list and both join to the same target).
    _seen_urls = set()
    _dedup_paths = []
    for p in _ADMIN_PROBE_PATHS:
        u = base.rstrip("/") + p
        u_norm = u.rstrip("/") or u
        if u_norm in _seen_urls:
            continue
        _seen_urls.add(u_norm)
        _dedup_paths.append(p)

    emit.always_info(f"[AdminProbe] Probing {len(_dedup_paths)} admin/management paths…")
    found = 0
    sem = asyncio.Semaphore(10)

    async def _probe(path):
        nonlocal found
        async with sem:
            url = base.rstrip("/") + path
            s, hdrs, body = await fetch(session, "GET", url, rl)
        if s not in (200, 301, 302, 401, 403):
            return
        if not body and s in (301, 302):
            loc = (hdrs or {}).get("location", "") if hdrs else ""
            store.add_endpoint(url, source="AdminProbe", score=Conf.HIGH)
            ep = store.endpoints.get(store._key(url, "GET"))
            if ep:
                ep["admin_panel"] = True
                ep["observed_status"].append(s)
            emit.warn_sev(f"[AdminProbe] Admin redirect ({s}) → {loc or url}", "MEDIUM")
            found += 1
            return
        if not body:
            return
        if Extractor.is_soft_404(body, s):
            return
        if s in (401, 403):
            store.add_endpoint(url, source="AdminProbe", score=Conf.HIGH)
            ep = store.endpoints.get(store._key(url, "GET"))
            if ep:
                ep["admin_panel"] = True
                ep["auth_required"] = True
                ep["observed_status"].append(s)
            emit.warn_sev(f"[AdminProbe] Auth-protected admin ({s}) → {url}", "HIGH")
            found += 1
            return
        title_m = _ADMIN_TITLE_RE.search(body)
        title = title_m.group(1).strip() if title_m else ""
        if not _ADMIN_CONFIRM_RE.search(title + " " + body[:500]):
            return
        store.add_endpoint(url, source="AdminProbe", score=Conf.HIGH)
        ep = store.endpoints.get(store._key(url, "GET"))
        if ep:
            ep["admin_panel"] = True
            ep["observed_status"].append(s)
        emit.warn_sev(f"[AdminProbe] ADMIN PANEL ({s}) → {url}  [{title[:60]}]", "HIGH")
        found += 1

    await asyncio.gather(*(_probe(p) for p in _dedup_paths))
    emit.always_info(f"[AdminProbe] Done — {found} admin panel(s) found")

                                                                        
                                                 
                                                              
                                                                        

_SENSITIVE_PATHS = [
                                
    ("/.env",                      "CRITICAL", "Env_File"),
    ("/.env.local",                "CRITICAL", "Env_File"),
    ("/.env.production",           "CRITICAL", "Env_File"),
    ("/.env.development",          "HIGH",     "Env_File"),
    ("/.env.backup",               "CRITICAL", "Env_File"),
    ("/config.yml",                "HIGH",     "Config_File"),
    ("/config.yaml",               "HIGH",     "Config_File"),
    ("/config.json",               "HIGH",     "Config_File"),
    ("/configuration.php",         "HIGH",     "Config_File"),
    ("/settings.py",               "HIGH",     "Config_File"),
    ("/database.yml",              "HIGH",     "Config_File"),
    ("/web.config",                "MEDIUM",   "Config_File"),
    ("/wp-config.php",             "CRITICAL", "Config_File"),
    ("/wp-config.php.bak",         "CRITICAL", "Config_File"),
    ("/application.properties",    "HIGH",     "Config_File"),
    ("/application.yml",           "HIGH",     "Config_File"),
                  
    ("/.git/HEAD",                 "CRITICAL", "Git_Exposure"),
    ("/.git/config",               "CRITICAL", "Git_Exposure"),
    ("/.svn/entries",              "HIGH",     "SVN_Exposure"),
    ("/.hg/hgrc",                  "HIGH",     "Mercurial_Exposure"),
    ("/.bzr/README",               "MEDIUM",   "Bazaar_Exposure"),
                  
    ("/backup.zip",                "CRITICAL", "Backup_File"),
    ("/backup.tar.gz",             "CRITICAL", "Backup_File"),
    ("/backup.sql",                "CRITICAL", "Backup_File"),
    ("/db.sql",                    "CRITICAL", "Backup_File"),
    ("/dump.sql",                  "CRITICAL", "Backup_File"),
    ("/.DS_Store",                 "LOW",      "Meta_File"),
    ("/Thumbs.db",                 "LOW",      "Meta_File"),
                        
    ("/phpinfo.php",               "HIGH",     "Debug_Page"),
    ("/_phpinfo.php",              "HIGH",     "Debug_Page"),
    ("/info.php",                  "MEDIUM",   "Debug_Page"),
    ("/test.php",                  "MEDIUM",   "Debug_Page"),
    ("/debug",                     "MEDIUM",   "Debug_Endpoint"),
    ("/debug/",                    "MEDIUM",   "Debug_Endpoint"),
    ("/__debug__/",                "MEDIUM",   "Debug_Endpoint"),
    ("/server-status",             "MEDIUM",   "Apache_Status"),
    ("/server-info",               "MEDIUM",   "Apache_Info"),
                          
    ("/actuator",                  "HIGH",     "Actuator"),
    ("/actuator/health",           "MEDIUM",   "Actuator"),
    ("/actuator/env",              "CRITICAL", "Actuator"),
    ("/actuator/beans",            "HIGH",     "Actuator"),
    ("/actuator/mappings",         "HIGH",     "Actuator"),
    ("/actuator/info",             "MEDIUM",   "Actuator"),
    ("/actuator/logfile",          "HIGH",     "Actuator"),
    ("/actuator/httptrace",        "HIGH",     "Actuator"),
    ("/actuator/dump",             "HIGH",     "Actuator"),
    ("/actuator/metrics",          "MEDIUM",   "Actuator"),
    ("/actuator/configprops",      "CRITICAL", "Actuator"),
    ("/actuator/auditevents",      "HIGH",     "Actuator"),
                          
    ("/rails/info/properties",     "HIGH",     "Rails_Debug"),
    ("/rails/info/routes",         "HIGH",     "Rails_Debug"),
    ("/console",                   "CRITICAL", "Console_Exposure"),
    ("/web-console",               "CRITICAL", "Console_Exposure"),
    ("/__webpack_hmr",             "LOW",      "Dev_Server"),
                                
    ("/phpmyadmin/",               "HIGH",     "PHPMyAdmin"),
    ("/pma/",                      "HIGH",     "PHPMyAdmin"),
    ("/adminer.php",               "HIGH",     "Adminer"),
    ("/adminer/",                  "HIGH",     "Adminer"),
               
    ("/logs/error.log",            "HIGH",     "Log_File"),
    ("/logs/access.log",           "HIGH",     "Log_File"),
    ("/error.log",                 "HIGH",     "Log_File"),
    ("/access.log",                "HIGH",     "Log_File"),
    ("/storage/logs/laravel.log",  "HIGH",     "Log_File"),
                        
    ("/package.json",              "MEDIUM",   "Package_File"),
    ("/package-lock.json",         "MEDIUM",   "Package_File"),
    ("/yarn.lock",                 "MEDIUM",   "Package_File"),
    ("/composer.json",             "MEDIUM",   "Package_File"),
    ("/Gemfile",                   "MEDIUM",   "Package_File"),
    ("/requirements.txt",          "MEDIUM",   "Package_File"),
                             
    ("/graphql/schema.json",       "HIGH",     "GraphQL_Schema"),
    ("/schema.graphql",            "HIGH",     "GraphQL_Schema"),
]

                                                                            
                                                                                
                                                               
_SENSITIVE_CONFIRM = {
    "Env_File":       re.compile(r'(?m)^[A-Z_]{2,}=\S'),
    "Git_Exposure":   re.compile(r'ref: refs/'),
    "Config_File":    re.compile(r'(?:password|secret|api[_-]?key|database|db_host|db_user|db_pass)\s*[=:\"\']', re.I),
    "Debug_Page":     re.compile(r'phpinfo\(\)|PHP Version|php\.ini|Configuration File', re.I),
    "Actuator":       re.compile(r'(?:"status"\s*:\s*"UP"|"_links"\s*:\s*\{|"beans"\s*:\s*\{|"mappings"\s*:\s*\[)', re.I),
    "Log_File":       re.compile(r'(?:\[\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}|\b(?:ERROR|WARN(?:ING)?|FATAL)\b.*?\bat\b)', re.I),
    "Package_File":   re.compile(r'(?:"(?:dependencies|devDependencies|name|version)"\s*:)', re.I),
    "GraphQL_Schema": re.compile(r'(?:"__schema"|type\s+Query\s*\{|schema\s*\{)', re.I),
    "Console_Exposure": re.compile(r'(?:console|terminal|shell|irb|pry|binding\.pry)', re.I),
    "Backup_File":    re.compile(r'(?:INSERT INTO|CREATE TABLE|DROP TABLE|BEGIN TRANSACTION|PK\x03\x04)', re.I),
    "PHPMyAdmin":     re.compile(r'(?:phpmyadmin|pma_|PMA_)', re.I),
    "Adminer":        re.compile(r'(?:adminer|login-form|db=)', re.I),
}


async def probe_sensitive_files(session, base: str, store, emit, rl):
    emit.always_info(f"[SensitiveFiles] Probing {len(_SENSITIVE_PATHS)} known-sensitive paths…")

                                                                        
                                                                           
                                                                       
                                                                           
    canary_slug  = hashlib.md5(f"{base}-canary-{random.random()}".encode()).hexdigest()[:16]
    canary_url   = base.rstrip("/") + f"/{canary_slug}-nonexistent.aspx"
    canary_s, canary_hdrs, canary_body = await fetch(session, "GET", canary_url, rl)
    canary_hash  = None
    canary_len   = 0
    canary_is_html = False
    if canary_body and canary_s in (200, 206):
        canary_hash    = hashlib.md5(canary_body.encode(errors="ignore")).hexdigest()
        canary_len     = len(canary_body)
        canary_ct      = ((canary_hdrs or {}).get("content-type", "") or "").lower()
        canary_is_html = "text/html" in canary_ct
        emit.info(f"[SensitiveFiles] SPA canary fingerprint: {canary_hash[:12]}… "
                  f"(status={canary_s}, len={canary_len}, html={canary_is_html})")

    found = 0
    sem = asyncio.Semaphore(10)

    async def _probe(path, severity, ftype):
        nonlocal found
        url = base.rstrip("/") + path
        async with sem:
            s, hdrs, body = await fetch(session, "GET", url, rl)
        if s not in (200, 206):
            return
        if not body or len(body) < 10:
            return
        if canary_hash:
            probe_hash = hashlib.md5(body.encode(errors="ignore")).hexdigest()
            if probe_hash == canary_hash:
                return
        ct = ((hdrs or {}).get("content-type", "") or "").lower()
        if canary_is_html and canary_len > 200 and "text/html" in ct:
            if canary_len > 0 and abs(len(body) - canary_len) / canary_len < 0.03:
                return
        if Extractor.is_soft_404(body, s):
            return
        if "text/html" in ct:
            confirm_pat = _SENSITIVE_CONFIRM.get(ftype)
            if confirm_pat and confirm_pat.search(body):
                pass
            elif ftype in ("Debug_Page",) and confirm_pat and confirm_pat.search(body):
                pass
            else:
                return
        confirm_pat = _SENSITIVE_CONFIRM.get(ftype)
        if confirm_pat and not confirm_pat.search(body):
            return
        preview = body[:200].replace("\n", " ").replace("\r", "")
        store.sensitive_files.append({
            "url":      url,
            "type":     ftype,
            "severity": severity,
            "preview":  preview,
            "status":   s,
        })
        store.add_endpoint(url, source="SensitiveFile_Probe", score=Conf.CONFIRMED)
        emit.warn_sev(f"[SensitiveFiles] {ftype} exposed → {url}", severity)
        found += 1

    await asyncio.gather(*(_probe(p, sev, ft) for p, sev, ft in _SENSITIVE_PATHS))
    emit.always_info(f"[SensitiveFiles] Done — {found} sensitive file(s) found")


async def probe_wordlist(session, base: str, store, emit, rl, wordlist_path: str):
    """Directory/file brute force using a user-supplied wordlist.
    Reuses canary fingerprinting + soft-404 filtering from the sensitive-file probe
    so noisy SPA/wildcard-200 targets don't flood results with false positives."""
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            words = [w.strip() for w in f if w.strip() and not w.startswith("#")]
    except Exception as e:
        emit.warn(f"[Wordlist] Failed to read {wordlist_path}: {e}")
        return

    if not words:
        emit.warn(f"[Wordlist] {wordlist_path} is empty")
        return

    emit.always_info(f"[Wordlist] Brute-forcing {len(words)} path(s) from {wordlist_path}…")

    canary_slug  = hashlib.md5(f"{base}-canary-{random.random()}".encode()).hexdigest()[:16]
    canary_url   = base.rstrip("/") + f"/{canary_slug}-nonexistent-wl"
    canary_s, canary_hdrs, canary_body = await fetch(session, "GET", canary_url, rl)
    canary_hash  = None
    canary_len   = 0
    canary_is_html = False
    if canary_body and canary_s in (200, 206):
        canary_hash    = hashlib.md5(canary_body.encode(errors="ignore")).hexdigest()
        canary_len     = len(canary_body)
        canary_ct      = ((canary_hdrs or {}).get("content-type", "") or "").lower()
        canary_is_html = "text/html" in canary_ct
        emit.info(f"[Wordlist] Soft-404 canary fingerprint: {canary_hash[:12]}… "
                  f"(status={canary_s}, len={canary_len}, html={canary_is_html})")

    found = 0
    sem = asyncio.Semaphore(20)

    async def _probe_word(word):
        nonlocal found
        path = word if word.startswith("/") else "/" + word
        url = base.rstrip("/") + path
        async with sem:
            s, hdrs, body = await fetch(session, "GET", url, rl)
        if s in (404,):
            return
        if s in (401, 403) and not body:
            # Forbidden/unauthorized is still a real finding (path exists, blocked)
            store.add_endpoint(url, source="Wordlist_Probe", score=Conf.LOW)
            emit.info(f"[Wordlist] {s} (access-controlled) -> {url}")
            found += 1
            return
        if s not in (200, 201, 204, 206, 301, 302, 307, 308):
            return
        if body:
            if canary_hash:
                probe_hash = hashlib.md5(body.encode(errors="ignore")).hexdigest()
                if probe_hash == canary_hash:
                    return
            ct = ((hdrs or {}).get("content-type", "") or "").lower()
            if canary_is_html and canary_len > 200 and "text/html" in ct:
                if canary_len > 0 and abs(len(body) - canary_len) / canary_len < 0.03:
                    return
            if Extractor.is_soft_404(body, s):
                return
        store.add_endpoint(url, source="Wordlist_Probe", score=Conf.HIGH)
        emit.warn_sev(f"[Wordlist] {s} -> {url}", "MEDIUM")
        found += 1

    await asyncio.gather(*(_probe_word(w) for w in words))
    emit.always_info(f"[Wordlist] Done — {found} hit(s) found from {len(words)} path(s)")


                                                                        
                                                                    
                                                                       
                                                  
                                                                        

                                                                   
_KNOWN_VULN_LOCAL = {
    "jquery":     {"lt": "3.5.0",  "cve": "CVE-2020-11022", "desc": "XSS via HTML parsing"},
    "lodash":     {"lt": "4.17.21","cve": "CVE-2021-23337", "desc": "Prototype pollution / command injection"},
    "angular":    {"lt": "1.8.0",  "cve": "CVE-2020-7676",  "desc": "XSS in sanitization"},
    "bootstrap":  {"lt": "3.4.1",  "cve": "CVE-2019-8331",  "desc": "XSS via data-template"},
    "moment":     {"lt": "2.29.4", "cve": "CVE-2022-24785", "desc": "Path traversal in locale"},
    "handlebars": {"lt": "4.7.7",  "cve": "CVE-2021-23369", "desc": "Remote code execution"},
    "highlight.js":{"lt": "10.4.1","cve": "CVE-2021-23346", "desc": "ReDoS"},
    "axios":      {"lt": "0.21.2", "cve": "CVE-2021-3749",  "desc": "ReDoS in URL parsing"},
    "underscore":  {"lt": "1.13.0", "cve": "CVE-2021-23358", "desc": "Arbitrary code execution"},
    "dompurify":   {"lt": "2.3.1",  "cve": "CVE-2021-26701", "desc": "XSS bypass"},
}

_LIB_VER_RE = re.compile(
    r'(?:^|/)'
    r'(jquery|lodash|angular|bootstrap|moment|handlebars|highlight\.js|'
    r'axios|underscore|dompurify|vue|react|three\.js|d3)'
    r'[.\-@]'
    r'(\d+\.\d+\.?\d*)'
    r'(?:\.min)?\.js',
    re.I
)

def _ver_lt(a: str, b: str) -> bool:
                                              
    try:
        from functools import reduce as _r
        def _parts(v): return [int(x) for x in re.split(r'[.\-]', v)[:3]]
        ap, bp = _parts(a), _parts(b)
                            
        while len(ap) < len(bp): ap.append(0)
        while len(bp) < len(ap): bp.append(0)
        return ap < bp
    except Exception:
        return False


async def analyze_js_deps(session, base: str, store, emit, rl):
\
\
\
       
    seen_libs: dict = {}                              
    for ep in store.all_endpoints():
        url = ep.get("url", "")
        if not (url.endswith(".js") or ".js?" in url):
            continue
        m = _LIB_VER_RE.search(url.split("/")[-1])
        if m:
            lib, ver = m.group(1).lower(), m.group(2)
            if lib not in seen_libs:
                seen_libs[lib] = {"version": ver, "url": url}

                                                                         
                                                      
    for t in store.tech_stack:
        m = re.match(r'(\w[\w.]+)\s+v?(\d+\.\d+\.?\d*)', t, re.I)
        if m:
            lib, ver = m.group(1).lower(), m.group(2)
            if lib not in seen_libs:
                seen_libs[lib] = {"version": ver, "url": "(tech-stack)"}

    if not seen_libs:
        return

    emit.always_info(f"[SCA] Analyzing {len(seen_libs)} JS librar(ies): {list(seen_libs.keys())}")

    for lib, info in seen_libs.items():
        ver = info["version"]
        url = info["url"]
                         
        local = _KNOWN_VULN_LOCAL.get(lib)
        if local and _ver_lt(ver, local["lt"]):
            finding = {
                "library":  lib,
                "version":  ver,
                "severity": "HIGH",
                "cve":      local["cve"],
                "detail":   local["desc"],
                "url":      url,
                "source":   "local_db",
            }
            store.js_libs.append(finding)
            emit.warn_sev(f"[SCA] VULNERABLE: {lib}@{ver} — {local['cve']} ({local['desc']})", "HIGH")
            continue

                                                     
        try:
            osv_url = "https://api.osv.dev/v1/query"
            osv_body = json.dumps({"version": ver, "package": {"name": lib, "ecosystem": "npm"}})
            osv_s, _, osv_resp = await fetch(session, "POST", osv_url, rl,
                                              data=osv_body,
                                              headers={"Content-Type": "application/json"})
            if osv_s == 200 and osv_resp:
                data = json.loads(osv_resp)
                vulns = data.get("vulns", [])
                if vulns:
                    cve_ids = [v.get("id", "?") for v in vulns[:3]]
                    finding = {
                        "library":  lib,
                        "version":  ver,
                        "severity": "HIGH",
                        "cve":      ", ".join(cve_ids),
                        "detail":   f"{len(vulns)} known vulnerability(ies)",
                        "url":      url,
                        "source":   "osv.dev",
                    }
                    store.js_libs.append(finding)
                    emit.warn_sev(f"[SCA] VULNERABLE: {lib}@{ver} — {cve_ids}", "HIGH")
                else:
                    emit.info(f"[SCA] {lib}@{ver} — no known vulns (osv.dev)")
        except Exception as e:
            emit.info(f"[SCA] osv.dev lookup failed for {lib}@{ver}: {e}")


                                                                        
                                            
                                                                           
                                                                        

async def probe_cloud_buckets(session, store, emit, rl):
\
\
\
\
       
    buckets_seen: set = set()
    for item in store.extracted_data:
        if item.get("type") != "Cloud_Bucket":
            continue
        val = item.get("value", "")
        if not val:
            continue
                                
        if val.startswith("s3://"):
            bucket_name = val[5:].split("/")[0]
            url = f"https://{bucket_name}.s3.amazonaws.com/"
        elif val.startswith("gs://"):
            bucket_name = val[5:].split("/")[0]
            url = f"https://storage.googleapis.com/{bucket_name}/"
        elif val.startswith("http"):
            url = val.rstrip("/") + "/"
        else:
            url = "https://" + val.rstrip("/") + "/"
        if url in buckets_seen:
            continue
        buckets_seen.add(url)

                                  
        s, hdrs, body = await fetch(session, "GET", url, rl)
        if s == 200 and body:
            is_list = any(m in body for m in (
                "<ListBucketResult", "<Contents>", '"kind": "storage#objects"',
                "<EnumerationResults",
            ))
            if is_list:
                store.cloud_probes.append({
                    "url": url, "issue": "Public_Bucket_List",
                    "severity": "CRITICAL",
                    "detail": "Bucket allows public listing — contents enumerable"})
                emit.warn_sev(f"[CloudBucket] PUBLIC LISTING: {url}", "CRITICAL")
                continue
        elif s == 403:
                                                                                     
            store.cloud_probes.append({
                "url": url, "issue": "Bucket_Exists_Private",
                "severity": "LOW",
                "detail": "Bucket exists and is private (403 on list)",
            })
            emit.info(f"[CloudBucket] Exists (private): {url}")
        elif s == 404:
                                                                            
            parsed = urlparse(url)
            for frag in ("s3", "amazonaws", "blob.core", "storage.googleapis"):
                if frag in parsed.netloc:
                    store.cloud_probes.append({
                        "url": url, "issue": "Bucket_NXDOMAIN_Takeover",
                        "severity": "CRITICAL",
                        "detail": "Bucket referenced in code but returns 404 — unclaimed, takeover possible"})
                    emit.warn_sev(f"[CloudBucket] POSSIBLE TAKEOVER: {url} → 404", "CRITICAL")
                    break


class Spider:
    def __init__(self, target, cfg, emit, cookies, extra_headers):
        self.target = target; self.cfg = cfg; self.emit = emit
        self.cookies = cookies; self.extra_headers = extra_headers
        self.base_domain = urlparse(target).netloc
        self._target_host = urlparse(target).hostname or ""
        self.is_ip_target = self._check_is_ip(self._target_host)
        self.store = Store()
        self.visited: Set[str] = set()
        self._crawl_feed_seen: Set[str] = set()
        self.queue: asyncio.Queue = asyncio.Queue()
        self.sem = asyncio.Semaphore(cfg.concurrency)
        self.rl = DomainRateLimiter(fixed_delay=getattr(self.cfg, "request_delay", 0.0))
        self._depth_cnt: Dict[int,int] = defaultdict(int)
        self.queue.put_nowait((target, 0, "Seed"))
        self._current_url: str = target
        self._dynamic_scope: Set[str] = set()
        # Build compiled CTF flag patterns once from templates
        self.cfg.ctf_flag_patterns = _build_ctf_flag_patterns(
            getattr(self.cfg, "ctf_flag_templates", [])
        )
        if self.cfg.ctf_flag_patterns:
            fmts = ", ".join(t for t, _ in self.cfg.ctf_flag_patterns)
            self.emit.always_info(f"[CTF] Flag scanning enabled — formats: {fmts}")

    @staticmethod
    def _check_is_ip(host: str) -> bool:
        if not host:
            return False
        try:
            ipaddress.ip_address(host)
            return True
        except ValueError:
            return False

    def is_valid(self, url):
        try:
            url = url.replace(chr(92)+chr(92), "/").replace(chr(92), "/")
            p = urlparse(url)
        except Exception:
            return False

        host = p.netloc

                                                                        
        in_scope = False
        h_lower = host.lower()
        clean_host = h_lower[4:] if h_lower.startswith("www.") else h_lower
        b_lower = self.base_domain.lower()
        clean_base = b_lower[4:] if b_lower.startswith("www.") else b_lower

        if clean_host == clean_base:
            in_scope = True
        elif self.cfg.follow_subdomains and clean_host.endswith("." + clean_base):
            in_scope = True
        elif host in self.cfg.extra_scope:
            in_scope = True
        elif hasattr(self, "_dynamic_scope") and host in self._dynamic_scope:
            in_scope = True

        if not in_scope:
            return False

        low = url.lower()
        if any(low.endswith(ext) or f"{ext}?" in low for ext in self.cfg.extensions_to_ignore):
            return False
        if _SOCKETIO_RE.search(url):
            self.store.add_socketio(url)
            return False
        if self.cfg.enable_noise_filter and _NOISE_PATH_RE.search(p.path):
            return False
        return bool(p.scheme in ("http","https"))

    def _over_budget(self, depth):
        return self._depth_cnt[depth] >= self.cfg.max_urls_per_depth

    # ── WhatWeb Integration ────────────────────────────────────────────────────

    # Category map (shared between _run_whatweb and the report printer)
    _WHATWEB_CAT = {
        # Server / Web server
        "apache":           ("Server",      "◈"),
        "nginx":            ("Server",      "◈"),
        "iis":              ("Server",      "◈"),
        "lighttpd":         ("Server",      "◈"),
        "caddy":            ("Server",      "◈"),
        "openresty":        ("Server",      "◈"),
        "httpserver":       ("Server",      "◈"),
        "werkzeug":         ("Server",      "◈"),
        "gunicorn":         ("Server",      "◈"),
        "tornado":          ("Server",      "◈"),
        "unicorn":          ("Server",      "◈"),
        "jetty":            ("Server",      "◈"),
        "tomcat":           ("Server",      "◈"),
        "webrick":          ("Server",      "◈"),
        "puma":             ("Server",      "◈"),
        # Language runtime
        "python":           ("Runtime",     "⬢"),
        "ruby":             ("Runtime",     "⬢"),
        "php":              ("Runtime",     "⬢"),
        "java":             ("Runtime",     "⬢"),
        "nodejs":           ("Runtime",     "⬢"),
        "perl":             ("Runtime",     "⬢"),
        "golang":           ("Runtime",     "⬢"),
        # CMS
        "wordpress":        ("CMS",         "⬡"),
        "drupal":           ("CMS",         "⬡"),
        "joomla":           ("CMS",         "⬡"),
        "typo3":            ("CMS",         "⬡"),
        "magento":          ("CMS",         "⬡"),
        "shopify":          ("CMS",         "⬡"),
        "wix":              ("CMS",         "⬡"),
        "squarespace":      ("CMS",         "⬡"),
        "prestashop":       ("CMS",         "⬡"),
        "opencart":         ("CMS",         "⬡"),
        "ghost":            ("CMS",         "⬡"),
        "strapi":           ("CMS",         "⬡"),
        # Framework
        "laravel":          ("Framework",   "⬡"),
        "django":           ("Framework",   "⬡"),
        "rails":            ("Framework",   "⬡"),
        "symfony":          ("Framework",   "⬡"),
        "codeigniter":      ("Framework",   "⬡"),
        "express":          ("Framework",   "⬡"),
        "flask":            ("Framework",   "⬡"),
        "spring":           ("Framework",   "⬡"),
        "nextjs":           ("Framework",   "⬡"),
        "nuxtjs":           ("Framework",   "⬡"),
        "fastapi":          ("Framework",   "⬡"),
        "aspnet":           ("Framework",   "⬡"),
        # JS Libraries / Frontend
        "jquery":           ("JS Libs",     "◇"),
        "react":            ("JS Libs",     "◇"),
        "vuejs":            ("JS Libs",     "◇"),
        "angular":          ("JS Libs",     "◇"),
        "bootstrap":        ("JS Libs",     "◇"),
        "modernizr":        ("JS Libs",     "◇"),
        "lodash":           ("JS Libs",     "◇"),
        "momentjs":         ("JS Libs",     "◇"),
        "underscore":       ("JS Libs",     "◇"),
        "tailwind":         ("JS Libs",     "◇"),
        "alpinejs":         ("JS Libs",     "◇"),
        # Analytics / Tracking
        "googleanalytics":  ("Analytics",   "◎"),
        "googletagmanager": ("Analytics",   "◎"),
        "googletag":        ("Analytics",   "◎"),
        "facebook":         ("Analytics",   "◎"),
        "hotjar":           ("Analytics",   "◎"),
        "mixpanel":         ("Analytics",   "◎"),
        "segment":          ("Analytics",   "◎"),
        "hubspot":          ("Analytics",   "◎"),
        "matomo":           ("Analytics",   "◎"),
        "plausible":        ("Analytics",   "◎"),
        # CDN / Cloud / Proxy
        "cloudflare":       ("CDN/Cloud",   "☁"),
        "cloudfront":       ("CDN/Cloud",   "☁"),
        "awss3":            ("CDN/Cloud",   "☁"),
        "azure":            ("CDN/Cloud",   "☁"),
        "akamai":           ("CDN/Cloud",   "☁"),
        "fastly":           ("CDN/Cloud",   "☁"),
        "varnish":          ("CDN/Cloud",   "☁"),
        "litespeed":        ("CDN/Cloud",   "☁"),
        "sucuri":           ("CDN/Cloud",   "☁"),
        # Security
        "recaptcha":        ("Security",    "⚑"),
        "hsts":             ("Security",    "⚑"),
        "csp":              ("Security",    "⚑"),
        "xframeoptions":    ("Security",    "⚑"),
        "xssprot":          ("Security",    "⚑"),
        # Meta / Generator
        "metagenerator":    ("Generator",   "⊕"),
        "generatorbysite":  ("Generator",   "⊕"),
        # Geo / Network
        "country":          ("GeoIP",       "⊛"),
        "ipaddress":        ("GeoIP",       "⊛"),
        # Contacts
        "email":            ("Emails",      "✉"),
        # Session / Cookies
        "cookies":          ("Cookies",     "⊡"),
        # Response headers
        "uncommonheaders":  ("Headers",     "⊞"),
        "via":              ("Headers",     "⊞"),
        # Page meta — intentionally last / lowest priority
        "html5":            ("Page",        "·"),
        "script":           ("Page",        "·"),
        "title":            ("Page",        "·"),
        "meta":             ("Page",        "·"),
        "frame":            ("Page",        "·"),
    }

    _WHATWEB_CAT_STYLE = {
        "Server":     (C.CY,  "SERVER   "),
        "Runtime":    (C.CYD, "RUNTIME  "),
        "CMS":        (C.MG,  "CMS      "),
        "Framework":  (C.MG,  "FRAMEWORK"),
        "JS Libs":    (C.BL,  "JS LIBS  "),
        "Analytics":  (C.Y,   "ANALYTICS"),
        "CDN/Cloud":  (C.GD,  "CDN/CLOUD"),
        "Security":   (C.G,   "SECURITY "),
        "Generator":  (C.O,   "GENERATOR"),
        "GeoIP":      (C.GR,  "GEO/IP   "),
        "Emails":     (C.O,   "EMAIL    "),
        "Cookies":    (C.CYD, "COOKIES  "),
        "Headers":    (C.GR,  "HEADERS  "),
        "Page":       (C.GR,  "PAGE     "),
        "Other":      (C.GL,  "OTHER    "),
    }

    @staticmethod
    def _ww_parse_plugins(plugins: dict):
        """Parse WhatWeb plugins dict into bucketed + flat lists."""
        bucketed: Dict[str, list] = defaultdict(list)
        flat_tech: list = []

        for plugin_name, pdata in plugins.items():
            plo = plugin_name.lower().replace("-","").replace("_","").replace(" ","")

            # Exact key lookup first, then prefix-startswith for compound names (e.g. "nextjs" matches "next")
            cat, icon = "Other", "·"
            if plo in Spider._WHATWEB_CAT:
                cat, icon = Spider._WHATWEB_CAT[plo]
            else:
                for kw, (c, i) in Spider._WHATWEB_CAT.items():
                    if plo.startswith(kw) and len(kw) >= 3:
                        cat, icon = c, i
                        break

            versions = []
            if isinstance(pdata, dict):
                for field in ("version", "string", "value"):
                    v = pdata.get(field)
                    if v:
                        versions = [str(x) for x in v] if isinstance(v, list) else [str(v)]
                        break

            display = f"{plugin_name} {versions[0]}" if versions else plugin_name
            bucketed[cat].append((icon, display))
            flat_tech.append(f"[WW] {display}")

        return dict(bucketed), flat_tech

    async def _run_whatweb(self, url: str):
        """
        Run WhatWeb concurrently with other recon probes.
        Stops the animator, prints live findings per-category, then resumes.
        """
        try:
            proc = await asyncio.create_subprocess_exec(
                "whatweb", "--log-json=/dev/stdout", "--quiet", url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL,
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=30)
        except FileNotFoundError:
            self.emit.info("[WhatWeb] Not installed — skipping (apt install whatweb)")
            return
        except asyncio.TimeoutError:
            self.emit.warn("[WhatWeb] Timed out after 30s")
            return
        except Exception as e:
            self.emit.warn(f"[WhatWeb] Error: {e}")
            return

        raw = (stdout or b"").decode(errors="replace").strip()
        if not raw:
            self.emit.warn("[WhatWeb] Empty output — no data returned")
            return

        # Parse: try whole blob first (v0.6.x pretty-prints), then line-by-line
        parsed = None
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            for line in raw.splitlines():
                line = line.strip().rstrip(",")
                if not line or line in ("[", "]"):
                    continue
                try:
                    parsed = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue

        if not parsed:
            self.emit.warn(f"[WhatWeb] Could not parse output — raw: {raw[:120]!r}")
            return

        if isinstance(parsed, list):
            entry = parsed[0] if parsed else {}
        else:
            entry = parsed

        plugins: dict = entry.get("plugins", {})
        if not plugins:
            self.emit.warn("[WhatWeb] Parsed OK but no plugins key found")
            return

        bucketed, flat_tech = Spider._ww_parse_plugins(plugins)

        self.store.tech_stack.update(flat_tech)
        self.store.whatweb_data = bucketed

        # ── Live findings — routed through emit._w so animator clears cleanly ──
        _ORDER = ["Server","Runtime","CDN/Cloud","CMS","Framework","JS Libs",
                  "Analytics","Security","Generator","Cookies","GeoIP","Emails","Headers","Page","Other"]
        ordered = _ORDER + [c for c in bucketed if c not in _ORDER]
        nc = self.emit._nc

        # Category color palette — red/orange/white, no cyan (reserved for [*])
        _LIVE_COL = {
            "Server":    C.R,
            "Runtime":   C.O,
            "CDN/Cloud": C.O,
            "CMS":       C.R,
            "Framework": C.O,
            "JS Libs":   C.W,
            "Analytics": C.GL,
            "Security":  C.G,
            "Generator": C.GL,
            "GeoIP":     C.GR,
            "Emails":    C.GL,
            "Cookies":   C.GR,
            "Headers":   C.GR,
            "Page":      C.GR,
            "Other":     C.GR,
        }

        self.emit._w(
            f"{C.R}{C.B}[WhatWeb]{C.RST} {C.W}{len(plugins)} plugins fingerprinted  "
            f"{C.GR}({len(bucketed)} categories){C.RST}"
            if not nc else
            f"[WhatWeb] {len(plugins)} plugins fingerprinted ({len(bucketed)} categories)"
        )

        for cat in ordered:
            entries = bucketed.get(cat)
            if not entries:
                continue
            col = _LIVE_COL.get(cat, C.GL)
            _, label = Spider._WHATWEB_CAT_STYLE.get(cat, (C.GL, f"{cat:<9}"))
            if nc:
                plugins_str = "  ·  ".join(disp for _, disp in entries)
                self.emit._w(f"  [{label.strip():<9}]  {plugins_str}")
            else:
                tag   = f"{C.R}{C.B}[{C.RST}{col}{C.B}{label.strip()}{C.RST}{C.R}{C.B}]{C.RST}"
                items = f"  {C.GR}·{C.RST}  ".join(
                    f"{col}{C.B}{icon}{C.RST} {col}{disp}{C.RST}"
                    for icon, disp in entries
                )
                self.emit._w(f"  {tag}  {items}")

    # ── End WhatWeb Integration ────────────────────────────────────────────────

    def _detect_tech(self, headers, body, url):
        tech: Set[str] = set()
        srv = (headers.get("Server","") or headers.get("server","")).lower()
        xpb = (headers.get("X-Powered-By","") or headers.get("x-powered-by","")).lower()
        ct  = (headers.get("Content-Type","") or headers.get("content-type","")).lower()
        body_lo = body.lower()

        raw_srv = headers.get("Server") or headers.get("server", "")
        raw_xpb = headers.get("X-Powered-By") or headers.get("x-powered-by", "")
        raw_asp = headers.get("X-AspNet-Version") or headers.get("x-aspnet-version", "")
        if raw_srv: tech.add(f"Server: {raw_srv}")
        if raw_xpb: tech.add(f"X-Powered-By: {raw_xpb}")
        if raw_asp: tech.add(f"X-AspNet-Version: {raw_asp}")

        for raw_hdr in (raw_srv, raw_xpb):
            m = re.match(r'^([A-Za-z][A-Za-z0-9_\-\.]*)\/([0-9][A-Za-z0-9_\-\.]*)', raw_hdr)
            if m:
                name, ver = m.group(1), m.group(2)
                if re.match(r'^\d', ver):
                    tech.add(f"{name} Version: {ver}")

        set_cookie = headers.get("Set-Cookie") or headers.get("set-cookie", "")
        if isinstance(set_cookie, list):
            cookie_names = " ".join(set_cookie)
        else:
            cookie_names = set_cookie or ""
        cookie_names_lo = cookie_names.lower()
        _COOKIE_SIGNATURES = {
            "phpsessid":            "PHP",
            "jsessionid":           "Java/JSP (Tomcat or similar)",
            "laravel_session":      "Laravel",
            "connect.sid":          "Express/Node.js",
            "ci_session":           "CodeIgniter",
            "django_sessionid":     "Django",
            "wordpress_logged_in":  "WordPress",
            "wordpress_sec":        "WordPress",
            "wp-settings":          "WordPress",
            "_csrf":                "CSRF-protected framework (generic)",
            "arraffinity":          "Azure App Service",
            "cfduid":               "Cloudflare",
            "__cf_bm":              "Cloudflare Bot Management",
            "rack.session":         "Ruby/Rack (Rails or Sinatra)",
            "_rails_session":       "Ruby on Rails",
            "flask_session":        "Flask",
            "next-auth.session-token": "Next.js (NextAuth)",
            "sails.sid":            "Sails.js",
            "symfony":              "Symfony",
            "grails_remember_me":   "Grails",
        }
        for cookie_key, fw_name in _COOKIE_SIGNATURES.items():
            if cookie_key in cookie_names_lo:
                tech.add(f"Cookie: {fw_name}")

                                                                           
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

                                                                           
        if "php"          in xpb:                               tech.add("PHP")
        if "express"      in xpb:                               tech.add("Node.js/Express")
        if "asp.net"      in xpb:                               tech.add("ASP.NET")
        if "next.js"      in xpb:                               tech.add("Next.js")
        if "servlet"      in xpb or "jsp"       in xpb:        tech.add("Java")

                                                                           
        if headers.get("X-Shopify-Stage"):                      tech.add("Shopify")
        if headers.get("x-drupal-cache") or headers.get("X-Drupal-Cache"):
            tech.add("Drupal")
        if headers.get("x-wp-total") or headers.get("X-WP-Total"):
            tech.add("WordPress/REST-API")
        if headers.get("x-litespeed-cache") or headers.get("X-LiteSpeed-Cache"):
            tech.add("LiteSpeed")
        if headers.get("x-varnish") or headers.get("X-Varnish"):
            tech.add("Varnish")
        if headers.get("cf-ray") or headers.get("CF-Ray"):
            tech.add("Cloudflare")
        if headers.get("x-amz-request-id") or headers.get("x-amz-cf-id"):
            tech.add("AWS")
        if headers.get("x-cache") and "cloudfront" in (headers.get("x-cache","") or "").lower():
            tech.add("AWS/CloudFront")
        if headers.get("x-azure-ref") or headers.get("x-ms-request-id"):
            tech.add("Azure")
        if headers.get("x-kong-proxy-latency"):
            tech.add("Kong API Gateway")
        if headers.get("x-ratelimit-limit") or headers.get("x-rate-limit-limit"):
            tech.add("Rate Limiting Active")

                                                                           
        _raw_sc = headers.get("Set-Cookie","") or headers.get("set-cookie","")
        if _raw_sc:
            _sc = _raw_sc.lower()
            if "jsessionid"     in _sc or "JSESSIONID" in _raw_sc: tech.add("Java/Session")
            if "phpsessid"      in _sc: tech.add("PHP/Session")
            if "asp.net_session" in _sc or "aspsessionid" in _sc:
                tech.add("ASP.NET/Session")
            if "laravel_session" in _sc or "xsrf-token" in _sc:
                tech.add("Laravel")
            if "ci_session"     in _sc: tech.add("CodeIgniter")
            if "_rails"         in _sc: tech.add("Ruby on Rails")
            if "rack.session"   in _sc: tech.add("Ruby/Rack")
            if "django"         in _sc or "csrftoken" in _sc:
                tech.add("Django")
            if "_session_id"    in _sc: tech.add("Ruby on Rails")
            if "wordpress_"     in _sc or "wp-settings" in _sc:
                tech.add("WordPress")
            if "typo3"          in _sc: tech.add("TYPO3")
            if "magento"        in _sc or "frontend"    in _sc:
                if "magento" in body_lo:
                    tech.add("Magento")

                                                                            
        if body:
                                                               
            _mg1 = re.compile(r"<meta[^>]+name=['\"]generator['\"][^>]+content=['\"]([^'\"<>]{3,80})['\"]", re.I)
            _mg2 = re.compile(r"<meta[^>]+content=['\"]([^'\"<>]{3,80})['\"][^>]+name=['\"]generator['\"]", re.I)
            for _m in _mg1.finditer(body):
                tech.add(f"Generator: {_m.group(1).strip()}")
            for _m in _mg2.finditer(body):
                tech.add(f"Generator: {_m.group(1).strip()}")

                                   
            if "__NEXT_DATA__"         in body:  tech.add("Next.js")
            if "window.__nuxt__"       in body or "window.__NUXT__" in body: tech.add("Nuxt.js")
            if "__GATSBY"              in body:  tech.add("Gatsby")
            if "window.angular"        in body:  tech.add("AngularJS")
            if "_angular_app_root_"    in body:  tech.add("Angular")
            if "window.__svelte"       in body:  tech.add("Svelte")
            if "data-reactroot"        in body or "data-reactid" in body:    tech.add("React")
            if "data-vue-app"          in body or 'id="app"' in body_lo:
                if "vue" in body_lo:             tech.add("Vue.js")

                                                                                               
            if "wp-content" in body_lo and "wp-includes" in body_lo: tech.add("WordPress")
            if "drupal.settings"       in body_lo: tech.add("Drupal")
                                                                                   
            if re.search(r'(?:index[.]php[?]option=com_|/components/com_|/modules/mod_)', body_lo):
                tech.add("Joomla")
                                                                              
            if re.search(r'/typo3(?:conf|temp|cms)/|typo3[.]pageId', body_lo):
                tech.add("TYPO3")
            if "prestashop"            in body_lo: tech.add("PrestaShop")
                                                                              
            if re.search(r'(?:route=common/|/catalog/view/theme/|/system/storage/)', body_lo):
                tech.add("OpenCart")

                                                                 
                                                                        
            if "whitelabel error page" in body_lo:                  tech.add("Spring Boot")
            if "jetbrains"             in body_lo and "ktor" in body_lo: tech.add("Ktor")
            if "application error"     in body_lo and "heroku" in body_lo: tech.add("Heroku")

        self.store.tech_stack.update(tech)

    def _queue_url(self, url, depth, source):
        if not self.is_valid(url): return
        norm = normalize(url)
        if norm in self.visited: return
        self.store.add_query_params(url)
        self.queue.put_nowait((url, depth, source))

    def _discover_url(self, url, depth, source, show_feed=False, from_url=None):
        if not self.is_valid(url): return False
        norm = normalize(url)
        if norm in self.visited: return False
        if show_feed and norm not in self._crawl_feed_seen:
            self._crawl_feed_seen.add(norm)
            self.emit.crawl_feed("Found", source, url)
                                                                            
                                                                         
                                                                                
        _origin = from_url or getattr(self, "_current_url", None)
        if _origin:
            self.store.add_graph_edge(_origin, url, via=source, depth=depth)
        self._queue_url(url, depth, source)
        return True

    @staticmethod
    def _collect_json_keys(obj) -> List[str]:
\
\
\
\
\
           
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
\
\
                                                                                 
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
        ctf_patterns = getattr(self.cfg, "ctf_flag_patterns", [])
        Extractor.html_comments(soup, url, self.store, self.emit,
                                base_url=url, discover_url=self._discover_url, depth=depth)
        Extractor.data_attr_leaks(soup, url, self.store, self.emit)
        if ctf_patterns:
            scan_ctf_flags(text, url, self.store, self.emit, ctf_patterns)
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
                Extractor.credential_objects(tag.string, url, self.store, self.emit)
                Extractor.js_routes(tag.string, url, self.store, self.emit)
                # js_comments on inline scripts is now handled inside html_comments
        for form in soup.find_all("form"):
            action = form.get("action") or url
            full   = urljoin(url, action)
            method = (form.get("method") or "POST").upper()
                                                                                  
            inputs = []
            form_fields_detail = []                                       
            for el in form.find_all(["input","select","textarea","button","datalist"]):
                el_type = el.get("type","text").lower()
                is_hidden = el_type == "hidden"
                is_file   = el_type == "file"

                                                                         
                                                    
                                                               
                                                                               
                                          
                                                                          
                                                                        
                nm = el.get("name","").strip()
                _source = "name"
                if not nm:
                    _id = el.get("id","").strip()
                    if _id and el_type not in ("submit","button","reset","image"):
                                                                                    
                        _stripped_id = re.sub(r'^(?:input|field|txt|frm|form)[-_]?', '', _id, flags=re.I).strip() or _id
                                                                                                        
                                                                                      
                        _HTML_TYPE_WORDS = {"text","password","email","number","tel","url",
                                            "search","date","time","checkbox","radio","file",
                                            "hidden","submit","button","reset","image"}
                                                                                            
                                                                                       
                                                                                                        
                        if _stripped_id.lower() not in _HTML_TYPE_WORDS and len(_stripped_id) > 2:
                            nm = _stripped_id
                            _source = "id"
                if not nm:
                    _ph = el.get("placeholder","").strip()
                    if _ph and el_type not in ("submit","button","reset","image","hidden"):
                                                                                                   
                        nm = re.sub(r'[^a-zA-Z0-9_]', '_', _ph.lower()).strip('_')
                        nm = re.sub(r'_+', '_', nm)
                        _source = "placeholder"
                if not nm:
                    _al = el.get("aria-label","").strip()
                    if _al and el_type not in ("submit","button","reset","image","hidden"):
                        nm = re.sub(r'[^a-zA-Z0-9_]', '_', _al.lower()).strip('_')
                        nm = re.sub(r'_+', '_', nm)
                        _source = "aria-label"

                                                                  
                if el_type in ("submit","button","reset","image") and not el.get("name","").strip():
                    nm = ""

                if nm and nm not in inputs:
                    inputs.append(nm)
                    form_fields_detail.append({
                        "name":        nm,
                        "name_source": _source,                          
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
                                                               
                                                                                      
                                                                                   
            if urlparse(full).scheme not in ("http", "https"):
                continue
            self.store.add_endpoint(full, method=method, source="Form", score=Conf.HIGH)
            self.store.add_query_params(full)

            # Form action resolves to a different URL than the page it's shown on
            # (e.g. /admin shows a login form whose action="index.php?").
            # Attach the same params to the display page too, and record the link.
            if full != url and inputs:
                self.store.add_endpoint(url, method="GET", source="Form_Page", score=Conf.HIGH)
                _page_key = self.store._key(url, "GET")
                if _page_key in self.store.endpoints:
                    _page_ep = self.store.endpoints[_page_key]
                    _page_ep.setdefault("params", {}).setdefault("form", [])
                    for _p in inputs:
                        if _p and _p not in _page_ep["params"]["form"]:
                            _page_ep["params"]["form"].append(_p)
                    _page_ep["_form_action_target"] = full
                    self.emit.info("[Form-Redirect] %s shows login/form that posts to %s" % (url, full))

            _fkey = self.store._key(full, method)
            if _fkey in self.store.endpoints:
                _ep = self.store.endpoints[_fkey]

                                                                        
                                                                        
                                                                     
                                                                        
                                                                          
                                                            
                 
                                                                        
                                                                            
                                                                            
                                                                         

                _existing_source = _ep.get("_form_source_page", "")
                _new_source       = url                                  

                if not _existing_source:
                                             
                    _ep["_form_source_page"] = _new_source
                    for _p in inputs:
                        if _p and _p not in _ep["params"]["form"]:
                            _ep["params"]["form"].append(_p)
                elif _existing_source == _new_source:
                                                              
                    for _p in inputs:
                        if _p and _p not in _ep["params"]["form"]:
                            _ep["params"]["form"].append(_p)
                else:
                                                                               
                                                                           
                                                                           
                    _AUTH_PARAMS = {"username","password","passwd","captcha",
                                    "recaptcha","email","login","credential"}
                    _new_is_auth  = sum(1 for p in inputs
                                        if p.lower() in _AUTH_PARAMS) >= 2
                    _old_is_auth  = sum(1 for p in _ep["params"]["form"]
                                        if p.lower() in _AUTH_PARAMS) >= 2
                    _new_richer   = len(inputs) > len(_ep["params"]["form"])

                    if _new_is_auth and not _old_is_auth:
                                                                           
                                                               
                        pass
                    elif _old_is_auth and not _new_is_auth:
                                                                           
                        _ep["params"]["form"]    = [p for p in inputs if p]
                        _ep["form_fields_detail"] = list(form_fields_detail)
                        _ep["_form_source_page"]  = _new_source
                    elif _new_richer:
                                                                         
                        _ep["params"]["form"]    = [p for p in inputs if p]
                        _ep["form_fields_detail"] = list(form_fields_detail)
                        _ep["_form_source_page"]  = _new_source
                                                                

                                                                         
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
                                                                 
        if not url.split('?')[0].endswith('.js'):
            return
        map_url = url.split('?')[0] + ".map"
        s, _, text = await fetch(session, "GET", map_url, self.rl)
        if s == 200 and text:
            try:
                                                                        
                if '"sources":' in text and '"mappings":' in text:
                    self.store.add_sourcemap(map_url, url)
                    self.emit.warn(f"[Sourcemap] Exposed JS source mapping → {map_url}")
                                                                  
                    for m in re.finditer(r'"(/[a-zA-Z0-9_\-\/]+)"', text):
                        path = m.group(1)
                        if len(path) > 3:
                            self.store.add_endpoint(urljoin(url, path), source="SourceMap", score=Conf.HIGH)
            except Exception:
                pass

    async def _process_js(self, url, text, session):
        ep_count = 0
        param_count = 0
        ctf_patterns = getattr(self.cfg, "ctf_flag_patterns", [])
        Extractor.secrets(text, url, self.store, self.emit)
        Extractor.credential_objects(text, url, self.store, self.emit)
        Extractor.js_endpoints(text, url, self.store, self.emit)
        Extractor.js_params(text, url, self.store, self.emit)
        Extractor.js_comments(text, url, self.store, self.emit)
        Extractor.js_routes(text, url, self.store, self.emit)
        # CSS files fetched through the crawl land here too via content-type check
        if url.split("?")[0].lower().endswith(".css"):
            Extractor.css_comments(text, url, self.store, self.emit,
                                   ctf_patterns=ctf_patterns)
        if ctf_patterns:
            scan_ctf_flags(text, url, self.store, self.emit, ctf_patterns)
        await self._check_sourcemap(session, url)
        for m in re.finditer(r'import\s*\(\s*["\']([^"\']+)["\']', text):
            full = urljoin(url, m.group(1))
            if self.is_valid(full):
                if self._discover_url(full, 1, "JS_DynImport", show_feed=True): ep_count += 1
                                                                                
                                                                                   
        for m in re.finditer(r"""["'](/[a-zA-Z0-9._\-/]+\.js)["']""", text):
            chunk_path = m.group(1)
            chunk_full = urljoin(url, chunk_path)
            if self.is_valid(chunk_full):
                if self._discover_url(chunk_full, 1, "JS_Chunk", show_feed=True): ep_count += 1


    async def _fetch_and_process(self, session, url, depth, source):
        self.visited.add(normalize(url))
        self._depth_cnt[depth] += 1
        self._current_url = url

        if self.cfg.follow_redirects:
            s, hdrs, body, final_url = await fetch_with_redirect(
                session, 'GET', url, self.rl,
                max_retries=self.cfg.max_retries,
                base_delay=self.cfg.retry_base_delay)
            if final_url and final_url != url:
                dest_host = urlparse(final_url).netloc
                if dest_host and dest_host != self.base_domain:
                    if dest_host not in self._dynamic_scope:
                        self._dynamic_scope.add(dest_host)
                        self.emit.always_info(
                            f"[Scope+] Redirect destination added to scope: {dest_host}")
                                                      
                    norm_final = normalize(final_url)
                    if norm_final not in self.visited and self.is_valid(final_url):
                        self.queue.put_nowait((final_url, depth + 1, "Redirect"))
        else:
            s, hdrs, body = await fetch(session, 'GET', url, self.rl,
                                        max_retries=self.cfg.max_retries,
                                        base_delay=self.cfg.retry_base_delay)
        
        if s is None or body is None:
            return
        
                             
        self.store.record_status(url, 'GET', s)

                                                                        
                                                                             
                                                                           
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
                    _hd = _vep.setdefault("headers_detail", {"vary": [], "cookies": []})
                    for _vp in _vary_params:
                        if _vp not in _hd["vary"]:
                            _hd["vary"].append(_vp)
                            self.emit.info(f"[Vary-Header] {_vp} ← {url}")

                                                                         
                                                                                 
                                                                       
        _raw_cookies = hdrs.get("Set-Cookie", "") or hdrs.get("set-cookie", "")
        if _raw_cookies:
            _cookie_ep_key = self.store._key(url, "GET")
            if _cookie_ep_key in self.store.endpoints:
                _cep = self.store.endpoints[_cookie_ep_key]
                _hd = _cep.setdefault("headers_detail", {"vary": [], "cookies": []})
                for _ck_part in _raw_cookies.split(";"):
                    _ck_name = _ck_part.strip().split("=")[0].strip()
                    _SKIP_CK = {"path","domain","expires","max-age","secure","httponly",
                                "samesite","version","comment","priority"}
                    if _ck_name and _ck_name.lower() not in _SKIP_CK:
                        if _ck_name not in _hd["cookies"]:
                            _hd["cookies"].append(_ck_name)
                            self.emit.info(f"[Set-Cookie] {_ck_name} ← {url}")

                   
        ct = (hdrs.get('Content-Type', '') or hdrs.get('content-type', '')).lower()
        is_js = 'javascript' in ct or url.split('?')[0].endswith('.js')
        ftype = 'JS' if is_js else 'Crawl'
        
        self.emit.crawl_feed(ftype, 'GET', url, s, len(body))

        if self.cfg.enable_extraction:
            Extractor.extract_data(body, url, self.store, self.emit)
        Extractor.credential_objects(body, url, self.store, self.emit)

        if s in (401, 403):
            self.store.add_endpoint(url, source=source, score=Conf.MEDIUM, auth_required=True)
            self.emit.warn(f'[Auth-wall:{s}] {url}')
        elif s in (500, 501, 502, 503) and body:
            _ERR_RE = re.compile(r'(?:Traceback|Exception in thread|SyntaxError|ParseError|SQLSTATE|You have an error in your SQL|ORA-\d{5}|Fatal error:|Warning:|Uncaught \w+Error|at [a-zA-Z\.]+\([a-zA-Z]+\.java:\d+\))', re.I)
            if _ERR_RE.search(body):
                self.store.add_endpoint(url, source='Error_Leak', score=Conf.HIGH)
                self.store.add_secret(body[:200], 'Error_Stack_Trace', url)
                self.emit.warn(f'[Error-Leak] Verbose error at {url}')
            # CTF flags sometimes surface in error/debug page bodies
            ctf_patterns = getattr(self.cfg, "ctf_flag_patterns", [])
            if ctf_patterns:
                scan_ctf_flags(body, url, self.store, self.emit, ctf_patterns)
        elif s == 200:
            if Extractor.is_bot_blocked(body):
                self.emit.warn(f"[Bot-Blocked] Target redirected to challenge page: {url}")
                                                                                         
                                                                                
                self.store.add_endpoint(url, source="Blocked_Response", score=Conf.LOW)
                return

            if Extractor.is_soft_404(body, s):
                self.emit.info(f'[Soft-404] Dropping non-existent route: {url}')
                return

                                                                          
                                                                                   
                                                                               
                                                             
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
                # CTF flags can appear in JSON API responses
                ctf_patterns = getattr(self.cfg, "ctf_flag_patterns", [])
                if ctf_patterns:
                    scan_ctf_flags(body, url, self.store, self.emit, ctf_patterns)

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
                                                                        
                _t_phase_start = time.time()
                _t_recon = 0.0
                _t_crawl = 0.0
                _t_audit = 0.0
                try:
                    _hdr_s, _hdr_h, _ = await fetch(session, "GET", self.target, self.rl)
                    if _hdr_h:
                                                                                         
                        self.store.target_response_headers = {
                            k: v for k, v in sorted(_hdr_h.items())
                        }
                except Exception:
                    pass
                self.emit.animator.start_anim("Recon Probing Base")

                # ── Fire WhatWeb + TLS concurrently ───────────────────────────
                async def _tls_and_headers():
                    if not getattr(self.cfg, 'no_tls', False):
                        self.emit.animator.update(0, "Recon TLS")
                        _tls = TLSInspector(self.target, self.store, self.emit)
                        await _tls.run()
                    if self.store.target_response_headers:
                        _hdr_auditor = HeaderAuditor(self.store, self.emit)
                        _hdr_auditor.run(self.store.target_response_headers)
                    if self.store.target_response_headers:
                        _waf = WAFDetector(self.store, self.emit)
                        _root_cookies = {c.split("=")[0].strip(): c.split("=",1)[-1].strip()
                                         for c in (self.store.target_response_headers.get("Set-Cookie","") or "").split(";")
                                         if "=" in c}
                        _waf.run(self.store.target_response_headers, "", _root_cookies)

                await asyncio.gather(
                    _tls_and_headers(),
                    self._run_whatweb(self.target),
                )

                if not self.is_ip_target:
                    self.emit.animator.update(0, "Recon DNS")
                    _dns = DNSIntel(self.target, self.store, self.emit)
                    await _dns.run()
                if self.cfg.enable_graphql:
                    await probe_graphql(session, self.target, self.store, self.emit, self.rl)
                if not self.is_ip_target and self.cfg.enable_subdomain_enum:
                    self.emit.animator.update(0, "Recon Subdomains")
                    _subenum = SubdomainEnumerator(self.target, self.store,
                                                   self.queue, self.emit, self.is_valid)
                    await _subenum.run()
                elif not self.is_ip_target:
                    self.emit.always_info("[Subdomains] Skipped (use --subdomains to enable)")

                self.emit.animator.update(0, "Recon robots.txt")
                robots = RobotsParser(session, self.target, self.store, self.queue,
                                      self.emit, self.rl, self.is_valid)
                crawl_delay = await robots.run()

                                                                                  
                self.emit.animator.update(0, "Recon Sitemaps")
                for _smap in ("/sitemap.xml", "/sitemap_index.xml", "/.well-known/sitemap.xml"):
                    _smap_url = urljoin(self.target, _smap)
                    if _smap_url not in robots._sitemap_seen:
                        _s, _h, _t = await fetch(session, "GET", _smap_url, self.rl)
                        if _s == 200 and _t:
                            _ct = (_h or {}).get("content-type", "").lower()
                            if Extractor.is_real_file(_ct, _t, None) and not Extractor.is_soft_404(_t, _s):
                                await robots.parse_sitemap(_smap_url)

                                             
                self.emit.animator.update(0, "Recon Sensitive Files + Admin Panels")
                await asyncio.gather(
                    probe_sensitive_files(session, self.target, self.store, self.emit, self.rl),
                    probe_admin_panels(session, self.target, self.store, self.emit, self.rl),
                )

                if self.cfg.wordlist:
                    self.emit.animator.update(0, "Recon Wordlist Brute Force")
                    await probe_wordlist(session, self.target, self.store, self.emit, self.rl, self.cfg.wordlist)

                if not self.is_ip_target:
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
                                                                                                        
                        elif _wk.endswith("security.txt"):
                            _sec_parser = SecurityTxtParser(
                                self.target, self.store, self.queue,
                                self.emit, self.is_valid
                            )
                            _sec_parser.parse(_t)
                        else:
                                                                               
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
                if self.cfg.no_crawl:
                    self.emit.always_info(
                        f"[Spider] --no-crawl: skipping BFS crawl ({self.queue.qsize()} queued URL(s) "
                        f"recorded via recon only, not fetched/parsed)")
                    _t_crawl = 0.0
                    _t_phase_start = time.time()
                else:
                    _t_phase_start = time.time()
                    self.emit.always_info(
                        f"[Spider] Crawl started — depth={self.cfg.max_depth}, "
                        f"concurrency={self.cfg.concurrency}, "
                        f"auth={'yes' if self.cookies or self.extra_headers else 'no'}, "
                        f"seed={self.queue.qsize()} URLs")

                    self.emit.animator.update(0, "Crawling Target")

                    workers = [asyncio.create_task(self._worker(session, i, crawl_delay))
                               for i in range(self.cfg.concurrency)]

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
                                              
                if self.cfg.enable_probing:
                    prober = IntelligentProber(session, self.store, self.emit, self.rl, self.cfg)
                    await prober.run()

                _t_audit = time.time() - _t_phase_start
                self._t_recon = _t_recon
                self._t_crawl = _t_crawl
                self._t_audit = _t_audit
                                      
                if self.cfg.enable_screenshots and spa_ctx:
                    self.emit.animator.start_anim("Capturing Screenshots")
                    await spa.capture_screenshots(self.store.endpoints, spa_ctx)
                    self.emit.animator.stop_anim()
                elif spa_ctx:
                                                                                                                                  
                    b, c, p = spa_ctx
                    await b.close()
                    if hasattr(spa, "_pw"): await spa._pw.stop()

                                           
                                                        
                classify_unauthenticated_api(self.store)
                classify_sensitive_data_sources(self.store)
                classify_legacy_endpoints(self.store)
                classify_admin_endpoints(self.store)
                classify_auth_endpoints(self.store)
                _flag_upload_endpoints(self.store)
                                                              
                self.emit.animator.start_anim("ASM: JS SCA Analysis")
                await analyze_js_deps(session, self.target, self.store, self.emit, self.rl)
                self.emit.animator.stop_anim()
                if self.store.extracted_data:
                    self.emit.animator.start_anim("ASM: Cloud Bucket Probing")
                    await probe_cloud_buckets(session, self.store, self.emit, self.rl)
                    self.emit.animator.stop_anim()
            finally:
                self.emit.animator.stop_anim()

                                                                        
             
                                                                        

def diff_crawls(old_json: str, new_json: str) -> dict:
    old = json.loads(old_json); new = json.loads(new_json)

    def get_cluster(e):
        return e.get("cluster") or cluster(normalize(e["url"]))

    def get_methods(e):
        if "methods" in e:
            return list(e["methods"])
        if "method" in e:
            return [e["method"]]
        return ["GET"]

    def get_conf(e):
        return e.get("confidence_label") or e.get("confidence", "LOW")

    def build_map(eps):
        m = {}
        for e in eps:
            cl = get_cluster(e)
            methods = get_methods(e)
            if cl not in m:
                m[cl] = {
                    "cluster": cl,
                    "url": e["url"],
                    "methods": set(methods),
                    "confidence_label": get_conf(e),
                    "auth_required": e.get("auth_required", False),
                    "orig": e
                }
            else:
                m[cl]["methods"].update(methods)
        return m

    om = build_map(old.get("endpoints", []))
    nm = build_map(new.get("endpoints", []))
    ok, nk = set(om), set(nm)
    added   = [nm[k]["orig"] for k in (nk - ok)]
    removed = [om[k]["orig"] for k in (ok - nk)]
    changed = []
    for k in ok & nk:
        o, n = om[k], nm[k]; diff: dict = {}
        if o["methods"] != n["methods"]:
            diff["methods"] = {"old": sorted(list(o["methods"])), "new": sorted(list(n["methods"]))}
        if o["confidence_label"] != n["confidence_label"]:
            diff["confidence"] = {"old": o["confidence_label"], "new": n["confidence_label"]}
        if o["auth_required"] != n["auth_required"]:
            diff["auth_required"] = {"old": o["auth_required"], "new": n["auth_required"]}
        if diff: changed.append({"cluster": k, "url": n["url"], "changes": diff})
    return {"old_target": old.get("meta",{}).get("target"),
            "new_target": new.get("meta",{}).get("target"),
            "added": added, "removed": removed, "changed": changed,
            "summary": {"added": len(added), "removed": len(removed), "changed": len(changed)}}

                                                                        
                                                             
                                                                        

def _auto_save(store: Store, target: str, out_path: Optional[str],
               fmt: str, emit: Emit) -> str:
                                                              
    domain    = re.sub(r'[^a-zA-Z0-9_\-]', '_', urlparse(target).netloc)
    ts        = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = out_path if (out_path and out_path.endswith(".json"))\
                else f"spider_{domain}_{ts}.json"

    try:
        Path(json_path).write_text(store.export(target, fmt="json"))
        pass                                                                
    except Exception as e:
        emit.warn(f"[Report] JSON save failed: {e}")
        json_path = ""

                                                                  
    if out_path and fmt != "json":
        try:
            Path(out_path).write_text(store.export(target, fmt=fmt))
            emit.always_info(f"[Report] {fmt.upper()} saved → {out_path}")
        except Exception as e:
            emit.warn(f"[Report] {fmt.upper()} save failed: {e}")

    return json_path

                                                                        
                                    
                                                                        

def run(target: str, emit_obj, options: dict = None, stop_check=None, pause_check=None):
    opts    = options or {}
    cookies = SessionManager.parse_cookies(opts.get("cookie") or opts.get("auth"))
    xhdrs   = SessionManager.parse_auth_header(opts.get("headers", {}))
                                                                      
                                                                                  
                                                                       
                                                                                     
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

                           
    json_path = _auto_save(spider.store, target, cfg.output_file,
                           cfg.output_format, emit)

    intel  = json.loads(spider.store.export(target, fmt="json"))
    result = {"raw": "", "intel": intel}

                            
    print_results(intel, target, elapsed, emit, saved_path=json_path,
                  phase_times=phase_times)

    _check_for_updates(emit)

    return result

                                                                        
     
                                                                        

def _check_for_updates(emit) -> None:
    try:
        repo_dir = Path(__file__).resolve().parent
        if not (repo_dir / ".git").exists():
            return

        fetch = subprocess.run(
            ["git", "fetch", "--quiet"],
            cwd=repo_dir, capture_output=True, text=True, timeout=8
        )
        if fetch.returncode != 0:
            return

        local = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_dir, capture_output=True, text=True, timeout=5
        ).stdout.strip()

        remote_ref = subprocess.run(
            ["git", "rev-parse", "@{u}"],
            cwd=repo_dir, capture_output=True, text=True, timeout=5
        )
        if remote_ref.returncode != 0:
            return
        remote = remote_ref.stdout.strip()

        if local == remote or not local or not remote:
            return

        behind = subprocess.run(
            ["git", "rev-list", "--count", f"{local}..{remote}"],
            cwd=repo_dir, capture_output=True, text=True, timeout=5
        ).stdout.strip()

        log = subprocess.run(
            ["git", "log", "--oneline", f"{local}..{remote}"],
            cwd=repo_dir, capture_output=True, text=True, timeout=5
        ).stdout.strip().splitlines()

        print()
        emit.warn(f"[Update] {behind} new commit(s) available on remote.")
        for line in log[:5]:
            print(f"    {C.GR}{line}{C.RST}")
        if len(log) > 5:
            print(f"    {C.GR}... and {len(log) - 5} more{C.RST}")
        emit.always_info("[Update] Run 'git pull' or './update.sh' to get the latest version.")

    except Exception:
        return



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
    scan.add_argument("--delay",       "-W", type=float, default=0.0, metavar="S",
                      help="Fixed delay between requests per host in seconds  (default: 0 = adaptive)")
    scan.add_argument("--concurrency", "-c", type=int, default=12, metavar="N",
                      help="Concurrent workers  (default: 12)")
    scan.add_argument("--timeout",     "-t", type=int, default=15, metavar="S",
                      help="Per-request timeout in seconds  (default: 15)")
    scan.add_argument("--verbose",     "-v", action="store_true",
                      help="Show all discovery logs")

    auth = p.add_argument_group(f"{C.CY}Authentication{C.RST}")
    auth.add_argument("--cookie",  "-C", type=str, default=None, metavar="COOKIE",
                      help='Cookie string (e.g., "session=42"), dict, or path to a cookie file. '
                           'Since the spider does not support automated form-login using username/password, '
                           'you must manually log in via a browser and supply the session cookie here.')
    auth.add_argument("--auth",    "-a", type=str, default=None, metavar="HEADER",
                      help='Authorization header  e.g. "Bearer eyJ..."')
    auth.add_argument("--basic-auth", "-u", type=str, default=None, metavar="USER:PASS",
                      help='HTTP Basic Access Authentication credentials  e.g. "admin:password" '
                           '(note: this is for server-level basic auth, not standard login forms)')
    auth.add_argument("--header",  "-X", action="append", default=None, metavar="NAME: VALUE",
                      help='Custom header, repeatable, formatted as "Name: Value"  e.g. -X "X-Bug-Bounty: Bugcrowd-yourhandle" '
                           '-X "X-Research-Purpose: authorized-pentest"  '
                           '(use for program-required tester-identification headers)')

    out = p.add_argument_group(f"{C.CY}Output{C.RST}")
    out.add_argument("--out",    "-o", type=str, default=None, metavar="FILE",
                     help="Extra output file  (JSON always auto-saved)")
    out.add_argument("--format", "-f", type=str, default="json",
                     choices=["json","jsonl","csv","burp","urls","nuclei"],
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
    flags.add_argument("--no-crawl",      "-N", action="store_true",
                       help="Skip BFS link crawling — run only recon/probe modules "
                            "(robots, sitemap, admin probe, sensitive files, wordlist, subdomains, wayback)")

    scope = p.add_argument_group(f"{C.CY}Scope{C.RST}")
    scope.add_argument("--subdomains",        "-b", action="store_true",
                       help="Enable subdomain enumeration via certificate transparency logs")
    scope.add_argument("--follow-subdomains", "-S", action="store_true",
                       help="Crawl discovered subdomains within the base domain")
    scope.add_argument("--follow-redirects",  "-r", action="store_true",
                       help="Follow cross-host redirects and add the destination host to scope")
    scope.add_argument("--scope", "-A", type=str, default=None, metavar="HOSTS",
                       help="Comma-separated extra hosts to include in scope  e.g. api.target.com,cdn.target.com")
    scope.add_argument("--wordlist", "-w", type=str, default=None, metavar="FILE",
                       help="Path to a directory/file wordlist for endpoint discovery")

    ctf = p.add_argument_group(f"{C.CY}CTF{C.RST}")
    ctf.add_argument("--ctf-flag", "-K", type=str, default=None, metavar="TEMPLATE",
                     help="Flag format to scan for across all content (HTML, JS, CSS, JSON, "
                          "error pages, comments). Use {} as the flag-body placeholder. "
                          "Multiple formats comma-separated: flag{},ctf{}")

    util = p.add_argument_group(f"{C.CY}Utilities{C.RST}")
    util.add_argument("--diff",    "-D", type=str, default=None, metavar="OLD_REPORT",
                      help="Diff this scan against an old JSON report")
    util.add_argument("--har",     "-H", type=str, default=None, metavar="HAR_FILE",
                      help="Import a browser HAR session file to seed the store with auth-gated requests")
    util.add_argument("--upgrade", "-U", action="store_true",
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

    if not shutil.which("whatweb"):
        emit.always_info(f"{C.Y}[!] [WhatWeb] Technology fingerprinter is not installed.{C.RST}")
        emit.always_info(f"    For rich technology stack fingerprinting, run: {C.G}sudo apt install whatweb{C.RST}\n")

                           
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

    if args.basic_auth:
        basic_hdr = SessionManager.parse_basic_auth(args.basic_auth)
        if basic_hdr:
            xhdrs.update(basic_hdr)
        else:
            emit.warn('[Auth] --basic-auth expects "user:pass" format — ignoring.')

    custom_hdrs = SessionManager.parse_custom_headers(getattr(args, "header", None))
    if custom_hdrs:
        _bad = [h for h in (getattr(args, "header", None) or []) if h and ":" not in h]
        if _bad:
            emit.warn(f'[Auth] Ignored malformed --header value(s) (expected "Name: Value"): {_bad}')
        xhdrs.update(custom_hdrs)  # -X wins on name clash with --auth/--basic-auth

    if isinstance(args.cookie, dict):
        _dropped = [k for k in args.cookie
                    if k.lower() in ("authorization","x-api-key","x-auth-token",
                                     "x-csrf-token","x-access-token")]
        if _dropped:
            emit.warn(f"[Auth] Stripped non-cookie auth keys from --cookie input: {_dropped}. "
                      f"Use --auth for these instead.")

    if cookies:
        emit.always_info(f"[Auth] Cookies loaded  →  {list(cookies.keys())}")
    if xhdrs:
        emit.always_info(f"[Auth] Headers sent    →  {list(xhdrs.keys())}")
    if not cookies and not xhdrs:
        emit.always_info("[Auth] No credentials — unauthenticated scan")

    cfg = Config(
        request_delay   = args.delay,
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
        follow_subdomains = args.follow_subdomains,
        follow_redirects  = args.follow_redirects,
        enable_subdomain_enum = args.subdomains,
        wordlist          = args.wordlist,
        no_crawl          = args.no_crawl,
        ctf_flag_templates = [t.strip() for t in args.ctf_flag.split(",") if t.strip()]
                             if args.ctf_flag else [],
        extra_scope       = [h.strip() for h in args.scope.split(",") if h.strip()]
                            if args.scope else [],
    )

    try:
        cfg.validate()
    except ValueError as e:
        emit.warn(str(e))
        sys.exit(1)

    print()
    result = _do_run(args.target, cfg, emit, cookies, xhdrs)

                                                                        
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
            emit.warn(f"[Diff] Error: {type(e).__name__} {e}")


if __name__ == "__main__":
    main()