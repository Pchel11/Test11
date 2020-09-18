import consts
import custom_types
import utils


def render_hello_page(
        request: custom_types.HttpRequest,
        new_user: custom_types.User,
        saved_user: custom_types.User,
) -> str:
    css_class_for_name = css_class_for_age = ""
    label_for_name = "Your name: "
    label_for_age = "Your age: "

    age_new = age_saved = saved_user.age
    name_new = name_saved = saved_user.name

    if new_user.errors:
        if "name" in new_user.errors:
            error = new_user.errors["name"]
            label_for_name = f"ERROR: {error}"
            css_class_for_name = consts.CSS_CLASS_ERROR

        if "age" in new_user.errors:
            error = new_user.errors["age"]
            label_for_age = f"ERROR: {error}"
            css_class_for_age = consts.CSS_CLASS_ERROR

        name_new = new_user.name
        age_new = new_user.age

    theme = utils.load_theme(request.session)
    year, era = utils.year_calc(age_saved)
    template = utils.read_static("hello.html").decode()

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
        "theme": theme,
    }

    content = template.format(**context)

    return content
