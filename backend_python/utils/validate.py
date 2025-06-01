# -*- coding: utf-8 -*-
import re
import json
import traceback

from functools import wraps
from marshmallow import Schema, fields, validate

from backend_python.utils.log_util import get_logger
from backend_python.utils.response import setResult

logger = get_logger("validate")
esp_list = ['"', '%', '|', '=', ';', '<', '>', ':', '\'', '\\', '--', '*']


def is_integer(arg):
    try:
        arg = int(arg)
    except Exception as e:
        return False
    return True


def is_valid_ipv4(ip):
    ipv4_pattern = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(ipv4_pattern, ip) is not None


class TransCoding(object):

    @staticmethod
    def transcoding(data, coding='utf-8'):
        if not data:
            return data
        if isinstance(data, str) and hasattr(data, 'decode'):
            result = data.decode(coding)
        else:
            result = data
        return result

    def transcoding_list(self, data, coding='utf-8'):
        if not isinstance(data, (list, tuple)):
            raise ValueError('Parameter must be list or tuple')
        result = []
        for item in data:
            if isinstance(item, dict):
                result.append(self.transcoding_dict(item, coding=coding))
                continue
            if isinstance(item, list):
                result.append(self.transcoding_list(item, coding=coding))
                continue
            if isinstance(item, str) and hasattr(item, 'decode'):
                result.append(self.transcoding(item, coding=coding))
                continue
            result.append(item)
        return result if isinstance(data, list) else tuple(result)

    def transcoding_dict(self, data, coding='utf-8'):
        if not isinstance(data, dict):
            raise ValueError('Parameter must be dict')
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                value = self.transcoding_dict(value, coding=coding)
            elif isinstance(value, list):
                value = self.transcoding_list(value, coding=coding)
            else:
                value = self.transcoding(value, coding=coding)
            result[key] = value
        return result


def validate_param(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            try:
                if request.method == "POST":
                    if "application/json" in request.content_type:
                        data = json.loads(request.body)
                    else:
                        data = dict(request.POST.items())
                else:
                    data = dict(request.GET.items())

                logger.info("data : {}".format(data))
                # 处理data中字段为中文时长度的问题
                data = TransCoding().transcoding_dict(data)
                res = schema().validate(data)
                if res:
                    logger.error(u"参数错误:{}".format(res))
                    return setResult({}, "参数校验不通过", 1)
            except Exception as e:
                logger.error(traceback.format_exc())
                return setResult({}, "参数校验失败", 1)
            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator
