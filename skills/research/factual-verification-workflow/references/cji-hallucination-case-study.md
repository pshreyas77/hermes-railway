# CJI Name Hallucination — Case Study (2026-07-20)

## What Happened
During CJP (Cockroach Janta Party) protest research, the assistant named "Chief Justice Bhanuja Das" as the CJI who made the "cockroach" remark. This CJI does not exist.

## Correct Facts (verified via Wikipedia/browsers)
- **Actual CJI at the time**: **Surya Kant** (not "Bhanuja Das")
- The "cockroach" remark was made in the context of a contempt plea about fake law degrees
- CJI Kant's actual quote: *"There are parasites of society who attack the system... There are youngsters like cockroaches; they don't get any employment, and they don't have any place in a profession. Some of them become media, some of them become social media, some of them become RTI activists, some of them become other activists..."*
- Context: He was specifically criticizing individuals who entered "legal, media, social media, and other noble professions" using **fake degrees** — not all youth or all protesters
- He later clarified his remarks were misquoted and specifically about fake-degree holders, not youth generally

## What Should Have Been Done
1. Never name the CJI or any SC justice from training data in current-affairs contexts
2. Always `browser_navigate` to Wikipedia's article on the specific event/case to get the actual names
3. Wikipedia is reliable for verifiable factual content (dates, titles, quotes) but should be cross-checked for contested claims

## Key Lesson
Indian judicial figures in active legal/political news are **high hallucination risk** — the training data may contain outdated CJI names or plausible-sounding names that don't exist. Always verify with browser.

## Related Pitfall
The `factual-verification-workflow` skill already has a "Wikipedia SSL Certificate Expiry" workaround: use `browser_navigate` instead of Python urllib when Wikipedia SSL fails.