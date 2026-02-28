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
