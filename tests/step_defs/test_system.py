"""System tests."""
import confluent_kafka
import testinfra_bdd
from pytest_bdd import given, parsers, scenarios, then, when

scenarios('../features/system.feature')


# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = testinfra_bdd.PYTEST_MODULES


@given('Kafka producer headers', target_fixture='producer_headers')
def _():
    """Kafka producer headers."""
    return []


@given(parsers.parse('Kafka producer message value is {message_value}'), target_fixture='message_value')
def _(message_value: str):
    """Kafka producer message value is <message_value>."""
    return message_value.encode()


@when(parsers.parse('Kafka producer header {header_key} is {header_value}'))
def _(header_key: str, header_value: str, producer_headers: list):
    """Kafka producer header <header_key> is <header_value>."""
    producer_headers.append((header_key, header_value))


@then(parsers.parse('Kafka producer should produce to {topic}'))
def _(topic: str, producer_headers: list, message_value: bytes):
    """Kafka producer should produce to <topic>."""
    config = {
        'bootstrap.servers': 'localhost:9092'
    }
    producer = confluent_kafka.Producer(config)
    producer.produce(topic, message_value, headers=producer_headers)
    producer.flush()
