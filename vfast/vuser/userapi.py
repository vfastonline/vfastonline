#!encoding:utf-8
from vuser import models
from vfast.api import get_object

def db_update_user(**kwargs):
    pass


def db_del_user(username):
    user = get_object(models.User, username=username)
    if user:
        user.delete()
