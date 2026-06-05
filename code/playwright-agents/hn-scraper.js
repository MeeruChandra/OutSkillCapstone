const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto('https://news.ycombinator.com');
  await page.waitForLoadState('networkidle');

  // Get the top 3 headlines
  const headlines = await page.$$eval('.titleline > a', elements =>
    elements.slice(0, 3).map((el, i) => ({
      rank: i + 1,
      title: el.textContent,
      url: el.href
    }))
  );

  console.log('Top 3 Hacker News Headlines:\n');
  headlines.forEach(h => {
    console.log(`${h.rank}. ${h.title}`);
    console.log(`   ${h.url}\n`);
  });

  await browser.close();
})();
