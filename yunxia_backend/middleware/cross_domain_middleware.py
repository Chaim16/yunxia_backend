from django.middleware.common import MiddlewareMixin


class CrossDomainMiddleware(MiddlewareMixin):
    """跨域处理中间件"""

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
