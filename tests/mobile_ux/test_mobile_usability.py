import pytest
from playwright.sync_api import expect


@pytest.mark.mobile
@pytest.mark.regression
class TestMobileUsabilityAndRWD:
    """
    Mobile responsiveness and thumb-friendly UX verification across mobile viewports.
    """

    @pytest.mark.parametrize("device_name", ["iPhone 14", "Pixel 7"])
    def test_mobile_layout_and_navigation_menu(self, mobile_page_factory, device_name: str):
        """Verify mobile viewport has no horizontal overflow and hamburger menu toggles properly."""
        mobile_home = mobile_page_factory(device_name)
        mobile_home.open()

        assert not mobile_home.has_horizontal_overflow(), (
            f"Horizontal layout overflow detected on {device_name}."
        )

        expect(mobile_home.mobile_menu_button).to_be_visible()
        expect(mobile_home.nav_menu).to_be_hidden()

        mobile_home.toggle_mobile_menu()
        expect(mobile_home.nav_menu).to_be_visible()

    def test_phone_cta_link_is_clickable_and_thumb_friendly(self, mobile_page_factory):
        """
        Verify the phone CTA uses a valid 'tel:' URI scheme and meets minimum
        touch target dimensions (44x44 px) for mobile users.
        """
        mobile_home = mobile_page_factory("iPhone 14")
        mobile_home.open()

        phone_link = mobile_home.phone_cta_link
        expect(phone_link).to_be_visible()

        href = phone_link.get_attribute("href")
        assert href is not None and href.startswith("tel:"), (
            f"Expected clickable 'tel:' link, got '{href}'."
        )

        bounding_box = phone_link.bounding_box()
        assert bounding_box is not None, "Phone link bounding box could not be determined."
        assert bounding_box["width"] >= 44 and bounding_box["height"] >= 44, (
            f"Touch target too small ({bounding_box['width']}x{bounding_box['height']}px). "
            "Minimum 44x44px required for mobile accessibility."
        )
