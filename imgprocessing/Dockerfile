FROM centos/python-36-centos7

USER root

RUN yum install -y cmake
RUN pip install celery
RUN pip install face_recognition
RUN pip install requests
RUN pip install flower

COPY entrypoint.py entrypoint.py
COPY lfw.py lfw.py
COPY task.py task.py
