from typing import Optional

import strawberry


@strawberry.interface
class BaseImageType:
    base_url: str

@strawberry.type
class BaseHttpResponse:
    status_code: int
    status_message: str
    error_message: Optional[str] = None