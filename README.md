# Aegis  
Automated Accessibility Testing with Selenium + axe-core

Aegis integrates automated accessibility (a11y) testing directly into a Selenium-powered test suite using axe-core, the industry-standard accessibility engine.

It includes a sample frontend web application intentionally containing both accessible and inaccessible patterns, making it a complete accessibility testing playground.

![Accessibility Tests](https://github.com/ayandafadar/Aegis/actions/workflows/a11y-tests.yml/badge.svg)
---

## Why Aegis?

Accessibility testing is often:

- Manual  
- Time-consuming  
- Inconsistent  
- Ignored in CI pipelines  

Aegis solves this by:

- Embedding WCAG validation into automated tests  
- Generating structured HTML reports  
- Running in CI/CD automatically  
- Catching accessibility regressions before merge  

---

## Project Structure

```
Aegis/
├── app/
│   ├── index.html
│   ├── dashboard.html
│   ├── form.html
│   ├── css/styles.css
│   └── js/app.js
├── tests/
│   ├── conftest.py
│   ├── test_home_a11y.py
│   ├── test_dashboard_a11y.py
│   ├── test_form_a11y.py
│   └── test_navigation_a11y.py
├── utils/
│   ├── axe_helper.py
│   └── report_generator.py
├── reports/
├── requirements.txt
├── pytest.ini
├── serve.py
└── README.md
```

---

## Features

### axe-core Integration
Injects axe-core directly into Selenium browser sessions.

### WCAG 2.1 Validation
Tests against:
- WCAG 2.0 Level A  
- WCAG 2.0 Level AA  
- WCAG 2.1 Level AA  
- Section 508  

### Keyboard Navigation Testing
- Tab order  
- Focus visibility  
- Skip links  
- Focus trapping  

### Color Contrast Checking
Automated validation of contrast ratios.

### ARIA Role & Landmark Validation
Ensures semantic structure and ARIA compliance.

### HTML Report Generation
Detailed accessibility reports with violation severity breakdown.

### CI/CD Ready
Runs automatically in GitHub Actions.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the sample app

```bash
python serve.py
```

### 3. Run accessibility tests

```bash
pytest tests/ -v --tb=short
```

### 4. Generate HTML report

```bash
pytest tests/ -v --html=reports/a11y_report.html
```

---

## Test Coverage Overview

| Test File | What It Validates |
|------------|------------------|
| test_home_a11y.py | Landmarks, headings, links, images |
| test_dashboard_a11y.py | Tables, charts, dynamic content |
| test_form_a11y.py | Labels, validation errors, required fields |
| test_navigation_a11y.py | Keyboard flow, focus management |

---

## Development Workflow

1. Modify frontend files inside `app/`
2. Run local tests using pytest
3. Fix any reported accessibility violations
4. Commit and push changes
5. CI runs automatically
6. Merge only if tests pass

---

## CI/CD Integration

Aegis includes a GitHub Actions workflow that:

- Triggers on push or pull request to `main`
- Installs Python 3.11
- Installs Chrome browser
- Starts local development server
- Runs headless Selenium tests
- Uploads HTML report as artifact
- Fails pull request if accessibility tests fail

## How axe-core Integration Works

1. Selenium launches the browser (headless mode).
2. `axe_helper.py` injects axe.min.js into the page.
3. `axe.run()` scans the DOM.
4. Violations are returned as JSON.
5. Pytest asserts based on severity.
6. HTML report is generated.

---

## Tech Stack

- Python 3.11+
- Selenium
- axe-core
- Pytest
- GitHub Actions

---

## Who Is This For?

- QA Engineers  
- Frontend Developers  
- DevOps Engineers  
- Accessibility Advocates  
- Teams implementing shift-left accessibility testing  

---

## Future Enhancements

- Lighthouse integration  
- Slack/Discord failure notifications  
- Accessibility score dashboard  
