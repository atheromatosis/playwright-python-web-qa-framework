# Master Test Plan – Web & WordPress Deployment QA Automation

## 1. Introduction & Objectives
The objective of this test plan is to define the quality assurance strategy and automated verification scope for web and WordPress/WooCommerce deployments prior to production release. All regression and pre-release checks are designed to run against isolated staging environments to prevent post-update regressions, broken lead-generation forms, mobile usability issues, and baseline security misconfigurations[span_3](start_span)[span_3](end_span)[span_4](start_span)[span_4](end_span)[span_5](start_span)[span_5](end_span).

## 2. Test Scope
### In-Scope
* **Post-Update Health & Smoke Checks (`@smoke`, `@regression`):** HTTP status validation, absence of exposed PHP runtime errors (`Fatal error`, `Warning`), JavaScript console error monitoring, and asset integrity after core/plugin updates[span_6](start_span)[span_6](end_span).
* **Lead Generation & GDPR Compliance (`@e2e`):** End-to-End form submission flow, backend REST API payload verification, mandatory GDPR consent enforcement, and input validation[span_7](start_span)[span_7](end_span).
* **Mobile Responsiveness & Touch Usability (`@mobile`):** Viewport rendering without horizontal overflow, mobile hamburger navigation toggle, and thumb-friendly `tel:` URI call-to-action elements (minimum `44x44 px` touch target)[span_8](start_span)[span_8](end_span).
* **Security Hardening Baseline (`@security`):** Presence of defensive HTTP headers (`X-Content-Type-Options`, `X-Frame-Options`), directory listing restrictions (`/wp-content/uploads/`), and XSS payload sanitization[span_9](start_span)[span_9](end_span).

### Out-of-Scope
* Load and stress performance testing under high concurrent traffic.
* Third-party payment gateway sandbox settlement testing.

## 3. Test Design Techniques (ISTQB Standard)
To maximize defect detection efficiency without redundant test cases, the following black-box and experience-based techniques are applied:
1. **Boundary Value Analysis (BVA):** Applied to text input constraints (e.g., contact message field boundaries: `4`, `5`, `2000`, and `2001` characters).
2. **Equivalence Partitioning (EP):** Applied to email validation rules (valid email partition vs. malformed syntax partitions without `@`, domain, or empty strings).
3. **Decision Table Testing:** Applied to GDPR compliance rules (`Valid Data × GDPR Consent Checked/Unchecked -> Expected API/UI Outcome`).
4. **Error Guessing & Negative Testing:** Applied to security sanitization (injecting `<script>` and `onerror` XSS vectors) and broken asset detection.

## 4. Entry & Exit Criteria
### Entry Criteria
* Changes or plugin updates are deployed to an isolated staging environment[span_10](start_span)[span_10](end_span).
* Environment configuration (`BASE_URL`) is accessible by the test runner.

### Exit Criteria
* 100% pass rate on all `@smoke` and `@security` test cases.
* Zero critical or high-severity defects open in lead-generation forms (`@e2e`) or mobile viewports (`@mobile`)[span_11](start_span)[span_11](end_span).
* Automated HTML/Allure test report generated and archived.

## 5. Defect Reporting & Evidence Collection
Every test failure automatically triggers Playwright screenshot capture via `pytest_runtest_makereport` in `tests/conftest.py`, attaching visual evidence directly to the execution report alongside HTTP status codes and browser console logs.
