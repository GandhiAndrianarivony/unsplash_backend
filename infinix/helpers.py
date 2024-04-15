import re
import base64

from strawberry.types import Info


def set_status_code(info: Info, status_code: int):
    info.context.response.status_code = status_code


def get_id(base64_string: str):
    res = None
    decoded_id = base64.b64decode(base64_string).decode("utf-8")
    match_ = re.search(r"\d+", decoded_id)
    if match_:
        res = int(match_.group(0))
    return res
