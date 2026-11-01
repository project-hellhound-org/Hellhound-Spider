# Changelog

All notable changes to Hellhound Spider are documented here.

## [14.1] — 2026-11-01

### Fixed
- Live crawl output could leave stray blank rows or wrap unpredictably on
  narrower or font-sensitive terminals. Root causes, now all fixed:
  - Parent-directory backtracking findings could emit very long, untruncated
    URLs into the live feed with no line-length cap — now bounded like the
    rest of the discovery feed.
  - The animator's progress bar used Braille-pattern characters, which some
    terminal/font combinations render wider than a single column, throwing
    off every carriage-return redraw. Replaced with plain ASCII.
  - Row-clearing switched from manually counting characters and overwriting
    with spaces to the terminal's own erase-in-line control sequence, so
    rendering no longer depends on guessing any glyph's on-screen width.
- Bitcoin address detection replaced a weak heuristic with real Base58Check
  checksum validation, eliminating false positives on random minified-JS
  strings that merely looked address-shaped.
- Apache `mod_autoindex` column-sort query strings (`?C=N;O=D`) were being
  picked up as real parameters. Filtered globally, at the same gate every
  discovered URL passes through — not just in the crawler, but for
  backtracking too.

### Changed
- Removed the "JS ORPHAN PARAMS" summary section (unused noise; the
  underlying data is still in the JSON export).

## [14.0] — 2026-10-31

### Added
- **Stdin/stdout piping.** `spider target.com | httpx` just works — no flag
  required. Auto-detected whenever stdout isn't a terminal; `--pipe`/`-Q`
  forces it explicitly. Defaults to plain newline-separated URLs when
  piped (`--format` still available to pick `json`, `jsonl`, `csv`, `burp`,
  or `nuclei`). Multiple targets via stdin, JSON mode, writes one compact
  JSONL line per target.
- **Parent-directory backtracking** (`--no-backtrack`/`-k` to disable, on
  by default). After the forward crawl, walks back up every discovered
  path to probe ancestor directories that were never directly linked to —
  e.g. finding `/js/` open to listing after only ever seeing individual
  `/js/*.min.js` hits. Mirrors what a recursive directory brute-forcer
  would find, without a separate wordlist pass. Findings now appear in
  both the live feed and a dedicated "PARENT DIRECTORY BACKTRACKING"
  section in the final summary.

## [13.21] — 2026-07-04

### Added
- **CTF Mode** (`--ctf`) — auto-enables sensitive file scanning, admin
  panel checks, OpenAPI/GraphQL discovery, CORS audits, flag extraction,
  high default concurrency, and highlights high-value parameters and
  backup files in summaries and reports.
- **Active CORS auditing** — built-in checks for permissive configurations
  reflecting custom origin values.
- **Parameter extraction & validation** — query parameters are now parsed
  from crawled URLs automatically and added to parameter maps.

## [13.19]

### Changed
- Admin-panel, sensitive-file, and Wayback Machine probing are now
  **off by default** (`--probe`, `--admin-probe`, `--sensitive-probe`,
  `--wayback` to opt in), for faster baseline scans.

### Added
- JavaScript endpoint extraction now detects template-literal paths
  containing runtime interpolations (e.g. `/api/user/${id}`) and flags
  them as requiring dynamic values.
