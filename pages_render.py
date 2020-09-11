from consts import CSS_CLASS_ERROR
from custom_types import User
from utils import read_static, year_calc


def render_hello_page(new_user: User, saved_user: User) -> str:
    css_class_for_name = css_class_for_age = ""
    label_for_name = "Your name: "
    label_for_age = "Your age: "

    age_new = age_saved = saved_user.age
    name_new = name_saved = saved_user.name

    year, era = year_calc(age_saved)

    if new_user.errors:
        if "name" in new_user.errors:
            error = new_user.errors["name"]
            label_for_name = f"ERROR: {error}"
            css_class_for_name = CSS_CLASS_ERROR

        if "age" in new_user.errors:
            error = new_user.errors["age"]
            label_for_age = f"ERROR: {error}"
            css_class_for_age = CSS_CLASS_ERROR

        name_new = new_user.name
        age_new = new_user.age

    template = read_static("hello.html").decode()

    context = {
        "age_new": age_new or "",
        "label_for_age": label_for_age,
        "label_for_name": label_for_name,
        "name_new": name_new or "",
        "name_saved": name_saved or "",
        "class_for_age": css_class_for_age,
        "class_for_name": css_class_for_name,
        "year": year,
        "era": era,
    }

    content = template.format(**context)

    return content
