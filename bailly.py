#!/usr/bin/env python3
"""
bailly_fetch.py — run in Pyto 3.0
Reads Greek words from fileone.txt (one per line),
writes Bailly entries to filebailly.txt.
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# ------------------------------------------------------------------
# 1. CONFIG
# ------------------------------------------------------------------

INPUT_FILE = Path("fileone.txt")
OUTPUT_FILE = Path("filebailly.txt")

# The Bailly API host. The correct production host is whatever bailly.app
# itself calls — check with your browser's Network tab while searching a
# word on bailly.app. Candidates to try, in order:
API_HOSTS = [
    "https://api.bailly.app",
    "https://bailly.app/api",
]

TIMEOUT = 20          # seconds per request
DELAY_BETWEEN_WORDS = 0.5   # be polite to their server
RETRIES = 3

# Fields we want per entry. If the API rejects a field name, the script
# falls back to fetching with no fields= parameter (server defaults).
FIELDS = "word,uri,translatedTerm"

# ------------------------------------------------------------------
# 2. HTTP helpers
# ------------------------------------------------------------------

def http_get_json(url, retries=RETRIES):
    """GET a URL, return parsed JSON, retrying on transient errors."""
    headers = {"User-Agent": "Pyto-BaillyFetcher/1.0"}
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                last_err = e
                time.sleep(2 * (attempt + 1))   # backoff
                continue
            raise   # 4xx other than above: don't retry
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Request failed after {retries} tries: {url} ({last_err})")


def discover_api_base():
    """Try each candidate host; a working API returns {"data": "OK"}."""
    for host in API_HOSTS:
        try:
            data = http_get_json(host + "/", retries=1)
            if isinstance(data, dict) and data.get("data") == "OK":
                print(f"[info] API base: {host}")
                return host.rstrip("/")
        except Exception as e:
            print(f"[info] {host} unreachable ({e}), trying next...")
    raise RuntimeError(
        "Could not reach the Bailly API. Open bailly.app in a browser "
        "with the Network tab open, search a word, and set API_HOSTS[0] "
        "to the exact hostname of the /lookup/... request."
    )


# ------------------------------------------------------------------
# 3. Bailly API calls
# ------------------------------------------------------------------

def lookup_word(api, word):
    """Search for a word. Returns dict with entries + morphology."""
    q = urllib.parse.quote(word, safe="")
    url = (f"{api}/lookup/{q}"
           f"?morphology=true&caseSensitive=false&fields={FIELDS}")
    try:
        return http_get_json(url).get("data", {})
    except urllib.error.HTTPError as e:
        # Bad field names etc. — retry without the fields restriction.
        if e.code in (400, 422):
            url = f"{api}/lookup/{q}?morphology=true"
            return http_get_json(url).get("data", {})
        raise


def fetch_entry(api, uri):
    """Fetch one full entry by its URI."""
    q = urllib.parse.quote(uri, safe="")
    url = f"{api}/entry/{q}?siblings=true&fields={FIELDS}"
    try:
        return http_get_json(url).get("data", {}).get("entry", {})
    except urllib.error.HTTPError as e:
        if e.code in (400, 422):
            url = f"{api}/entry/{q}?siblings=true"
            return http_get_json(url).get("data", {}).get("entry", {})
        raise


# ------------------------------------------------------------------
# 4. Formatting entries as readable text
# ------------------------------------------------------------------

def entry_to_text(entry):
    """Render an entry dict as plain text (unknown keys dumped as JSON)."""
    lines = []
    for key in ("word", "uri", "translatedTerm"):
        val = entry.get(key)
        if val not in (None, ""):
            lines.append(f"{key}: {val}")
    # Dump anything else we don't explicitly format
    known = {"word", "uri", "translatedTerm", "children"}
    extra = {k: v for k, v in entry.items() if k not in known}
    if extra:
        lines.append(json.dumps(extra, ensure_ascii=False, indent=2))
    return "\n".join(lines)


# ------------------------------------------------------------------
# 5. MAIN
# ------------------------------------------------------------------

def main():
    if not INPUT_FILE.exists():
        raise SystemExit(f"Input file not found: {INPUT_FILE.resolve()}")

    words = [w.strip() for w in INPUT_FILE.read_text(encoding="utf-8").splitlines()
             if w.strip()]
    print(f"[info] {len(words)} words to process.")

    api = discover_api_base()

    results, failures = [], []
    for i, word in enumerate(words, start=1):
        print(f"[{i}/{len(words)}] {word} ... ", end="")
        try:
            data = lookup_word(api, word)
            entries = data.get("entries", [])
            if not entries:
                # Nothing exact — try Morpheus results as fallback lemmas
                morphology = data.get("morphology", {}) or {}
                lemmas = []
                for parse_list in morphology.values():
                    for p in parse_list:
                        lem = (p.get("dict") or {}).get("hdwd") \
                              if isinstance(p, dict) else None
                        if isinstance(lem, dict):
                            lem = lem.get("$")
                        if lem:
                            lemmas.append(lem)
                if lemmas:
                    seen, merged = set(), []
                    for lem in lemmas:
                        if lem not in seen:
                            seen.add(lem)
                            merged.append(lem)
                    entries = [fetch_entry(api, lem)
                               for lem in merged if fetch_entry(api, lem)]
                if not entries:
                    raise RuntimeError("no entries found")

            texts = []
            for e in entries[:5]:   # cap at 5 matches per word
                full = fetch_entry(api, e.get("uri", e.get("word", "")))
                texts.append(entry_to_text(full or e))

            block = (f"{'=' * 70}\nWORD: {word}\n"
                     f"matches: {data.get('countAll', '?')}\n\n"
                     + "\n\n---\n\n".join(texts) + "\n")
            results.append(block)
            print(f"ok ({len(entries)} matches)")

        except Exception as e:
            failures.append((word, str(e)))
            results.append(f"{'=' * 70}\nWORD: {word}\nERROR: {e}\n")
            print(f"FAILED ({e})")

        time.sleep(DELAY_BETWEEN_WORDS)

    OUTPUT_FILE.write_text("\n".join(results), encoding="utf-8")
    print(f"\n[done] Written to {OUTPUT_FILE.resolve()}")

    if failures:
        print(f"\n[warn] {len(failures)} words failed:")
        for w, err in failures:
            print(f"  - {w}: {err}")


if __name__ == "__main__":
    main()