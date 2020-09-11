from datetime import date
from typing import AnyStr

import settings
from consts import USERS_DATA
from errors import NotFound


def to_bytes(text: AnyStr) -> bytes:
    """
    Safely converts any string to bytes.
    :param text: any string
    :return: bytes
    """

    if isinstance(text, bytes):
        return text

    if not isinstance(text, str):
        err_msg = f"cannot convert {type(text)} to bytes"
        raise ValueError(err_msg)

    result = text.encode()
    return result


def to_str(text: AnyStr) -> str:
    """
    Safely converts any string to str.
    :param text: any string
    :return: str
    """

    result = text

    if not isinstance(text, (str, bytes)):
        result = str(text)

    if isinstance(result, bytes):
        result = result.decode()

    return result


def read_static(path: str) -> bytes:
    """
    Reads and returns the content of static file.
    If there is no file, then NotFound exception is raised.
    :param path: path to static content
    :return: bytes of content
    """

    static_obj = settings.STATIC_DIR / path
    if not static_obj.is_file():
        static_path = static_obj.resolve().as_posix()
        err_msg = f"file <{static_path}> not found"
        raise NotFound(err_msg)

    with static_obj.open("rb") as src:
        content = src.read()

    return content


def save_user_data(data: str) -> None:
    with USERS_DATA.open("w") as dst:
        dst.write(data)


def load_user_data() -> str:
    if not USERS_DATA.is_file():
        return ""

    with USERS_DATA.open("r") as src:
        data = src.read()

    data = to_str(data)

    return data


def year_calc(age_saved):
    year = date.today().year - age_saved
    if year < 0:
        year = -year
        era = "BC"
    elif year >= 0:
        year = year
        era = "AC"
    return year, era
