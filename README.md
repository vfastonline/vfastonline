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