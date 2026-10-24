# tv-feed (public)
Fire TV home app feed. **Public: put only public info here.**

URLs: https://ryofssmax-a11y.github.io/tv-feed/{ainews,yamada,sakamichi,rss}.json

## Schema
```
{ "date":"YYYY-MM-DD", "updatedAt":"ISO8601+09:00", "source":"...",
  "items":[ ... ] }
```
- ainews.json / rss.json item: `{title, summary?, url?, publisher?}` (max ~10)
- yamada.json / sakamichi.json item: `{time:"HH:MM", end?, title, channel, member?, note?}` (today only, sorted by time)
Files with `"source":"SAMPLE"` are seed data.

## Update recipe for bots (box, GITHUB_TOKEN env)
1. Write today's items as a JSON array to /tmp/items.json (schema above).
2. `python3 /workspace/update_tv_feed.py <ainews|yamada|sakamichi> /tmp/items.json`
3. Expect `updated <name> N items`; TV picks it up within 30 min.

rss.json is refreshed every 30 min by GitHub Actions (rss.yml).
