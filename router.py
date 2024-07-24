#!/usr/bin/env python
"""
A configurable router for Kafka messages.

For detailed documentation, see
<https://github.com/cbdq-io/a-fake-rotor-true/blob/main/README.md>.
"""
import logging
import os
import sys

PROG = os.path.basename(sys.argv[0]).removesuffix('.py')
logging.basicConfig()
logger = logging.getLogger(PROG)
log_level = os.getenv('LOG_LEVEL', 'WARN')
logger.setLevel(log_level)
logger.debug(f'Log level has been set to "{log_level}".')

RULE_SCHEMA = """
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "source_topic": {
      "type": "string"
    },
    "destination_topic": {
      "type": "string"
    },
    "regexp": {
      "type": "string"
    },
    "jmespath": {
      "type": "string"
    }
  },
  "required": [
    "source_topic",
    "destination_topic",
    "regexp"
  ]
}
"""

__version__ = '0.1.0'


class EnvironmentConfig:
    """Extract configuration from environment variables."""

    def get_config(self, prefix: str) -> dict:
        """
        Extract configuration from the environment variables.

        Parameters
        ----------
        prefix : str
            The prefix to identify the relevant environment variables
            (e.g. KAFKA_CONSUMER_).

        Returns
        -------
        dict
            A dictionary containing the keys and values of the configuration.
        """
        response = {}

        for key in sorted(os.environ):
            if key.startswith(prefix):
                value = os.environ[key]
                message = f'Converted "{key}" to '
                key = key.removeprefix(prefix).replace('_', '.').lower()
                message += f'"{key}".'
                logger.debug(message)
                response[key] = value

        return response


env_config = EnvironmentConfig()
env_config.get_config('KAFKA_CONSUMER_')
