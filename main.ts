// News-image-20261120 entry: a one-page newspaper front page summing up the
// world's news of Friday 20 November 2026.
//
// The poster itself is embedded in image-data.ts as one base64 line. This
// program only decodes it and writes it to entry.png, so every run produces
// byte-identical output: no network, no clock, and no randomness anywhere in
// this path. The poster was drawn from scratch with PIL (see build_poster.py):
// 36 verified stories of the day, 13 featured with original illustrations,
// a world map with numbered pins, 23 numbered briefs, a six-number stat strip,
// and a date-check box naming the Thursday 19 November stories left off the
// page. Every featured story carries its time stamp and a REPORTED tag.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { Buffer } from "node:buffer";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

import { ENTRY_PNG_BASE64 } from "./image-data.ts";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const png = Buffer.from(ENTRY_PNG_BASE64, "base64");

// The PNG signature, as a cheap guard against a corrupted payload: a real
// PNG always starts with these eight bytes. The embedded poster is 1024x1024
// and under 1 MiB, as the bounty requires.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (png.length === 0 || !png.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("embedded poster is not a valid PNG");
}

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), png);
