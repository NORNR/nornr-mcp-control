import { createRequire } from "node:module";
import { mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(join(process.cwd(), "package.json"));
const { chromium } = require("playwright");

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const assetsDir = join(root, "assets");
const framesDir = join(assetsDir, "frames");

mkdirSync(framesDir, { recursive: true });

const stills = [
  "still-01-proposed.svg",
  "still-02-queued.svg",
  "still-03-review.svg",
  "still-04-released.svg",
];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });

for (let index = 0; index < stills.length; index += 1) {
  const still = stills[index];
  const input = `file://${join(assetsDir, still)}`;
  const output = join(framesDir, `frame-${String(index + 1).padStart(2, "0")}.png`);
  await page.goto(input);
  await page.screenshot({ path: output });
}

await browser.close();
