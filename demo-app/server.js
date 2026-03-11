const express = require("express");
const path = require("path");
const fs = require("fs");

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
  const reportHtml = path.join(__dirname, "..", "reports", "report.html");
  if (fs.existsSync(reportHtml)) {
    return res.sendFile(reportHtml);
  }
  return res.status(404).send("No report found yet. Run npm test first.");
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
    .map((run) => `<li><a href="/reports/history/${run}/report.html">Run ${run}</a></li>`)
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
