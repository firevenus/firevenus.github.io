---
title: "Waiting on AI? Here Are the YouTube Channels I Actually Listen to"
description: "Bored in the gaps between AI outputs? Here's how I built a background layer of YouTube channels worth keeping on - verified people, verified freshness."
date: 2026-08-03
author: Enki Yan
tags: [YouTube, AI, Productivity]
---

# Waiting on AI? Here Are the YouTube Channels I Actually Listen to

*Bored in the gaps between AI outputs? You're not alone. Here's how I built a "background layer" of YouTube worth keeping on — curated from my own taste, with a lot of AI help.*

## The problem: dead air while the AI works

You know the moment. You've sent the prompt, the AI is churning — maybe it's writing code, generating an image, crunching through a report. That gap is too short for real work and too long to sit in silence. You reach for your phone… and instantly you're gone: scrolling, reacting, pulled out of the flow. Coming back to the result feels like waking up.

I'm a heavy YouTube user, so my solution is a "background layer" — channels I can *listen to* while I work, pause the moment a result lands, and pick right back up. No feed-switching, no rabbit holes. Just content that earns the right to sit in the corner of my attention.

The catch: content that's always-on needs to be *trustworthy*. And YouTube's finance/trading/tech corner is one of the noisiest places on the internet — day-trading gurus, "get rich quick" promoters, course salesmen, signal pushers. So I built a simple process, and had AI do the grunt work. Two filters, that's it.

## The two filters (my taste, enforced by AI)

**Filter 1 — Real people who actually do the thing.** The person behind the channel has to be independently verifiable as a practitioner: a hedge fund partner who teaches finance on the side, a professor who runs a quant fund, a working developer explaining the job. If I can't confirm who they are outside their own channel's marketing, they don't make the cut — no matter how good the videos look.

**Filter 2 — Active within the last 6 months.** A great channel that stopped uploading two years ago is a museum, not a listening companion. My AI checks each channel's official YouTube RSS feed and stamps the real date of the latest upload — no guessing, no trusting third-party "last video" sites.

> Small technical note, since I learned this the hard way: the feed-level `<published>` tag in a YouTube RSS feed is the channel's *creation* date, not a video date — you have to read the dates inside each `<entry>`. And Python's default `urllib` user-agent gets blocked by Cloudflare (HTTP 403, error 1010) — send a browser `User-Agent` header and it works.

## What made my list (English, verified active in 2026)

### Quant & data science

| Channel | Who's behind it | Latest upload |
|---|---|---|
| Patrick Boyle on Finance | Quant HF partner + King's College professor | 2026-07-25 |
| StatQuest with Josh Starmer | Stats/ML educator | 2026-07-13 |
| QuantPy | Financial mathematics, Python strategy implementation | 2026-02-20 |
| Flirting with Models | CIO of Newfound Research, factor investing podcast | 2026-07-06 |
| The Algorithmic Advantage | Interviews with professional systematic traders | 2026-07-20 |
| Coding Jesus | Working quant developer | 2026-07-31 |

### AI

| Channel | Why it's on | Latest upload |
|---|---|---|
| AI Explained | Calm, non-hyped AI industry analysis | 2026-07-22 |
| Matt Wolfe | Weekly AI tools reviews | 2026-08-01 |
| AI Jason | Building LLM apps and multi-agent systems | 2026-07-30 |
| Andrej Karpathy | *Special case — see below* | 2025-02-27 |

### Game development (my day job)

| Channel | Why it's on | Latest upload |
|---|---|---|
| Game Maker's Toolkit | Game design analysis (Boss Keys series) | 2026-07-22 |
| GDC | Official game developers conference talks | 2026-07-31 |
| Sebastian Lague | Procedural generation & simulations | 2026-07-25 |

## What got cut (saying no is the point)

- A famous economist with great macro takes → dropped: no personal channel; their content lives on media outlets, nothing stable to subscribe to.
- A popular science channel, 615 days silent → dropped: a museum, not a feed.
- A classic Unity tutorial channel, 195 days idle → dropped from the active list.
- **The special case**: Andrej Karpathy publishes maybe twice a year (520+ days of silence at check time) — but every video is a masterclass in understanding AI from first principles. The freshness rule would kill it, so it gets an explicit carve-out: *low-frequency, high-quality exceptions are flagged and decided by the human, not auto-deleted.*

That's the nuance: the filters are a **default**, not a dictatorship. They exist to force a conscious decision about every subscription — not to automate taste.

## If you want to try one tonight

- **Pure background listening** (no screen needed): Patrick Boyle, Flirting with Models, AI Explained — long-form, spoken-word, zero visual dependency.
- **Worth keeping an eye on**: StatQuest, Sebastian Lague — great content, but you'll want to actually watch.
- **The "waiting room" starter pack**: one channel from each table above. That's a solid month of gap-filling.

*Verified August 2026. This is my personal list built on my own taste — the AI did the verifying, not the choosing. If you have channels that survive these two filters, I'd genuinely love to hear them — the list is always hungry.*
