FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/opt/django_app


ARG GID=1000
ARG UID=1000
ARG USER=ubuntu

RUN apk add --update --no-cache python3-dev postgresql-dev curl nginx gettext && \
    addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID" && \
    mkdir -p /gunicorn_socket && \
    chmod -R 755 /gunicorn_socket && \
    chown -R $USER:$USER /gunicorn_socket

WORKDIR $APP_HOME

COPY --chown=$USER:$USER ./docker/dev/django_app/entrypoints/entrypoint.sh /
COPY ./docker/dev/nginx/conf.d /etc/nginx/conf.d
COPY ./docker/dev/nginx/nginx.conf /etc/nginx/nginx.conf
COPY --chown=$USER:$USER ./django_app $APP_HOME

RUN pip install --upgrade pip setuptools && \
    pip install --editable .[prod]


RUN chmod +x /*.sh && \
    mkdir -p media && \
    python manage.py collectstatic --no-input && \
    chown -R $USER:$USER $APP_HOME media && \
    chown -R $USER:$USER /etc/nginx /var/lib/nginx/ /var/log /run/nginx/

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "example.asgi:application"]

EXPOSE 8000

USER $USER