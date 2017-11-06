# coding=utf-8
import logging
import traceback
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from vperm import models as vperm_apps
from vperm.models import *

print '2222'
@receiver(post_migrate, sender=vperm_apps)  # 信号的名字，发送者
def init_role_info(sender, **kwargs):  # 回调函数，收到信号后的操作
    """初始化角色信息
    :param sender:
    :param kwargs:
    :return:
    """
    print '3333'
    try:
        print "111111"
        init_info = ["Student", "Teacher", "HR"]
        [Role.objects.get_or_create(rolename=name) for name in init_info]
    except:
        logging.getLogger().error(traceback.print_exc())
