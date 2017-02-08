#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
import json, logging, traceback, base64
import time
import os
from vuser import models
from vfast.api import encry_password, send_mail


# Create your views here.
def test(request):
    return HttpResponse('hello,world~!')


def userexists(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email', None)
            username = request.POST.get('username', None)
            if email:
                result = models.User.objects.filter(email=email).exists()
                print result
                if result:
                    return HttpResponse(json.dumps({'code': 1, 'msg': u'用户已存在'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({'code': 0, 'msg': u'还未注册'}, ensure_ascii=False))
            else:
                result = models.User.objects.filter(username=username).exists()
                print result
                if result:
                    return HttpResponse(json.dumps({'code': 1, 'msg': u'用户已存在'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({'code': 0, 'msg': u'还未注册'}, ensure_ascii=False))
        else:
            return render(request, 'usertest.html')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(u'服务器错误')


def register(request):
    try:
        if request.method == 'GET':
            return render(request, 'usertest.html')
        else:
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            email = request.POST.get('email', None)
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if (email and username and password):
                password = encry_password(password)
            else:
                return HttpResponse(json.dumps({'code': 1, 'msg': u'参数错误'}))
            program_exp = request.POST.get('program_exp', '')
            comp_use_time_day = request.POST.get('comp_use_time_day', '')
            into_it = request.POST.get('into_it', '')
            learn_habit = request.POST.get('learn_habit', '')
            active = base64.b64encode('%s|%s|%s' % (email, settings.SECRET_KEY, t)).strip()
            subject = u'Vfast用户账号激活'
            message = u'''
                                    恭喜您,注册V-fast学习账号成功!
                                    您的账号为: %s
                                    V-fast账号需要激活才能正常使用!
                                    点我激活账号

                                    如果无法点击请复制一下链接到浏览器地址
                                    %s/user/active?active=%s
                                ''' % (email, settings.HOST, active)
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email, ])
            result = models.User.objects.get_or_create(email=email, username=username, password=password,
                                                       program_exp=program_exp,
                                                       comp_use_time_day=comp_use_time_day, into_it=into_it,
                                                       learn_habit=learn_habit, active=active)
            if result:
                return HttpResponse(json.dumps({'code': 0, 'msg': u'注册成功, 请激活账号!'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'code': 1, 'msg': u'数据库错误'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 2, 'msg': u'服务器错误'}, ensure_ascii=False))


def useractive(request):
    try:
        active = request.GET.get('active', ' ')
        user = models.User.objects.get(active=active)
        if user:
            user.status = 1
            print user.status
            user.save()
            return HttpResponse(json.dumps({'code': 0, 'msg': u'激活成功'}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'服务器错误'}, ensure_ascii=False))


def resetpw(request):
    try:
        if request.method == 'GET':
            return render(request, 'usertest.html')
        else:
            email = request.POST.get('email', ' ')
            user = models.User.objects.filter(email=email).exists()
            if user:
                t = int(time.time())
                active = base64.b64encode('%s|%s' % (email, t)).strip()
                models.User.objects.filter(email=email).update(active=active)
                subject = u'Vfast用户账号密码重置'
                message = u'''
                            您在访问Vfast时点击了“忘记密码”链接，这是一封密码重置确认邮件。

您可以通过点击以下链接重置帐户密码:

%s/user/active?active=%s

为保障您的帐号安全，请在24小时内点击该链接，您也可以将链接复制到浏览器地址栏访问。 若如果您并未尝试修改密码，请忽略本邮件，由此给您带来的不便请谅解。


本邮件由系统自动发出，请勿直接回复！

                                                ''' % (settings.HOST, active)
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email, ])
                return HttpResponse(json.dumps({'code': 0, 'msg': u'重置密码邮件已发送'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({'code': 1, 'msg': u'用户不存在'}, ensure_ascii=False))

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 2, 'msg': u'服务器错误'}))


def resetpassword(request):
    try:
        if request.method == 'GET':
            return render(request, 'usertest.html')
        else:
            email = request.POST.get('email', ' ')
            password = request.POST.get('password', ' ')
            password = encry_password(password)
            models.User.objects.filter(email=email).update(password=password)
            return HttpResponse('update password successful')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 2, 'msg': u'服务器错误'}))


def login(request):
    try:
        if request.method == 'GET':
            return render(request, 'usertest.html')
        else:
            email = request.POST.get('email', ' ')
            password = request.POST.get('password', ' ')
            password = encry_password(password)
            user = models.User.objects.get(Q(email=email) | Q(username=email), password=password)
            if user.status == 0:
                return HttpResponse(u'账号未激活')
            else:
                return HttpResponse('login successful')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 2, 'msg': u'服务器错误'}))


def userdetail(request):
    try:
        if request.method == 'GET':
            uid = request.GET.get('uid', ' ')
            user = models.User.objects.get(id=uid)
            print user
            return HttpResponse()
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse(json.dumps({'code': 1, 'msg': u'用户不存在'}))


def logout(request):
    pass


def comapny_add(request):
    try:
        if request.method == 'GET':
            return render(request, 'test.html')
        else:
            fullname = request.POST.get('fullname', ' ')
            name = request.POST.get('name', ' ')
            trade = request.POST.get('trade', ' ')
            scale = request.POST.get('scale', ' ')
            intro = request.POST.get('intro', ' ')
            forwho = request.POST.get('forwho', ' ')
            period = request.POST.get('period', ' ')
            technology_type = request.POST.get('technology_type', ' ')
            wanted_exp = request.POST.get('wanted_exp', ' ')
            work_address = request.POST.get('work_address', ' ')
            homepage = request.POST.get('homepage', ' ')
            finacing = request.POST.get('finacing', ' ')
            logofile = request.FILES.get('logo', None)
            business_license_file = request.FILES.get('business_license', None)
            manager_id = request.POST.get('manager_id', 1)

            createtime = time.strftime('%Y-%m-%d %H:%M:%S')
            manager = models.User.objects.get(id=manager_id)
            day = time.strftime('%Y%m%d')
            comppath = os.path.join(settings.MEDIA_ROOT, 'company/%s' % day)
            os.system('mkdir -p %s' % comppath)

            # 获取需要保存的logo, business_license的相对路径
            logo = 'company/%s/%s' % (day, logofile.name) if logofile else ' '
            business_license = 'company/%s/%s' % (day, business_license_file.name) if business_license_file else ' '

            for f in [logofile, business_license_file]:
                try:
                    filename = open(os.path.join(comppath, f.name), 'wb+')
                    for chunk in f.chunks():
                        filename.write(chunk)
                    filename.close()
                except AttributeError:
                    logging.getLogger().error('创建公司时, 保存logo图片, 营业执照错误')

            subject = u'您申请HR注册公司资质信息正在审核中......'
            message = u'''
                                    HR注册信息, 正在审核中.......
                        '''
            send_mail(subject, message, settings.EMAIL_HOST_USER, [manager.email, ])

            result = models.Company.objects.create(createtime=createtime, fullname=fullname, name=name, trade=trade,
                                                   scale=scale,
                                                   intro=intro, forwho=forwho, period=period,
                                                   technology_type=technology_type,
                                                   wanted_exp=wanted_exp,
                                                   work_address=work_address, logo=logo, homepage=homepage,
                                                   finacing=finacing,
                                                   business_license=business_license,
                                                   audit_status=0, manager_id=manager.id)
            if result:
                return HttpResponse('company register ok')
            else:
                return HttpResponse('company register failed')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('company error')


def company_verify(request):
    try:
        compid = request.GET.get('id')
        result = models.Company.objects.filter(id=compid).update(audit_status=1)
        if result:
            return HttpResponse('comp audit_status successful')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('comp verify error')


def company_info(request):
    try:
        compid = request.GET.get('id')
        company = models.Company.objects.get(id=compid)
        return  render(request)
    except:
        pass


def company_edit(request):
    try:
        pass
    except:
        pass


def company_del(request):
    try:
        pass
    except:
        pass


def hr_register(request):
    try:
        pass
    except:
        pass
