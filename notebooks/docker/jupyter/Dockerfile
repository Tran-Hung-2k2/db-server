FROM jupyter/minimal-notebook

COPY ./notebooks/requirements.txt /tmp/requirements.txt
USER root
RUN sudo apt-get update && sudo apt-get install -y iputils-ping net-tools
RUN pip install -r /tmp/requirements.txt