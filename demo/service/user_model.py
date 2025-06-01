
from django.core.paginator import Paginator

from demo.models import User
from yunxia_backend.utils.constants_util import Role
from yunxia_backend.utils.exception_util import BusinessException
from yunxia_backend.utils.log_util import get_logger

logger = get_logger("user")


class UserModel(object):

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