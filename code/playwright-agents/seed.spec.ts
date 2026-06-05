import { test } from '@playwright/test';

test('seed', async ({ page }) => {
  await page.goto('https://parabank.parasoft.com/parabank/register.htm');
});
