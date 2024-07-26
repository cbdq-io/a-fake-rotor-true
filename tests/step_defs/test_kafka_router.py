"""The KafkaRouter class. feature tests."""
import json

from pytest_bdd import given, parsers, scenario, then, when

from router import KafkaRouter


@scenario('../features/kafka-router.feature', 'Validate Consumer Config')
def test_validate_consumer_config():
    """Validate Consumer Config."""


@given(parsers.parse('consumer config to be validated is {config}'), target_fixture='consumer_config')
def _(config: str):
    """consumer config to be validated is <config>."""
    return json.loads(config)


@when('the consumer config is validated')
def _():
    """the consumer config is validated."""
    pass


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
