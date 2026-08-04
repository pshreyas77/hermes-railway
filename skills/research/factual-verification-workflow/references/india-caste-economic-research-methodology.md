# India Caste/Economic Data Research Methodology — Session Reference

**Session:** 2026-07-27 | **Context:** Caste-based economic/resource ownership across Indian states

---

## Primary Government Data Sources (Verified Accessible)

| Source | Dataset | Access Method | Key Variables |
|--------|---------|---------------|---------------|
| **NSSO 70th Round (2013)** | Land & Livestock Holdings | MOSPI reports / EPW articles | % agri land by social group (SC/ST/OBC/General) |
| **SECC 2011** | Socio-Economic Caste Census | Govt portal (partial) | Asset ownership, deprivation indices by caste |
| **PLFS (Annual)** | Periodic Labour Force Survey | MOSPI dashboard | WPR, unemployment, wages by social group |
| **AIDIS (2019)** | All India Debt & Investment Survey | RBI/MOSPI | Credit access, indebtedness by caste |
| **Economic Census (2013/2019)** | Establishment & enterprise data | MOSPI | Business ownership by social group |
| **Bihar Caste Survey 2023** | State-level caste enumeration | Bihar govt PDFs | Population %, land, jobs, education by jati |
| **Telangana SEEPC 2024** | Socio-Economic Educational Political Caste | Telangana govt | 7 castes control 51.4% land (Reddy 13.5%) |

---

## Trusted Non-Godi Media Sources (Per User Rule)

**Allowed:** The Wire, Scroll.in, The Hindu, Indian Express, Article 14, BBC, Reuters, Al Jazeera, DW, EPW, IndiaSpend, The Federal, NewsClick, Newslaundry, Caravan, Frontline, Down to Earth, PARI, Behanbox, Khabar Lahariya

**Excluded:** Republic TV, Zee News, Times Now, Aaj Tak, India TV, NewsX, TV9, OpIndia, Swarajya, PGurus

---

## PDF Download Workflow (Internet Archive)

```bash
# 1. Search archive.org for govt orders / reports
# 2. Get item identifier from search results
# 3. Direct PDF download:
curl -L -o "OUTPUT.pdf" "https://archive.org/download/ITEM_ID/ITEM_ID.pdf"

# Example (Telangana GOs):
curl -L -o "TSGO_2022.pdf" "https://archive.org/download/TSGO-2022-05-19/TSGO-2022-05-19.pdf"
curl -L -o "TSGO_2025.pdf" "https://archive.org/download/TSGO-2025-05-12/TSGO-2025-05-12.pdf"
```

---

## Confidence Labeling Standard (Per User Requirement)

| Label | Criteria |
|-------|----------|
| **HIGH** | NSSO/SECC/PLFS direct tables; Bihar/Telangana official survey PDFs; MOSPI published reports |
| **MEDIUM** | EPW/academic studies citing govt data; state economic surveys; reputable media citing official RTI |
| **LOW** | Media reports without source links; aggregated "estimates"; pre-2011 data used for current claims |
| **VERIFIED ABSENT** | Exhaustive search found no data (e.g., no self-authored English PDFs by historical figure) |

**Always tag:** `[HIGH CONFIDENCE]`, `[MEDIUM CONFIDENCE]`, `[LOW CONFIDENCE]`, `[VERIFIED ABSENT]`

---

## Research Patterns Discovered This Session

### 1. Wikipedia Extraction (Fastest for Demographics)
```javascript
// In browser console on Wikipedia page:
(() => { const t = document.querySelector('#mw-content-text').innerText; return t.substring(t.indexOf('Population'), t.indexOf('Population')+2000); })()
```
- Ezhava: "about 23% of Kerala population in 2010s" (infobox: 8M/33M)
- Jat: "~25-30% of Punjab/Haryana population"
- Patidar: "12-21.7% of Gujarat" (range across sources)

### 2. Government PDF Direct Links (When Search Works)
- `https://www.mospi.gov.in/publication_reports` → NSSO reports
- `https://censusindia.gov.in/census.website/` → SECC (partial)
- State portals: `telangana.gov.in`, `bihar.gov.in` → "Caste Survey" sections

### 3. Academic Citation Chaining
- EPW articles → reference lists → NSSO report numbers → MOSPI PDFs
- Ghanta (2013) "From Reform to Revolution" → cites Kshīrasāgara (1994), Shyamlal (2002)

---

## Output Format Template (Per User Spec)

```markdown
## STATE NAME
**Data Confidence: HIGH/MEDIUM/LOW**

### Land Ownership (% agri land by caste)
- **Caste A**: X% [SOURCE, YEAR] — [CONFIDENCE]
- **Caste B**: Y% [SOURCE, YEAR] — [CONFIDENCE]

### Government Jobs / Bank Credit / Business Ownership
- **Metric**: Value by caste [SOURCE] — [CONFIDENCE]

### Dominant Economic Castes (2-3)
1. **Caste** — Land % / Business sector / Political leverage
2. **Caste** — ...

### Unique Patterns
- e.g., "Cooperative sector dominance (Maharashtra sugar)"
- e.g., "Diaspora wealth reinvestment (Gujarat Patidars)"
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Correction |
|--------------|------------|
| Single-number claims without range | Always give range + source year |
| "OBC owns X%" without sub-caste | Disaggregate where possible (Yadav vs Kurmi vs Koeri) |
| Citing media without govt source link | Trace to NSSO/SECC/PLFS table number |
| Using 2011 Census for 2024 claims | Label "[2011 DATA — MAY BE STALE]" |
| Assuming all-India applies to state | State-level variation is massive (Kerala ≠ Bihar) |

---

## Vault Storage Convention

```
E:/_Knowledge/ObsidianVault/Research/India/
├── Caste_Resource_Ownership_by_State.md     # Master synthesis
├── Figures/
│   ├── bhagya_reddy_varma.md
│   └── sources/
│       ├── ghanta_2013_adi_hindu.pdf
│       ├── TSGO_BhagyaReddyVarma_2022.pdf
│       ├── TSGO_BhagyaReddyVarma_2025.pdf
│       └── shyamlal_2002_citation.txt
└── Methodology/
    └── india_caste_economic_research.md     # This file
```

---

*Generated from 2026-07-27 session — caste economic research across 16 Indian states*