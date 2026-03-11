const { By, until } = require("selenium-webdriver");
const { createDriver } = require("../utils/driver");
const { scanPage } = require("../utils/accessibilityScanner");

const BASE_URL = process.env.BASE_URL || "http://localhost:3000";

async function contactTest() {
  console.log("\n📬 CONTACT PAGE TEST");
  console.log("─".repeat(40));

  const driver = await createDriver();

  try {
    // Step 1: Navigate to contact page
    console.log("  → Navigating to contact page...");
    await driver.get(`${BASE_URL}/contact`);
    await driver.wait(until.titleContains("Contact"), 5000);
    console.log("  ✓ Contact page loaded");

    // Step 2: Verify form elements
    const firstNameInput = await driver.findElement(By.id("firstName"));
    const lastNameInput = await driver.findElement(By.id("lastName"));
    const emailInput = await driver.findElement(By.id("contactEmail"));
    const messageInput = await driver.findElement(By.id("message"));
    const submitBtn = await driver.findElement(By.css(".btn-submit"));
    console.log("  ✓ Contact form elements found");

    // Step 3: Fill form
    console.log("  → Filling contact form...");
    await firstNameInput.sendKeys("Jane");
    await lastNameInput.sendKeys("Doe");
    await emailInput.sendKeys("jane@company.com");
    await messageInput.sendKeys(
      "I'd like to learn more about Signal's data integration features."
    );
    console.log("  ✓ Form filled with test data");

    // Step 4: Run accessibility scan
    console.log("  → Running accessibility scan...");
    const violations = await scanPage(driver, "/contact");

    // Step 5: Submit form
    console.log("  → Submitting contact form...");
    await submitBtn.click();
    await driver.sleep(1000);
    console.log("  ✓ Form submitted");

    return {
      page: "/contact",
      passed: true,
      violationCount: violations.length,
    };
  } catch (err) {
    console.error(`  ✗ Contact test failed: ${err.message}`);
    return { page: "/contact", passed: false, error: err.message };
  } finally {
    await driver.quit();
  }
}

module.exports = { contactTest };
