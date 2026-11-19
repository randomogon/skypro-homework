
from selenium import webdriver
from login_page import LoginPage
from main_shop_page import MainShopPage
from cart_page import CartPage
from checkout_page import CheckoutPage


def test_shop():
    driver = webdriver.Firefox()
    products = []
    total = None

    try:
        login = LoginPage(driver)
        shop = MainShopPage(driver)
        cart = CartPage(driver)
        checkout = CheckoutPage(driver)

        login.open()
        login.login("standard_user", "secret_sauce")

        shop.add_product("add-to-cart-sauce-labs-backpack")
        shop.add_product("add-to-cart-sauce-labs-bolt-t-shirt")
        shop.add_product("add-to-cart-sauce-labs-onesie")

        shop.open_cart()

        products = cart.get_product_names()
        cart.checkout()

        checkout.fill_customer_info(
            "Alex", "Tester", "12345"
        )
        checkout.continue_checkout()

        total = checkout.get_total()

    finally:
        driver.quit()

    expected_products = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie",
    ]

    assert sorted(products) == sorted(expected_products), (
        f"Неверные товары в корзине: {products}"
    )

    assert total == "Total: $58.29", (
        f"Ожидали Total: $58.29, получили {total}"
    )
