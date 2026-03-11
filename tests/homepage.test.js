const { By, until } = require("selenium-webdriver");
const { createDriver } = require("../utils/driver");
const { scanPage } = require("../utils/accessibilityScanner");

const BASE_URL = process.env.BASE_URL || "http://localhost:3000";

async function homepageTest() {
  console.log("\n🏠 HOMEPAGE TEST");
  console.log("─".repeat(40));

  const driver = await createDriver();

  try {
    // Step 1: Open homepage
    console.log("  → Navigating to homepage...");
    await driver.get(BASE_URL);
    await driver.wait(until.titleContains("Signal"), 5000);
    console.log("  ✓ Homepage loaded");

    // Step 2: Verify hero content
    const heading = await driver.findElement(By.css(".hero h1"));
    const headingText = await heading.getText();
    console.log(`  ✓ Hero heading found: "${headingText.substring(0, 40)}..."`);

    // Step 3: Verify nav links
    const navLinks = await driver.findElements(By.css(".nav-links a"));
    console.log(`  ✓ Navigation links found: ${navLinks.length}`);

    // Step 4: Verify features section
    const features = await driver.findElements(By.css(".feature-card"));
    console.log(`  ✓ Feature cards found: ${features.length}`);

    // Step 5: Click "Book a demo" CTA
    const ctaButton = await driver.findElement(By.css(".hero .btn-demo"));
    console.log("  → Clicking 'Book a demo' CTA...");
    await ctaButton.click();
    await driver.wait(until.urlContains("/contact"), 5000);
    console.log("  ✓ Navigated to contact page");

    // Navigate back to homepage for accessibility scan
    await driver.get(BASE_URL);
    await driver.wait(until.titleContains("Signal"), 5000);

    // Step 6: Run accessibility scan
    console.log("  → Running accessibility scan...");
    const violations = await scanPage(driver, "/home");

    return {
      page: "/home",
      passed: true,
      violationCount: violations.length,
    };
  } catch (err) {
    console.error(`  ✗ Homepage test failed: ${err.message}`);
    return { page: "/home", passed: false, error: err.message };
  } finally {
    await driver.quit();
  }
}

module.exports = { homepageTest };
