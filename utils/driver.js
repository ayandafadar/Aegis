const { Builder } = require("selenium-webdriver");
const chrome = require("selenium-webdriver/chrome");

/**
 * Creates and returns a configured Selenium WebDriver instance.
 * Uses headless Chrome for CI compatibility.
 */
async function createDriver() {
  const options = new chrome.Options();
  options.addArguments(
    "--headless=new",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--window-size=1280,900"
  );

  const driver = await new Builder()
    .forBrowser("chrome")
    .setChromeOptions(options)
    .build();

  return driver;
}

module.exports = { createDriver };
