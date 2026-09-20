#!/usr/bin/env python3
"""
bailly_pages.py — run in Pyto
Reads Greek words from fileone.txt, fetches the bailly.app page
for each, appends the entry text to filebailly.txt.
"""

import re
import time
import unicodedata
import urllib.request
import urllib.parse
import urllib.error
from html import unescape
from pathlib import Path

INPUT_FILE  = Path("fileone.txt")
OUTPUT_FILE = Path("filebailly.txt")
BASE = "https://bailly.app/"

# Browser-like UA helps get past Cloudflare
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                   "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
                   "Mobile/15E148 Safari/604.1")
}

DELAY = 1.0        # seconds between words — be kind to their server
TIMEOUT = 20

# ---------------------------------------------------------------
# 1. Greek -> Bailly URL transliteration
#    (rules verified against the live site:
#     logos, phengô, emplêsai)
# ---------------------------------------------------------------

SIMPLE = {
    "α": "a", "β": "b", "γ": "g", "δ": "d", "ε": "e", "ζ": "z",
    "θ": "th", "ι": "i", "κ": "k", "λ": "l", "μ": "m", "ν": "n",
    "ξ": "x", "ο": "o", "π": "p", "ρ": "r", "σ": "s", "ς": "s",
    "τ": "t", "υ": "y", "φ": "ph", "χ": "ch", "ψ": "ps",
    "ϝ": "w",                      # digamma
}
LONG   = {"η": "ê", "ω": "ô"}
VOWELS = set("αεηιουω")

# circumflex carried over onto the latin vowel
CIRCUM = {"a": "â", "e": "ê", "i": "î", "o": "ô", "y": "û"}

# gamma-nasal combinations: γγ -> ng, γκ -> nk, γξ -> nx, γχ -> nch
NASAL  = {"γ": "ng", "κ": "nk", "ξ": "nx", "χ": "nch"}

def transliterate(word: str) -> str:
    """Convert a Greek word to bailly.app's URL slug."""
    word = unicodedata.normalize("NFD", word.lower())
    out = []
    pending_circum = False
    pending_rough  = False

    i = 0
    while i < len(word):
        ch = word[i]
        # combining marks
        if unicodedata.combining(ch):
            if ch == "\u0314":            # rough breathing
                pending_rough = True
            elif ch == "\u0342":           # Greek circumflex (perispomeni)
                pending_circum = True
            # acute, grave, smooth, iota-subscript, diaeresis, etc.: ignored
            i += 1
            continue
        # iota subscript as separate char (after NFD it may appear)
        if ch in ("\u0345", "\u0344"):
            i += 1
            continue

        base = SIMPLE.get(ch) or LONG.get(ch)

        # upsilon after a/o/e-ish vowel becomes u (handled via diphthongs below)
        if base is None:
            i += 1
            continue

        # diphthongs: look ahead to next base letter
        nxt = word[i+1] if i + 1 < len(word) else ""
        nxt_base = SIMPLE.get(nxt) or LONG.get(nxt)
        if ch in "αεηο" and nxt_base == "y":
            pair_map = {("α", "y"): "au", ("ε", "y"): "eu",
                       ("η", "y"): "êu", ("ο", "y"): "ou"}
            seg = pair_map.get((ch, "y"), base + "y")
            if pending_circum and seg[0] in CIRCUM:
                seg = CIRCUM[seg[0]] + seg[1:]
            out.append(("h" + seg) if pending_rough else seg)
            pending_circum = pending_rough = False
            i += 2
            continue

        # gamma nasal: γγ γκ γξ γχ
        if ch == "γ" and out:
            nxt_char = word[i+1] if i + 1 < len(word) else ""
            if nxt_char in NASAL and out and out[-1].endswith("g"):
                out[-1] = out[-1][:-1] + NASAL[nxt_char]   # g + γ/κ/ξ/χ
                i += 2
                continue

        seg = base
        if pending_circum and seg in CIRCUM:
            seg = CIRCUM[seg]
        if pending_rough and ch in VOWELS:
            seg = "h" + seg
        pending_circum = pending_rough = False
        out.append(seg)
        i += 1

    return "".join(out)

def slug_candidates(word: str):
    """Primary slug + fallback without circumflex markers."""
    s = transliterate(word)
    yield s
    plain = re.sub("[âêîôû]", lambda m: {"â":"a","ê":"e","î":"i","ô":"o","û":"u"}[m.group()], s)
    if plain != s:
        yield plain

# ---------------------------------------------------------------
# 2. Fetch page & extract entry text
# ---------------------------------------------------------------

def fetch_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")

def extract_entry(html: str) -> str:
    """Pull the main content block and reduce it to plain text."""
    # keep only <main> if present
    m = re.search(r"<main\b.*?</main>", html, re.S | re.I)
    if m:
        html = m.group(0)
    # drop scripts, styles, nav, header, footer, svg icons, forms
    html = re.sub(r"<(script|style|nav|header|footer|svg|form)\b.*?</\1>",
                  "", html, flags=re.S | re.I)
    # block-level tags become line breaks
    html = re.sub(r"</(p|div|li|h1|h2|h3|h4|section|article|ul|ol|dl|dt|dd)>",
                  "\n", html, flags=re.I)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    # remaining tags out
    text = re.sub(r"<[^>]+>", "", html)
    text = unescape(text)
    # tidy whitespace
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)

# ---------------------------------------------------------------
# 3. Main
# ---------------------------------------------------------------

def main():
    if not INPUT_FILE.exists():
        raise SystemExit(f"Not found: {INPUT_FILE.resolve()}")
    words = [w.strip() for w in INPUT_FILE.read_text(encoding="utf-8").splitlines() if w.strip()]
    print(f"{len(words)} words to fetch.\n")

    ok, fail = 0, 0
    for n, word in enumerate(words, 1):
        print(f"[{n}/{len(words)}] {word} ... ", end="")
        text = None
        used = None
        for slug in slug_candidates(word):
            url = BASE + urllib.parse.quote(slug, safe="")
            try:
                text = extract_entry(fetch_html(url))
                used = url
                break
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    continue
                raise
        if text:
            with OUTPUT_FILE.open("a", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write(f"{word}\n<{used}>\n\n")
                f.write(text + "\n\n")
            ok += 1
            print("ok")
        else:
            with OUTPUT_FILE.open("a", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write(f"{word}\nNOT FOUND (tried: "
                        + ", ".join(BASE + s for s in slug_candidates(word))
                        + ")\n\n")
            fail += 1
            print("not found")
        time.sleep(DELAY)

    print(f"\nDone. {ok} saved, {fail} not found -> {OUTPUT_FILE.resolve()}")

if __name__ == "__main__":
    main()