FROM python:3.12-alpine
LABEL maintainer="solopdev.com"

ENV PYTHONUNBUFFERED=1
ENV PATH="/py/bin:$PATH"

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt


ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
        fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps 

COPY ./app /app
WORKDIR /app

EXPOSE 8000

RUN adduser --disabled-password --no-create-home user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R user:user /vol && \
    chmod -R 755 /vol

USER user

#CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]