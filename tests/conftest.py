"""
Aegis - Pytest Configuration & Fixtures
Sets up Selenium WebDriver and local server for accessibility tests.
"""

import pytest
import sys
import os
import socket
import shutil

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from serve import start_server_background

BASE_URL = "http://localhost:8888"


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def get_available_browser():
    """Detect which browser is available (Chrome for CI, Edge for Windows)."""
    # Check for Chrome first (CI environments)
    if shutil.which("google-chrome") or shutil.which("chrome") or shutil.which("chromium"):
        return "chrome"
    # Check for Chrome on Windows
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for p in chrome_paths:
        if os.path.exists(p):
            return "chrome"
    # Fall back to Edge (Windows default)
    return "edge"


@pytest.fixture(scope="session")
def server():
    """Start the local dev server for the test session."""
    import time
    import urllib.request

    if not is_port_in_use(8888):
        thread = start_server_background(8888)
        # Wait until server is actually responding (up to 5 seconds)
        for _ in range(10):
            try:
                urllib.request.urlopen(f"{BASE_URL}/index.html", timeout=1)
                break
            except Exception:
                time.sleep(0.5)
    yield BASE_URL


@pytest.fixture(scope="session")
def driver(server):
    """Create a Selenium WebDriver instance for the test session."""
    browser = get_available_browser()
    
    if browser == "chrome":
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")
        options.add_argument("--disable-gpu")
        drv = webdriver.Chrome(options=options)
    else:
        from selenium.webdriver.edge.options import Options
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")
        options.add_argument("--disable-gpu")
        drv = webdriver.Edge(options=options)
    
    drv.set_script_timeout(30)
    drv.implicitly_wait(5)

    yield drv

    drv.quit()


@pytest.fixture
def home_page(driver, server):
    """Navigate to the home page."""
    driver.get(f"{server}/index.html")
    return driver


@pytest.fixture
def dashboard_page(driver, server):
    """Navigate to the dashboard page."""
    driver.get(f"{server}/dashboard.html")
    return driver


@pytest.fixture
def form_page(driver, server):
    """Navigate to the form page."""
    driver.get(f"{server}/form.html")
    return driver
