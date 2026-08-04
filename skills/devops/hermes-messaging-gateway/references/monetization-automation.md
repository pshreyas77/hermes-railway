# Monetization Automation with Hermes + Obsidian

## Pattern: "Research Vault as a Service"

### Concept
Use Hermes Agent + Obsidian vault to build sellable knowledge products automatically.

### Automation Stack (3 Cron Jobs)

| Job | Schedule | Purpose |
|-----|----------|---------|
| **Sample Vault Builder** | Sun 10 AM | Builds 1 sellable vault/week in `0-Inbox/Marketplace/` |
| **Marketplace Poster** | Daily 11 AM | Drafts 1 promotional post/day (Twitter, Reddit, LinkedIn) |
| **Vault Quality Check** | Sat 2 PM | Audits vaults, reports which are ready to sell |

### Sample Vault Builder Prompt Template
```yaml
# Skills: obsidian
# Workdir: E:\_Knowledge\ObsidianVault
# Schedule: "0 10 * * 0" (Sun 10 AM)

Mission: Build 1 complete sample vault per week ready for Gumroad/Notion/Etsy.

Steps:
1. Pick topic from priority list (rotate)
2. Web research: 8-12 fresh sources
3. Create vault in 0-Inbox/Marketplace/[topic]/
   - README.md, MOC.md, 00-sources.md
   - 01-core-concepts/ (5-8 notes)
   - 02-deep-dives/ (3-5 notes)
   - 03-timeline.md, 04-connections.md
4. Apply vault structure (frontmatter, wikilinks, tags)
5. Generate SELL.md with title, description, price, platform suggestions
6. Update BUILD-LOG.md
```

### Marketplace Poster Prompt Template
```yaml
# Skills: obsidian
# Workdir: E:\_Knowledge\ObsidianVault
# Schedule: "0 11 * * *" (Daily 11 AM)

Mission: Draft 1 promotional post/day for different platforms.

Rotation:
- Mon: Twitter/X thread (5-7 tweets)
- Tue: Reddit (r/ObsidianMD, r/SecondBrain, r/AcademicPhilosophy)
- Wed: LinkedIn (professional, longer form)
- Thu: Fiverr gig description improvement
- Fri: Twitter/X single tweet with hook
- Sat: Reddit (different sub)
- Sun: LinkedIn (case study / build-in-public)

Output: POSTS/[YYYY-MM-DD]-[platform].md + CONTENT-CALENDAR.md
```

### Vault Quality Check Prompt Template
```yaml
# Skills: obsidian
# Workdir: E:\_Knowledge\ObsidianVault
# Schedule: "0 14 * * 6" (Sat 2 PM)

Mission: Audit Marketplace vaults for sell-readiness.

Checks per vault:
- README.md > 200 words
- MOC.md links to all notes
- Sources cited (count in 00-sources.md)
- Note count: 10+ (Starter), 30+ (Standard), 50+ (Premium)
- Frontmatter on all notes
- Wikilinks present
- SELL.md exists

Output: QUALITY-REPORT-[YYYY-MM-DD].md + stdout summary
```

### Created Files Structure
```
0-Inbox/Marketplace/
├── BUILD-LOG.md          # Build history
├── CONTENT-CALENDAR.md   # Post schedule
├── POSTS/                # Draft posts (auto-generated)
│   └── [date]-[platform].md
├── [topic-1]/
│   ├── README.md
│   ├── MOC.md
│   ├── 00-sources.md
│   ├── 01-core-concepts/
│   ├── 02-deep-dives/
│   ├── 03-timeline.md
│   ├── 04-connections.md
│   └── SELL.md
├── [topic-2]/
└── QUALITY-REPORT-[date].md
```

### Key Insight
The automation produces **drafts only** — human reviews and posts manually. Safer, no spam risk.

### Pricing Tiers for Output
| Tier | Notes | Price |
|------|-------|-------|
| Starter | 15 + MOC + PDF | ₹999 |
| Standard | 30 + MOC + PDF + graph | ₹1999 |
| Premium | 50 + MOC + PDF + graph + sources | ₹2999 |