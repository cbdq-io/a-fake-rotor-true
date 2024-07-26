FROM python:3.12

RUN useradd \
    --comment "Kafka Router" \
    --home /home/kr \
    --no-log-init \
    --create-home \
    --shell /usr/sbin/nologin \
    --user-group \
    kr

USER kr
WORKDIR /home/kr
COPY --chown=kr:kr --chmod=0644 requirements.txt /home/kr/requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt
COPY --chown=kr:kr --chmod=0755 router.py /home/kr/router.py
