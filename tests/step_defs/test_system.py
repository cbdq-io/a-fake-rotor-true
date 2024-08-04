"""System tests."""
import confluent_kafka
import testinfra_bdd
from pytest_bdd import given, parsers, scenarios, then, when

scenarios('../features/system.feature')


# Ensure that the PyTest fixtures provided in testinfra-bdd are available to
# your test suite.
pytest_plugins = testinfra_bdd.PYTEST_MODULES


def message_matches_headers(message: confluent_kafka.Message, header_name: str, header_value: str) -> bool:
    """
    Check if the message that matches the header criteria.

    Parameters
    ----------
    message : confluent_kafka.Message
        The message consumed.
    header_name : str
        The name of a header we're looking for in the headers.
    header_value : str
        The value the header must match.

    Returns
    -------
    bool
        True if the header is found and matches the specified value.  False otherwise.
    """
    headers = {key: value.decode() for key, value in message.headers()}
    print(f'Headers are "{headers}".')

    if header_name not in headers:
        return False

    return headers[header_name] == header_value


@given('Kafka producer headers', target_fixture='producer_headers')
def _():
    """Kafka producer headers."""
    return []


@given(parsers.parse('Kafka producer message value is {message_value}'), target_fixture='message_value')
def _(message_value: str):
    """Kafka producer message value is <message_value>."""
    return message_value.encode()


@given('a Kafka Consumer Config', target_fixture='kafka_consumer_config')
def _():
    """a Kafka Consumer Config."""
    return {}


@given(parsers.parse('the Kafka Topic Name is {topic_name}'), target_fixture='kafka_topic_name')
def _(topic_name: str) -> str:
    """the Kafka Topic Name is <topic_name>."""
    return topic_name


@when(parsers.parse('the Kafka Consumer Config Setting {key} is {value}'))
def _(key: str, value: str, kafka_consumer_config: dict) -> None:
    """the Kafka Consumer Config Setting auto.offset.reset is earliest."""
    kafka_consumer_config[key] = value


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


@then(parsers.parse('the Kafka Topic Contains a Message With a Header Called {header_name} Set to {header_value}'))
def _(header_name: str, header_value: str, kafka_topic_name: str, kafka_consumer_config: str):
    """the Kafka Topic Contains a Message With a Header Called <header_name> Set to <header_value>."""
    consumer = confluent_kafka.Consumer(kafka_consumer_config)
    message_found = False
    consumer.subscribe([kafka_topic_name])

    while not message_found:
        message = consumer.poll(timeout=1.0)

        if message is None:
            break

        print(f'Message value is "{message.value().decode("utf-8")}".')
        if message_matches_headers(message, header_name, header_value):
            message_found = True
            break

    consumer.close()
    message = f'No message found in the {kafka_topic_name} with a header "{header_name}" set to "{header_value}".'
    assert message_found, message
