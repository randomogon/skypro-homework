from selenium import webdriver
from selenium.webdriver.common.by import By


def test_navigation():
    driver = webdriver.Chrome()

    driver.get("https://httpbin.qa-territory.online/")
    original_url = driver.current_url

    driver.find_element(By.LINK_TEXT, "HTML Form").click()

    assert driver.current_url.endswith("/forms/post")

    driver.back()

    assert driver.current_url == original_url

    driver.quit()
