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
        # 获取路线下所有技能点信息
        skill_objs = Skill.objects.filter(path_id=path_id)
        skill_name_list = list(skill_objs.values_list("name", flat=True))
        result_dict["skill_name_data"] = [one.encode('unicode-escape').decode('string_escape') for one in
                                          skill_name_list]

        # 未完成课程图表底色
        result_dict["undone_color_data"] = ['#F0F2F4' for i in range(len(skill_name_list))]

        # 外环技能点课程学习进度占比数据
        skill_dict = {}
        # 获取路线信息
        path_objs = Path.objects.filter(id=path_id)
        if path_objs.exists():
            course_objs = path_objs[0].course.all()  # 路线下所有课程
            for one_course in course_objs:
                section_objs = Section.objects.filter(course=one_course)
                for one_section in section_objs:
                    section_skill = one_section.skill
                    if section_skill in skill_name_list:  # 此章节包含需统计的技能点
                        # 获取该章节下所有的视频
                        video_objs = Video.objects.filter(section=one_section)

                        # 组装指定技能下视频观看进度
                        if not skill_dict.has_key(section_skill):
                            skill_dict[section_skill] = {"total": 0, "done": 0}  # 视频总数, 已完成
                        skill_dict[section_skill]["total"] += video_objs.count()

                        # 查找已完成数
                        done_count = WatchRecord.objects.filter(video__in=video_objs, user_id=user_id, status=0).count()
                        skill_dict[section_skill]["done"] += done_count

        for one_skill in skill_objs:
            one_skill_weight = one_skill.weight
            one_skill_name = one_skill.name
            one_skill_undone_name = one_skill.name + ' Undone'

            # 内环技能点占比
            result_dict["inner_ring_data"].append({"value": str(one_skill_weight),
                                                   "name": one_skill_name.encode('unicode-escape').decode(
                                                       'string_escape')})

            # 外环技能学习进度
            schedule_dict = skill_dict.get(one_skill_name, {})
            if not schedule_dict:  # 没有观看进度，全部未完成
                result_dict["outer_ring_data"].append(
                    {"value": 0, "name": one_skill_name.encode('unicode-escape').decode('string_escape')})
                result_dict["outer_ring_data"].append({"value": str(one_skill_weight),
                                                       "name": one_skill_undone_name.encode('unicode-escape').decode(
                                                           'string_escape')})
            else:
                total = schedule_dict.get("total", 0)
                done = schedule_dict.get("done", 0)
                tmp_done = round(((total - done) / 1.0 / total) * one_skill_weight, 2)
                result_dict["outer_ring_data"].append({"value": str(tmp_done),
                                                       "name": one_skill_name.encode('unicode-escape').decode(
                                                           'string_escape')})
                result_dict["outer_ring_data"].append({"value": str(one_skill_weight - tmp_done),
                                                       "name": one_skill_undone_name.encode('unicode-escape').decode(
                                                           'string_escape')})
    except:
        logging.getLogger().error(traceback.format_exc())
        traceback.print_exc()
    finally:
        # print "skill_name_data==", result_dict["skill_name_data"]
        # print "undone_color_data==", result_dict["undone_color_data"]
        # print "inner_ring_data==", result_dict["inner_ring_data"]
        # print "outer_ring_data==", result_dict["outer_ring_data"]
        return result_dict
