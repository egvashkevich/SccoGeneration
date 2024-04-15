FROM python:3.10

#ARG PROJECT_ROOT=project_root
ENV SERVICE_DIR=/data_preprocessing

RUN mkdir ${SERVICE_DIR}
COPY . ${SERVICE_DIR}
WORKDIR ${SERVICE_DIR}

RUN pip3 install -r requirements.txt

# Installation
# ENTRYPOINT or CMD to run service. Link to their difference:
# https://docs.docker.com/reference/dockerfile/#understand-how-cmd-and-entrypoint-interact
ENTRYPOINT python3 data_preprocessing.py
