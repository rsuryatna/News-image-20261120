[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/rsuryatna/News-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)
[![reward](https://make.fun/badge/news-image-20261120/rsuryatna/News-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# The World Today — 20 November 2026

A one-page newspaper front page summing up the world's news of Friday
20 November 2026 in a single 1024x1024 image: **36 stories** — 13 featured
with original illustrations, a world map with numbered pins, 23 numbered
briefs, a six-number stat strip, and a date-check box naming the Thursday
19 November stories left off the page. Every featured story carries its time
stamp and a REPORTED tag.

## Poster

The embedded poster is 1024x1024, 543,117 bytes, sha256
`bb256d7ead7c624087375d11cd7e427e165ec711eac1b0ff64ec25dd9eb314fb`.
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
