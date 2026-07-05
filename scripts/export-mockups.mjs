/**
 * Export Etsy mockup HTML artboards to PNG images.
 * Usage: node scripts/export-mockups.mjs
 */
import { chromium } from "playwright";
import { fileURLToPath } from "url";
import path from "path";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const mockupsDir = path.join(root, "mockups");
const outDir = path.join(mockupsDir, "images");

const exports = [
  { html: "etsy-shop-banner.html", png: "etsy-shop-banner.png" },
  { html: "etsy-shop-icon.html", png: "etsy-shop-icon.png" },
  { html: "listing-etsy-website.html", png: "listing-etsy-website.png" },
  { html: "listing-beyond-etsy.html", png: "listing-beyond-etsy.png" },
  { html: "listing-summit-ecommerce.html", png: "listing-summit-ecommerce.png" },
  { html: "listing-waas-care.html", png: "listing-waas-care.png" },
  { html: "etsy-shop-page.html", png: "etsy-shop-page.png" },
];

fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage();

for (const { html, png } of exports) {
  const filePath = path.join(mockupsDir, html);
  const outPath = path.join(outDir, png);

  await page.goto(`file:///${filePath.replace(/\\/g, "/")}`, { waitUntil: "networkidle" });
  await page.addStyleTag({
    content: `
      body { margin: 0 !important; padding: 0 !important; background: transparent !important; display: block !important; }
      .artboard { transform: none !important; margin: 0 !important; }
    `,
  });
  await page.waitForTimeout(300);

  const artboard = page.locator(".artboard");
  await artboard.screenshot({ path: outPath, type: "png" });
  console.log(`Wrote ${path.relative(root, outPath)}`);
}

await browser.close();
console.log("Done.");
