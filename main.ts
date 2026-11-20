// Entry program for the news-image-20261120 bounty (v2 poster).
//
// This program builds the poster and hands the finished image to the
// grader. It runs build_poster.py (PIL, deterministic: fixed seed, no
// timestamps), checks that entry.png was produced, and copies it to the
// output directory when MAKEFUN_OUTPUT_DIR is set. Nothing here touches
// the network or the clock, so two runs produce the same bytes.

import { spawnSync } from "node:child_process";
import { copyFileSync, existsSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const ENTRY = "entry.png";

function fail(message: string): never {
  console.error(`news-image-20261120: ${message}`);
  process.exit(1);
}

// The poster must carry exactly 36 stories: 13 featured, 23 briefs.
// image-data.ts holds the DATA literal as strict JSON, so read it as text
// and parse it here instead of importing the module (keeps this entry
// point free of cross-module TypeScript imports).
const dataText = readFileSync("image-data.ts", "utf-8");
const anchor = dataText.indexOf("export const DATA");
const jsonStart = dataText.indexOf("{", anchor);
const jsonEnd = dataText.lastIndexOf("}") + 1;
const data = JSON.parse(dataText.slice(jsonStart, jsonEnd)) as {
  featured: unknown[];
  briefs: unknown[];
  dateCheck: unknown[];
};
if (data.featured.length !== 13 || data.briefs.length !== 23) {
  fail(
    `expected 13 featured + 23 briefs, got ${data.featured.length} + ${data.briefs.length}`,
  );
}
if (data.dateCheck.length !== 11) {
  fail(`expected 11 DATE CHECK items, got ${data.dateCheck.length}`);
}

const result = spawnSync("python3", ["build_poster.py"], {
  stdio: "inherit",
});
if (result.error) {
  fail(`could not run build_poster.py: ${result.error.message}`);
}
if (result.status !== 0) {
  fail(`build_poster.py exited with status ${result.status}`);
}

// build_poster.py writes entry.png to MAKEFUN_OUTPUT_DIR when it is set
// (the grader's /output, the only writable directory there), else next
// to this script. Look for it where the builder put it.
const builtPath = process.env.MAKEFUN_OUTPUT_DIR
  ? join(OUTPUT_DIR, ENTRY)
  : ENTRY;

if (!existsSync(builtPath)) {
  // Fallback: the builder may have written next to the script instead;
  // copy it over when that copy exists.
  if (process.env.MAKEFUN_OUTPUT_DIR && existsSync(ENTRY)) {
    try {
      copyFileSync(ENTRY, builtPath);
    } catch (err) {
      fail(`could not copy ${ENTRY} to ${OUTPUT_DIR}: ${(err as Error).message}`);
    }
  } else {
    fail(`build finished but ${builtPath} is missing`);
  }
}
const size = statSync(builtPath).size;
if (size === 0) {
  fail(`${builtPath} is empty`);
}

console.log(`poster built: ${builtPath} (${size} bytes)`);
