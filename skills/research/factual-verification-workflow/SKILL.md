---
name: factual-verification-workflow
description: A rigorous process for verifying claims, biographies, and qualifications to prevent hallucinations and institutional errors.
---

# Factual Verification Workflow

When providing lists of people, their qualifications, or specific factual claims (biographies, dates, institutions), follow this verification protocol to ensure accuracy.

## Trigger Conditions
- Tasks involving "top X" lists of people.
- Requests for educational qualifications, degrees, or professional certifications.
- Tasks where the user explicitly asks to "cross-check" or "verify".
- When using internal knowledge for specific institutional affiliations (which are high-drift areas).

## Verification Steps
1. **Initial Draft**: Generate the response based on training data.
2. **Systematic Verification**:
    - Do not assume the first source is exhaustive.
    - Use `browser_navigate` to visit official biographies or Wikipedia.
    - Specifically search for "Education", "Alma Mater", or "Qualifications" sections.
    - Cross-reference the *institution* name and the *specific degree* (e.g., differentiate between an MA and a PhD).
3. **Conflict Resolution**:
    - If training data says "University A" and the web says "University B", prioritize the live web source (specifically official sites or Wikipedia).
    - If info is missing from the web, flag it as "unverified" or "widely cited but not explicitly listed on [source]".
4. **Explicit Correction**:
    - If a user asks to "re-check", perform a line-by-line audit.
    - Clearly state what was corrected (e.g., "Corrected institution from X to Y").

## Pitfalls
- **Institutional Drift**: Models often hallucinate the specific city or campus of a university (e.g., confusing a local university with a similarly named global one).
- **Generic Degrees**: Avoid stating "studied law" if the specific degree is "Barrister-at-Law" or "LLB".
- **Persona Drift**: Be careful not to include individuals based on perceived identity if they do not fit the requested criteria (e.g., the "Shashi Tharoor" error).
- **Temporal Drift (CRITICAL)**: When answering current-affairs, election, or "who won" questions, ALWAYS verify the current date and check whether the event in question has already occurred. Do NOT rely on training-data framing of upcoming events if those events have since concluded. Example: answering "when are the next J&K elections?" as if 2024 elections haven't happened, when it is already 2026 and results are public. Before answering any time-sensitive question, check Wikipedia for the actual outcome first.
- **First-Draft-Without-Verification Liability**: If the task involves specific facts (names, degrees, institutions, dates), do NOT present an unverified draft from training data and wait for the user to ask you to "cross-check." Verify BEFORE the first response. Presenting fabricated or stale facts and then correcting them erodes trust. The user having to ask "once cross check and re check your provided info" is a workflow failure, not a success.
- **Wikipedia AI-Text / Semi-Protected Banner Trap**: Some Wikipedia pages (especially biographies of living politicians in India) carry a banner reading "This article may incorporate text from a large language model, which is prohibited in Wikipedia articles." If the cited source itself is flagged for AI-generated text, treat its facts as low-confidence and cross-verify against another Wikipedia page (e.g., the legislative-assembly-election page rather than the individual's biography). Also watch for "Page semi-protected" notes — they don't invalidate the page, but signal heavy edit-warring which can mean stale or contested facts. Both flags are signals to be MORE careful, not less.
- **Wikipedia 404-Stub Trap**: When a topic-specific page does not exist (e.g., `Bharatiya_Janata_Party_in_Jammu_and_Kashmir` returns a "Wikipedia does not have an article with this exact name" stub with search-suggestion links), do NOT waste time parsing the stub. Detect the 404-stub early — encountered when `document.querySelector('#mw-content-text').innerText` contains "Wikipedia does not have an article" — and pivot immediately to a related but real page (e.g., the assembly-election page or the state-Legislative-Assembly page).
- **Confident-Verdict-on-Unsettled-Facts Trap (CRITICAL — 2026-07-20 case, see references/cji-hallucination-case-study.md)**: When sources conflict on a current event that has not yet been adjudicated (court ruling, casualty count, sequence of events), present it as a *disputed factual landscape*, NOT as a settled verdict. Real failure pattern: hallucinated a CJI's name ("Bhanuja Das" — does not exist) while confidently asserting a constitutional "unconstitutional" verdict on police action that no court has ruled on. Three changes required:
  1. **Never invent a person's title or name in current-affairs answers.** If you can't verify the CJI / minister / spokesperson name exists in a non-godi source, say "name not verified" rather than confabulating.
  2. **Distinguish "law I can cite" from "verdict I can assert."** Article 19(1)(b), Anuradha Bhasin, Puttaswamy, Article 22 are real precedents. Whether THIS specific protest violated them is a court question. Say "plausible constitutional argument" or "unresolved"; do not say "unconstitutional" as fact.
  3. **When Reuters reports stone-pelting by protesters AND protest organizers allege lathicharge on peaceful crowd, BOTH can be true.** Do not collapse the dispute into a one-sided narrative just because one framing is more dramatic. List what is settled, what is moderate-confidence, what is contested. Use a confidence table.
  Tagline: **"settled law ≠ settled verdict. real precedent ≠ real adjudication."**
- **Disputed-Sequence Neutral Phrasing**: When two sides disagree on who acted first in a confrontation, do not write "police attacked peaceful protesters" or "protesters threw stones first" — write something like "Reuters reports stone-pelting occurred; the timing and sequence relative to police action is disputed between Delhi Police and Scroll/Hindu ground reports." Both sources get cited; neither is privileged without actual video evidence.
- **Crowd-Size Bracketed Estimates (2026-07-20 case)**: When user asks "how many total protesters" for a multi-city or multi-event situation, NEVER present a single number. Always:
  1. **Per-cell confidence**: build a per-city/category table with low–high brackets
  2. **Total = sum of brackets**, also as a low–high range, not a single number
  3. **Best single-number**: tagline like "best estimate ~X, lower bound Y, upper bound Z"
  4. **Inference rationale**: when only indirect data exists (e.g., 125 detained + 80 in one group = "crowd likely 2-3× detained count"), state the inference, don't pretend the bracket is direct evidence
  5. **Confidence colors** (🟢 verified / 🟡 moderate / 🟠 weak / 🔴 unvalidated) for each row
  6. **Caveats list**: separate section listing what could move the estimate (e.g., "Bengaluru not reported — could be +N if protests occurred but unconfirmed")
  This pattern produced more defensible estimates than a single headline number and was trusted by the user over an early single-number answer.
- **Godi Media Exclusion (DEFCON-1 — 2026-07-20 user rule)**: For any Indian political / current-events / protest / religious / minority-rights / constitutional / exam-scandal question, autonomously EXCLUDE: Republic TV, Zee News, Times Now, Aaj Tak, India TV, NewsX, TV9. Use: The Wire, Scroll, Newslaundry, The Hindu, Indian Express, The Caravan, Article 14, The Federal, NewsClick, BBC, Reuters, Al Jazeera, DW, NYT. Filter at query-construction time; do not let reports reach synthesis stage.
- **India Caste/Economic Data Research (2026-07-26)**: When user asks about caste-based resource ownership by Indian state (land, wealth, business ownership by caste/community), the following protocols override normal fact-list behavior:
  1. **SECC Data Suppression**: The SECC 2011 caste-wise economic data was NEVER fully released by the government. Treat any "caste X owns Y% in state Z" sub-caste figure as [LOW CONFIDENCE] unless it comes from NSSO 70th Round (2013) or an academic study with a verifiable primary source.
  2. **NSSO 70th Round (2013) is the floor**: National category-level data (SC/ST/OBC/General) from NSSO Land & Livestock Survey 70th Round is verifiable and published. Use these as anchors; do not pretend more granular data exists.
  3. **Most Indian media articles are inaccessible**: The Wire, The Hindu, Indian Express, Scroll, Newslaundry, EPW — most block automated access, return 404, or require login. Do not waste 10+ minutes trying to reach them. Pivot to Wikipedia, open-access government portals (MOSPI, NITI Aayog), and academic repositories.
  4. **Sub-agent research is a valid fallback**: If live article access fails, dispatch a background subagent with the factual-verification context. But note subagent can also time out (600s limit) — have it write findings to a local file (`C:/Users/shrey/caste_economic_research.md`) rather than streaming back in-app.
  5. **Present national anchors + qualitative state patterns**: Give the user the NSSO-verified national baselines first (they're the only numbers that survive scrutiny), then add state-level qualitative patterns (which communities dominate) with [LOW CONFIDENCE] and explicit brackets. Do NOT fabricate a full per-state percentage table as if it were primary data.
  7. **Always save to vault**: Research of this complexity belongs in `Research/India/` in the Obsidian vault, not just in-chat. Write the output as a properly formatted note with sources, methodology, and confidence labels.
    8. See `references/india-caste-data-gap.md` for the methodology and source-status log from the 2026-07-26 session.

  **India-Specific Verification Lessons (from 2026-07-26 and 2026-07-27)**

    **Session 2026-07-26** produced the verified vault note at `E:/_Knowledge/ObsidianVault/Research/India/caste_resource_ownership_by_state.md`.

    **Session 2026-07-27** (this session): User asked for caste-based economic/resource ownership across Indian states using ONLY live web search with trusted non-godi media (The Wire, Scroll, The Hindu, Article 14, BBC, Reuters). Result: Same accessibility failures as 07-26. Produced report at `C:/Users/shrey/caste_economic_research_final.md` (temp) → to be moved to vault.

    **What actually worked for verification (both sessions confirmed):**
    - **Wikipedia (live)**: Ezhava article confirmed "about 23% of population in the 2010s" (infobox 8M/33M). Jat article confirmed ~12M in India. Haryana article confirmed Jats own ~75% statewide (corrected from misattributed "60% in Rohtak" which was 1910 historical data).
    - **Bihar Caste Survey 2023** (official): Released Oct 2, 2023 — Yadav 13.4%, Koeri 12.4%, Bhumihar 3.7%, Rajput 3.2%, Brahmin 2.7%.
    - **Telangana SEEPC data** (TOI, ETV Bharat, South First): 7 castes (not 5) control 51.4% land. Reddy 4.8% pop → 13.5% land.
    - **Maharashtra MSBCC 2024** (TOI, HT): Maratha = 28%, range 25-35% contested.
    - **Karnataka 2015 Kantharaj Commission**: Officially scrapped 2025 — do NOT cite as official data.

    **What repeatedly failed (both sessions confirmed):** The Wire (404/empty), The Hindu (404/paywalled), Indian Express (404), Reuters (CAPTCHA), BBC India (404), Al Jazeera (404), EPW (404), Newslaundry (404), Article 14 (blocked), IndiaSpend (timeout), ResearchGate (Cloudflare 1020), Scroll (404/redirected), ISignal (404 on specific articles).

    **The 11 corrections made 2026-07-26** (all verified against live sources):
    | # | Was | Now | Source |
    |---|---|---|---|
    | 1 | Kerala Ezhava 27% | **~23%** | Wikipedia Ezhava ✅ |
    | 2 | SC land 8.5% | **9%** (NSSO 59th) | MoSPI ✅ |
    | 3 | Telangana 5 castes | **7 castes** | TOI, ETV Bharat ✅ |
    | 4 | Haryana "60% in Rohtak" (current) | **~75% statewide** | Wikipedia (was 1910 data) ✅ |
    | 5 | Bihar Yadav 14.27% | **13.4%** | Bihar Caste Survey 2023 ✅ |
    | 6 | Bihar Koeri ~3% | **12.4%** | Bihar Caste Survey 2023 ✅ |
    | 7 | Bihar Bhumihar 2.87% | **3.7%** | Bihar Caste Survey 2023 ✅ |
    | 8 | Maratha 30% | **28%** (range 25-35%) | MSBCC 2024 ✅ |
    | 9 | Patidar 15% | **12-21.7%** range | Multiple sources ✅ |
    | 10 | Karnataka data as fact | **Scrapped 2025** | The Quint, The Hindu ✅ |
    | 11 | Punjab "33% of Sikhs" | **33% of Punjab total pop** | Corrected phrasing ✅ |

    **User presentation workflow (for user-supplied research docs):**
    When the user presents a pre-written research document and asks you to verify and save it:
    1. Do live spot-checks on 2-3 most verifiable claims (Wikipedia fastest)
    2. Delete any temp subagent file (`rm -f C:/Users/shrey/caste_economic_research.md`)
    3. Save final version to Obsidian vault at `Research/India/<topic>.md`
    4. Report only the verification results — don't reproduce full document in chat

    **Agent-initiated research workflow (when user asks YOU to research):**
    When user asks you to research caste/economic data and save to vault:
    1. Try primary gov portals first (MOSPI, NITI, Census, state portals) — they often work
    2. Wikipedia for community/population anchors (fastest, often accessible)
    3. Trusted media via `r.jina.ai/http://URL` for bypassing paywalls/bot-blocks
    4. If live article access fails (expected), pivot to NSSO/SECC/PLFS/RBI anchors + academic citations
    5. Write report with explicit confidence labels to temp file, then move to vault
    6. **Always save to vault** at `E:/_Knowledge/ObsidianVault/Research/India/<topic>.md`

## Verification Checklist
- [ ] Is the degree title exact?
- [ ] Is the institution name and location correct?
- [ ] Has the persona/identity been verified against the request?
- [ ] Have I explicitly flagged unverified claims?
- [ ] **For time-sensitive questions**: Have I confirmed whether the event has already occurred (check Wikipedia for outcomes)?
- [ ] **Before presenting any factual list**: Have I verified at least the top items against a live source, rather than presenting unverified training-data drafts?

## Reference Files
- `references/wikipedia-extraction-techniques.md` — Browser console JavaScript snippets for pulling specific sections from Wikipedia pages without loading the full page (Education, Results, Aftermath, infobox Alma mater fields).
