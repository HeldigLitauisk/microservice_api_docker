FROM python:3.7.4-alpine3.10

RUN mkdir /code
WORKDIR /code
ADD . /code/

COPY requirements.txt .
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
RUN pip install connexion[swagger-ui]

EXPOSE 8080
CMD ["python", "/code/app.py"]