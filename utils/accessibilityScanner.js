const fs = require("fs");
const path = require("path");
const axeSource = require("axe-core").source;

const REPORTS_DIR = path.join(__dirname, "..", "reports");
const REPORT_FILE = path.join(REPORTS_DIR, "accessibility-report.json");

/**
 * Inject axe-core into the current page and run an accessibility scan.
 * Returns the full axe results object.
 */
async function runAccessibilityScan(driver) {
  // Inject axe-core source
  await driver.executeScript(axeSource);

  // Run axe and return results
  const results = await driver.executeAsyncScript(`
    var callback = arguments[arguments.length - 1];
    axe.run().then(function(results) {
      callback(results);
    }).catch(function(err) {
      callback({ error: err.message });
    });
  `);

  return results;
}

/**
 * Print a formatted accessibility report to the console.
 */
function printResults(pageName, results) {
  const violations = results.violations || [];

  console.log("\n" + "=".repeat(50));
  console.log("Accessibility Test Results");
  console.log("-".repeat(50));
  console.log(`Page: ${pageName}`);
  console.log(`Scanned: ${new Date().toISOString()}`);
  console.log(`Passes: ${(results.passes || []).length}`);
  console.log(`Violations: ${violations.length}`);
  console.log("-".repeat(50));

  if (violations.length === 0) {
    console.log("  ✓ No accessibility violations found!");
  } else {
    console.log("\nViolations:");
    violations.forEach((v, i) => {
      console.log(`\n  ${i + 1}. ${v.id} (${v.impact})`);
      console.log(`     ${v.description}`);
      console.log(`     Help: ${v.helpUrl}`);
      console.log(`     Affected elements: ${v.nodes.length}`);
      v.nodes.forEach((node) => {
        console.log(`       - ${node.html.substring(0, 100)}`);
      });
    });
  }

  console.log("=".repeat(50));
  return violations;
}

/**
 * Save scan results to the JSON report file.
 * Appends to an array of page results.
 */
function saveReport(pageName, results) {
  if (!fs.existsSync(REPORTS_DIR)) {
    fs.mkdirSync(REPORTS_DIR, { recursive: true });
  }

  let report = [];
  if (fs.existsSync(REPORT_FILE)) {
    try {
      report = JSON.parse(fs.readFileSync(REPORT_FILE, "utf-8"));
    } catch {
      report = [];
    }
  }

  report.push({
    page: pageName,
    timestamp: new Date().toISOString(),
    url: results.url || "",
    violations: (results.violations || []).map((v) => ({
      id: v.id,
      impact: v.impact,
      description: v.description,
      helpUrl: v.helpUrl,
      nodes: v.nodes.map((n) => ({
        html: n.html,
        target: n.target,
        failureSummary: n.failureSummary,
      })),
    })),
    passes: (results.passes || []).length,
    violationCount: (results.violations || []).length,
  });

  fs.writeFileSync(REPORT_FILE, JSON.stringify(report, null, 2), "utf-8");
  console.log(`  📄 Report saved to ${REPORT_FILE}`);
}

/**
 * Take a screenshot and save to the screenshots directory.
 */
async function takeScreenshot(driver, pageName) {
  const screenshotsDir = path.join(__dirname, "..", "screenshots");
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  const safeName = pageName.replace(/[^a-z0-9]/gi, "_").toLowerCase();
  const filePath = path.join(screenshotsDir, `${safeName}.png`);

  const image = await driver.takeScreenshot();
  fs.writeFileSync(filePath, image, "base64");
  console.log(`  📸 Screenshot saved to ${filePath}`);
}

/**
 * Full accessibility workflow for a page:
 *  1. Run axe scan
 *  2. Print results
 *  3. Save to report JSON
 *  4. Take screenshot
 */
async function scanPage(driver, pageName) {
  const results = await runAccessibilityScan(driver);
  const violations = printResults(pageName, results);
  saveReport(pageName, results);
  await takeScreenshot(driver, pageName);
  return violations;
}

module.exports = {
  runAccessibilityScan,
  printResults,
  saveReport,
  takeScreenshot,
  scanPage,
};
