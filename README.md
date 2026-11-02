<p align="center">
  <img src="Images/spider.jpg" alt="Hellhound Spider" width="600"/>
</p>

<h1 align="center">Hellhound Spider</h1>

<p align="center">
  Fully autonomous web crawler for security testing — maps endpoints, parameters, and security issues across traditional and SPA web applications. Drop a URL. Walk away.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/version-14.2-red?style=flat-square"/>
  <img src="https://img.shields.io/badge/pypi-hellhound--spider-blue?style=flat-square&logo=pypi&logoColor=white"/>
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square"/>
  <img src="https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square"/>
</p>
<p align="center">
  <a href="https://devlist.app/listings/hellhound-spider"><img src="https://devlist.app/badges/listed-on-devlist-large.svg" alt="Listed on DevList"/></a>
</p>

---

## What It Does

Hellhound Spider crawls a web application and produces a complete map of every endpoint, parameter, and security surface it can reach. The output is a structured JSON report — sorted by confidence, with parameters grouped by source, ready to feed directly into attack agents or import into Burp Suite.

It runs two crawl engines in parallel: async HTTP workers for speed, and headless Chromium for JavaScript-heavy SPAs. For SPAs it intercepts live XHR and fetch calls as the browser actually makes them — including POST body parameters and response IDs. Once the forward crawl is done, it also walks back up every discovered path to probe ancestor directories that were never directly linked to, the way a directory brute-forcer would. When the crawl finishes, it classifies every endpoint automatically so downstream agents start with context, not cold discovery.

Output pipes straight into other tools — `spider https://target.com | httpx` just works, no extra flag needed.

---

## Installation

### via pip (any OS)

```bash
pip install hellhound-spider
```

This gets you the core crawler — HTTP-only scanning (`--no-playwright`) works right away. Everything else is opt-in, since not everyone needs a headless browser just to crawl:

```bash
pip install "hellhound-spider[spa]"   # SPA scanning: Playwright + Patchright
playwright install chromium           # the browser binary itself — not a pip package, separate ~150MB download

pip install "hellhound-spider[dns]"   # full DNS intel (SPF/DMARC/MX via dnspython)
pip install "hellhound-spider[full]"  # spa + dns together
```

One thing pip genuinely can't install for you: **WhatWeb** (optional technology fingerprinting) is a system binary, not a Python package — `apt install whatweb` (or your distro's equivalent) if you want it. Spider runs fine without it either way.

### From source (Linux / macOS)

```bash
git clone https://github.com/project-hellhound-org/hellhound-spider.git
cd hellhound-spider
chmod +x install.sh
./install.sh
```

The installer creates an isolated virtual environment (`.venv`), handles Playwright/Patchright/WhatWeb for you interactively, and installs a system-wide `spider` wrapper — this is the same thing `pip install` gives you, just with the optional pieces walked through for you instead of opt-in flags.

```bash
spider https://target.com
```

### Uninstall

```bash
./uninstall.sh                   # if installed via install.sh
pip uninstall hellhound-spider   # if installed via pip
```

---

## Usage

```bash
spider <target> [options]
```

A handful of the flags you'll actually reach for day to day:

```
-d, --depth            Maximum crawl depth              (default: 4)
-c, --concurrency       Concurrent async workers          (default: 12)
-C, --cookie            Session cookie string or cookie file
-a, --auth              Authorization header, e.g. "Bearer eyJ..."
-x, --extract           Extract emails, IPs, cloud buckets, secrets
-s, --screenshot        Capture screenshots (all/standard/api/admin/...)
-f, --format            json / jsonl / csv / burp / urls / nuclei
-o, --out               Output file path
-v, --verbose           Show all discovery logs
    --ctf                CTF mode — probes, CORS, flag scanning, high concurrency
```

That's the short list. Spider has a lot more surface than that — auth, scope control, modular probing, SPA interaction, HAR replay, subdomain enumeration, and more. Run `spider --help` or `man spider` for the full, always-current reference rather than relying on a table here that can drift out of sync with the tool.

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## Examples

```bash
# Basic scan — drop a URL, spider does the rest
spider https://target.com

# Authenticated with a session cookie
spider https://target.com -C "session=abc123; csrf=xyz"

# Authenticated with Bearer token / HTTP Basic Auth
spider https://target.com -a "Bearer eyJhbGci..."
spider https://target.com -u "admin:password"

# Pipe discovered URLs straight into another tool
spider https://target.com | httpx
spider https://target.com | nuclei -t cves/

# Export for Burp Suite
spider https://target.com -f burp -o burp.xml

# Extraction and screenshots
spider https://target.com -x -s all

# Deeper crawl, all logs visible
spider https://target.com -d 6 -v

# Seed crawl with a HAR file (authenticated session replay)
spider https://target.com --har session.har

# Scan and extract specific CTF flags from all source files and comments
spider https://target.com --ctf-flag "HELLCORP{},FLAG{}"
```

---

## What Gets Found

### Discovery Vectors

HTML crawl, live SPA XHR interception, parent-directory backtracking (probes ancestor directories the forward crawl never linked to), Intelligent Robots Analysis (Disallow/Allow mapping + comment mining), sitemap XML (with index recursion), `.well-known` (OIDC/JWKS), JSON path chaining, SPA hash routes, lazy-load attributes, CSP header hints, OpenAPI/Swagger specs, GraphQL introspection, crt.sh certificate transparency, Wayback Machine CDX API, security.txt (RFC 9116), HAR file import, HTML comment mining, response header analysis, TLS/DNS intel, WAF fingerprinting, and JS SCA analysis.

### Parameter Mining

Form fields (with type metadata: hidden, file, required), JS fetch/axios body keys, URL query strings, OpenAPI spec fields, POST body params from live browser requests, structural normalization (clustering dynamic segments).

---

## Output Formats

- **JSON** — Full-fidelity report with all classification metadata.
- **Burp** — XML format for direct import into Burp Suite.
- **CSV** — Spreadsheet-ready endpoint and parameter list.
- **JSONL** — One endpoint per line for streaming pipelines.
- **URLs** — Raw newline-separated list of discovered URLs (the default when piped to another tool).
- **Nuclei** — Target list formatted for direct piping into Nuclei.

---

## Requirements

- Python 3.10+
- `aiohttp`, `beautifulsoup4`, `lxml`
- Playwright + Chromium *(optional, for SPA targets)*
- Patchright *(optional, automatic bot-bypass fallback when WAF blocks Playwright)*
- WhatWeb *(optional, automatic system technology fingerprinter; installed by install.sh)*

---

For authorized security testing only. This software is licensed under the **GNU General Public License v3 (GPLv3)**.

---

## Author

<a href="https://l4zz3rj0d.github.io">
  <img src="https://img.shields.io/badge/Founder-L4ZZ3RJ0D-c0392b?style=for-the-badge" alt="L4ZZ3RJ0D"/>
</a>