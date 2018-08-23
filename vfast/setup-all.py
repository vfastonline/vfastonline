# coding:utf-8
import os


def install_conda():
	os.system("sh ../Anaconda2-5.2.0-Linux-x86_64.sh")


def make_conda_env():
	os.system("conda create -n vfastonline python=2.7")
	os.system("source activate vfastonline")
	os.system("pip install -U pip")


def install_vfast_setup():
	os.system("tar -zxvf vfast-1.0.tar.gz -C /usr/local/vfastonline/vfast -O > vfast")
	os.system("mv /usr/local/vfastonline/vfast-1.0 /usr/local/vfastonline/vfast")
	os.system("python /usr/local/vfastonline/vfast/setup.py build")
	os.system("python /usr/local/vfastonline/vfast/setup.py install")


def install_uwsgi():
	os.system("conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/")
	os.system("conda config --set show_channel_urls yes")
	os.system("conda install --channel https://conda.anaconda.org/conda-forge -n vfastonline uwsgi")


def install_nginx():
	os.system("conda install -n vfastonline nginx")


def mv_uwsgi_nginx_config():
	pass


def install_all():
	install_conda()
	make_conda_env()
	install_vfast_setup()
	install_uwsgi()
	install_nginx()
	mv_uwsgi_nginx_config()


if __name__ == "__main__":
	install_all()
