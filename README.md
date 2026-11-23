# Playwright Python Web QA Automation Framework

[![QA Automation Regression Suite](https://github.com/atheromatosis/playwright-python-web-qa-framework/actions/workflows/qa_pipeline.yml/badge.svg)](https://github.com/atheromatosis/playwright-python-web-qa-framework/actions/workflows/qa_pipeline.yml)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33?logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Framework-0A9EDC?logo=pytest&logoColor=white)
![ISTQB](https://img.shields.io/badge/QA_Methodology-ISTQB_Foundation-orange)

An End-to-End, Regression, Mobile UX, and Security QA Automation Framework built with **Python**, **Playwright**, and **Pytest** using the **Page Object Model (POM)** design pattern.

Designed to automate pre-release and post-update quality checks on staging environments (WordPress / custom web deployments), validating lead-generation forms, GDPR compliance, mobile responsiveness, and baseline security hardening.

> **Note on Confidentiality (NDA):** To ensure full compliance with client confidentiality agreements, this public repository includes a self-contained **FastAPI Staging Mock Environment** (`demo_site/`). The framework can be pointed at any live staging URL via a single `.env` configuration variable (`BASE_URL`).

---

## Key Features & QA Methodology

* **Page Object Model (POM) Architecture:** Clean separation between page locators/actions (`pages/`), core browser utilities (`core/base_page.py`), and test assertions (`tests/`).
* **ISTQB Test Design Techniques:**
  * **Boundary Value Analysis (BVA):** Validates minimum and maximum input constraints (`4`, `5`, `2000`, `2001` chars).
  * **Equivalence Partitioning (EP):** Parameterized validation across valid and malformed email partitions.
  * **Decision Table Testing:** Enforces mandatory GDPR consent rules before form submission.
  * **Negative & Security Testing:** Tests XSS payload sanitization, defensive HTTP headers, and `/wp-content/uploads/` directory listing restrictions.
* **Network Interception:** Uses Playwright's `expect_response` to verify that form submissions actually reach the backend REST API (`/wp-json/contact/v1/submit`) and return `HTTP 200` rather than relying solely on UI notifications.
* **Mobile UX & Touch Target Audits:** Emulates mobile devices (`iPhone 14`, `Pixel 7`) to detect horizontal layout overflow, test hamburger navigation, and verify thumb-friendly `tel:` CTA dimensions (`>= 44x44 px`).
* **Automated Evidence Collection & CI/CD:** Captures full-page failure screenshots automatically and runs on every push via **GitHub Actions**, publishing self-contained HTML reports.

---

## Project Structure

```text
playwright-python-web-qa-framework/
├── .github/workflows/
│   └── qa_pipeline.yml              # GitHub Actions CI workflow
├── config/
│   └── settings.py                  # Pydantic environment configuration
├── core/
│   └── base_page.py                 # BasePage wrapper & JS console error listeners
├── demo_site/
│   ├── app.py                       # Self-contained FastAPI staging mock server
│   └── templates/index.html         # Mock WordPress landing page with GDPR form
├── docs/
│   ├── test_plan.md                 # Master Test Plan (ISTQB / ISO 29119)
│   └── traceability_matrix.md       # Requirements Traceability Matrix (RTM)
├── pages/
│   └── home_page.py                 # HomePage Page Object (Mobile Nav, Phone CTA, Form)
├── test_data/
│   └── data_generator.py            # Dynamic test data generation via Faker
├── tests/
│   ├── conftest.py                  # Pytest fixtures, auto-server startup & screenshot hooks
│   ├── smoke_regression/            # Post-update PHP/JS/asset health checks
│   ├── e2e/                         # Contact form & GDPR compliance tests
│   ├── mobile_ux/                   # Mobile RWD & touch usability tests
│   └── security/                    # HTTP headers, uploads & XSS sanitization checks
├── pytest.ini                       # Pytest markers & execution settings
└── requirements.txt                 # Project dependencies
```

---

## Getting Started

### 1. Clone the repository & set up virtual environment
```bash
git clone https://github.com/atheromatosis/playwright-python-web-qa-framework.git
cd playwright-python-web-qa-framework

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install dependencies & Playwright browsers
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Execute tests
The local FastAPI staging mock server starts automatically during the test session.

```bash
# Run the complete test suite
pytest

# Run specific test suites using markers
pytest -m smoke
pytest -m e2e
pytest -m mobile
pytest -m security

# Generate a standalone HTML report
pytest --html=report.html --self-contained-html
```

### Running Against an External Staging Environment
Create a `.env` file in the project root and override `BASE_URL`:
```env
BASE_URL=https://staging.example.com
HEADLESS=true
```

---

## Documentation
* [Master Test Plan](docs/test_plan.md) – Scope, ISTQB techniques, and Entry/Exit criteria.
* [Requirements Traceability Matrix](docs/traceability_matrix.md) – Mapping between quality requirements and automated test cases.
