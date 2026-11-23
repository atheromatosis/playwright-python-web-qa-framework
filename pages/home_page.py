from playwright.sync_api import Page, Locator, Response
from core.base_page import BasePage


class HomePage(BasePage):
    """Page Object representing the main landing page, mobile navigation, and GDPR contact form."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Navigation & Mobile UX locators
        self.mobile_menu_button: Locator = page.locator("#mobile-menu-btn")
        self.nav_menu: Locator = page.locator("#nav-menu")
        self.phone_cta_link: Locator = page.locator("#header-phone-link")

        # Contact Form & GDPR locators
        self.full_name_input: Locator = page.locator("#full_name")
        self.email_input: Locator = page.locator("#email")
        self.phone_input: Locator = page.locator("#phone")
        self.message_input: Locator = page.locator("#message")
        self.gdpr_checkbox: Locator = page.locator("#gdpr_consent")
        self.submit_button: Locator = page.locator("#submit-btn")
        self.form_feedback_alert: Locator = page.locator("#form-feedback")

    def open(self) -> Response | None:
        """Open the home page."""
        return self.navigate("/")

    def toggle_mobile_menu(self) -> None:
        """Click the mobile hamburger menu button."""
        self.mobile_menu_button.click()

    def fill_contact_form(
        self,
        full_name: str,
        email: str,
        message: str,
        phone: str = "",
        accept_gdpr: bool = True,
    ) -> None:
        """Populate all contact form fields and optionally check the GDPR consent box."""
        self.full_name_input.fill(full_name)
        self.email_input.fill(email)
        if phone:
            self.phone_input.fill(phone)
        self.message_input.fill(message)

        if accept_gdpr and not self.gdpr_checkbox.is_checked():
            self.gdpr_checkbox.check()
        elif not accept_gdpr and self.gdpr_checkbox.is_checked():
            self.gdpr_checkbox.uncheck()

    def submit_form(self) -> None:
        """Click the form submit button."""
        self.submit_button.click()

    def submit_form_and_wait_for_api(self) -> Response:
        """Submit the form and intercept the backend REST API response."""
        with self.page.expect_response("**/wp-json/contact/v1/submit") as response_info:
            self.submit_button.click()
        return response_info.value
