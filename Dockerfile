FROM ubuntu:16.04

MAINTAINER Pushyami Gundala <pushyami@umich.edu>

RUN apt-get update \
	&& apt-get install -y vim python python-pip git

# create place for app to run from
WORKDIR /app/

COPY . /app/

RUN pip install -r requirements.txt

CMD ["python", "groupsforsections.py"]