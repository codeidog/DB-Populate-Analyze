FROM python:3.9.1
ENV DB_SERVER=
ENV DB_NAME=
ENV DB_USER=
ENV DB_PWD=
#Install dependencies
RUN mkdir /opt/dbpopulator
COPY requirements.txt /opt/dbpopulator
RUN pip3 install -r /opt/dbpopulator/requirements.txt

#Copy the binaries
COPY bin /opt/minidetctor
WORKDIR /opt/minidetctor

ENTRYPOINT [ "main.py" ]
