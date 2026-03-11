const express = require("express");
const path = require("path");
const fs = require("fs");
const { renderDashboardHtml, safeReadJson } = require("../utils/reportManager");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, "public")));
app.use("/reports", express.static(path.join(__dirname, "..", "reports")));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get("/", (_req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.get("/login", (_req, res) => {
  res.sendFile(path.join(__dirname, "public", "login.html"));
});

app.get("/contact", (_req, res) => {
  res.sendFile(path.join(__dirname, "public", "contact.html"));
});

app.get("/report", (_req, res) => {
  const reportsDir = path.join(__dirname, "..", "reports");
  const summaryFile = path.join(reportsDir, "run-summary.json");
  const a11yFile = path.join(reportsDir, "accessibility-report.json");

  if (!fs.existsSync(summaryFile)) {
    return res.status(404).send("No report found yet. Run npm test first.");
  }

  const summary = safeReadJson(summaryFile, null);
  if (!summary) {
    return res.status(500).send("Report summary is invalid.");
  }

  const a11yData = safeReadJson(a11yFile, []);
  const html = renderDashboardHtml(summary, a11yData);
  return res.send(html);
});

app.get("/report-history", (_req, res) => {
  const historyDir = path.join(__dirname, "..", "reports", "history");
  if (!fs.existsSync(historyDir)) {
    return res.send("No report history found yet. Run npm test first.");
  }

  const runs = fs
    .readdirSync(historyDir)
    .filter((entry) => fs.statSync(path.join(historyDir, entry)).isDirectory())
    .sort()
    .reverse();

  const links = runs
    .map((run) => `<li><a href="/report-history/${run}">Run ${run}</a></li>`)
    .join("");

  return res.send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Report History</title>
  <style>
    body { font-family: Segoe UI, Arial, sans-serif; padding: 24px; }
    li { margin: 8px 0; }
  </style>
</head>
<body>
  <h1>Report History</h1>
  <p><a href="/report">Latest report</a></p>
  <ul>${links}</ul>
</body>
</html>`);
});

app.get("/report-history/:runId", (req, res) => {
  const { runId } = req.params;
  const runDir = path.join(__dirname, "..", "reports", "history", runId);

  if (!fs.existsSync(runDir) || !fs.statSync(runDir).isDirectory()) {
    return res.status(404).send("Run not found.");
  }

  const summaryFile = path.join(runDir, "run-summary.json");
  const a11yFile = path.join(runDir, "accessibility-report.json");

  if (!fs.existsSync(summaryFile)) {
    return res.status(404).send("Run summary not found.");
  }

  const summary = safeReadJson(summaryFile, null);
  if (!summary) {
    return res.status(500).send("Run summary is invalid.");
  }

  const a11yData = safeReadJson(a11yFile, []);
  return res.send(renderDashboardHtml(summary, a11yData));
});

app.post("/login", (_req, res) => {
  res.json({ success: true, message: "Login successful" });
});

app.post("/contact", (_req, res) => {
  res.json({ success: true, message: "Message sent" });
});

const server = app.listen(PORT, () => {
  console.log(`Demo app running at http://localhost:${PORT}`);
});

module.exports = server;
