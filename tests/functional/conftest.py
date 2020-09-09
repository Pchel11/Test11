import pytest
from selenium import webdriver

from consts import USERS_DATA


@pytest.yield_fixture(scope="function", autouse=True)
def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")

    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.implicitly_wait(10)

    try:
        yield browser
    finally:
        browser.close()
        browser.quit()


@pytest.yield_fixture(scope="function", autouse=True)
def users_data():
    data = ""
    if USERS_DATA.is_file():
        with USERS_DATA.open("r") as src:
            data = src.read()

    with USERS_DATA.open("w"):
        pass

    yield

    with USERS_DATA.open("w") as dst:
        dst.write(data)