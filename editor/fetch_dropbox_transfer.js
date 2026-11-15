// Download a Dropbox *Transfer* link (dropbox.com/transfer/...) headlessly: clicks Download -> "continue with download only".
// usage: node fetch_dropbox_transfer.js <transfer-url> <out-dir>   (output is usually a .zip)
const { chromium } = require('playwright');
(async () => {
  const [url, outdir] = process.argv.slice(2);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ acceptDownloads: true, viewport: { width: 1400, height: 1000 } });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
  await page.waitForTimeout(2000);
  try { await page.getByRole('button', { name: 'Decline' }).click({ timeout: 3000 }); } catch {}
  await page.getByRole('button', { name: 'Download' }).first().click();
  await page.waitForTimeout(2500);
  const dlP = page.waitForEvent('download', { timeout: 180000 });
  await page.getByText('continue with download only', { exact: false }).first().click();
  const dl = await dlP;
  const name = dl.suggestedFilename(); console.log('downloading', name);
  await dl.saveAs(outdir + '/' + name);
  console.log('saved', name);
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
