const fs = require("fs");
const path = require("path");

// Clear previous reports and screenshots
const reportsDir = path.join(__dirname, "reports");
const screenshotsDir = path.join(__dirname, "screenshots");

if (fs.existsSync(path.join(reportsDir, "accessibility-report.json"))) {
  fs.unlinkSync(path.join(reportsDir, "accessibility-report.json"));
}

const { homepageTest } = require("./tests/homepage.test");
const { loginTest } = require("./tests/login.test");
const { contactTest } = require("./tests/contact.test");

let server;

async function run() {
  console.log("╔══════════════════════════════════════════════════╗");
  console.log("║   Aegis - Accessibility Testing Integration     ║");
  console.log("║   Selenium + axe-core Automated Scans           ║");
  console.log("╚══════════════════════════════════════════════════╝");

  // Step 1: Start demo web app
  console.log("\n🚀 Starting demo web app...");
  server = require("./demo-app/server");

  // Wait for server to be ready
  await new Promise((resolve) => setTimeout(resolve, 1500));

  const results = [];

  try {
    // Step 2: Run all tests sequentially
    results.push(await homepageTest());
    results.push(await loginTest());
    results.push(await contactTest());

    // Step 3: Print summary
    console.log("\n\n╔══════════════════════════════════════════════════╗");
    console.log("║              TEST SUMMARY                        ║");
    console.log("╠══════════════════════════════════════════════════╣");

    let totalViolations = 0;
    let allPassed = true;

    results.forEach((r) => {
      const status = r.passed ? "✓ PASS" : "✗ FAIL";
      const violations = r.violationCount !== undefined ? r.violationCount : "N/A";
      console.log(`║  ${status}  ${r.page.padEnd(12)} Violations: ${String(violations).padEnd(4)} ║`);
      totalViolations += r.violationCount || 0;
      if (!r.passed) allPassed = false;
    });

    console.log("╠══════════════════════════════════════════════════╣");
    console.log(`║  Total Accessibility Violations: ${String(totalViolations).padEnd(16)} ║`);
    console.log("╚══════════════════════════════════════════════════╝");

    console.log("\n📁 Reports saved to:    ./reports/accessibility-report.json");
    console.log("📸 Screenshots saved to: ./screenshots/");

    // Shut down
    server.close();

    // Exit with appropriate code
    if (!allPassed) {
      console.log("\n❌ Some tests failed.");
      process.exit(1);
    } else if (totalViolations > 0) {
      console.log(`\n⚠️  Tests passed but ${totalViolations} accessibility violation(s) detected.`);
      process.exit(0);
    } else {
      console.log("\n✅ All tests passed with no accessibility violations!");
      process.exit(0);
    }
  } catch (err) {
    console.error("\n💥 Test runner error:", err.message);
    if (server) server.close();
    process.exit(1);
  }
}

run();
