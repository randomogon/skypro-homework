
from selenium import webdriver
from calculator_page import CalculatorPage


def test_calculator():
    driver = webdriver.Chrome()

    try:
        calculator = CalculatorPage(driver)

        calculator.open()
        calculator.set_delay(45)

        calculator.click_button("7")
        calculator.click_button("+")
        calculator.click_button("8")
        calculator.click_button("=")

        result = calculator.get_result("15")

        assert result == "15", (
            f"Ожидали результат 15, получили {result}"
        )

    finally:
        driver.quit()
