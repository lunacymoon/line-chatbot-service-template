ARG ENV_ECR_URI

FROM ${ENV_ECR_URI}:python-build-image

WORKDIR /app
ADD . /app

RUN pip3 install -r requirements.txt

EXPOSE 8216
CMD python3 main.py
