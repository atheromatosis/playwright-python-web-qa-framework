from playwright.sync_api import Page, Locator, Response
from config.settings import settings


class BasePage:
    """Base class for all Page Objects providing common Playwright wrappers and error listeners."""

    def __init__(self, page: Page):
        self.page = page
        self.base_url = settings.BASE_URL
        self.console_errors: list[str] = []
        self.page_errors: list[str] = []

        self.page.on("pageerror", lambda err: self.page_errors.append(str(err)))
        self.page.on(
            "console",
            lambda msg: self.console_errors.append(msg.text) if msg.type == "error" else None,
        )

    def navigate(self, path: str = "/") -> Response | None:
        """Navigate to a relative path and wait until network is idle."""
        target_url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        return self.page.goto(target_url, wait_until="networkidle")

    def get_title(self) -> str:
        """Return the current document title."""
        return self.page.title()

    def get_page_source(self) -> str:
        """Return full rendered HTML content."""
        return self.page.content()

    def is_visible(self, locator: Locator) -> bool:
        """Safely check if an element is visible on the viewport."""
        return locator.is_visible()

    def has_horizontal_overflow(self) -> bool:
        """Verify whether the page content overflows the viewport width (RWD check)."""
        return self.page.evaluate(
            "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )
