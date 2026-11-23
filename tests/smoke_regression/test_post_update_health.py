import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.regression
class TestPostUpdateHealth:
    """
    Post-deployment & post-plugin-update health checks executed on staging
    before promoting changes to production.
    """

    PHP_ERROR_SIGNATURES = [
        "Fatal error:",
        "Parse error:",
        "Warning:",
        "Notice:",
        "Uncaught Error:",
        "There has been a critical error on this website",
    ]

    def test_page_loads_with_200_and_no_php_errors(self, home_page: HomePage):
        """Verify HTTP 200 status and absence of exposed PHP/WordPress runtime errors in DOM."""
        response = home_page.open()
        assert response is not None, "Expected a valid HTTP response from the server."
        assert response.status == 200, f"Expected HTTP 200 OK, got {response.status}."

        html_content = home_page.get_page_source()
        for signature in self.PHP_ERROR_SIGNATURES:
            assert signature not in html_content, (
                f"Detected exposed PHP/WordPress error signature in page source: '{signature}'"
            )

    def test_no_uncaught_javascript_or_console_errors(self, home_page: HomePage):
        """Verify no uncaught JS exceptions or console errors occur after plugin updates."""
        home_page.open()
        assert len(home_page.page_errors) == 0, (
            f"Uncaught page errors detected: {home_page.page_errors}"
        )
        assert len(home_page.console_errors) == 0, (
            f"Browser console errors detected: {home_page.console_errors}"
        )

    def test_all_images_and_critical_sections_render_properly(self, home_page: HomePage):
        """Verify critical page sections are visible and no broken images exist."""
        home_page.open()
        expect(home_page.phone_cta_link).to_be_visible()
        expect(home_page.submit_button).to_be_visible()

        broken_images = home_page.page.evaluate(
            """() => {
                const imgs = Array.from(document.querySelectorAll('img'));
                return imgs.filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src);
            }"""
        )
        assert len(broken_images) == 0, f"Found broken images on page: {broken_images}"
