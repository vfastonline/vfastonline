#!encoding:utf-8
import logging
import time

from django.http import HttpResponseRedirect

from vcourse.api import course_process
from vcourse.models import *
from vfast.api import require_login
from vfast.error_page import *
from vrecord.models import WatchRecord


# Create your views here.
def test(request):
	w = WatchRecord.objects.filter(id=1).values('user__username')
	from vpractice.models import Replay
	r = Replay.objects.filter(id=1).values('question__user__username')
	return render(request, "search_Result.html")


def getpath(request):
	"""
	获取学习路线详细信息, 学习路线下包含的所有课程
	path为path对象, courseall包含所有的course对象
	"""
	result_dict = dict()
	try:
		pid = request.GET.get('id')  # 学习路线ID
		path = Path.objects.get(id=pid)
		courses_obj_list, courses_dict_list = path.get_after_sorted_course()  # 路线中所有课程

		courses_list = []
		for one_course in courses_obj_list:
			videos = Video.objects.filter(course=one_course).order_by('sequence').values()
			courses_list.append(dict(course=one_course, video=videos))

		# 获取用户现有学习路线，如果没有页面显示切换路线
		try:
			uid = request.session['user']['id']
			path_id = User.objects.get(id=uid).pathid
		except:
			path_id = 0

		result_dict["path"] = path
		result_dict["path_id"] = path_id
		result_dict["courses"] = courses_list
		result_dict["xingxing"] = [0, 1, 2, 3, 4]
		return render(request, 'learnPath_show.html', result_dict)
	except:
		logging.getLogger().error(traceback.format_exc())
		return page_not_found(request)


def getcourses(request):
	"""获取所有的课程"""
	try:
		type = request.GET.get('type', None)
		vps = Technology.objects.all().values()
		if type:
			techobj = Technology.objects.get(name=type)
			pubs = Course.objects.filter(tech=techobj, pubstatus=0).values('id', 'name', 'desc', 'totaltime',
																		   'difficult', 'icon', 'color', 'tech__color',
																		   'tech__name')
			not_pubs = Course.objects.filter(tech=techobj, pubstatus=1).values('id', 'name', 'desc', 'totaltime',
																			   'difficult', 'icon', 'color',
																			   'tech__color', 'tech__name', 'pubdate')
		else:
			techobj = ''
			pubs = Course.objects.filter(pubstatus=0).values('id', 'name', 'desc', 'totaltime', 'difficult', 'icon',
															 'color', 'tech__color', 'tech__name')
			not_pubs = Course.objects.filter(pubstatus=1).values('id', 'name', 'desc', 'totaltime', 'difficult', 'icon',
																 'color', 'tech__color', 'tech__name', 'pubdate')
		return render(request, 'course_library.html',
					  {'pubs': pubs, 'not_pubs': not_pubs, 'vps': vps, 'tech_obj': techobj,
					   'xingxing': [0, 1, 2, 3, 4]})
	except:
		logging.getLogger().error(traceback.format_exc())
		# return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))
		return page_not_found(request)


def getpaths(request):
	"""获取所有的路线"""
	try:
		paths = Path.objects.all()
		return render(request, 'learning_path.html', {'paths': paths})
	except:
		logging.getLogger().error(traceback.format_exc())
		# return HttpResponse(json.dumps({'code': 128}, ensure_ascii=False))
		return page_not_found(request)


@require_login()
def join_path(request):
	try:
		pid = request.GET.get('pid')
		uid = request.session['user']['id']
		user = User.objects.get(id=uid)
		path = Path.objects.get(id=pid)
		courses, courses_values = path.get_after_sorted_course()
		User.objects.filter(id=uid).update(pathid=pid)
		if UserPath.objects.filter(user=user, path=path).exists():
			video = WatchRecord.objects.filter(user=user, course__in=courses).order_by('-createtime').values(
				'video_id', 'video__vtype', 'createtime').first()
			logging.getLogger().info(video)
			if video:
				url = '/video/%s' % video['video_id'] if video['video__vtype'] == 0 else '/practice/%s' % video[
					'video_id']
			else:
				video = Video.objects.filter(course=courses[0], sequence=1).values('vtype', 'id').first()
				url = '/video/%s' % video['id'] if video['vtype'] == 0 else '/practice/%s' % video['id']
			return HttpResponseRedirect(url)
		else:
			t = time.strftime('%Y-%m-%d %H:%M:%S')
			UserPath.objects.create(user=user, path=path, createtime=t)
			video = Video.objects.filter(course=courses[0], sequence=1).values('vtype', 'id').first()
			url = '/video/%s' % video['id'] if video['vtype'] == 0 else '/practice/%s' % video['id']
			return HttpResponseRedirect(url)
	except:
		logging.getLogger().error(traceback.format_exc())
		return page_error(request)


def course_detail(request):
	try:
		cid = request.GET.get('cid')
		course = Course.objects.get(id=cid)
		sections = Section.objects.filter(course=course).values()  # 课程下面所有的章节
		videos_course = Video.objects.filter(course_id=cid).count()  # 课程下所有的视频
		try:
			uid = request.session['user']['id']
			jindu, c_jindu = course_process(uid, cid)
			# 课程下面用户观看完成的视频
			videos_watched = WatchRecord.objects.filter(course_id=cid, user_id=uid, status=0).values('status',
																									 'video_id',
																									 'createtime')
			for section in sections:
				videos_section = Video.objects.filter(section_id=section['id']).order_by('sequence').values()
				tmp = 0
				for v_section in videos_section:  # video_section
					for v_watched in videos_watched:  # video_watched
						if v_section['id'] == v_watched['video_id'] and v_watched['status'] == 0:
							v_section['status'] = v_watched['status']
							tmp += 1
							break
					if not v_section.has_key('status'):
						v_section['status'] = 2
					section['videos'] = videos_section
					if tmp / videos_section.count() == 1:
						section['process'] = u'已完成'
					else:
						section['process'] = '%s/%s' % (tmp, videos_section.count())
			video = WatchRecord.objects.filter(course_id=cid, user_id=uid).order_by('-createtime').values('video_id',
																										  'video__vtype',
																										  'createtime').first()
			if video and jindu != "100.00%":
				url = '/video/%s' % video['video_id'] if video['video__vtype'] == 0 else '/practice/%s' % video[
					'video_id']
			elif jindu == '100.00%':
				url = ""  # 课程问卷调查的URL
			else:
				v = Video.objects.filter(course_id=cid, sequence=1).values().first()  # 如果课程下面没有视频会抛出异常
				try:
					url = '/video/%s' % v['id'] if v['vtype'] == 0 else '/practice/%s' % v['id']
				except:
					url = "#"

			return render(request, 'course_detail.html', {'sections': sections, 'course': course,
														  'course_process': c_jindu, 'url': url,
														  'xingxing': [0, 1, 2, 3, 4], 'jindu': jindu})
		except KeyError:
			traceback.print_exc()
			for section in sections:
				videos_section = Video.objects.filter(section_id=section['id']).order_by('sequence')
				section['videos'] = videos_section
				section['process'] = '0/%s' % videos_section.count()
			return render(request, 'course_detail.html',
						  {'sections': sections, 'course': course, 'course_process': '0/%s' % videos_course,
						   'xingxing': [0, 1, 2, 3, 4], 'jindu': '0%'})
	except:
		traceback.print_exc()
		logging.getLogger().error(traceback.format_exc())
		return page_not_found(request)


def lobby_live(request):
	try:
		vps = Technology.objects.all().values()
		return render(request, 'lobby_live.html', {'vps': vps})
	except:
		logging.getLogger().error(traceback.format_exc())
		return page_not_found(request)
