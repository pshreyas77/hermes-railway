# CJP Live Protest Monitor — Cron + Script Pattern

> **User preference (2026-07-20, confirmed 2026-07-21):** Do NOT deliver to Telegram — user wants updates shown **in chat** when they ask.
> Set `deliver='local'`. Results written to vault. User manually asks "CJP update" or "now?" to trigger.

**Active setup (2026-07-20, verified 2026-07-21):**
- Script: `C:/Users/shrey/AppData/Local/hermes/scripts/cjp-check.py`
- Cron: `91cbd511877c`, every 15 min, `deliver='local'`
- Vault output: `E:/_Knowledge/ObsidianVault/04 - DAILY/CJP-LIVE-UPDATES.md`
- User trigger phrase: "CJP update" or "now?" → run script manually, report in chat

## Pattern

1. `no_agent=True` cron job → Python script every N minutes
2. Script scrapes news sites → filters keywords → writes to vault
3. User asks "CJP update" → run script in terminal → report in chat

## Key Technical Lessons

### Hindustan Times uses JSON-LD, NOT plain HTML

**FAIL:** `<h2>` / `<h3>` regex — HT headlines live inside `<script type="application/ld+json">` blocks.

**WORK:** Extract from JSON-LD structured data:

```python
for match in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL):
    data = json.loads(match)
    if isinstance(data, list):
        for item in data:
            if "headline" in item:
                items.append(item["headline"])
```

### Scroll.in is the best live-updating source

Scroll.in had 7+ fresh CJP articles today — more reliable than HT's live blog (which required JS rendering). Always check `scroll.in/latest`.

### NDTV blocks Python's urllib with 403

Use Hindustan Times, The Hindu, Indian Express, Scroll, Al Jazeera instead. All work with stdlib `urllib`.

## Source Reliability (Tested 2026-07-20, updated 2026-07-21)

| Source | Works | Notes |
|--------|-------|-------|
| Hindustan Times | ✅ | Use JSON-LD extraction; `india-news/` section URL works |
| The Hindu | ✅ | Standard HTML parsing works |
| Indian Express | ✅ | Standard HTML parsing works |
| Scroll.in | ✅ | Best live coverage, RSS-style feed; `scroll.in/latest` works |
| Al Jazeera | ✅ | Direct article URL works; slug format: `aljazeera.com/news/2026/7/20/[slug...]` |
| Reuters | ✅ | Direct article URL works |
| NDTV | ❌ | 403 Forbidden — blocked by urllib |
| Reddit | ❌ | 403 blocked at network level — completely inaccessible |
| Nitter (Twitter mirrors) | ❌ | All failed: poast.org (403), privacydev.net (DNS fail), cz (cert expired) |
| Bing/DDG web search | ❌ | No "lakh" CJP mentions in search index results |
| CJP Official Site | ✅ | `cockroachjantaparty.raizian.in/` + `/protest-schedule` — verified URLs |

## What Actually Works for CJP News

```python
sources = [
    ("Scroll", "https://scroll.in/latest"),
    ("Hindustan Times", "https://www.hindustantimes.com/india-news/"),
    ("The Hindu", "https://www.thehindu.com/news/national/"),
    ("Indian Express", "https://indianexpress.com/section/india/"),
    ("Al Jazeera", "https://www.aljazeera.com/news/2026/youth-led-protesters-answer-call..."),
    ("CJP Official Site", "https://cockroachjantaparty.raizian.in/"),
    ("CJP Protest Schedule", "https://cockroachjantaparty.raizian.in/protest-schedule"),
]
```

## CJP Social Media (Real Handles — Found 2026-07-21)

| Platform | Handle | URL |
|----------|--------|-----|
| X/Twitter | **@Cockroachisback** | (not @CockroachParty) |
| Telegram | **@thecockroachchannel** | t.me/thecockroachchannel |
| WhatsApp | CJP Official Updates | (via cockroachjantaparty.raizian.in) |
| Instagram | @cockroachjantaparty | |
| Facebook | Cockroach Janta Party | |

**Note:** Nitter/Twitter mirrors ALL failed. CJP's X handle is `@Cockroachisback` (not the obvious name).

## Crowd-Size Verification Workflow

When user asks "how many protesters?" or surfaces a claim like "1 lakh+":

1. **Bracketed estimate, never a single number** — provide RANGE (low/high) from multiple sources
2. **Identify the SOURCE** — organizer self-report vs. independent media vs. police vs. eyewitness
3. **Apply plausibility filter:**
   - Jantar Mantar physical capacity: ~10K–15K max (seated + standing combined)
   - Metro cordons + barricades cap crowd regardless of claims
   - Wire services (Reuters/AP/AFP) lead with crowd numbers — if they didn't say "X lakh", they didn't verify it
4. **Distinguish organizational stats from attendance** — "20 lakh registered members" ≠ "20 lakh at one march"
5. **Flag unverified claims directly but respectfully** — say "I couldn't verify X; here is what sources confirm"

**Confirmed crowd data (July 20, 2026 — Delhi):**
| Source | Estimate |
|--------|-----------|
| Reuters / AP | 10,000+ |
| Hindustan Times | 10,000–20,000 |
| Delhi Police (via HT) | 10,000 |
| NDTV | 20,000 |
| Scroll.in | "thousands" |
| Al Jazeera | "thousands" |

## Godi Media Exclusions (Never Source From)

Republic TV, Zee News, Times Now, Aaj Tak, India TV, NewsX, TV9, TV9 Bharatvarsh, Times of India

## Safe Sources

The Hindu, Indian Express, Hindustan Times, Scroll, Newslaundry, The Wire, The Quint, Al Jazeera, Reuters, BBC, DW, Logical Indian, The Federal

## Search Terms (CJP / Cockroach Janta Party)

**Core:** cockroach janta party, cjp, chalo sansad
**People:** wangchuk, dipke, pradhan, nadda
**Events:** hunger strike, lathicharge, tear gas, detained, parliament march
**Context:** neet ug, exam leak, paper leak, safdarjung, internet shutdown
**Politics:** rahul gandhi, modi anti-youth, opposition

## How to Recreate This Monitor

**Step 1: Write script** to `C:/Users/shrey/AppData/Local/hermes/scripts/<name-check.py>`

**Step 2: Test**
```bash
"/c/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe" \
  "C:/Users/shrey/AppData/Local/hermes/scripts/<name-check.py>"
```

**Step 3: Create cron (NO telegram)**
```python
cronjob(action='create', name='<Name>', no_agent=True,
        script='<name-check.py', schedule='*/15 * * * *',
        deliver='local')  # NOT 'telegram'
```

**Step 4: Run on demand**
```
terminal → run the script → report in chat
```

## What to Tell the User

When they say "now?" or "CJP update":
1. Run the script: `"/c/Users/shrey/AppData/Local/Programs/Python/Python314/python.exe" "C:/Users/shrey/AppData/Local/hermes/scripts/cjp-check.py"`
2. Report new headlines in a clean table
3. Note any breaking developments (injuries, Wangchuk status, new arrests, national spread)
4. Always list source(s)