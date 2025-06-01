import traceback

from django.middleware.common import MiddlewareMixin

from yunxia_backend.utils.exception_util import DataExistsException, DataNotExistsException, BusinessException, ParamsException
from yunxia_backend.utils.log_util import get_logger
from yunxia_backend.utils.response import setResult

logger = get_logger("error")


class ExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求对象
        :param exception: 异常对象
        """
        code = 1
        if isinstance(exception, DataExistsException):
            message = str(exception)
        elif isinstance(exception, DataNotExistsException):
            message = str(exception)
        elif isinstance(exception, BusinessException):
            message = str(exception)
        elif isinstance(exception, ParamsException):
            message = str(exception)
        else:
            message = "请求处理异常"

        logger.error("异常：{}，详细堆栈：{}".format(message, traceback.format_exc()))
        return setResult({}, message, code)
