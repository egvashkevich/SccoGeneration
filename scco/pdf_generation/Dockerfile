FROM python:3.10

#ARG PROJECT_ROOT=project_root
ENV SERVICE_DIR=/pdf_generation

RUN mkdir ${SERVICE_DIR}
COPY . ${SERVICE_DIR}
WORKDIR ${SERVICE_DIR}

# Installation
# ENTRYPOINT or CMD to run service. Link to their difference:
# https://docs.docker.com/reference/dockerfile/#understand-how-cmd-and-entrypoint-interact
