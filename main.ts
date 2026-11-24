// make.fun entry runner for competition news-image-20261124.
// Sums up the world's news of Tuesday 24 November 2026 in one image; this
// program copies the generated entry.png into the make.fun output directory.
//
// Runs with no network access and reads nothing beyond the bundled entry.png.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

function copyEntry(): string {
  const source = resolve(process.cwd(), "entry.png");
  if (!existsSync(source)) {
    throw new Error(`entry.png not found at ${source}`);
  }

  // Create the output directory (and any missing parents) before writing.
  mkdirSync(OUTPUT_DIR, { recursive: true });

  const destination = join(resolve(OUTPUT_DIR), "entry.png");
  copyFileSync(source, destination);

  const { size } = statSync(destination);
  console.log(`Copied entry.png -> ${destination} (${size} bytes)`);
  return destination;
}

try {
  copyEntry();
} catch (err) {
  console.error("Failed to publish entry:", err instanceof Error ? err.message : err);
  process.exitCode = 1;
}