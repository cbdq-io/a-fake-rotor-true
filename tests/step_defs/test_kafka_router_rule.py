"""Kafka Router Rule feature tests."""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

import router


class MockConfluentKafkaMessage:
    """
    Provide an API that is compatible with the Confluent Kafka Message.

    Parameters
    ----------
    value : object, optional
        The value of the string.  Will be encoded and stored as bytes, by default None
    topic : str, optional
        The topic name, by default None
    headers : list, optional
        A list of tuples to set as headers, by default None
    """

    def __init__(self, value: object = None, topic: str = None, headers: list = []) -> None:
        self._value = None
        self._topic = None
        self._headers = []
        self._partition = 0
        self._offset = 0
        self.value(value)
        self.topic(topic)

    def append_header(self, key: str, value: str) -> None:
        """
        Append a header.

        Parameters
        ----------
        key : str
            The key of the header.
        value : str
            The value of the header.
        """
        headers = self.headers()
        headers.append(
            (
                key,
                value.encode()
            )
        )
        self.headers(headers)

    def headers(self, headers: list = None) -> list:
        """
        Get or set the headers of the message.

        Parameters
        ----------
        headers : list, optional
            If not None, set the headers, by default None

        Returns
        -------
        list
            The headers of the message.
        """
        if headers is not None:
            self._headers = headers

        return self._headers

    def offset(self, offset: int = None) -> int:
        """
        Get or set the offset.

        Parameters
        ----------
        offset : int, optional
            If provided, set the offset to this value.

        Returns
        -------
        int
            The offset of the message.
        """
        if offset is not None:
            self._offset = offset

        return self._offset

    def partition(self, partition: int = None) -> int:
        """
        Get or set the partition.

        Parameters
        ----------
        partition : int, optional
            The partition number, by default None

        Returns
        -------
        int
            The partition number.
        """
        if partition is not None:
            self._partition = partition

        return self._partition

    def topic(self, topic: str = None) -> str:
        """
        Get or set the topic name.

        Parameters
        ----------
        topic : str, optional
            If not None, set the topic name, by default None

        Returns
        -------
        str
            The topic name.
        """
        if topic is not None:
            self._topic = topic

        return self._topic

    def value(self, value: object = None) -> bytes:
        """
        Get or set the value of the message.

        Parameters
        ----------
        value : object, optional
            The value to set the message to if not None, by default None

        Returns
        -------
        bytes
            The value of the message.
        """
        if value is not None:
            if type(value) is str:
                self._value = value.encode('utf-8')
            else:
                self._value = value

        return self._value


scenarios('../features/kafka-router-rule.feature')


@given(parsers.parse('a Kafka Router Rule of {rule}'), target_fixture='kafka_router_rule')
def _(rule: str):
    """a Kafka Router Rule of <rule>."""
    return router.KafkaRouterRule('test', rule)


@given('a KafkaRouter with DLQ topic "dlq_topic"', target_fixture='kafka_router')
def _():
    """a KafkaRouter with DLQ topic "dlq_topic"."""
    return router.KafkaRouter('dlq_topic')


@given(parsers.parse('a message with a value of {message_value}'), target_fixture='mock_confluent_message')
def _(message_value: str):
    """a message with a value of <message_value>."""
    message = MockConfluentKafkaMessage(message_value)
    message.topic('input')
    return message


@given(parsers.parse('an Invalid Kafka Router Rule of {rule}'), target_fixture='invalid_rule')
def _(rule: str):
    """an Invalid Kafka Router Rule of <rule>."""
    return rule


@given(parsers.parse('with message topic {topic}'))
def _(topic: str, mock_confluent_message: MockConfluentKafkaMessage):
    """with message topic <topic>."""
    mock_confluent_message.topic(topic)


@when(parsers.parse('append message header {key} with value {value}'))
def _(key: str, value: str, mock_confluent_message: MockConfluentKafkaMessage):
    """append message header status with value TEST."""
    mock_confluent_message.append_header(key, value)


@when('the message is checked')
def _():
    """the message is checked."""
    pass


@when('the rule is initialised')
def _():
    """the rule is initialised."""
    pass


@then(parsers.parse('message is a match is {expected_outcome}'))
def _(expected_outcome: str, mock_confluent_message: MockConfluentKafkaMessage,
      kafka_router_rule: router.KafkaRouterRule):
    """message is a match is <expected_outcome>."""
    expected_outcome = expected_outcome == 'True'
    actual_outcome = kafka_router_rule.is_match(mock_confluent_message)
    assert actual_outcome == expected_outcome


@then('the SystemExit is 2')
def _(invalid_rule: str):
    """the SystemExit is 2."""
    with pytest.raises(SystemExit) as exit_info:
        router.KafkaRouterRule('test', invalid_rule)

    assert exit_info.value.code == 2
