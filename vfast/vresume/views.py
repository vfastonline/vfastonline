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
    context_object_name = "Resume"
    template_name = ""
    pk_url_kwarg = "id"
    model = Resume

    def get_context_data(self, **kwargs):
        try:
            user_id = self.kwargs.get("id")
            kwargs["CareerObjective"] = CareerObjective.objects.filter(user_id=user_id)
            kwargs["WorkExperience"] = WorkExperience.objects.filter(user_id=user_id)
            kwargs["ProjectExperience"] = ProjectExperience.objects.filter(user_id=user_id)
            kwargs["EducationExperience"] = EducationExperience.objects.filter(user_id=user_id)
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
            resume_type_model = resume_type_model_dict.get(resume_type)
            if resume_type_model:
                resume_type_model.objects.filter(id=pk_id).delete()
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
            if user_obj.exists():
                resume_info_dict["user_id"] = user_obj[0]
                resume_type_model = resume_type_model_dict.get(resume_type)
                obj_id = resume_type_model.objects.create(**resume_info_dict)
                result_dict["id"] = obj_id.id
            else:
                result_dict["err"] = 1
                result_dict["msg"] = u"未找到用户信息"
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
            resume_type_model = resume_type_model_dict.get(resume_type)
            resume_type_model.objects.filter(id=pk_id).update(**resume_info_dict)
        except:
            logging.getLogger().error(traceback.format_exc())
            result_dict["err"] = 1
            result_dict["msg"] = traceback.format_exc()
        finally:
            return HttpResponse(json.dumps(result_dict, ensure_ascii=False))
