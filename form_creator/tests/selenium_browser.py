"""Helper functions related to testing using selenium."""

import typing as _t
from base64 import b64encode
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from django.test import Client
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def selenium_browser(
    headless: bool = settings.SELENIUM_HEADLESS_MODE,
) -> webdriver.Chrome:
    """Helper function to create a selenium web browser.
    :param headless: Whether or not the browser should run on headless mode.
    :type headless: bool
    """

    try:
        browser = webdriver.Chrome(settings.CHROMEDRIVER_PATH)
    except WebDriverException as e:
        print(e)
        opt = webdriver.ChromeOptions()
        opt.add_argument("--disable-extensions")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--no-sandbox")
        opt.add_experimental_option("prefs", {"dark_mode": True})
        opt.add_argument("--force-dark-mode")
        if not headless:
            opt.add_argument("--headless")
        opt.add_argument("--disable-web-security")
        opt.add_argument("--allow-running-insecure-content")

        browser = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=opt,
        )

    browser.set_window_size(1920, 1080)
    return browser


def browser_from_response(response: _t.Union[bytes, str]) -> webdriver:
    """Given some arbitrary response, create a selenium browser from it."""
    response_encoded = b64encode(response.encode("utf-8")).decode()
    driver = selenium_browser()
    driver.get(f"data:text/html;base64,{response_encoded}")
    return driver


def browser_login(browser: webdriver, user: User) -> None:
    """Logins a into the browser. This is done by using a Django client's login
    feature and copying the session ID cookie over to the browser.
    """
    client = Client()
    client.force_login(user)

    # Ensure user has visited a page so that the cookie can be set.
    current_url = browser.current_url
    if current_url == "data:,":
        raise RuntimeError("You must visit a page before logging in.")

    browser.add_cookie(
        {
            "name": "sessionid",
            "value": client.cookies["sessionid"].value,
        }
    )
    browser.refresh()
