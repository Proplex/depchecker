FROM python:3.6-alpine

MAINTAINER David Lohle "Proplex@users.noreply.github.com"

COPY . /depchecker

WORKDIR /depchecker

RUN pip install -r requirements.txt

CMD ["python", "app.py"]