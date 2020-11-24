.ONESHELL :

SHELL= /bin/bash
CONDAROOT = /opt/anaconda3


create:
# 		source $(CONDAROOT)/bin/activate;
		conda config --prepend channels conda-forge;
		conda create -n CS520-InfinityEleNa --strict-channel-priority osmnx;

install:
# 		source $(CONDAROOT)/bin/activate;
		pip install django;
		pip install django-cors-headers;
		pip install django_nose;
