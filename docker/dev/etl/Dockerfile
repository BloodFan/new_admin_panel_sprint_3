FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/opt/etl

ARG GID=1000
ARG UID=1000
ARG USER=ubuntu

RUN apk add --update --no-cache python3-dev postgresql-dev curl && \
    addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID" && \
    mkdir -p /redis_socket && \
    chmod -R 777 /redis_socket && \
    chown -R $USER:$USER /redis_socket

WORKDIR $APP_HOME

COPY --chown=$USER:$USER ./etl $APP_HOME
COPY --chown=$USER:$USER ./requirements.txt $APP_HOME/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

USER $USER

CMD ["python", "main.py"]