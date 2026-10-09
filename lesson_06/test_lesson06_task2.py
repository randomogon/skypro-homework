import os

import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_profile(session, profile_url):
    driver = webdriver.Chrome()

    try:
        driver.get("https://gitflic.ru/")
        driver.delete_all_cookies()

        driver.add_cookie({
            "name": "SESSION",
            "value": session,
            "path": "/",
        })

        cookie = driver.get_cookie("SESSION")
        assert cookie is not None
        assert cookie["value"] == session

        driver.refresh()

        driver.get(profile_url)

        WebDriverWait(driver, 20).until(
            EC.url_to_be(profile_url)
        )

        current_url = driver.current_url

        driver.delete_all_cookies()

        return current_url

    finally:
        driver.quit()


def test_session_storage_auth():
    session1 = os.getenv("GITFLIC_USER1_SESSION")
    session2 = os.getenv("GITFLIC_USER2_SESSION")

    if not session1 or not session2:
        pytest.skip(
            "Для запуска нужны реальные SESSION cookie "
            "двух аккаунтов GitFlic"
        )

    assert session1 != session2

    url1 = open_profile(
        session1,
        "https://gitflic.ru/user/randomogon",
    )

    url2 = open_profile(
        session2,
        "https://gitflic.ru/user/randomogon1",
    )

    assert url1 != url2
