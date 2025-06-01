import json
import uuid

from django.middleware.common import MiddlewareMixin
from backend_python.utils.log_util import get_logger
from backend_python.utils.response import setResult
from backend_python.utils.validate import TransCoding

logger = get_logger("access")


class HTTPLogMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_request(self, request):
        """预处理请求，记录日志"""
        request_id = str(uuid.uuid4())
        request.request_id = request_id
        params = ""
        if request.method == "GET":
            params = TransCoding().transcoding_dict(dict(request.GET.items()))
        elif request.method == "POST":
            try:
                params = json.loads(request.body)
            except Exception as e:
                params = request.POST.dict()
        elif request.method == "OPTIONS":
            return
        else:
            return setResult({}, "不支持的请求方法", 1)
        msg = "access with request_id:{}, method:{}, path:{}, params:{}".format(
            request_id, request.method, request.path, params)
        logger.info(msg)

    def process_response(self, request, response):
        """预处理响应，记录日志"""
        request_id = request.request_id
        response_data = response.content[:200]  # 只记录前200个字符
        msg = "response request:{}, with data:{}".format(request_id, response_data)
        logger.info(msg)
        return response

