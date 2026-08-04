# Live News Research — CJP Protest Session Notes

**Date:** 2026-07-20
**Context:** Research on CJP (Cockroach Janta Party) Parliament march, July 20, 2026

---

## What Actually Worked

### Browser tools over delegation
`delegate_task` with news research goals returned results but didn't surface them in a structured way. Direct browser navigation was faster and produced more reliable output.

### Search engine choice
- **Google**: blocked (captcha/403)
- **Bing**: worked — returned 341,000 results with good snippet previews
- **The Wire / Scroll / The Quint**: search URLs don't work as direct navigation (404s on `/search?q=...`). Better to navigate to article directly via known publication URLs.

### Source credibility tiering (for India news)
| Tier | Sources | Notes |
|------|---------|-------|
| ✅ Reliable | The Hindu, Indian Express, The Quint, Scroll.in, Newslaundry, Article 14, The Wire, BBC | Independent journalism, editorial standards |
| ⚠️ Mixed | NDTV, Times of India | Can be useful but verify |
| ❌ Godi/Exclude | Republic TV, Zee News, Aaj Tak, Times Now, India TV, TV9, NewsX | Pro-BJP "lap dog" channels — user explicitly excludes |

### Cross-verification pattern
1. Find headline on Bing → open on reliable outlet (The Hindu, Indian Express)
2. Check Wikipedia for entity context (CJP page had good background)
3. Check official website for direct statements (cockroachjantaparty.raizian.in had live updates)
4. Verify with 2+ independent sources before storing as fact

---

## CJP (Cockroach Janta Party) — Key Facts Verified

- **What:** "Chalo Sansad" march — Parliament march on Monsoon Session opening day
- **Date:** July 20, 2026
- **Route:** Jantar Mantar → Parliament House, New Delhi, 10:00 AM IST
- **Demand:** Education Minister Dharmendra Pradhan's resignation over NEET-UG / UGC-NET paper leaks
- **Police:** Denied permission, banned large gatherings, alleged tear gas/baton charge
- **Context:** Sonam Wangchuk hunger strike Day 32 (now in Safdarjung Hospital); CJP founder Abhijeet Dipke started indefinite fast today in solidarity
- **Celebrity split:** Shabana Azmi + Prakash Raj joined march; Kangana Ranaut + Hema Malini backed government
- **Verified press:** BBC, The Hindu, Indian Express, The Quint

---

## Vault Integration Done

- Saved as: `07 - SYSTEM/audit-dashboard.md` (pending review for permanent storage)
- Related existing note: `Dravidian Folk Deities & Sanskritization` — youth movements + political context relevant to anti-caste / Dravidian political research

---

## Pattern for Future News Research Sessions

```
1. Bing search for the event/topic
2. Identify entities (organizations, people) — verify on Wikipedia
3. Navigate to 2+ reliable outlets (The Hindu, Indian Express, The Quint)
4. Check official source if available (party websites, press releases)
5. Cross-verify key claims (numbers, dates, quotes) across 2+ sources
6. Note godi sources to exclude (Republic, Zee, Times Now, etc.)
7. Synthesize: What, Who, Where, When, Why, Police Response, Celebrity Split
8. Ask: does this connect to any existing vault research domains?
   → If yes: create/found relevant research note, link to project
   → If no: store in 07 - SYSTEM/ as current-events capture for later classification
```

---

## Note on "CJP" Ambiguity

"CJP" in India has TWO meanings:
1. **Cockroach Janta Party** — youth political satire/activism movement (this session's subject)
2. **Citizens for Justice and Peace** — Teesta Setalvad's human rights organization

Always disambiguate in search queries. The Cockroach Janta Party dominates Bing results for "CJP protest."