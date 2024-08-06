"""The KafkaRouter class. feature tests."""
import json
import os
import signal

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from router import KafkaRouter, KafkaRouterRule

scenarios('../features/kafka-router.feature')


@given(parsers.parse('a KafkaRouter with DLQ topic {dlq_topic}'), target_fixture='kafka_router')
def _(dlq_topic):
    """a KafkaRouter with DLQ topic <dlq_topic>."""
    if dlq_topic == 'None':
        dlq_topic = ''

    return KafkaRouter(dlq_topic)


@given(parsers.parse('consumer config to be validated is {config}'), target_fixture='consumer_config')
def _(config: str):
    """consumer config to be validated is <config>."""
    return json.loads(config)


@given('populated headers')
def _(kafka_router: KafkaRouter):
    """populated headers."""
    kafka_router.headers(
        [
            ('a', 1)
        ]
    )


@given(parsers.parse('System Signal is {signal_name}'), target_fixture='system_signal')
def _(signal_name: str):
    """System Signal is <signal>."""
    signal_map = {
        'SIGINT': signal.SIGINT,
        'SIGTERM': signal.SIGTERM
    }

    return signal_map[signal_name]


@when('System Signal is sent')
def _():
    """System Signal is sent."""
    pass


@when(parsers.parse('rule {rule} is added to the KafkaRouter'))
def _(rule: str, kafka_router: KafkaRouter):
    """rule <rule> is added to the KafkaRouter."""
    kafka_router.add_rule(
        KafkaRouterRule('KAFKA_ROUTER_RULE_TEST', rule)
    )


@when('the consumer config is validated')
def _():
    """the consumer config is validated."""
    pass


@when(parsers.parse('OS environment {key} is {value}'))
def _(key: str, value: str) -> None:
    """OS environment KAFKA_CONSUMER_CLIENT_ID is <kafka_consumer_client_id>."""
    if value == 'None' and key in os.environ:
        del os.environ[key]
    elif value != 'None':
        os.environ[key] = value


@when('new headers are appended')
def _(kafka_router: KafkaRouter):
    """new headers are appended."""
    kafka_router.upsert_header('a', 2)
    kafka_router.upsert_header('b', 3)


@then(parsers.parse('DLQ ID is {expected_value}'))
def _(expected_value: str, kafka_router: KafkaRouter):
    """DLQ ID is <expected_value>."""
    assert kafka_router.get_dlq_id() == expected_value


@then(parsers.parse('KafkaRouter source topics include {source_topic}'))
def _(source_topic: str, kafka_router: KafkaRouter):
    """KafkaRouter source topics include <source_topic>."""
    assert source_topic in kafka_router.source_topics


@then(parsers.parse('ValueError exception is raised is {is_true}'))
def _(is_true: str, consumer_config: dict):
    """ValueError exception is raised is <is_true>."""
    router = KafkaRouter(DLQ_topic_name='test.dlq')
    expected = is_true == 'True'

    try:
        router.validate_consumer_config(consumer_config)
        actual = False
    except ValueError:
        actual = True

    assert actual == expected


@then('headers count is two')
def _(kafka_router: KafkaRouter):
    """headers count is two."""
    headers = kafka_router.headers()
    assert len(headers) == 2


@then('KafkaRouter handler catches it')
def _(system_signal: int):
    """KafkaRouter handler catches it."""
    with pytest.raises(SystemExit) as exit_info:
        signal.raise_signal(system_signal)

    assert exit_info.value.code == 0
