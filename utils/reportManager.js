const fs = require("fs");
const path = require("path");

const REPORTS_DIR = path.join(__dirname, "..", "reports");
const HISTORY_DIR = path.join(REPORTS_DIR, "history");
const SCREENSHOTS_DIR = path.join(__dirname, "..", "screenshots");

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

function buildRunId() {
  const now = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}-${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
}

function initializeRun() {
  ensureDir(REPORTS_DIR);
  ensureDir(HISTORY_DIR);

  const runId = buildRunId();
  const runDir = path.join(HISTORY_DIR, runId);
  ensureDir(runDir);

  return {
    runId,
    runDir,
    logFile: path.join(REPORTS_DIR, "test-run.log"),
    runLogFile: path.join(runDir, "test-run.log"),
    summaryFile: path.join(REPORTS_DIR, "run-summary.json"),
    runSummaryFile: path.join(runDir, "run-summary.json"),
    dashboardFile: path.join(REPORTS_DIR, "report.html"),
    runDashboardFile: path.join(runDir, "report.html"),
    accessibilityFile: path.join(REPORTS_DIR, "accessibility-report.json"),
    runAccessibilityFile: path.join(runDir, "accessibility-report.json"),
  };
}

function clearCurrentRunLog(logFile) {
  fs.writeFileSync(logFile, "", "utf-8");
}

function appendLine(filePath, line) {
  fs.appendFileSync(filePath, line + "\n", "utf-8");
}

function attachConsoleToLog(logFile) {
  const original = {
    log: console.log,
    error: console.error,
    warn: console.warn,
  };

  const toLine = (args) =>
    args
      .map((v) => (typeof v === "string" ? v : JSON.stringify(v)))
      .join(" ");

  console.log = (...args) => {
    appendLine(logFile, toLine(args));
    original.log(...args);
  };

  console.error = (...args) => {
    appendLine(logFile, toLine(args));
    original.error(...args);
  };

  console.warn = (...args) => {
    appendLine(logFile, toLine(args));
    original.warn(...args);
  };

  return () => {
    console.log = original.log;
    console.error = original.error;
    console.warn = original.warn;
  };
}

function writeSummary(summaryFile, summary) {
  fs.writeFileSync(summaryFile, JSON.stringify(summary, null, 2), "utf-8");
}

function safeReadJson(filePath, fallback) {
  if (!fs.existsSync(filePath)) {
    return fallback;
  }

  try {
    return JSON.parse(fs.readFileSync(filePath, "utf-8"));
  } catch {
    return fallback;
  }
}

function renderDashboardHtml(summary, accessibilityReport) {
  const rows = summary.results
    .map((r) => {
      const status = r.passed ? "PASS" : "FAIL";
      const statusClass = r.passed ? "pass" : "fail";
      const violations = r.violationCount !== undefined ? r.violationCount : "N/A";
      const error = r.error ? `<div class="error">${escapeHtml(r.error)}</div>` : "";
      return `
        <tr>
          <td>${escapeHtml(r.page)}</td>
          <td class="${statusClass}">${status}</td>
          <td>${violations}</td>
          <td>${error}</td>
        </tr>`;
    })
    .join("\n");

  const a11yCards = accessibilityReport
    .map((page) => {
      const top = (page.violations || [])
        .slice(0, 4)
        .map((v) => `<li>${escapeHtml(v.id)} (${escapeHtml(v.impact || "unknown")})</li>`)
        .join("");
      return `
        <article class="card">
          <h3>${escapeHtml(page.page)}</h3>
          <p>Violations: <strong>${page.violationCount}</strong></p>
          <p>Passes: <strong>${page.passes}</strong></p>
          <ul>${top || "<li>No violations</li>"}</ul>
        </article>`;
    })
    .join("\n");

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Aegis Test Report</title>
  <style>
    body { font-family: Segoe UI, Arial, sans-serif; background:#f4f6fb; color:#111827; margin:0; }
    .wrap { max-width: 1100px; margin: 24px auto; padding: 0 16px; }
    .top { background:#fff; border:1px solid #dbe1ea; border-radius:10px; padding:16px; margin-bottom:16px; }
    .meta { color:#4b5563; font-size:14px; }
    table { width:100%; border-collapse:collapse; background:#fff; border:1px solid #dbe1ea; border-radius:10px; overflow:hidden; }
    th, td { padding:10px 12px; border-bottom:1px solid #e5e7eb; text-align:left; vertical-align:top; }
    th { background:#f9fafb; }
    .pass { color:#166534; font-weight:700; }
    .fail { color:#991b1b; font-weight:700; }
    .error { color:#7f1d1d; font-size:13px; }
    .cards { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:12px; margin-top:16px; }
    .card { background:#fff; border:1px solid #dbe1ea; border-radius:10px; padding:12px; }
    .links a { color:#1d4ed8; text-decoration:none; margin-right:10px; }
  </style>
</head>
<body>
  <div class="wrap">
    <section class="top">
      <h1>Aegis Automated Test Report</h1>
      <p class="meta">Run ID: ${escapeHtml(summary.runId)} | Time: ${escapeHtml(summary.timestamp)}</p>
      <p class="meta">Tests Passed: ${summary.passedCount}/${summary.results.length} | Total A11y Violations: ${summary.totalViolations}</p>
      <p class="links">
        <a href="/reports/run-summary.json">run-summary.json</a>
        <a href="/reports/accessibility-report.json">accessibility-report.json</a>
        <a href="/reports/test-run.log">test-run.log</a>
        <a href="/report-history">history</a>
      </p>
    </section>

    <table>
      <thead>
        <tr>
          <th>Page</th>
          <th>Status</th>
          <th>Violations</th>
          <th>Error</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>

    <section class="cards">${a11yCards}</section>
  </div>
</body>
</html>`;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function copyIfExists(fromPath, toPath) {
  if (fs.existsSync(fromPath)) {
    fs.copyFileSync(fromPath, toPath);
  }
}

function copyScreenshotsToRunDir(runDir) {
  if (!fs.existsSync(SCREENSHOTS_DIR)) {
    return;
  }

  const screenshotsOut = path.join(runDir, "screenshots");
  ensureDir(screenshotsOut);

  const files = fs.readdirSync(SCREENSHOTS_DIR).filter((f) => f.endsWith(".png"));
  files.forEach((fileName) => {
    fs.copyFileSync(path.join(SCREENSHOTS_DIR, fileName), path.join(screenshotsOut, fileName));
  });
}

function finalizeRun(run, summary) {
  writeSummary(run.summaryFile, summary);
  writeSummary(run.runSummaryFile, summary);

  const accessibilityReport = safeReadJson(run.accessibilityFile, []);
  const html = renderDashboardHtml(summary, accessibilityReport);
  fs.writeFileSync(run.dashboardFile, html, "utf-8");
  fs.writeFileSync(run.runDashboardFile, html, "utf-8");

  copyIfExists(run.accessibilityFile, run.runAccessibilityFile);
  copyIfExists(run.logFile, run.runLogFile);
  copyScreenshotsToRunDir(run.runDir);
}

module.exports = {
  initializeRun,
  clearCurrentRunLog,
  attachConsoleToLog,
  finalizeRun,
  renderDashboardHtml,
  safeReadJson,
};
