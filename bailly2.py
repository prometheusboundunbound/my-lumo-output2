import requests

BASE = "https://api.bailly.app"  # verify this — see below!

def lookup(word):
    r = requests.get(f"{BASE}/lookup/{word}",
                     params={"morphology": "true",
                             "fields": "word,uri,excerpt"},
                     timeout=15)
    r.raise_for_status()
    return r.json()["data"]

d = lookup("λόγος")
print(d["count"], "entries")
for e in d["entries"]:
    print(e["word"])
print(d.get("morphology"))

def entry(uri):
    r = requests.get(f"{BASE}/entry/{uri}",
                     params={"siblings": "true"}, timeout=15)
    return r.json()["data"]["entry"]