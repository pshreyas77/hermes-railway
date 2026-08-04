# Wikipedia Extraction Techniques for Factual Verification

## Problem
Wikipedia pages are large (often 3000+ lines in the accessibility tree). `browser_snapshot(full=true)` truncates. You need specific sections (Education, Results, Aftermath) without loading the entire page.

## Technique: browser_console + innerText + indexOf

Navigate to the Wikipedia page, then use `browser_console` with a JavaScript expression to extract just the section you need:

### Extract a named section (e.g., "Early life and education")
```javascript
(() => {
  const text = document.querySelector('#mw-content-text').innerText;
  const idx = text.indexOf('Early life and education');
  return idx >= 0 ? text.substring(idx, idx + 1000) : 'not found';
})()
```

### Extract the infobox (contains Alma mater, Born, Education fields)
```javascript
(() => {
  const text = document.querySelector('#mw-content-text').innerText;
  return text.substring(0, 1500); // infobox is always at the top
})()
```

### Extract election results table
```javascript
(() => {
  const text = document.querySelector('#mw-content-text').innerText;
  const idx = text.indexOf('Results');
  return text.substring(idx, idx + 3000);
})()
```

### Search for a keyword within the page text
```javascript
(() => {
  const text = document.querySelector('#mw-content-text').innerText;
  const idx = text.indexOf('barrister') > -1 ? text.indexOf('barrister') : text.indexOf('Barrister');
  return idx >= 0 ? text.substring(Math.max(0, idx - 100), idx + 500) : 'not found';
})()
```

### Extract a specific results subsection (e.g., "Results by division")
```javascript
(() => {
  const text = document.querySelector('#mw-content-text').innerText;
  const idx = text.indexOf('Results by division');
  return idx >= 0 ? text.substring(idx, idx + 2000) : 'not found';
})()
```

### Extract the "Aftermath" / "Government formation" section
```javascript
(() => {
  const text = document.querySelector('#mw-content-text').innerText;
  const idx = text.indexOf('Aftermath');
  return idx >= 0 ? text.substring(idx, idx + 2000) : 'not found';
})()
```

### Detect a Wikipedia 404-stub page (no article exists at this URL)
```javascript
(() => {
  const text = document.querySelector('#mw-content-text').innerText;
  return text.includes('Wikipedia does not have an article with this exact name');
})()
```
If this returns `true`, the page is a stub. Do NOT try to extract content — pivot immediately to a related real page (e.g., from a topic-keyword article to its parent state/region page).

## Key Notes
- `#mw-content-text` is the main content div on Wikipedia
- Section headings appear as plain text in `innerText` (e.g., "Early life and education\n\n...")
- The infobox (with Alma mater, Born date, Party) is always at the very start of `innerText`
- Election results include "Results by division", "Results by district" subsections — adjust substring length accordingly
- If `indexOf` returns -1, try alternative spellings (e.g., "education" vs "Education")
- For Wikipedia pages with edit-warning banners, ignore the banner text and search for the actual section heading

## Session Example
When verifying Indian Muslim political leaders' qualifications:
1. Navigated to `https://en.wikipedia.org/wiki/Najma_Heptulla`
2. Used `indexOf('Early life and background')` to extract: "obtained an M.Sc. and a Ph.D. degree, both in Zoology (Cardiac Anatomy) from Vikram University, Ujjain"
3. Corrected training-data claim of "Colorado" to actual: "Vikram University, Ujjain"

## Session Example: Election results (J&K 2024)
1. Browsed `https://en.wikipedia.org/wiki/2024_Jammu_and_Kashmir_Legislative_Assembly_election`
2. Used `indexOf('Results')` to extract the party/alliance seat-share table
3. Used `indexOf('Aftermath')` to extract the government-formation narrative
4. Used `indexOf('Results by division')` to extract the Kashmir-vs-Jammu split
5. Result: got accurate, current-year numbers without relying on stale training data

## Session Example: 404-stub detection
1. Tried `https://en.wikipedia.org/wiki/Bharatiya_Janata_Party_in_Jammu_and_Kashmir` — returned a "Wikipedia does not have an article with this exact name" stub
2. Detected via the `text.includes('Wikipedia does not have an article with this exact name')` snippet
3. Pivoted immediately to `Jammu_and_Kashmir_Legislative_Assembly` and `2014_Jammu_and_Kashmir_Legislative_Assembly_election` for the historical data instead
