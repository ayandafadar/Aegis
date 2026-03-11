const { By, until } = require("selenium-webdriver");
const { createDriver } = require("../utils/driver");
const { scanPage } = require("../utils/accessibilityScanner");

const BASE_URL = process.env.BASE_URL || "http://localhost:3000";

async function loginTest() {
  console.log("\n🔐 LOGIN PAGE TEST");
  console.log("─".repeat(40));

  const driver = await createDriver();

  try {
    // Step 1: Navigate from homepage to login
    console.log("  → Navigating to homepage...");
    await driver.get(BASE_URL);
    await driver.wait(until.titleContains("Signal"), 5000);

    console.log("  → Clicking 'Sign in' link...");
    const signInLink = await driver.findElement(By.css('a.signin'));
    await signInLink.click();
    await driver.wait(until.urlContains("/login"), 5000);
    console.log("  ✓ Login page loaded");

    // Step 2: Verify login form elements
    const emailInput = await driver.findElement(By.id("email"));
    const passwordInput = await driver.findElement(By.id("password"));
    const submitBtn = await driver.findElement(By.css(".btn-login"));
    console.log("  ✓ Login form elements found");

    // Step 3: Fill form
    console.log("  → Filling login form...");
    await emailInput.sendKeys("test@signal.io");
    await passwordInput.sendKeys("TestPass123!");
    console.log("  ✓ Form filled with test credentials");

    // Step 4: Run accessibility scan BEFORE submit
    console.log("  → Running accessibility scan...");
    const violations = await scanPage(driver, "/login");

    // Step 5: Submit form
    console.log("  → Submitting login form...");
    await submitBtn.click();

    // Wait a moment for submission
    await driver.sleep(1000);
    console.log("  ✓ Form submitted");

    return {
      page: "/login",
      passed: true,
      violationCount: violations.length,
    };
  } catch (err) {
    console.error(`  ✗ Login test failed: ${err.message}`);
    return { page: "/login", passed: false, error: err.message };
  } finally {
    await driver.quit();
  }
}

module.exports = { loginTest };
