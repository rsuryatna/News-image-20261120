[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/rsuryatna/News-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)
[![reward](https://make.fun/badge/news-image-20261120/rsuryatna/News-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# Friday 20 November 2026 — The World in One Day

A one-page newspaper front page summing up the world's news of Friday
20 November 2026 in a single 1024x1024 image: **36 stories across 7
regions** — 3 illustrated hero stories (Kyiv bridges, Cyclone Akvan,
the Asia AI sell-off), 10 featured stories with original illustrations,
a world map with numbered pins, 23 numbered briefs, a six-number stat
strip, and a date-check box naming the Thursday 19 November stories
left off the page. Every story carries its source.

This is a brand-new poster (v3), rebuilt from scratch for entry 6 with
a different layout from v2: the date itself is the masthead, the hero
art is drawn as full scenes, and the colour scheme is teal-and-crimson
on warm cream. See NOTES-v3.md for the story list and sources.

## Poster

The embedded poster is 1024x1024, 243,545 bytes, sha256
`a40ae67fb49d99ace4855d7ef7ee7c289082abb7e677359d8dc1a9d48bfeef2e`.
Decoding `ENTRY_PNG_BASE64` reproduces it byte-for-byte; `main.ts` refuses
to write anything else (it checks the PNG signature and the exact size).

## How it runs

The poster is embedded in `image-data.ts` as one base64 line. `main.ts`
only decodes it and writes it to `entry.png`, so every run produces
byte-identical output: no network, no clock, no randomness, no subprocess,
no Python. Run it with:

```sh
node main.ts
```

or, outside the grader, with an explicit output directory:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Bounty

Built for the [news-image-20261120 bounty on make.fun](https://make.fun/bounty/news-image-20261120).
