FROM python:3.12

LABEL org.opencontainers.image.description A configurable router for Kafka messages.

RUN useradd \
    --comment "Kafka Router" \
    --home /home/router \
    --no-log-init \
    --create-home \
    --shell /usr/sbin/nologin \
    --user-group \
    router \
  && apt-get clean \
  && apt-get update \
  && apt-get --yes upgrade libaom3 libpq-dev libpq5 \
  && apt-get clean \
  && rm -rf /vaar/lib/apt/lists \
  && chmod 0700 /home/router

USER router

ENV KAFKA_ROUTER_PROMETHEUS_PORT=8000

WORKDIR /home/router
COPY --chown=router:router --chmod=0644 rule-schema.json /home/router/rule-schema.json
COPY --chown=router:router --chmod=0644 requirements.txt /home/router/requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt
COPY --chown=router:router --chmod=0755 router.py /home/router/router.py

CMD [ "/home/router/router.py" ]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "/usr/bin/sh", "-c", "curl --fail http://localhost:${KAFKA_ROUTER_PROMETHEUS_PORT}"]
