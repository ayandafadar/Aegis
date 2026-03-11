const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, "public")));
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
