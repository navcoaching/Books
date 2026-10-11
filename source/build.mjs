// يبني ملف PDF من book.html باستخدام Chromium (Playwright).
// الاستخدام: node source/build.mjs [مسار الإخراج] [--shots مجلد_اللقطات]
import { createRequire } from 'module';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
let pw;
try { pw = require('playwright'); } catch { pw = require('/opt/node-tools/node_modules/playwright'); }

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const out = path.resolve(args[0] && !args[0].startsWith('--') ? args[0] : path.join(here, '..', 'output', args.includes('--mobile') ? 'navcoaching-training-booklet-mobile.pdf' : 'navcoaching-training-booklet.pdf'));
const shotsIdx = args.indexOf('--shots');
const shots = shotsIdx > -1 ? path.resolve(args[shotsIdx + 1]) : null;
const mobile = args.includes('--mobile');

const browser = await pw.chromium.launch();
const page = await browser.newPage({ viewport: { width: 900, height: 1200 }, deviceScaleFactor: 2 });
page.on('pageerror', (e) => console.log('[err]', e.message));
page.on('console', (m) => { if (m.type() === 'warning' || m.type() === 'error') console.log('[page]', m.text()); });
await page.goto('file://' + path.join(here, 'book.html') + (mobile ? '?m=1' : ''));
await page.waitForSelector('body[data-ready="1"]', { timeout: 60000, state: 'attached' });
const layout = await page.evaluate(() => window.__layout);
console.log('pages:', layout.pages, 'issues:', JSON.stringify(layout.issues));

if (shots) {
  fs.mkdirSync(shots, { recursive: true });
  const els = await page.$$('#book > .page');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: path.join(shots, `p${String(i + 1).padStart(2, '0')}.png`) });
}
fs.mkdirSync(path.dirname(out), { recursive: true });
await page.emulateMedia({ media: 'print' });
await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true, tagged: true, outline: true });
console.log('PDF:', out);
await browser.close();
