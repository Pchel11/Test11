from selenium.webdriver.common.by import By

from .abstract import PageElement, PageObject


class HelloPage(PageObject):
    button_greet = PageElement(By.CSS_SELECTOR, "button#greet-button-id")
    button_reset = PageElement(By.CSS_SELECTOR, "button#reset-button-id")
    button_style = PageElement(By.CSS_SELECTOR, "button#style-button-id")
    input_name = PageElement(By.CSS_SELECTOR, "input#name-id")
    input_age = PageElement(By.CSS_SELECTOR, "input#age-id")
