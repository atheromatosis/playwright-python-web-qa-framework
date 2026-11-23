import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage
from test_data.data_generator import generate_valid_contact_payload


@pytest.mark.e2e
@pytest.mark.regression
class TestContactFormAndGDPR:
    """
    End-to-End tests for lead generation forms and GDPR compliance.
    Applies ISTQB techniques: Decision Table Testing, Equivalence Partitioning, and Boundary Value Analysis.
    """

    def test_successful_form_submission_with_gdpr_consent(self, home_page: HomePage):
        """
        Verify complete E2E form submission: UI feedback + intercepted HTTP 200 REST API response.
        """
        home_page.open()
        payload = generate_valid_contact_payload()

        home_page.fill_contact_form(
            full_name=payload["full_name"],
            email=payload["email"],
            phone=payload["phone"],
            message=payload["message"],
            accept_gdpr=True,
        )

        api_response = home_page.submit_form_and_wait_for_api()
        assert api_response.status == 200, f"Expected API 200 OK, got {api_response.status}"

        response_json = api_response.json()
        assert response_json.get("status") == "mail_sent"

        expect(home_page.form_feedback_alert).to_be_visible()
        expect(home_page.form_feedback_alert).to_contain_text("Thank you for your message")

    def test_submission_blocked_without_gdpr_consent(self, home_page: HomePage):
        """
        Decision Table Rule: Valid user data + Missing GDPR consent -> Submission blocked on client side.
        """
        home_page.open()
        payload = generate_valid_contact_payload()

        home_page.fill_contact_form(
            full_name=payload["full_name"],
            email=payload["email"],
            message=payload["message"],
            accept_gdpr=False,
        )
        home_page.submit_form()

        expect(home_page.form_feedback_alert).to_be_visible()
        expect(home_page.form_feedback_alert).to_contain_text("GDPR consent")

    @pytest.mark.parametrize(
        "invalid_email",
        [
            "plainaddress",
            "@missingusername.com",
            "username@.com",
            "username@domain..com",
            "",
        ],
    )
    def test_invalid_email_equivalence_partitions(self, home_page: HomePage, invalid_email: str):
        """
        Equivalence Partitioning (EP): Verify backend rejects malformed email partitions with HTTP 422.
        """
        home_page.open()
        payload = generate_valid_contact_payload()

        home_page.fill_contact_form(
            full_name=payload["full_name"],
            email=invalid_email,
            message=payload["message"],
            accept_gdpr=True,
        )

        api_response = home_page.submit_form_and_wait_for_api()
        assert api_response.status == 422, (
            f"Expected HTTP 422 Unprocessable Entity for invalid email '{invalid_email}', got {api_response.status}"
        )

    @pytest.mark.parametrize(
        "message_length, expected_status",
        [
            (4, 422),     # Lower boundary - 1 (Invalid)
            (5, 200),     # Lower boundary (Valid minimum)
            (2000, 200),  # Upper boundary (Valid maximum)
            (2001, 422),  # Upper boundary + 1 (Invalid)
        ],
    )
    def test_message_length_boundary_values(
        self, home_page: HomePage, message_length: int, expected_status: int
    ):
        """
        Boundary Value Analysis (BVA): Verify message field boundaries (min=5, max=2000 characters).
        """
        home_page.open()
        payload = generate_valid_contact_payload()
        boundary_message = "A" * message_length

        home_page.fill_contact_form(
            full_name=payload["full_name"],
            email=payload["email"],
            message=boundary_message,
            accept_gdpr=True,
        )

        api_response = home_page.submit_form_and_wait_for_api()
        assert api_response.status == expected_status, (
            f"Boundary test failed for length={message_length}: expected {expected_status}, got {api_response.status}"
        )
