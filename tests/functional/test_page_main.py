# import pytest
#
#
# @pytest.mark.functional
# def test_html(chrome):
#     chrome.get("https://firstapppchel.herokuapp.com/")
#     assert "PchelApp" in chrome.title
#     assert "VK" in chrome.page_source
#     assert "/style/" in chrome.page_source
#     assert "/img/back.jpg/" in chrome.page_source
#
#
# @pytest.mark.functional
# def test_logo_svg(chrome):
#     chrome.get("http://localhost:8050/img/logo.svg")
#     assert "svg" in chrome.page_source
#     assert "logo" in chrome.page_source
#
#
# @pytest.mark.functional
# def test_main_css(chrome, main_css):
#     chrome.get("http://localhost:8000/style")
#     assert main_css in chrome.page_source
