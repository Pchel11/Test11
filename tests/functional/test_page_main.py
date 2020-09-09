# import pytest
#
#
# @pytest.mark.functional
# def test_html(browser):
#     browser.get("https://firstapppchel.herokuapp.com/")
#     assert "PchelApp" in browser.title
#     assert "VK" in browser.page_source
#     assert "/st/style.css" in browser.page_source
#     assert "/img/back.jpg/" in browser.page_source
#
#
# # @pytest.mark.functional
# # def test_logo_svg(chrome):
# #     chrome.get("http://localhost:8050/img/logo.svg")
# #     assert "svg" in chrome.page_source
# #     assert "logo" in chrome.page_source
#
#
# @pytest.mark.functional
# def test_main_css(browser, style):
#     browser.get("http://localhost:8050/st/style.css")
#     assert style.csss in browser.page_source
