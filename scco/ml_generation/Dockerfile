FROM python:3.10

#ARG PROJECT_ROOT=project_root
ENV SERVICE_DIR=/ml_generator

RUN mkdir ${SERVICE_DIR}
COPY src/* ${SERVICE_DIR}
WORKDIR ${SERVICE_DIR}

RUN pip3 install -r ${SERVICE_DIR}/requirements.txt
