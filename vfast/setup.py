# coding:utf-8
# package project

from setuptools import setup, find_packages

requires = [
	'django==1.10.5',
	'Pillow',
	'MySQL-python',
	'Django-Select2==5.11.1',
	'django-suit',
	'django-colorfield',
	'requests'
]

setup(
	name="vfast",
	version="1.0",

	author="xuhuiliang",
	author_email="593548215@qq.com",

	# 自动寻找带有 __init__.py 的文件夹
	packages=find_packages(exclude=["logs"]),

	install_requires=requires,

	description="vfast",

	# 单独的一些py脚本,不是在某些模块中
	scripts=["manage.py"],

	# 静态文件等，配合MANIFEST.in (package_data 参数不太好使)
	include_package_data=True,

	# 如果是正式的项目，还会有更多的信息（例如开源证书写在下面）
	# url="http://wifi21.com",
)
