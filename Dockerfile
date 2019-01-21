FROM ubuntu:16.04

MAINTAINER David Lohle "Proplex@users.noreply.github.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev git

RUN git clone https://github.com/proplex/depchecker.git

WORKDIR /depchecker

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]