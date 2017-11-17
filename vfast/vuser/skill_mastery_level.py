#!encoding:utf-8
import logging

from vcourse.models import *
from vrecord.models import *


def statistics_skill_mastery_level_by_path(user_id, path_id):
    """
    根据用户ID，学习路线；汇总各个技能点的学习进度，用于页面嵌套环形图显示。
    :param user_id: 最终用户ID
    :param path_id: 学习路线ID
    :return:用于回显嵌套环形图的数据
    """
    result_dict = {
        "skill_name_data": [],  # 路线下所有技能点
        "undone_color_data": [],  # 技能点未完成底色
        "inner_ring_data": [],  # 内环技能点占比
        "outer_ring_data": [],  # 外环技能点完成占比
    }
    try:
        path_objs = Path.objects.filter(id=path_id)

        if path_objs.exists():
            skill_objs = Skill.objects.filter(path_id=path_id)
            course_objs = path_objs[0].course.all()  # 路线下所有课程

            skill_name_list = list(skill_objs.values_list("name", flat=True))
            result_dict["skill_name_data"] = [format_str(one) for one in skill_name_list]

            # 未完成课程图表底色
            result_dict["undone_color_data"] = ['#F0F2F4' for i in range(len(skill_name_list))]

            for one_skill in skill_objs:
                one_skill_weight = one_skill.weight
                one_skill_name = one_skill.name
                one_skill_undone_name = one_skill.name + ' Undone'

                section_objs = Section.objects.filter(course__in=course_objs, skill=one_skill_name)
                video_objs = Video.objects.filter(section__in=section_objs)

                total_count = video_objs.count()
                done_count = WatchRecord.objects.filter(video__in=video_objs, user_id=user_id, status=0).count()

                # 内环技能点占比
                result_dict["inner_ring_data"].append({"value": str(one_skill_weight), "name": format_str(one_skill_name)})

                # 外环技能点课程学习进度占比数据
                if total_count:
                    tmp_done = round(((total_count - done_count) / 1.0 / total_count) * one_skill_weight, 2)

                    result_dict["outer_ring_data"].append({"value": str(tmp_done), "name": format_str(one_skill_name)})
                    result_dict["outer_ring_data"].append(
                        {"value": str(one_skill_weight - tmp_done), "name": format_str(one_skill_undone_name)})
                else:
                    result_dict["outer_ring_data"].append({"value": 0, "name": format_str(one_skill_name)})
                    result_dict["outer_ring_data"].append(
                        {"value": str(one_skill_weight), "name": format_str(one_skill_undone_name)})
    except:
        logging.getLogger().error(traceback.format_exc())
        traceback.print_exc()
    finally:
        # print "skill_name_data==", result_dict["skill_name_data"]
        # print "undone_color_data==", result_dict["undone_color_data"]
        # print "inner_ring_data==", result_dict["inner_ring_data"]
        # print "outer_ring_data==", result_dict["outer_ring_data"]
        return result_dict


def format_str(str_param):
    try:
        str_param = str_param.encode('unicode-escape').decode('string_escape')
    except:
        traceback.print_exc()
        logging.getLogger().error(traceback.format_exc())
    finally:
        return str_param
