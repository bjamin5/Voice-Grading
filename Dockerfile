# docker build . -t voicegrade
# docker run --name voicegrade -p 8080:8080 voicegrade

FROM python:3.9-slim
ENV USER 'app'
ENV UID '999'
ENV TINI_VERSION="v0.19.0"
ENV TZ 'America/Denver'
ENV PATH="/home/app/.local/bin:${PATH}"
ENV PROMETHEUS_MULTIPROC_DIR /dev/shm
ENV METRICS_PORT 8081
ENV VERSION=${VERSION}

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

WORKDIR /app

RUN apt update && \
    apt upgrade -y && \
    apt clean && rm -rf /var/lib/apt/lists/*  && \
    useradd -m -r $USER && \
    chown -R $USER:$USER /app && \
    echo $TZ > /etc/timezone && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

USER $USER

RUN python -m pip install -U \
    pip \
    setuptools

COPY --chown=$USER . /app

RUN pip install --no-cache-dir --user -r requirements.txt

EXPOSE 8080
EXPOSE 8081
ENTRYPOINT ["/tini", "--"]

CMD gunicorn -c gunicorn_config.py "server:create_app()"
