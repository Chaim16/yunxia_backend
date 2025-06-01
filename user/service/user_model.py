import requests
from django.core.paginator import Paginator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

from user.models import User
from yunxia_backend.utils.conf_util import get_wx_config
from yunxia_backend.utils.constants_util import Role
from yunxia_backend.utils.exception_util import BusinessException
from yunxia_backend.utils.log_util import get_logger

logger = get_logger("user")


class UserModel(object):

    def auth(self, code):
        wx_config = get_wx_config()
        app_id = wx_config.get('app_id')
        app_secret = wx_config.get('app_secret')
        if not app_id or not app_secret:
            logger.error("未配置APP_ID或APP_SECRET")
            raise BusinessException("授权失败")
        url = wx_config.get("auth_url")
        params = {
            "appid": wx_config.get("app_id"),
            "secret": wx_config.get("app_secret"),
            "js_code": code,
            "grant_type": "authorization_code",
        }
        try:
            logger.info("请求微信接口：{}, params:{}".format(url, params))
            wx_response = requests.get(url, params=params).json()
            openid = wx_response.get("openid")
            logger.info("获取到openid：{}".format(openid))
        except Exception as e:
            logger.error(f"获取openid失败")
            raise BusinessException("获取openid失败")

        # 查找用户是否已存在
        user = User.objects.filter(openid=openid)
        if not user.exists():
            # 注册用户
            add_params = {
                "username": openid[-6:],
                "password": make_password("yunxia123"),
                "phone": "",
                "role": Role.GENERAL.value,
                "openid": openid,
            }
            user = User(**add_params)
            user.save()
            logger.info("注册用户：{}".format(openid))
        else:
            user = user.first()
            logger.info("用户已存在：{}".format(openid))
        # 发放token
        refresh = RefreshToken.for_user(user)
        token = refresh.access_token
        logger.info("用户授权成功：{}".format(token))
        return {
            "token": str(token),
            "refresh": str(refresh),
        }

    def register(self, username, password, nickname, gender, phone):
        # 判断用户是否存在
        if User.objects.filter(username=username).exists():
            raise BusinessException("用户名{}已存在".format(username))

        # 保存用户信息
        add_params = {
            "username": username,
            "password": password,
            "nickname": nickname,
            "gender": gender,
            "phone": phone,
            "role": Role.GENERAL.value,
        }
        logger.info("注册用户信息：{}".format(add_params))
        User.objects.create_user(**add_params)
        logger.info("注册用户成功：{}".format(username))

    def whoami(self, username):
        user = User.objects.get(username=username)
        return {
            "username": user.username,
            "role": user.role,
        }

    def detail(self, username):
        user = User.objects.get(username=username)
        user_dict = {
            "username": user.username,
            "nickname": user.nickname,
            "gender": user.gender,
            "phone": user.phone,
            "role": user.role,
        }
        return user_dict

    def modify(self, username, nickname, gender, phone, role):

        modify_params = {}
        if nickname:
            modify_params["nickname"] = nickname
        if gender is not None:
            modify_params["gender"] = gender
        if phone:
            modify_params["phone"] = phone
        if role:
            modify_params["role"] = role
        logger.info("修改用户信息：{}".format(modify_params))
        User.objects.filter(username=username).update(**modify_params)

    def id_by_username(self, username):
        user = User.objects.get(username=username)
        return user.id

    def user_list(self, page, size,**kwargs):
        user_list = User.objects.all().order_by("-id")
        if kwargs.get("username"):
            user_list = user_list.filter(username=kwargs.get("username"))
        if kwargs.get("gender") is not None:
            user_list = user_list.filter(gender=kwargs.get("gender"))
        if kwargs.get("phone"):
            user_list = user_list.filter(phone=kwargs.get("phone"))
        if kwargs.get("role"):
            user_list = user_list.filter(role=kwargs.get("role"))
        count = user_list.count()
        paginator = Paginator(user_list, size)
        user_list = paginator.get_page(page)
        data_list = []
        for item in user_list:
            data_list.append({
                "id": item.id,
                "username": item.username,
                "nickname": item.nickname,
                "gender": item.gender,
                "phone": item.phone,
                "role": item.role,
            })
        return {"count": count, "list": data_list}

    def del_user(self, username):
        user = User.objects.get(username=username)
        user.delete()
        logger.info("已删除用户：{}".format(username))