import pytest


@pytest.mark.functional
def test(chrome):
    chrome.get("http://localhost:8000/")
    assert "PchelApp" in chrome.title
    assert "MyFirstProject" in chrome.page_source
