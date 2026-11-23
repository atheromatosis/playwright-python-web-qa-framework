import pytest
import requests
from config.settings import settings
from pages.home_page import HomePage
from test_data.data_generator import generate_valid_contact_payload


@pytest.mark.security
@pytest.mark.regression
class TestWordPressSecurityBaseline:
    """
    Security hardening checks: HTTP security headers, directory listing restrictions,
    and basic XSS payload sanitization.
    """

    def test_http_security_headers_present(self):
        """Verify essential defensive HTTP headers are returned by the server."""
        response = requests.get(settings.BASE_URL, timeout=10)
        assert response.status_code == 200

        headers = {k.lower(): v for k, v in response.headers.items()}
        assert headers.get("x-content-type-options") == "nosniff", (
            "Missing or invalid 'X-Content-Type-Options: nosniff' header."
        )
        assert "x-frame-options" in headers, (
            "Missing 'X-Frame-Options' clickjacking protection header."
        )

    def test_uploads_directory_listing_is_forbidden(self):
        """Verify public directory indexing under /wp-content/uploads/ is disabled (HTTP 403)."""
        target_url = f"{settings.BASE_URL.rstrip('/')}/wp-content/uploads/"
        response = requests.get(target_url, timeout=10)
        assert response.status_code in (403, 404), (
            f"Security risk: /wp-content/uploads/ returned HTTP {response.status_code} instead of 403/404."
        )

    def test_contact_form_handles_xss_payload_safely(self, home_page: HomePage):
        """
        Negative / Security Testing: Submit an XSS payload in the message field and confirm
        no script execution occurs and the server handles input gracefully without HTTP 500.
        """
        dialog_triggered = False

        def handle_dialog(dialog):
            nonlocal dialog_triggered
            dialog_triggered = True
            dialog.dismiss()

        home_page.page.on("dialog", handle_dialog)
        home_page.open()

        payload = generate_valid_contact_payload()
        xss_vector = "<script>alert('XSS_TEST')</script><img src=x onerror=alert(1)>"

        home_page.fill_contact_form(
            full_name=payload["full_name"],
            email=payload["email"],
            message=xss_vector,
            accept_gdpr=True,
        )

        api_response = home_page.submit_form_and_wait_for_api()
        assert api_response.status != 500, "Server crashed (HTTP 500) on XSS payload input."
        assert not dialog_triggered, "Critical Security Vulnerability: Reflected/DOM XSS executed!"
