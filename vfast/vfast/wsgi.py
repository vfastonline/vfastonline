"""
WSGI config for vfast project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

from django.core.wsgi import get_wsgi_application

os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vfast.settings")

application = get_wsgi_application()
