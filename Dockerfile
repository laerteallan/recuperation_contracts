FROM python:3.12.6-alpine
RUN  apk add --no-cache --update bash libxslt libxslt-dev libffi-dev linux-headers alpine-sdk build-base gcc postgresql-dev bash
ARG DEPLOY_PATH='/home/deploy/contracts'
RUN mkdir -p $DEPLOY_PATH
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY recuperation_contracts $DEPLOY_PATH/recuperation_contracts
RUN pip install -r $DEPLOY_PATH/recuperation_contracts/requirements.txt
WORKDIR $DEPLOY_PATH/recuperation_contracts
CMD ["python", "manage.py", "runserver"]
