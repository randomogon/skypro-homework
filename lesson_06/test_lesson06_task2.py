
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_profile(driver, session, profile_url):
    driver.get("https://gitflic.ru/")
    driver.delete_all_cookies()

    driver.add_cookie({
        "name": "SESSION",
        "value": session,
        "path": "/",
    })

    driver.refresh()

    cookie = driver.get_cookie("SESSION")
    assert cookie is not None

    driver.get(profile_url)

    WebDriverWait(driver, 15).until(
        EC.url_to_be(profile_url)
    )

    return driver.current_url


def test_session_storage_auth():
    session1 = os.environ["GITFLIC_USER1_SESSION"]
    session2 = os.environ["GITFLIC_USER2_SESSION"]

    assert session1
    assert session2
    assert session1 != session2

    driver = webdriver.Chrome()

    try:
        url1 = open_profile(
            driver,
            session1,
            "https://gitflic.ru/user/randomogon",
        )

        driver.delete_all_cookies()

    finally:
        driver.quit()

    driver = webdriver.Chrome()

    try:
        url2 = open_profile(
            driver,
            session2,
            "https://gitflic.ru/user/randomogon1",
        )

        assert url1 != url2

    finally:
        driver.quit()
