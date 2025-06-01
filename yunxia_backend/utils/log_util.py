"""
* @Author : 喻清明
* @FileName: log_utils.py
* @Date : 2024/7/9
"""

import os.path

from loguru import logger
from yunxia_backend.settings import log_conf

handler_dict = {}


def get_logger(module: str = ""):
    # 如果module为空或者None，直接使用全局的logger
    if not module:
        return logger
    global handler_dict
    if module in handler_dict:
        return handler_dict.get(module)

    log_path = os.path.join(log_conf.get("log_path"), '{}.log'.format(module))
    logger.add(log_path, format=log_conf.get("format_string"),
               filter=lambda record: module in record["extra"].get("mod", ""),
               level=log_conf.get("level"), rotation="00:00", retention="7 days")

    current_logger = logger.bind(mod=module)
    handler_dict[module] = current_logger

    return current_logger
