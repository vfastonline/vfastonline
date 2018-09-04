# vfastonline

### 配置文件
* vfast/vfast.conf

### 安装部署
```
git clone https://github.com/vfastonline/vfastonline.git
cd vfastonline 
git checkout dev
pip install -r vfast/requirements.txt

安装mysql数据库
username:root，password:111111

初始化数据库
python vfast/manege.py makemigrations
python vfast/manege.py migrate

创建超级管理员
python vfast/manege.py creatsuperuser

网站服务
python manege.py runserver 0.0.0.0:8000
```

### Architecture
* git, django, python, mysql

# 项目目录结构
oauth:github auth登陆，获取账号相关信息，项目信息
templates:前端模版文件.
top:第三方接口。
vbadge:
vcompany:
vcourse:
vfast:
vinform:
vinspect:
vperm:
vpractice:
vrecord:
vuser:


# vfastonline
定时任务
每日邮件推送
生成用户通知,  新课程发布通知     接口   /info/create_info
生成学习任务,  新建学习任务推送   接口   /info/studyplan                每天凌晨三点执行

