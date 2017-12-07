# coding=utf-8
import logging

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from vcourse.models import *


@receiver(post_migrate)
def migrate_path_course_info(sender, **kwargs):
    """学习路线增加包含课程字段，增加路线下课程顺序表，
    将学习路线下现有课程顺序迁移到上述数据表中
    :param sender:
    :param kwargs:
    :return:
    """
    try:
        if sender.name == "vcourse":
            all_path = Path.objects.all()
            for one_path in all_path:
                p_sequence_list = one_path.p_sequence.split(",")
                if p_sequence_list:
                    course_id_list = map(int, p_sequence_list)
                    index = 1

                    # 迁移path.course字段中课程信息到PathCourseOrder顺序表
                    courses = one_path.course.all()
                    if courses.exists():
                        for one_course in courses:
                            pathcourseorders = PathCourseOrder.objects.filter(path=one_path) \
                                .order_by("-sequence_number")
                            if pathcourseorders.exists():
                                index = pathcourseorders.first().sequence_number + 1
                            if not PathCourseOrder.objects.filter(path=one_path, course=one_course).exists():
                                PathCourseOrder.objects.get_or_create(path=one_path, course=one_course,
                                                                  sequence_number=index)
                    # 迁移p_sequence顺序字段中课程信息
                    for course_id in course_id_list:
                        course_obj = Course.objects.filter(id=course_id)
                        if course_obj.exists() and not one_path.course.filter(id=course_id).exists():
                            one_path.course.add(course_obj.first())
                            pathcourseorders = PathCourseOrder.objects.filter(path=one_path) \
                                .order_by("-sequence_number")
                            if pathcourseorders.exists():
                                index = pathcourseorders.first().sequence_number + 1
                            if not PathCourseOrder.objects.filter(path=one_path, course=course_obj.first()).exists():
                                PathCourseOrder.objects.get_or_create(path=one_path, course=course_obj.first(),
                                                                  sequence_number=index)
                            index += 1
    except:
        logging.getLogger().error(traceback.print_exc())
        traceback.print_exc()
