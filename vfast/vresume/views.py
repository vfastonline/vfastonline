#!encoding:utf-8
import json
import logging
import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import DetailView, View

from share_module.permissionMixin import class_view_decorator
from vresume.models import *


@class_view_decorator(login_required)
class ResumeDetail(DetailView):
    context_object_name = "User"
    template_name = "resume.html"
    pk_url_kwarg = "user_id"
    model = User

    def get_context_data(self, **kwargs):
        try:
            user_id = self.kwargs.get("user_id")

            if user_id:
                kwargs["Resumes"] = Resume.objects.filter(user_id=user_id).first()
                kwargs["CareerObjectives"] = CareerObjective.objects.filter(user_id=user_id)
                kwargs["WorkExperiences"] = WorkExperience.objects.filter(user_id=user_id)
                kwargs["ProjectExperiences"] = ProjectExperience.objects.filter(user_id=user_id)
                kwargs["EducationExperiences"] = EducationExperience.objects.filter(user_id=user_id)
            return super(ResumeDetail, self).get_context_data(**kwargs)
        except:
            logging.getLogger().error(traceback.format_exc())


resume_type_model_dict = {
    "resume": Resume,
    "careerobjective": CareerObjective,
    "workexperience": WorkExperience,
    "projectexperience": ProjectExperience,
    "educationexperience": EducationExperience,
}


@class_view_decorator(login_required)
class ResumeDelete(View):
    def post(self, request, *args, **kwargs):
        result_dict = {"err": 0, "msg": ""}
        try:
            resume_type = self.kwargs.get("resume_type", "")
            pk_id = self.kwargs.get("pk", "")
            if resume_type and pk_id:
                resume_type_model = resume_type_model_dict.get(resume_type)
                resume_type_model.objects.filter(id=pk_id).delete()
            else:
                result_dict["err"] = 1
                result_dict["msg"] = "删除简历信息不完善，删除失败!"
        except:
            logging.getLogger().error(traceback.format_exc())
            result_dict["err"] = 1
            result_dict["msg"] = traceback.format_exc()
        finally:
            return HttpResponse(json.dumps(result_dict, ensure_ascii=False))


@class_view_decorator(login_required)
class ResumeAdd(View):
    def post(self, request, *args, **kwargs):
        result_dict = {"err": 0, "msg": "", "id": ""}
        try:
            resume_type = self.kwargs.get("resume_type", "")
            resume_info_dict = self.request.POST.get("resume_info_dict", {})
            resume_info_dict = eval(resume_info_dict)
            user_id = resume_info_dict.get("user_id")
            user_obj = User.objects.filter(id=user_id)
            if user_obj.exists() and resume_info_dict:
                resume_info_dict["user_id"] = user_obj[0]
                resume_type_model = resume_type_model_dict.get(resume_type)
                obj_id = resume_type_model.objects.create(**resume_info_dict)
                result_dict["id"] = obj_id.id
            else:
                result_dict["err"] = 1
                result_dict["msg"] = "未找到用户信息，新增失败!"
        except:
            logging.getLogger().error(traceback.format_exc())
            result_dict["err"] = 1
            result_dict["msg"] = traceback.format_exc()
        finally:
            return HttpResponse(json.dumps(result_dict, ensure_ascii=False))


@class_view_decorator(login_required)
class ResumeUpdate(View):
    def post(self, request, *args, **kwargs):
        result_dict = {"err": 0, "msg": ""}
        try:
            resume_type = self.kwargs.get("resume_type", "")
            pk_id = self.kwargs.get("pk", "")
            resume_info_dict = self.request.POST.get("resume_info_dict", {})
            resume_info_dict = eval(resume_info_dict)
            if resume_type and pk_id and resume_info_dict:
                resume_type_model = resume_type_model_dict.get(resume_type)
                resume_type_model.objects.filter(id=pk_id).update(**resume_info_dict)
            else:
                result_dict["err"] = 1
                result_dict["msg"] = "简历修改数据不完善，修改失败!"
        except:
            logging.getLogger().error(traceback.format_exc())
            result_dict["err"] = 1
            result_dict["msg"] = traceback.format_exc()
        finally:
            return HttpResponse(json.dumps(result_dict, ensure_ascii=False))
