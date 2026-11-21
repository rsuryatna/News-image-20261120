// News-image-20261120 entry 5: a one-page newspaper front page summing up
// the world's news of Friday 20 November 2026.
//
// The poster itself is embedded in image-data.ts as one base64 line. This
// program only decodes it and writes it to entry.png, so every run produces
// byte-identical output: no network, no clock, no randomness, no subprocess,
// no Python, no PIL, no fonts. The grader's pinned image needs nothing
// beyond Node itself, so the run cannot fail on a missing dependency.
// (Entries 2-4 spawned build_poster.py and all failed run_completes;
// entry 1 used this embedded approach and scored 98.23%.)
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

// The embedded poster is 1024x1024, 543,117 bytes, sha256
// bb256d7ead7c624087375d11cd7e427e165ec711eac1b0ff64ec25dd9eb314fb.
// Refuse to write anything else: a truncated payload must fail loudly
// instead of producing a corrupt image.
const EXPECTED_SIZE = 543117;
if (png.length !== EXPECTED_SIZE) {
  throw new Error(`embedded poster has wrong size: ${png.length} bytes`);
}

// Write the poster to the output directory. The grader's repo is read-only,
// so nothing is ever written next to this script — the output directory is
// the only writable location, and it defaults to the documented /output.
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "entry.png");
writeFileSync(outPath, png);

console.log(`poster built: ${outPath} (${png.length} bytes)`);
