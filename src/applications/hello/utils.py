from datetime import date
from typing import Dict

from django.http import HttpRequest

from applications.hello.forms.fields import HelloForm


def build_context_for_hello(request: HttpRequest) -> Dict:
    name_saved = request.session.get("name")
    age_saved = request.session.get("age")
    age_new = ""
    name_new = ""

    if not age_saved:
        age_saved = 0

    year = date.today().year - int(age_saved)
    if year < 0:
        year = -year
        era = "BC"
    elif year >= 0:
        year = year
        era = "AC"

    if name_saved:
        name_new = name_saved

    if age_saved:
        age_new = age_saved

    context = {
        "age_new": age_new,
        "age_saved": age_saved,
        "name_new": name_new,
        "name_saved": name_saved or "anonymous",
        "theme": "dark",
        "year": year,
        # "form": HelloForm(),
    }
    return context


def theme_switcher(current_theme):
    themes = {"theme_light.css": "theme_dark.css",
              "theme_dark.css": "theme_light.css"}
    theme = themes.get(current_theme)
    return theme
