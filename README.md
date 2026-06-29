<p align="center">
  <img src="Images/spider.jpg" alt="Hellhound Spider" width="600"/>
</p>

<h1 align="center">Hellhound Spider</h1>

<p align="center">
  Fully autonomous web crawler for security testing — maps endpoints, parameters, and security issues across traditional and SPA web applications. Drop a URL. Walk away.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/version-13.19-red?style=flat-square"/>
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square"/>
  <img src="https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square"/>
</p>

---

## What It Does

Hellhound Spider crawls a web application and produces a complete map of every endpoint, parameter, and security surface it can reach. The output is a structured JSON report — sorted by confidence, with parameters grouped by source, ready to feed directly into attack agents or import into Burp Suite.

It runs two crawl engines in parallel: async HTTP workers for speed, and headless Chromium for JavaScript-heavy SPAs. For SPAs it intercepts live XHR and fetch calls as the browser actually makes them — including POST body parameters and response IDs. When the crawl finishes, it classifies every endpoint automatically so downstream agents start with context, not cold discovery.

---

## Installation

### Linux / macOS

```bash
git clone https://github.com/project-hellhound-org/hellhound-spider.git
cd hellhound-spider
chmod +x install.sh
./install.sh
```

The installer creates an isolated virtual environment (`.venv`) and a system-wide `spider` wrapper:

```bash
spider https://target.com
```

A man page is also installed — run `man spider` for the full reference.

### Windows

```bash
git clone https://github.com/project-hellhound-org/hellhound-spider.git
cd hellhound-spider
pip install -e .                    # core install
pip install -e ".[spa]"             # with Playwright SPA support
playwright install chromium
```

### Uninstall

```bash
./uninstall.sh           # Linux / macOS
pip uninstall hellhound-spider   # Windows
```

---

## v13.19 — Modular Probing & JS Interpolation

v13.19 introduces opt-in modular probing (admin panels, sensitive files, and Wayback machine queries are now off by default for faster baseline scans) and adds detection for dynamic runtime values in JavaScript endpoint extraction.

### New in v13.19

- **Opt-in Modular Probing** (`--probe`, `--admin-probe`, `--sensitive-probe`, `--wayback`) — Probing for admin panels, sensitive files, and Wayback Machine archived URLs is now off by default. Use the new flags to enable them when appropriate.
- **Dynamic JS Value Detection** — JavaScript endpoint extraction now detects template-literal paths containing runtime interpolations (e.g. `/api/user/${id}`) and flags them as requiring dynamic values.

---

## Interface Preview

<p align="center">
  <img src="Images/Interface.png" alt="Hellhound Spider Interface" width="800"/>
</p>

<p align="center">
  <img src="Images/Discovery.png" alt="Discovery Results" width="800"/>
</p>

<p align="center">
  <img src="Images/crawl_details.png" alt="Crawl Details" width="800"/>
</p>

---

## Automated Evidence Collection

The spider can automatically capture screenshots of high-value targets (admin panels, login pages, API documentation) during the crawl.

```bash
spider http://127.0.0.1:5000 --extract --screenshot all
```

<p align="center">
  <img src="Images/spider_screenshot.jpeg" alt="Automated Screenshot 1" width="800"/>
</p>

<p align="center">
  <img src="Images/spider_screenshot2.jpg" alt="Automated Screenshot 2" width="800"/>
</p>

---

## Usage

```
spider <target> [options]
```

### Scan Options

| Flag | Short | Default | Description |
|---|---|---|---|
| `--depth` | `-d` | `4` | Maximum crawl depth |
| `--concurrency` | `-c` | `12` | Concurrent async workers |
| `--timeout` | `-t` | `15` | Per-request timeout in seconds |
| `--delay` | `-W` | `0.0` | Delay between requests in seconds |
| `--verbose` | `-v` | off | Show all discovery logs |

### Authentication

| Flag | Short | Description |
|---|---|---|
| `--cookie` | `-C` | Cookie string `"name=value"` or path to a cookie file. Since standard form-login is not supported, log in manually via browser and pass active session cookies here. |
| `--auth` | `-a` | Authorization header value e.g. `"Bearer eyJ..."` |
| `--basic-auth` | `-u` | HTTP Basic Access Authentication credentials e.g. `"admin:password"` (not for standard login forms) |
| `--header` | `-X` | Custom header formatted as `"Name: Value"`, repeatable. |

### Output

| Flag | Short | Default | Description |
|---|---|---|---|
| `--out` | `-o` | auto-named | Output file path |
| `--format` | `-f` | `json` | `json` `jsonl` `csv` `burp` `urls` `nuclei` |

### Feature Flags

| Flag | Short | Description |
|---|---|---|
| `--no-playwright` | `-P` | HTTP crawl only, no headless browser |
| `--probe` | `-p` | Enable intelligent probing phase |
| `--admin-probe` | `-m` | Probe common admin/management panel paths |
| `--sensitive-probe` | `-e` | Probe known sensitive file paths |
| `--wayback` | `-y` | Query the Wayback Machine for archived URLs |
| `--spa-interact` | `-I` | Enable SPA form filling and button clicking |
| `--no-cors` | `-R` | Skip CORS misconfiguration checks |
| `--no-graphql` | `-G` | Skip GraphQL introspection probe |
| `--no-openapi` | `-O` | Skip OpenAPI / Swagger discovery |
| `--extract` | `-x` | Enable passive data extraction (emails, IPs, buckets) |
| `--screenshot` | `-s` | Capture screenshots. Preset: `all`, `standard`, `blocked`, `errors`, `api`, `admin`, or custom regex |
| `--no-filter` | `-F` | Disable noise path filter (include repo-browser and CDN paths) |
| `--no-crawl` | `-N` | Skip BFS crawling — run only recon and enabled opt-in probe modules |
| `--har` | | Seed crawl from a browser-exported HAR file |

### Scope

| Flag | Short | Description |
|---|---|---|
| `--subdomains` | `-b` | Enable subdomain enumeration via certificate transparency logs |
| `--follow-subdomains` | `-S` | Crawl discovered subdomains within the base domain |
| `--follow-redirects` | `-r` | Follow cross-host redirects and add destination to scope |
| `--scope` | `-A` | Comma-separated extra hosts to include in scope |
| `--wordlist` | `-w` | Path to a directory/file wordlist for endpoint discovery |

### CTF

| Flag | Short | Description |
|---|---|---|
| `--ctf-flag TEMPLATE` | `-K` | Flag format to scan for across all content (e.g. `HELLCORP{}`, `HTB{}`). Placeholder `{}` expands to flag body. Supports comma-separated templates. |

### Utilities

| Flag | Short | Description |
|---|---|---|
| `--diff OLD_REPORT` | `-D` | Diff this scan against a previous JSON report |
| `--upgrade` | `-U` | Pull latest version |

---

## Examples

```bash
# Basic scan — drop a URL, spider does the rest
spider https://target.com

# Authenticated with a session cookie
spider https://target.com -C "session=abc123; csrf=xyz"

# Authenticated with a JWT
spider https://target.com -C "token=eyJhbGci..."

# Authenticated with Bearer token
spider https://target.com -a "Bearer eyJhbGci..."

# Authenticated with HTTP Basic Auth
spider https://target.com -u "admin:password"

# Authenticated with custom HTTP headers
spider https://target.com -X "X-Bug-Bounty: handle" -X "X-Research-Purpose: testing"

# Load cookies from a browser-exported file
spider https://target.com -C /path/to/cookies.txt

# Deeper crawl, all logs visible
spider https://target.com -d 6 -v

# Export for Burp Suite
spider https://target.com -f burp -o burp.xml

# Extraction and screenshots
spider https://target.com -x -s all

# No headless browser (HTTP only)
spider https://target.com -P

# Diff two scans
spider https://target.com -D previous.json

# SPA with form interaction enabled
spider https://target.com -I -v

# Disable noise filter to see everything (including CDN/repo paths)
spider https://target.com -F

# Seed crawl with a HAR file (authenticated session replay)
spider https://target.com --har session.har

# Combine HAR seed + extraction + screenshots
spider https://target.com --har session.har -x -s all

# Scan and extract specific CTF flags from all source files and comments
spider https://target.com --ctf-flag "HELLCORP{},FLAG{}"
```

---

## What Gets Found

### Discovery Vectors

HTML crawl, live SPA XHR interception, Intelligent Robots Analysis (Disallow/Allow mapping + Comment Mining), sitemap XML (with index recursion), `.well-known` (OIDC/JWKS), JSON path chaining, SPA hash routes, lazy-load attributes, CSP header hints, OpenAPI/Swagger specs, GraphQL introspection, **crt.sh certificate transparency**, **Wayback Machine CDX API**, **security.txt (RFC 9116)**, **HAR file import**, **HTML comment mining**, **response header analysis**, **TLS/DNS Intel**, **WAF fingerprinting**, and **JS SCA Analysis**.

### Parameter Mining

Form fields (with type metadata: hidden, file, required), JS fetch/axios body keys, URL query strings, OpenAPI spec fields, POST body params from live browser requests, structural normalization (clustering dynamic segments).



---

## Output Formats

- **JSON** — Full-fidelity report with all classification metadata, orphan params, and socket.io section.
- **Burp** — XML format for direct import into Burp Suite.
- **CSV** — Spreadsheet-ready endpoint and parameter list.
- **JSONL** — One endpoint per line for streaming pipelines.
- **URLs** — Raw newline-separated list of discovered URLs.
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