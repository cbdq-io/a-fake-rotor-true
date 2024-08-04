"""Kafka Router Rule feature tests."""

import pytest
from pytest_bdd import given, parsers, scenario, then, when

import router


class MockMessage():
    """A mock class as a stand in for a Kafka Message."""

    def __init__(self, value: str) -> None:
        self.value(value.encode())

    def topic(self, topic: str = None) -> str:
        """
        Get or set the topic name.

        Parameters
        ----------
        topic : str, optional
            Set the topic name, by default None

        Returns
        -------
        str
            The topic name.
        """
        if topic is not None:
            self._topic = topic

        return self._topic

    def value(self, value: bytes = None) -> bytes:
        """
        Get or set the message value.

        Parameters
        ----------
        value : bytes, optional
            Set the class value, by default None

        Returns
        -------
        bytes
            The class value.
        """
        if value is not None:
            self._value = value

        return self._value


@scenario('../features/kafka-router-rule.feature', 'Test How a Message Will Be Routed')
def test_test_how_a_message_will_be_routed():
    """Test How a Message Will Be Routed."""


@scenario('../features/kafka-router-rule.feature', 'Rule Exceptions')
def test_rule_exceptions():
    """Rule Exceptions."""


@given(parsers.parse('a Kafka Router Rule of {rule}'), target_fixture='kafka_router_rule')
def _(rule: str):
    """a Kafka Router Rule of <rule>."""
    return router.KafkaRouterRule('test', rule)


@given('a KafkaRouter with DLQ topic "dlq_topic"', target_fixture='kafka_router')
def _():
    """a KafkaRouter with DLQ topic "dlq_topic"."""
    return router.KafkaRouter('dlq_topic')


@given(parsers.parse('a message with a value of {message_value}'), target_fixture='message')
def _(message_value: str):
    """a message with a value of <message_value>."""
    message = MockMessage(message_value)
    message.topic('input')
    return message


@given(parsers.parse('an Invalid Kafka Router Rule of {rule}'), target_fixture='invalid_rule')
def _(rule: str):
    """an Invalid Kafka Router Rule of <rule>."""
    return rule


@when('the message is checked')
def _():
    """the message is checked."""
    pass


@when('the rule is initialised')
def _():
    """the rule is initialised."""
    pass


@then(parsers.parse('message is a match is {expected_outcome}'))
def _(expected_outcome: str, message: MockMessage, kafka_router_rule: router.KafkaRouterRule):
    """message is a match is <expected_outcome>."""
    expected_outcome = expected_outcome == 'True'
    actual_outcome = kafka_router_rule.match_message(message)
    assert actual_outcome == expected_outcome


@then('the SystemExit is 2')
def _(invalid_rule: str):
    """the SystemExit is 2."""
    with pytest.raises(SystemExit) as exit_info:
        router.KafkaRouterRule('test', invalid_rule)

    assert exit_info.value.code == 2
