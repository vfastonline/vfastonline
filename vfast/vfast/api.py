# encoding: utf8
import hashlib
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import logging
import logging.handlers
import time, os, json, base64
from django.core.mail import send_mail


def get_validate(email, uid, role, fix_pwd):
    t = int(time.time())
    validate_key = hashlib.md5('%s%s%s' % (email, t, fix_pwd)).hexdigest()
    return base64.b64encode('%s|%s|%s|%s|%s' % (email, t, uid, role, validate_key)).strip()


def validate(key, fix_pwd):
    # t = int(time.time())
    key = base64.b64decode(key)
    x = key.split('|')
    print x
    if len(x) != 5:
        logging.getLogger().warning('token参数数量不足')
        return json.dumps({'code': 1, 'msg': u'token参数不足'}, ensure_ascii=False)
    validate_key = hashlib.md5('%s%s%s' % (x[0], x[1], fix_pwd)).hexdigest()
    if validate_key == x[4]:
        logging.getLogger().info('认证通过')
        return json.dumps({'code': 0, 'email': x[0], 'uid': x[1], 'role': x[2]})
    else:
        logging.getLogger().warning('密码不正确')
        return json.dumps({'code': 1, 'msg': '密码不正确'}, ensure_ascii=False)


def encry_password(password, salt='salt'):
    string = password + salt
    return hashlib.new('md5', string).hexdigest()


class ConcurrentDayRotatingFileHandler(logging.handlers.BaseRotatingHandler):
    def __init__(self, filename, encoding=None, delay=False):
        logging.handlers.BaseRotatingHandler.__init__(self, filename, 'a', encoding, delay)
        self.day = time.strftime('%Y-%m-%d', time.localtime())

    def shouldRollover(self, record):
        now_day = time.strftime('%Y-%m-%d', time.localtime())
        if self.stream is None:
            self.stream = self._open()
        if now_day == self.day:
            return False
        return True

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        rotate_log = "%s.%s" % (self.baseFilename, self.day)
        if not os.path.exists(rotate_log):
            os.rename(self.baseFilename, rotate_log)
        self.day = time.strftime('%Y-%m-%d', time.localtime())

        if not self.delay:
            self.stream = self._open()


def set_logging(log_path, log_level='error'):
    def add_handler(log_name, formatter, level, logger=None):
        if not logger:
            return
        log_handler = ConcurrentDayRotatingFileHandler(log_name)
        log_formatter = logging.Formatter(formatter)
        log_handler.setFormatter(log_formatter)
        logger.addHandler(log_handler)
        logger.setLevel(level)

    LOG_LEVELS = {
        'critical': logging.CRITICAL, 'error': logging.ERROR,
        'warning': logging.WARNING, 'info': logging.INFO,
        'debug': logging.DEBUG
    }

    if not os.path.isdir(log_path):
        os.makedirs(log_path)

    # log_name = os.path.join(log_path, 'record.log')
    # logger = logging.getLogger('record')
    # formatter = '%(asctime)s %(message)s'
    # add_handler(log_name, formatter, logging.DEBUG, logger)

    log_name = os.path.join(log_path, 'service.log')
    logger = logging.getLogger()
    formatter = '%(asctime)s %(levelname)s %(process)d %(thread)d %(filename)s-%(funcName)s:%(lineno)d %(message)s'
    add_handler(log_name, formatter, LOG_LEVELS.get(log_level.lower(), logging.ERROR), logger)


def write_log(user, msg):
    logging.getLogger('record').debug('%s %s %s' % (int(time.time()), user, msg))


def get_id_name(model, **kwargs):
    result = model.objects.filter(**kwargs).values('id', 'name')
    return result

def require_role(role=2):
    def _deco(func):
        def __deco(request, *args, **kwargs):
            request.session['pre_url'] = request.path
            try:
                if role != request.session.get('user')['role']:
                    return HttpResponse(json.dumps({'errmsg': '权限不够'}, ensure_ascii=False))
            except TypeError:
                HttpResponseRedirect(reverse('login'))
            return func(request, *args, **kwargs)
        return __deco
    return _deco


def require_login():
    def _deco(func):
        def __deco(request, *args, **kwargs):
            request.session['pre_url'] = request.path
            if not request.session.get('login', None):
                return HttpResponseRedirect(reverse('login'))
            return func(request, *args, **kwargs)
        return __deco
    return _deco