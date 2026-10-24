#!/usr/bin/env python3
"""Usage: python3 update_tv_feed.py <ainews|yamada|sakamichi> <items.json>
items.json = JSON array of items (or {"items":[...]}). Needs env GITHUB_TOKEN.
Retries 409/422 (sha conflict) up to 5 times with jitter; prints the commit sha."""
import base64, json, os, sys, time, random, urllib.request, urllib.error, datetime
name, src = sys.argv[1], sys.argv[2]
assert name in ("ainews", "yamada", "sakamichi"), "name must be ainews|yamada|sakamichi"
items = json.load(open(src)); items = items["items"] if isinstance(items, dict) else items
jst = datetime.timezone(datetime.timedelta(hours=9)); now = datetime.datetime.now(jst)
body = json.dumps({"date": now.strftime("%Y-%m-%d"), "updatedAt": now.isoformat(timespec="seconds"),
                   "source": name + "-bot", "items": items}, ensure_ascii=False, indent=1)
api = f"https://api.github.com/repos/ryofssmax-a11y/tv-feed/contents/{name}.json"
h = {"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"], "Accept": "application/vnd.github+json", "User-Agent": "tv-feed"}
def req(method, data=None):
    r = urllib.request.Request(api + ("?ref=main" if method == "GET" else ""), method=method, headers=h,
                               data=json.dumps(data).encode() if data else None)
    return json.load(urllib.request.urlopen(r, timeout=30))
for attempt in range(1, 6):
    try:
        sha = req("GET")["sha"]
        res = req("PUT", {"message": f"update {name} ({len(items)} items)", "sha": sha, "branch": "main",
                          "content": base64.b64encode(body.encode()).decode()})
        print(f"updated {name} {len(items)} items commit={res['commit']['sha']}")
        print(f"live in ~1-2 min: https://ryofssmax-a11y.github.io/tv-feed/{name}.json")
        break
    except urllib.error.HTTPError as e:
        if e.code in (409, 422) and attempt < 5:
            w = attempt + random.uniform(0, 1.5); print(f"HTTP {e.code}, retry {attempt}/5 in {w:.1f}s", file=sys.stderr); time.sleep(w); continue
        print(f"FAILED {name}: HTTP {e.code} {e.read()[:200]!r}", file=sys.stderr); sys.exit(1)
