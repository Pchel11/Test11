import pytest


@pytest.mark.functional
def test_html(browser):
    browser.get("https://firstapppchel.herokuapp.com/")
    assert "PchelApp" in browser.title
    assert "VK" in browser.page_source
    assert "/s/style.css" in browser.page_source
    assert "/i/back.jpg/" in browser.page_source


@pytest.mark.functional
def test_logo_svg(browser):
    browser.get("http://localhost:8050/img/logo.svg")
    assert "svg" in browser.page_source


@pytest.mark.functional
def test_main_css(browser, main_css):
    browser.get("http://localhost:8050/s/style.css")
    assert main_css in browser.page_source
