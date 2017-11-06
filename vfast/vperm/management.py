# coding=utf-8
import logging
import traceback

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from vperm.models import *


@receiver(post_migrate)
def init_db_info(sender, **kwargs):
    """初始化字典信息
    :param sender:
    :param kwargs:
    :return:
    """
    try:
        if sender.name == "vperm":
            init_info = ["Student", "Teacher", "HR"]
            [Role.objects.get_or_create(rolename=name) for name in init_info]
    except:
        logging.getLogger().error(traceback.print_exc())
