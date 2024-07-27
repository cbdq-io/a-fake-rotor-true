FROM python:3.12

RUN useradd \
    --comment "Kafka Router" \
    --home /home/router \
    --no-log-init \
    --create-home \
    --shell /usr/sbin/nologin \
    --user-group \
    router \
  && chmod 0700 /home/router

USER router
WORKDIR /home/router
COPY --chown=router:router --chmod=0644 requirements.txt /home/router/requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt
COPY --chown=router:router --chmod=0755 router.py /home/router/router.py
