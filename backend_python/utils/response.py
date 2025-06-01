import json
from django.http import HttpResponse


def setResult(data={}, message=u"成功", code=0):
    result = {
        "code": code,
        "data": data,
        "message": message,
    }
    return HttpResponse(json.dumps(result), status=200, content_type="text/json")
