# -*- encoding: utf-8 -*-
class BusinessException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class DataExistsException(Exception):
    """数据存在异常"""

    def __init__(self, message, code=1, http_code=200):
        self.message = message
        self.code = code
        self.http_code = http_code
        super().__init__(self.message)

    def __str__(self):
        return self.message


class DataNotExistsException(Exception):
    """数据不存在异常"""

    def __init__(self, message, code=1, http_code=200):
        self.message = message
        self.code = code
        self.http_code = http_code
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ParamsException(Exception):
    """参数异常"""

    def __init__(self, message, code=1, http_code=400):
        self.message = message
        self.code = code
        self.http_code = http_code
        super().__init__(self.message)

    def __str__(self):
        return self.message