import os

import yaml

from yunxia_backend.settings import CONFIG_PATH


with open(CONFIG_PATH, "r") as f:
    application_config = yaml.safe_load(f)


def get_wx_config():
    wx_config = application_config.get("wx_config", {})
    wx_config["app_id"] = os.getenv("WECHAT_APPID")
    wx_config["app_secret"] = os.getenv("WECHAT_SECRET")
    return application_config.get("wx_config")
