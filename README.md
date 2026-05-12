<p align="center">
  <img src="Images/spider.jpg" alt="Hellhound Spider" width="600"/>
</p>

<h1 align="center">Hellhound Spider</h1>

<p align="center">
  Fully autonomous web crawler for security testing — maps endpoints, parameters, and security issues across traditional and SPA web applications. Drop a URL. Walk away.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/version-12.4-red?style=flat-square"/>
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square"/>
  <img src="https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square"/>
</p>

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

## v12.4 — Autonomous Assistant Update

v12.4 makes the Spider a fully autonomous recon assistant. You give it a URL — it does the rest, makes smart decisions, and produces output that humans can read and agents can consume directly.

**Noise Filter** — Repository browser paths (`/blob/`, `/tree/`, `/commits/`, etc.), CDN artefacts, and structural UI links are now detected and suppressed before they ever enter the endpoint store. The real API surface is no longer buried in 80+ GitHub viewer fake-endpoints.


**JS Orphan Params** — Parameters found in JS files that can't be resolved to a real API endpoint are stored separately as `js_orphan_params` — labelled as wordlist hints, never as injectable targets. The terminal shows them in a dedicated section with a red warning so they can't be confused for real attack surface.

**Form Field Intelligence** — Every form field now carries rich metadata: `type`, `hidden`, `file`, `required`. Hidden CSRF tokens are flagged `[hidden]` in the param map. File inputs are flagged `[file]`. Downstream agents can skip CSRF tokens and prioritise real injectable fields without any guesswork.

**Robots Tree** — The ROBOTS DISALLOWED section now shows all child endpoints found under each disallowed path as a tree. First 5 shown inline, overflow shown as `[+N more — see JSON report]`.

**Shorthand Flags** — Every flag now has a short single-letter alias. `-d`, `-c`, `-t`, `-v`, `-C`, `-a`, `-o`, `-f`, `-x`, `-s`, `-D` — full list below.


---

## What It Does

Hellhound Spider crawls a web application and produces a complete map of every endpoint, parameter, and security surface it can reach. The output is a structured JSON report — sorted by confidence, with parameters grouped by source, ready to feed directly into attack agents or import into Burp Suite.

It runs two crawl engines in parallel: async HTTP workers for speed, and headless Chromium for JavaScript-heavy SPAs. For SPAs it intercepts live XHR and fetch calls as the browser actually makes them — including POST body parameters and response IDs. When the crawl finishes, it classifies every endpoint automatically and scores injection candidates so downstream agents start with context, not cold discovery.

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
| `--verbose` | `-v` | off | Show all discovery logs |

### Authentication

| Flag | Short | Description |
|---|---|---|
| `--cookie` | `-C` | Cookie string `"name=value"` or path to a cookie file |
| `--auth` | `-a` | Authorization header value e.g. `"Bearer eyJ..."` |

### Output

| Flag | Short | Default | Description |
|---|---|---|---|
| `--out` | `-o` | auto-named | Output file path |
| `--format` | `-f` | `json` | `json` `jsonl` `csv` `burp` |

### Feature Flags

| Flag | Short | Description |
|---|---|---|
| `--no-playwright` | `-P` | HTTP crawl only, no headless browser |
| `--no-probing` | `-p` | Skip Method Oracle and CORS probes |
| `--spa-interact` | `-I` | Enable SPA form filling and button clicking |
| `--no-cors` | `-R` | Skip CORS misconfiguration checks |
| `--no-graphql` | `-G` | Skip GraphQL introspection probe |
| `--no-openapi` | `-O` | Skip OpenAPI / Swagger discovery |
| `--extract` | `-x` | Enable passive data extraction (emails, IPs, buckets) |
| `--screenshot` | `-s` | Capture screenshots. Preset: `all`, `standard`, `blocked`, `errors`, `api`, `admin`, or custom regex |
| `--no-filter` | `-F` | Disable noise path filter (include repo-browser and CDN paths) |

### Utilities

| Flag | Short | Description |
|---|---|---|
| `--diff OLD_REPORT` | `-D` | Diff this scan against a previous JSON report |
| `--upgrade` | | Pull latest version |

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
```

---

## What Gets Found

### Discovery Vectors

HTML crawl, live SPA XHR interception, Intelligent Robots Analysis (Disallow/Allow mapping + Comment Mining), sitemap XML, `.well-known` (OIDC/JWKS), JSON path chaining, SPA hash routes, lazy-load attributes, CSP header hints, OpenAPI/Swagger specs, GraphQL introspection.

### Parameter Mining

Form fields (with type metadata: hidden, file, required), JS fetch/axios body keys, URL query strings, OpenAPI spec fields, POST body params from live browser requests, structural normalization (clustering dynamic segments).

### Passive Security Detection

| Signal | Description |
|---|---|
| `[SECRET:*]` | API keys, JWTs, Bitcoin/Ethereum addresses, private keys |
| `[SourceMap]` | Exposed `.js.map` files leaking original source code |
| `[Tech]` | Server/version headers (Server, X-Powered-By, X-AspNet-Version) |
| `[CORS]` | Wildcard or reflected CORS misconfiguration |
| `[Error-Leak]` | Verbose stack traces or DB errors in 5xx responses |
| `[Geo-Leak]` | Latitude/longitude coordinates exposed in JSON API responses |
| `[Auth-wall:*]` | Endpoints returning 401/403 |
| `[Robots-Leak]` | Sensitive keywords in `robots.txt` comments |
| `[Email]` | Email addresses found in JS/HTML content |
| `[IP]` | Internal RFC1918 IP addresses leaked in content |
| `[CloudBucket]` | S3, Google Storage, or Azure Blob storage references |
| `[DB-Error]` | Database error strings leaking architectural details |

### Intelligence Classification

| Tag | Meaning |
|---|---|
| `admin_panel` | Management/Administration interface detected |
| `auth_classification` | login, logout, register, token, mfa, password_reset |
| `idor_candidate` | Endpoints with ID-like parameters or UUIDs in the path |
| `sqli_candidate` | Parameters prone to SQL injection (id, query, filter, sort) |
| `cmdi_candidate` | Parameters prone to Command injection (cmd, exec, file, path) |
| `file_upload` | Endpoints that accept file or media upload |
| `form_fields_detail` | Per-field type metadata: hidden, file, required flags |

### Special Sections in Output

| Section | Description |
|---|---|
| `js_orphan_params` | Params found in JS files with no resolvable target URL — wordlist hints only, not injectable targets |
| `websocket_endpoints` | socket.io / WS endpoints separated from HTTP attack surface |
| `robots_disallowed` | Disallowed paths with discovered child endpoints shown as a tree |

---

## Output Formats

- **JSON** — Full-fidelity report with all classification metadata, orphan params, and socket.io section.
- **Burp** — XML format for direct import into Burp Suite.
- **CSV** — Spreadsheet-ready endpoint and parameter list.
- **JSONL** — One endpoint per line for streaming pipelines.

---

## Requirements

- Python 3.10+
- `aiohttp`, `beautifulsoup4`, `lxml`
- Playwright + Chromium *(optional, for SPA targets)*

---

For authorized security testing only. This software is licensed under the **GNU General Public License v3 (GPLv3)**.

---

## Author

<a href="https://l4zz3rj0d.github.io">
  <img src="https://img.shields.io/badge/Founder-L4ZZ3RJ0D-c0392b?style=for-the-badge" alt="L4ZZ3RJ0D"/>
</a>