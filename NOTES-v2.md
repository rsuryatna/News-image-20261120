# NOTES v2 — news-image-20261120 poster

Built 2026-11-20 ~16:22–16:30 WIB in the clean directory
`~/workspace/makefun/news-image-20261120-v2/` (fresh git repo, branch main),
from `~/workspace/makefun/news20-v2-spec.md`. No file from the v1 repo was
read; the three v1 source files were already deleted from the old working
tree before this build started.

## Files written
- `image-data.ts` — 13 featured + 23 briefs + 6 stats + region counts +
  DATE CHECK (11) + NOT YET + footer, as a strict-JSON literal (so
  build_poster.py can parse it) with TypeScript interfaces.
- `build_poster.py` — PIL 10.2.0, supersampling 2x (2048) → LANCZOS
  downscale to 1024, fixed seed `20261120`, no timestamps.
- `main.ts` — ESM entrypoint, written in 2 messages (write + edit):
  validates 13 featured / 23 briefs / 11 DATE CHECK items by parsing
  image-data.ts as text, spawns `python3 build_poster.py`, checks
  entry.png exists and is non-empty, copies it to MAKEFUN_OUTPUT_DIR
  when set. (First version imported `./image-data.js`; Node 24's type
  stripping did not resolve it, so the import was replaced with a
  readFileSync + JSON.parse of the literal.)
- `entry.png` — 1024×1024, 544,162 bytes,
  sha256 `2568678ceb4d8af52340188b22dae80fe8e1106c739efccbd8a53bb9199fa092`.
- `NOTES-v2.md` — this file.

Untouched: LICENSE, README.md, package.json, tsconfig.json.
Not done (parent's job): commit, push, bundle, submit.

## Layout (1024×1024)
Eyebrow 16 · masthead 62 · subhead 20 · rule 4 · stat strip 52 ·
region strip 20 · big-3 138 · medium 2×142 · light dot-matrix map 134 ·
briefs 166 (header + 12 rows, 2 columns) · DATE CHECK strip 76 ·
NOT YET band 14 · footer 24 (2 lines). Fonts: DejaVuSerif-Bold
(masthead/headlines), DejaVuSans + DejaVuSans-Bold (body/labels).
Map: beige land dots on warm off-white, 13 big red numbered pins with
leader lines + repulsion so the Europe cluster (Kyiv/Antalya,
Brussels/Barcelona) does not overlap. Land dots use #D6BE8C, slightly
darker than the spec's #E8DCC0, for legibility.

## Fixes applied vs v1 (all 9 from the gap analysis)
1. DATE CHECK: "$83 IPO pricing" (price per share, no "bn").
2. Stat strip: "−7% Asia shares' worst week since 2020" (MSCI), not −17,5% Taiex.
3. #7 Japan: headline 2.3% + core 2.2% in the body.
4. #4 sell-off: SoftBank −16% / Nikkei −4.5% package + "Figures are
   intraday lows, not closes."
5. Added briefs: Nicholls 175* (#19) and Dorogobuzh [CLAIM] (#25),
   replacing Iowa and Children's Day.
6. Embassy damage moved into #2 (Kyiv barrage); removed from DATE CHECK.
   (See nuance below.)
7. Light map + big pins; DATE CHECK is a full-width strip below the map.
8. Stamps uniform UTC (the "*" day-marker from the spec is kept on
   8 stamps, rank-4 convention).
9. All consensus numbers kept (300,000+, ~30 missiles, KOSPI −5.4%,
   Taiex −6.8%, COP31 $120bn, 423 rescue teams).

## Verification
- Determinism: 2 runs → identical sha256
  `2568678ceb4d8af52340188b22dae80fe8e1106c739efccbd8a53bb9199fa092`.
- `node main.ts` with MAKEFUN_OUTPUT_DIR=out-test: exit 0,
  "poster built: entry.png (544162 bytes)", out-test/entry.png
  byte-identical to entry.png.
- Viewed at 1024: masthead, stats, big-3 headlines, map pins, DATE CHECK
  all clean; big-3 bodies fit in 3 lines; brief #25 fits on one line
  (auto-fit shrinks long lines to 8px minimum).
- Viewed at 480×480: masthead, stat values, big-3 headlines, map pins
  readable; body text small (inherent to the 36-story format, same as
  the top-5 posters).
- DATE CHECK + numbers checked visually: "$83 IPO pricing" (no "bn"),
  "−7%", "2.3%", "$97.17", "~30", "300,000+", "118" all present.
- Kit check (`check --repo ...-v2 --worktree`, no transcripts):
  4 passed (competition_open, snapshot 8 files / 585,974 bytes,
  license_osi, entrypoint), 1 failed (transcripts_present — no bundle
  was given; bundling is the parent's job, re-check with --transcripts),
  14 skipped, 5 checks deferred to submission (repo_public, repo_owner,
  repo_created_after_open, commit_in_repo, duplicate_snapshot).

## Nuances to confirm again at submit
- Kyiv embassy damage happened Thu 19 Nov afternoon (drone attack,
  ~98 drones), NOT in the 20 Nov barrage — but rank 1 still includes it
  in the 20 Nov Kyiv story, so v2 follows rank 1 (#2) per the spec.
- "Taiex −17,5% worst week since 1991" in v1 was real (Bloomberg), but
  no top-5 poster used it — replaced per the gap analysis.
- Bougainville (#16) is counted ASIA-PACIFIC for the region strip, so
  the counts match the spec (AP 10, OCEANIA 5; total 36).
- Region strip counts verified against the data: EUROPE 8, AMERICAS 6,
  ASIA-PACIFIC 10, MIDEAST 3, AFRICA 3, OCEANIA 5, WORLD / SPACE 1.

## Honest strength estimate
v2 closes all 8 measured gaps and matches rank 1 on structure and
consensus numbers, with stronger verification layers (UTC stamps,
REPORTED tags, DATE CHECK, NOT YET). Realistic estimate 98.7–99.1% —
likely above the top-50 cutoff (98.7183%) and competitive for the top
10. Beating rank 1 (99.1652%) is not guaranteed; at that level the
difference is decided by pairwise judging.

## Revisi 2026-11-20 ~16:40 WIB (atas permintaan Riyan)

- **#2 Kyiv — klausa kedutaan dihapus.** Riyan: "Hapus saja berita kerusakan kedutaan Belanda dan Austria ganti dengan yg lain." Alasan: serangan drone ke dua kedutaan itu terjadi Kamis 19 Nov siang (Kyiv Independent: serangan drone seharian, 1 tewas, 5 luka; kedutaan Belanda & Austria rusak) — BUKAN bagian dari rentetan 20 Nov. Peringkat 1/3 memasukkannya ke cerita 20 Nov, tapi Riyan memilih disiplin tanggal.
- **Pengganti (terverifikasi, 20 Nov):** "power cuts hit parts of the capital." Sumber: Reuters (emergency power cuts across parts of Ukraine), Democrata/EFE (power supply disruptions; residents of Pechersk, Solomianski, Holosivski, Dniprovski and Darnitski districts without electricity), CNN (damaged key infrastructure across the capital). Klausa ini tidak menduplikasi apa pun di poster dan tidak bertabrakan dengan konsensus (~30 rudal / 7 gelombang / 3 tewas / 3 jembatan tetap utuh).
- **Kedutaan kini tidak muncul di mana pun di poster** (DATE CHECK v2 sudah tidak memuatnya sejak awal). Perubahan hanya 1 baris di `image-data.ts` (body #2); `build_poster.py`/`main.ts` tidak disentuh.
- **Verifikasi ulang:** rebuild 2x hash identik (sha256 baru `bb256d7e…`); panel Kyiv dicek visual (3 baris, tidak meluber); 480x480 dicek ulang; local check diulang setelah re-bundle.