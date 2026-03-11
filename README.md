# Aegis

**Automated Accessibility Testing with Selenium + axe-core**

Aegis is an automated accessibility testing framework that integrates **axe-core**, the industry-standard accessibility engine, into a **Selenium-based testing workflow using Node.js**.

The project includes a **demo web application with intentional accessibility issues**, allowing developers to test, detect, and understand accessibility violations in a controlled environment.

Aegis helps teams integrate **WCAG accessibility validation directly into automated testing and CI/CD pipelines**.

---

# Why Aegis?

Accessibility testing is often:

- Manual  
- Time-consuming  
- Inconsistent  
- Ignored in CI pipelines  

Aegis solves this by:

- Embedding accessibility validation directly into automated tests
- Detecting **WCAG violations automatically**
- Generating structured accessibility reports
- Running accessibility checks in **CI/CD pipelines**
- Catching accessibility regressions before deployment

---

# Project Structure

```
Aegis/
│
├── demo-app/
│   ├── public/
│   │   ├── index.html
│   │   ├── login.html
│   │   └── contact.html
│   └── server.js
│
├── tests/
│   ├── homepage.test.js
│   ├── login.test.js
│   └── contact.test.js
│
├── utils/
│
├── reports/
│   ├── history/
│   │   └── timestamped test runs
│   ├── report.html
│   ├── accessibility-report.json
│   ├── run-summary.json
│   └── test-run.log
│
├── screenshots/
│
├── .github/workflows/
│   ├── ci.yml
│   └── deploy-pages.yml
│
├── runner.js
├── Dockerfile
├── docker-compose.yml
├── package.json
├── package-lock.json
└── README.md
```


# Quick Start

## 1 Install dependencies

```bash
npm install
```

---

## 2 Start the demo application

```bash
node demo-app/server.js
```

The demo site will run locally.

---

## 3 Run accessibility tests

```bash
node runner.js
```

This will:

- Run Selenium tests
- Execute axe-core accessibility scans
- Capture screenshots
- Generate accessibility reports

---

## 4 View the report

Open the generated report:

```
reports/report.html
```

Historical reports are available in:

```
reports/history/
```

---

# Example Accessibility Violations Detected

Aegis can detect issues such as:

- Missing image alt text
- Low color contrast
- Missing form labels
- Improper ARIA roles
- Invalid heading structure
- Missing landmarks
- Keyboard navigation issues

---

# Development Workflow

```
Developer edits frontend code
        │
        ▼
Run accessibility tests locally
        │
        ▼
Selenium loads web pages
        │
        ▼
axe-core scans the DOM
        │
        ▼
Accessibility violations detected
        │
        ▼
Reports generated automatically
        │
        ▼
CI pipeline runs tests on push/PR
        │
        ▼
Accessibility regressions prevented
```

---

# Tech Stack

Runtime

- Node.js

Testing

- Selenium WebDriver
- axe-core

Automation

- JavaScript (Node.js)

Reporting

- HTML reports
- JSON reports
- Screenshots

Infrastructure

- Docker
- GitHub Actions

---
