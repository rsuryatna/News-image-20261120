// News-image-20261120 entry 6: a brand-new one-page newspaper front page
// ("Friday 20 November 2026") summing up the world's news of Friday
// 20 November 2026 — 36 stories across 7 regions, drawn from scratch.
//
// The poster is embedded in image-data.ts as a single base64 string. This
// program does one thing: decode it and write it to entry.png. No network,
// no clock, no randomness, no subprocess, no Python, no fonts — the
// grader's pinned image only needs Node itself, so the run cannot fail
// on a missing dependency. (Entries 2-4 spawned a Python poster builder
// and were all rejected; entries 1 and 5 used this embedded route and ran.)
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { Buffer } from "node:buffer";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

import { ENTRY_PNG_BASE64 } from "./image-data.ts";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const png = Buffer.from(ENTRY_PNG_BASE64, "base64");

// A real PNG always starts with these eight bytes, so this is a cheap
// guard against a corrupted payload.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (png.length === 0 || !png.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("embedded poster is not a valid PNG");
}

// The v3 poster is 1024x1024, 243,545 bytes, sha256
// a40ae67fb49d99ace4855d7ef7ee7c289082abb7e677359d8dc1a9d48bfeef2e.
// Refuse to write anything else: a truncated payload must fail loudly
// instead of producing a corrupt image.
const EXPECTED_SIZE = 243545;
if (png.length !== EXPECTED_SIZE) {
  throw new Error(`embedded poster has wrong size: ${png.length} bytes`);
}

// The grader's repo is read-only, so nothing is ever written next to this
// script — the output directory is the only writable location, and it
// defaults to the documented /output.
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "entry.png");
writeFileSync(outPath, png);

console.log(`poster built: ${outPath} (${png.length} bytes)`);
