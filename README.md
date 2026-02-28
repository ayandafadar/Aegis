<<<<<<< HEAD
# Aegis - Accessibility Testing Integration

**Category:** Testing | **Difficulty:** Intermediate

Aegis integrates automated accessibility (a11y) tests into a Selenium-based test suite using **axe-core** — the industry-standard accessibility engine. It ships with a sample frontend web application containing both accessible and inaccessible patterns, making it a complete testing playground.

## Project Structure

```
Aegis/
├── app/                        # Frontend web application
│   ├── index.html              # Home page
│   ├── dashboard.html          # Dashboard page
│   ├── form.html               # Form page
│   ├── css/
│   │   └── styles.css          # Stylesheets
│   └── js/
│       └── app.js              # Frontend JavaScript
├── tests/                      # Test suite
│   ├── conftest.py             # Pytest fixtures (Selenium setup)
│   ├── test_home_a11y.py       # Home page accessibility tests
│   ├── test_dashboard_a11y.py  # Dashboard page accessibility tests
│   ├── test_form_a11y.py       # Form page accessibility tests
│   └── test_navigation_a11y.py # Navigation & keyboard tests
├── reports/                    # Generated test reports (gitignored)
├── utils/
│   ├── axe_helper.py           # axe-core integration helper
│   └── report_generator.py     # HTML report generator
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── serve.py                    # Local dev server
└── README.md                   # This file
```

## Features

- **axe-core Integration** — Runs axe-core accessibility engine via Selenium
- **WCAG 2.1 Compliance** — Tests against WCAG 2.0 A, AA, and 2.1 AA standards
- **Multiple Page Testing** — Tests home, dashboard, and form pages
- **Keyboard Navigation** — Verifies tab order and focus management
- **ARIA Validation** — Checks ARIA attributes and roles
- **Color Contrast** — Validates color contrast ratios
- **HTML Reports** — Generates detailed HTML accessibility reports
- **CI-Ready** — Pytest-based suite ready for CI/CD pipelines

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the sample web app
python serve.py &

# Run all accessibility tests
pytest tests/ -v --tb=short

# Run with HTML report
pytest tests/ -v --html=reports/a11y_report.html
```

## Test Categories

| Test File | What It Checks |
|---|---|
| `test_home_a11y.py` | Page structure, landmarks, headings, images, links |
| `test_dashboard_a11y.py` | Data tables, charts, dynamic content, ARIA live regions |
| `test_form_a11y.py` | Form labels, error messages, required fields, fieldsets |
| `test_navigation_a11y.py` | Keyboard nav, focus order, skip links, focus trapping |

## WCAG Standards Tested

- **WCAG 2.0 Level A** — Minimum accessibility
- **WCAG 2.0 Level AA** — Standard compliance target
- **WCAG 2.1 Level AA** — Current recommended standard
- **Section 508** — US federal accessibility standard

## CI/CD Integration

The project includes a GitHub Actions workflow that runs automatically on:
- Every push to `main` or `master`
- Every pull request to `main` or `master`
- Manual trigger via workflow_dispatch

### GitHub Actions Workflow

```yaml
# .github/workflows/a11y-tests.yml
- Checkout code
- Setup Python 3.11
- Install dependencies
- Install Chrome browser
- Start web server in background
- Run pytest accessibility tests
- Upload HTML report as artifact
- Comment on PR if tests fail
```

### Add Status Badge

Add this to your README after pushing to GitHub:
```markdown
![Accessibility Tests](https://github.com/YOUR_USERNAME/Aegis/actions/workflows/a11y-tests.yml/badge.svg)
```

## Complete Project Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DEVELOPMENT WORKFLOW                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. DEVELOP                    2. TEST LOCALLY                              │
│  ┌─────────────────┐           ┌─────────────────────────────────────────┐  │
│  │ Edit HTML/CSS   │           │ python serve.py                        │  │
│  │ in app/ folder  │ ────────► │ python -m pytest tests/ -v             │  │
│  └─────────────────┘           └─────────────────────────────────────────┘  │
│                                              │                              │
│                                              ▼                              │
│                                ┌─────────────────────────────────────────┐  │
│                                │ axe-core scans page via Selenium        │  │
│                                │ Returns WCAG violations by severity     │  │
│                                └─────────────────────────────────────────┘  │
│                                              │                              │
│  3. COMMIT & PUSH                            ▼                              │
│  ┌─────────────────┐           ┌─────────────────────────────────────────┐  │
│  │ git add .       │           │ 48 tests pass, 4 fail (intentional)     │  │
│  │ git commit      │           │ Report: reports/report.html             │  │
│  │ git push        │           └─────────────────────────────────────────┘  │
│  └─────────────────┘                                                        │
│          │                                                                  │
│          ▼                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     GITHUB ACTIONS (CI)                             │    │
│  ├─────────────────────────────────────────────────────────────────────┤    │
│  │  • Triggered on push/PR to main                                     │    │
│  │  • Spins up Ubuntu runner with Python + Chrome                      │    │
│  │  • Installs dependencies from requirements.txt                      │    │
│  │  • Starts serve.py in background                                    │    │
│  │  • Runs full pytest suite headlessly                                │    │
│  │  • Uploads HTML report as downloadable artifact                     │    │
│  │  • Comments on PR if tests fail                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                              │                              │
│                                              ▼                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  ✓ All tests pass → PR can be merged                                │    │
│  │  ✗ Tests fail → Fix accessibility issues before merging             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## How axe-core Integration Works

1. **Selenium navigates to page** → Opens Chrome/Edge headlessly
2. **axe_helper.py injects axe-core** → Downloads axe.min.js from CDN, caches locally
3. **axe.run() executes in browser** → Scans DOM for WCAG violations
4. **Results returned to Python** → JSON with violations, passes, incomplete
5. **pytest assertions check results** → Fail if critical violations found

## License

MIT
=======
# Aegis

**Aegis** is an integrated DevOps system that combines **accessibility testing in CI/CD pipelines** with **alert correlation** to reduce alert fatigue and improve user-focused application reliability.

---

## 📌 Project Overview

In many DevOps teams, testing and monitoring happen in isolation. Accessibility checks run during CI/CD, and monitoring tools raise alerts in production, but these signals are rarely connected. As a result, teams receive many alerts without clear insight into how real users are affected, which can delay response to important issues.

Aegis connects these two stages by linking accessibility test results with monitoring alerts, helping teams focus on alerts that actually matter and respond faster to problems that impact users.

---

## 🎯 Objectives

- Integrate accessibility testing into the CI/CD pipeline  
- Correlate accessibility issues with monitoring alerts  
- Reduce alert noise using correlation techniques  
- Improve overall software quality and user experience  
- Demonstrate core DevOps automation principles  

---

## 🧩 System Components

### 1. Accessibility Testing Module
- Runs automated accessibility tests during CI/CD
- Uses tools such as Lighthouse or axe-core
- Generates structured test reports (pass/fail, severity)
- Stores results in JSON format

### 2. Alert Correlation Engine
- Ingests alerts from monitoring tools or mocked data
- Groups related alerts
- Suppresses duplicate alerts
- Assigns priority based on correlation rules

### 3. Integration Layer
- Links accessibility test results with monitoring alerts
- Applies rule-based logic
- Generates a single meaningful alert

---

## 🔁 Workflow

1. Developer pushes code to the repository  
2. CI/CD pipeline is triggered  
3. Accessibility tests are executed  
4. Test results are stored  
5. Application is deployed  
6. Monitoring alerts are generated  
7. Alert correlation engine analyzes alerts and test results  
8. A prioritized alert is sent to the DevOps team  

---

## ⚙️ Tech Stack

- **CI/CD:** GitHub Actions / Jenkins  
- **Accessibility Testing:** Lighthouse
- **Monitoring:** Prometheus
- **Backend:** Node.js  
- **Alerting:** Console / Slack / Email  
- **Storage:** JSON

---

## ⚡ DevOps Concepts Used

- Continuous Integration (CI)  
- Continuous Testing  
- Monitoring and Alerting  
- Alert Correlation  
- Automation  
- Feedback Loops  

---

## Team Members

- **Ayan Dafadar**  
	- Accessibility testing integration  
	- CI/CD pipeline configuration  
	- Accessibility severity classification  

- **Rishab Aggarwal**  
	- Alert ingestion  
	- Alert correlation logic  
	- Alert prioritization  

---

## Example Scenario

- Accessibility test fails for keyboard navigation on login
- Monitoring tool reports high latency for authentication service

**Aegis Output:**
> Login service issue detected with accessibility impact – High Priority

---

## Future Enhancements

- Alert visualization dashboard  
- Support for multiple monitoring tools  
- Advanced alert scoring  
- Historical alert analysis  

---

## Conclusion

Aegis demonstrates how accessibility testing and monitoring can be integrated in a DevOps pipeline to provide meaningful alerts, reduce noise, and improve user-focused reliability.

---

This project is developed for academic purposes as part of a DevOps course.
>>>>>>> e3a162bceb62a158f3e0fad3f6087d71a0d1f8e0
