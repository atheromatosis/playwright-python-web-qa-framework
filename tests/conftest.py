import socket
import threading
import time
from typing import Generator

import allure
import pytest
import uvicorn
from playwright.sync_api import Page

from config.settings import settings
from demo_site.app import app
from pages.home_page import HomePage


def _is_port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


@pytest.fixture(scope="session", autouse=True)
def start_local_mock_server() -> Generator[None, None, None]:
    """
    Automatically start the local FastAPI WordPress staging mock server
    for the test session when running against localhost.
    """
    if "127.0.0.1" not in settings.BASE_URL and "localhost" not in settings.BASE_URL:
        yield
        return

    if _is_port_in_use("127.0.0.1", 8000):
        yield
        return

    config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="error")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait until the local server is ready to accept connections
    timeout = time.time() + 10
    while not _is_port_in_use("127.0.0.1", 8000):
        if time.time() > timeout:
            raise RuntimeError("Local mock server failed to start within 10 seconds.")
        time.sleep(0.1)

    yield

    server.should_exit = True
    thread.join(timeout=5)


@pytest.fixture(scope="function")
def home_page(page: Page) -> HomePage:
    """Provide an initialized HomePage instance with configured default timeout."""
    page.set_default_timeout(settings.TIMEOUT)
    return HomePage(page)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a full-page screenshot on test failure and attach it to Allure reports."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")
        if page:
            screenshot_bytes = page.screenshot(full_page=True)
            allure.attach(
                screenshot_bytes,
                name=f"failure_screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )

import socket
import threading
import time
from typing import Generator

import allure
import pytest
import uvicorn
from playwright.sync_api import Page, Playwright

from config.settings import settings
from demo_site.app import app
from pages.home_page import HomePage


def _is_port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


@pytest.fixture(scope="session", autouse=True)
def start_local_mock_server() -> Generator[None, None, None]:
    """
    Automatically start the local FastAPI WordPress staging mock server
    for the test session when running against localhost.
    """
    if "127.0.0.1" not in settings.BASE_URL and "localhost" not in settings.BASE_URL:
        yield
        return

    if _is_port_in_use("127.0.0.1", 8000):
        yield
        return

    config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="error")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    timeout = time.time() + 10
    while not _is_port_in_use("127.0.0.1", 8000):
        if time.time() > timeout:
            raise RuntimeError("Local mock server failed to start within 10 seconds.")
        time.sleep(0.1)

    yield

    server.should_exit = True
    thread.join(timeout=5)


@pytest.fixture(scope="function")
def home_page(page: Page) -> HomePage:
    """Provide an initialized HomePage instance with configured default timeout."""
    page.set_default_timeout(settings.TIMEOUT)
    return HomePage(page)


@pytest.fixture(scope="function")
def mobile_page_factory(playwright: Playwright, browser):
    """Factory fixture creating isolated mobile browser contexts for RWD & touch usability tests."""
    contexts = []

    def _create_mobile_page(device_name: str) -> HomePage:
        device_config = playwright.devices[device_name]
        context = browser.new_context(**device_config)
        contexts.append(context)
        page = context.new_page()
        page.set_default_timeout(settings.TIMEOUT)
        return HomePage(page)

    yield _create_mobile_page

    for ctx in contexts:
        ctx.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a full-page screenshot on test failure and attach it to Allure reports."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")
        if page:
            screenshot_bytes = page.screenshot(full_page=True)
            allure.attach(
                screenshot_bytes,
                name=f"failure_screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )
