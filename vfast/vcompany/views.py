#!encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from vuser.models import User
from vcompany.models import Company
from django.conf import settings
from vfast.api import send_mail, encry_password

import os
import logging
import time
import traceback
import json
import base64


# Create your views here.
def company_add(request):
    try:
        if request.method == 'GET':
            return render(request, 'testdu.html')
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
            manager = User.objects.get(id=manager_id)
            comppath = os.path.join(settings.IMG_ROOT, 'company/')
            os.system('mkdir -p %s' % comppath)

            # 获取需要保存的logo, business_license的相对路径
            logo = 'company/%s' % logofile.name if logofile else ' '
            business_license = 'company/%s' % business_license_file.name if business_license_file else ' '

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

            result = Company.objects.create(createtime=createtime, fullname=fullname, name=name, trade=trade,
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
        result = Company.objects.filter(id=compid).update(audit_status=1)
        if result:
            return HttpResponse('comp audit_status successful')
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('comp verify error')


def company_info(request):
    try:
        compid = request.GET.get('id')
        company = Company.objects.filter(id=compid).values()[0]
        print company['createtime']
        print company
        return HttpResponse(json.dumps({'comp': company}, ensure_ascii=False))
    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('error')


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
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password', '123456')
            idfile = request.FILES.get('idcard', None)
            gpfile = request.FILES.get('gongpai', None)
            onjobfile = request.FILES.get('joblevel', None)
            joblevel = request.POST.get('joblevel')
            createtime = time.strftime('%Y-%m-%d %H:%M:%S')
            password = encry_password(password, settings.SECRET_KEY)

            t = int(time.time())
            active = base64.b64encode('%s|%s|%s' % (email, settings.SECRET_KEY, t)).strip()

            # 获取需要保存的图片的目录
            hrpath = os.path.join(settings.IMG_ROOT, 'static/hr')
            print hrpath
            os.system('mkdir -p %s' % hrpath)
            idcard = os.path.join('/static/hr', idfile.name) if idfile else ' '
            gongpai = os.path.join('/static/hr', gpfile.name) if gpfile else ' '
            on_job_verify = os.path.join('/static/hr', onjobfile.name) if onjobfile else ' '

            # 保存图片
            for f in [idfile, gpfile, onjobfile]:
                try:
                    filename = open(os.path.join(hrpath, f.name), 'wb+')
                    for chunk in f.chunks():
                        filename.write(chunk)
                    filename.close()
                except AttributeError:
                    logging.getLogger().error('HR注册, 保存身份证, 工牌, 在职证明文件时出错')

            User.objects.create(email=email, password=password, gongpai=gongpai, idcard=idcard,
                                       on_job_verify=on_job_verify, active=active,
                                       createtime=createtime, joblevel=joblevel)
            # sendmail
            # subject = u'Vfast HR用户账号激活'
            # message = u'''
            #                                     恭喜您,注册V-fast HR账号成功!
            #                                     您的账号为: %s
            #                                     V-fast账号需要激活才能正常使用!
            #                                     点我激活账号
            #
            #                                     如果无法点击请复制一下链接到浏览器地址
            #                                     %s/u/active?active=%s
            #                                 ''' % (email, settings.HOST, active)
            # send_mail(subject, message, settings.EMAIL_HOST_USER, [email, ])
            hr = User.objects.filter(email=email).values('id', 'email')[0]
            print hr
            return HttpResponse(json.dumps(hr, ensure_ascii=False))

        else:
            return render(request, 'testdu.html')

    except:
        logging.getLogger().error(traceback.format_exc())
        return HttpResponse('failed')