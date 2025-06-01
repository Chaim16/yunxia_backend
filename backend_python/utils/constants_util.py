from enum import Enum


class Danger(Enum):

    man = 1
    woman = 0


class Role(Enum):

    GENERAL = "general"
    ADMINISTRATOR = "administrator"


class OrderStatus(Enum):

    PENDING = "pending"        # 待支付
    PAID = "paid"              # 已支付
    PAY_FAILED = "pay_failed"  # 支付失败
    SHIPPED = "shipped"        # 已发货
    DELIVERED = "delivered"    # 已收货
    CANCELLED = "cancelled"    # 已取消
