from rest_framework.exceptions import APIException


class ImageNotFound(APIException):
    def __init__(self, detail=None, code=None, info=None):
        self.detail = detail
        self.code = code
        info.context.response.status_code = code


class CollectionNotFound(APIException):
    def __init__(self, detail=None, code=None, info=None):
        self.detail = detail
        self.code = code
        info.context.response.status_code = code
