## 远程部署步骤
                                                                                                                                                                                   
```
* python setup.py sdist
* mv dist/vfast-1.0.tar.gz doc/vfast_install/
* rm  vfastonline/vfast/dist
* vim doc/install.sh 
    * 修改：SERVERS，123456； SERVERS可用空格分隔填写多个，例：SERVERS="127.0.0.1 127.0.0.2"
* sh install.sh
```

### NGINX:
```
/usr/local/openresty/nginx/conf/nginx.conf 添加include servers/*.conf;
/usr/local/openresty/nginx/conf/servers/m.conf   nginx配置文件
```

### UWSGI:
```
/etc/init.d/uwsgi
```

### rc.local

```
/usr/local/openresty/nginx/sbin/nginx
sh /etc/init.d/uwsgi stop       
sh /etc/init.d/uwsgi start
```

### 文件说明
```
media  课程视频文件
vfast.sql  数据库备份文件
deploy.sh   服务器部署各个服务脚本
install.sh  远程部署脚本
uwsgi   uwsgi服务启动停止脚本
m.conf  nginx配置文件
openresty_repo  yum源配置文件
vfast-1.0.tar.gz    网站安装包
```