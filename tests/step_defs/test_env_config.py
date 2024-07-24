"""Environment Config feature tests."""

import os

from pytest_bdd import given, parsers, scenario, then, when

from router import EnvironmentConfig


@scenario('../features/env-config.feature', 'Kafka Consumer')
def test_kafka_consumer():
    """Kafka Consumer."""


@given('an EnvironmentConfig object', target_fixture='environment_config')
def _():
    """an EnvironmentConfig object."""
    return EnvironmentConfig()


@given(parsers.parse('the EnvironmentConfig prefix setting is {prefix}'), target_fixture='environment_config_prefix')
def _(prefix: str):
    """the EnvironmentConfig prefix is <prefix>."""
    return prefix


@when(parsers.parse('the environment variable {key} is set to {value}'))
def _(key: str, value: str):
    """the environment variable <key> is set to <value>."""
    os.environ[key] = value


@then(parsers.parse('config {config_key} has a value of {value}'))
def _(config_key: str, value: str, environment_config: EnvironmentConfig, environment_config_prefix: str):
    """config <config_key> has a value of <value>."""
    config = environment_config.get_config(environment_config_prefix)
    assert config[config_key] == value
