<p align="center">
  <img src="Images/spider.jpg" alt="Hellhound Spider" width="600"/>
</p>

<h1 align="center">Hellhound Spider</h1>

<p align="center">
  Fully autonomous web crawler for security testing — maps endpoints, parameters, and security issues across traditional and SPA web applications. Drop a URL. Walk away.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/version-13.5-red?style=flat-square"/>
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

## v13.5 — Orbital Recon Release

v13.5 transforms the Spider from a crawler into a multi-vector recon platform. This release introduces external intelligence sources, protocol-level bypass engines, and full security header auditing — on top of the surgical accuracy hardened in v13.0.

### New in v13.5

**Patchright Bot-Bypass** — When a target's WAF or bot-detection blocks Playwright, Spider automatically falls back to [Patchright](https://github.com/nicegist/patchright) — a binary-patched Chromium engine that bypasses fingerprint checks at the browser level. Zero config: detection and fallback happen transparently.

**Response Header Analysis** — Every response is now audited for missing and misconfigured security headers. The terminal shows a dedicated `HEADER ANALYSIS` section with `[MISSING]` / `[PRESENT]` / `[LEAK]` tags for: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, `Permissions-Policy`, `Referrer-Policy`, `Cache-Control`. Information leak headers (`Server`, `X-Powered-By`, `X-AspNet-Version`) are flagged and extracted automatically.

**crt.sh Subdomain Enumeration** — Certificate Transparency log mining via crt.sh discovers sibling subdomains for the target. Results are shown in a dedicated `CRT.SH SUBDOMAINS` section and included in the JSON report for downstream tooling.

**Wayback Machine Integration** — Historical endpoint discovery via the Wayback CDX API. Archived URLs from the target's history are pulled, deduplicated, and merged into the crawl store — surfacing forgotten endpoints, legacy APIs, and dead routes that still respond.

**Sitemap.xml Deep Parse** — Full recursive sitemap parsing including sitemap index files. Discovered URLs are merged with the crawl store and shown in a dedicated `SITEMAP` section.

**Robots.txt Allow/Disallow Tree** — The ROBOTS section now displays full Allow and Disallow trees with child endpoint mapping. Comment-mined sensitive paths are flagged with `[Robots-Leak]`.

**security.txt Parser (RFC 9116)** — Full-field extraction from `/.well-known/security.txt`: Contact, Expires, Encryption, Acknowledgments, Preferred-Languages, Canonical, Policy, and Hiring fields. Comments are mined for sensitive metadata.

**HAR File Import** — Seed the crawl with a browser-exported HAR file (`--har session.har`). Every request in the HAR is parsed and injected into the crawl store before spidering begins — perfect for authenticated flows captured in DevTools.

**HTML Comment Leak Detection** — HTML comments (`<!-- ... -->`) are now extracted, deduplicated across pages, and surfaced as `[Comment-Leak]` intelligence. TODO markers, debug flags, internal URLs, and developer notes are captured automatically.

**WebSocket / Socket.io Detection** — WebSocket and socket.io endpoints are detected and separated from the HTTP attack surface in a dedicated `websocket_endpoints` section.

**Attack Surface Management (ASM)** — TLS inspection, DNS intelligence, WAF/CDN fingerprinting, active JS SCA (Software Composition Analysis), and cloud bucket verification.
**Active Probing** — Automatically probes for exposed sensitive files and admin panels.

### Carried from v13.0

**Enhanced Accuracy** — Near-zero false positives on complex SPAs. Hardened extraction for erratic DOM structures and obfuscated JS routes.

**Noise Filter** — Repository browser paths (`/blob/`, `/tree/`, `/commits/`), CDN artefacts, and structural UI links are suppressed before entering the endpoint store.

**JS Orphan Params** — Parameters found in JS files without a resolvable target URL are stored as `js_orphan_params` — wordlist hints, not injectable targets.

**Form Field Intelligence** — Rich per-field metadata: `type`, `hidden`, `file`, `required`. Downstream agents can skip CSRF tokens and prioritise real injectable fields.

**Shorthand Flags** — Every flag has a short single-letter alias. `-d`, `-c`, `-t`, `-v`, `-C`, `-a`, `-o`, `-f`, `-x`, `-s`, `-D` — full list below.


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
| `--delay` | | `0` | Delay between requests in seconds |
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
| `--format` | `-f` | `json` | `json` `jsonl` `csv` `burp` `urls` `nuclei` |

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
| `--har` | | Seed crawl from a browser-exported HAR file |

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

# Seed crawl with a HAR file (authenticated session replay)
spider https://target.com --har session.har

# Combine HAR seed + extraction + screenshots
spider https://target.com --har session.har -x -s all
```

---

## What Gets Found

### Discovery Vectors

HTML crawl, live SPA XHR interception, Intelligent Robots Analysis (Disallow/Allow mapping + Comment Mining), sitemap XML (with index recursion), `.well-known` (OIDC/JWKS), JSON path chaining, SPA hash routes, lazy-load attributes, CSP header hints, OpenAPI/Swagger specs, GraphQL introspection, **crt.sh certificate transparency**, **Wayback Machine CDX API**, **security.txt (RFC 9116)**, **HAR file import**, **HTML comment mining**, **response header analysis**, **TLS/DNS Intel**, **WAF fingerprinting**, and **JS SCA Analysis**.

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
| `[Header-Missing]` | Critical security headers absent from responses (CSP, HSTS, X-Frame-Options, etc.) |
| `[Header-Leak]` | Server identity or technology leaked via response headers |
| `[Comment-Leak]` | Sensitive developer comments in HTML (TODO, debug, internal URLs) |
| `[CRT-Sub]` | Sibling subdomains discovered via certificate transparency logs |
| `[Wayback]` | Historical endpoints recovered from the Wayback Machine |
| `[TLS-Intel]` | Certificate expiry, weak protocols, and self-signed issues |
| `[WAF-Detected]` | Active WAF or CDN technology fingerprinted via headers and cookies |
| `[DNS-Intel]` | Discovered TXT, CNAME, and A records |
| `[JS-SCA]` | JavaScript software composition and dependency versions |

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
| `robots_allowed` | Explicitly allowed paths with child endpoint mapping |
| `header_audit` | Per-header security audit with missing/present/leak status |
| `crt_subdomains` | Subdomains discovered via certificate transparency logs |
| `wayback_urls` | Historical URLs recovered from the Wayback Machine CDX API |
| `sitemap_urls` | URLs discovered from sitemap.xml / sitemap index files |
| `security_txt` | Parsed fields from RFC 9116 security.txt |
| `html_comments` | Deduplicated HTML comments extracted across pages |
| `tls_findings` | TLS certificate issues (expiry, weak protocols, self-signed) |
| `waf_findings` | WAF/CDN fingerprinting results |
| `dns_findings` | Discovered DNS records |
| `js_libs` | JS dependency tree |
| `sensitive_files` | Discovered sensitive files and configurations |
| `cloud_probes` | Status of discovered cloud buckets |

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

---

For authorized security testing only. This software is licensed under the **GNU General Public License v3 (GPLv3)**.

---

## Author

<a href="https://l4zz3rj0d.github.io">
  <img src="https://img.shields.io/badge/Founder-L4ZZ3RJ0D-c0392b?style=for-the-badge" alt="L4ZZ3RJ0D"/>
</a>