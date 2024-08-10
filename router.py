#!/usr/bin/env python
"""
A configurable router for Kafka messages.

For detailed documentation, see
<https://github.com/cbdq-io/a-fake-rotor-true/blob/main/README.md>.

LICENCE
-------
BSD 3-Clause License

Copyright (c) 2024, Cloud Based DQ

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import json
import logging
import os
import re
import signal
import sys
import time
import traceback
import types

import jmespath
import jsonschema
from confluent_kafka import (Consumer, KafkaError, KafkaException, Message,
                             Producer)
from prometheus_client import Counter, Info, Summary, start_http_server

__version__ = '0.1.2'
PROG = os.path.basename(sys.argv[0]).removesuffix('.py')
logging.basicConfig()
logger = logging.getLogger(PROG)
log_level = os.getenv('LOG_LEVEL', 'WARN')
logger.setLevel(log_level)
logger.debug(f'Log level has been set to "{log_level}".')

""" Prometheus Metrics. """
kafka_prefix = os.getenv('KAFKA_ROUTER_PROMETHEUS_PREFIX', '')
PROCESS_TIME = Summary(f'{kafka_prefix}processing_time_seconds', 'Time spent processing message.')
VERSION_INFO = Info(f'{kafka_prefix}run_version', 'The currently running version.')
VERSION_INFO.info({f'{kafka_prefix}version': __version__})
consumer_message_count = Counter(f'{kafka_prefix}consumer_message_count', 'The count of messages consumed.')
consumer_message_committed_count = Counter(f'{kafka_prefix}consumer_message_committed_count',
                                           'The count of messages consumed and committed.')
non_routed_error_count = Counter(f'{kafka_prefix}non_routed_error_count',
                                 'The count of messages that could not be routed.')
producer_message_count = Counter(f'{kafka_prefix}producer_message_count', 'The count of messages produced.')


class EnvironmentConfig:
    """Extract configuration from environment variables."""

    def get_boolean(self, key: str) -> bool:
        """
        Get a boolean value from an environment variable.

        If the environment variable is not set, return False.

        Parameters
        ----------
        key : str
            The name of the environment variable.

        Returns
        -------
        bool
            If the environment variable value indicated True or False.

        Raises
        ------
        ValueError
            If the environment is set, but can't ascertain from its value if
            it should be True or False.
        """
        value_map = {
            'TRUE': True,
            'T': True,
            '1': True,
            'YES': True,
            'Y': True,
            'FALSE': False,
            'F': False,
            '0': False,
            'NO': False,
            'N': False
        }
        value = os.getenv(key, 'False')

        try:
            return value_map[value.upper()]
        except KeyError:
            raise ValueError(f'Unknown value ("{value}") for boolean set in "{key}".')

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
                message = f'Converted environment variable "{key}" to '
                key = key.removeprefix(prefix).replace('_', '.').lower()
                message += f' config item "{key}".'
                logger.debug(message)
                response[key] = value

        return response


class KafkaRouterRule:
    """
    A rule for the Kafka router.

    Parameters
    ----------
    name : str
        The name of the rule as found in the environment variables.
    rule : str
        The rule itself as a JSON string.
    """

    def __init__(self, name: str, rule: str) -> None:
        logger.debug(f'Adding the {name} KafkaRouterRule "{rule}".')
        with open('rule-schema.json', 'r') as stream:
            schema = json.load(stream)

        try:
            instance = json.loads(rule)
            logger.debug(f'Instance is "{instance}".')
            jsonschema.validate(instance=instance, schema=schema)
        except json.decoder.JSONDecodeError:
            logger.error(f'{name} is not valid JSON.')
            sys.exit(2)
        except jsonschema.exceptions.ValidationError as ex:
            logger.error(f'{name} is not valid {ex}')
            sys.exit(2)

        self.name = name.removeprefix('KAFKA_ROUTER_RULE_')
        self.destination_topic = instance['destination_topic']
        self.header_jmespath = instance.get('header_jmespath', None)
        self.jmespath = instance.get('jmespath', None)
        self.regexp = instance.get('regexp', None)
        self.source_topic = instance['source_topic']

    def get_data(self, message: Message) -> str:
        """
        Return the data specific to how the message will be matched.

        Parameters
        ----------
        message : Message
            The message to be parsed.

        Returns
        -------
        str
            The data to be matched against.  If the rule is that no jmespath is specified,
            this will be the decoded message.  If a jmespath is required, then the
            message will be parsed from JSON and the relevant path will be
            returned.
        """
        raw_message = message.value().decode('utf-8')

        if self.jmespath:
            data = json.loads(raw_message)
            logger.debug(f'JMESPath is looking for "{self.jmespath}" in "{data}".')
            return jmespath.search(self.jmespath, data)

        return raw_message

    def match_message(self, message: Message) -> bool:
        """
        Check if the provided message matches this rule.

        Parameters
        ----------
        message : Message
            The message to be matched against.

        Returns
        -------
        bool
            True if the message matches the rule, false otherwise,
        """
        source_topic = message.topic()
        raw_message = message.value().decode('utf-8')
        logger.debug(f'Matching message "{raw_message}" against the {self.name} rule.')

        if source_topic == self.source_topic and not self.regexp:
            return True

        data = self.get_data(message)
        logger.debug(f'Data extracted for comparison is "{data}".')

        if data and re.search(self.regexp, data):
            return True

        return False


class KafkaRouter:
    """
    A class for routing Kafka traffic to/from topics according to configurable rule.

    Parameters
    ----------
    DLQ_topic_name : str, optional
        The name of the dead letter queue topic, by default None
    """

    def __init__(self, DLQ_topic_name: str = None) -> None:
        env_config = EnvironmentConfig()
        self._headers = []
        self.consumer_conf = env_config.get_config('KAFKA_CONSUMER_')
        self.producer_conf = env_config.get_config('KAFKA_PRODUCER_')
        self.DLQ_topic_name = DLQ_topic_name
        self.source_topics = []
        self.rules = []
        self.get_rules()
        signal.signal(signal.SIGINT, self.handler)
        signal.signal(signal.SIGTERM, self.handler)
        self.running(True)
        self.dlq_mode(env_config.get_boolean('KAFKA_ROUTER_DLQ_MODE'))
        self.dry_run_mode(env_config.get_boolean('KAFKA_ROUTER_DRY_RUN_MODE'))

        if self.dlq_mode():
            self.timeout_ms = int(os.getenv('KAFKA_ROUTER_TIMEOUT_MS', '500'))
        else:
            self.timeout_ms = 0

        self.consumer = None
        self.producer = None

    def add_rule(self, rule: KafkaRouterRule) -> None:
        """
        Append the KafkaRouterRule to the rules.

        Also append the source topic to the source topics if it's not already there.

        Parameters
        ----------
        rule : KafkaRouterRule
            The KafkaRouterRule to be added.
        """
        self.rules.append(rule)

        source_topic = rule.source_topic

        if source_topic not in self.source_topics:
            self.source_topics.append(source_topic)

    def check_for_timeout(self, time_of_last_message: int) -> None:
        """
        Check if we have exceeded the timeout_ms.

        Only does anything significant is DLQ mode is enabled.

        Parameters
        ----------
        time_of_last_message : int
            The timestamp (in ms) of when the last message was processed.
        """
        if not self.dlq_mode():
            logger.debug('DLQ Mode is disabled.')
            return

        time_now = time.time() * 1000

        if time_now - time_of_last_message >= self.timeout_ms:
            logger.warning(f'Timeout ({self.timeout_ms}ms) since last message consumed.')
            self.running(False)

    def commit(self, message: Message) -> None:
        """
        Commit the consumer unless DLQ mode is enabled.

        Parameters
        ----------
        message : Message
            The message to be committed.
        """
        if not self.dlq_mode():
            self.consumer.commit(message)
            consumer_message_committed_count.inc()

    def dlq_mode(self, dlq_mode: bool = None) -> bool:
        """
        Get or set the DLQ mode.

        Parameters
        ----------
        dlq_mode : bool, optional
            Set the DLQ mode, by default None

        Returns
        -------
        bool
            Get the DLQ mode.
        """
        if dlq_mode is not None:
            self._dlq_mode = dlq_mode

        return self._dlq_mode

    def dry_run_mode(self, dry_run_mode: bool = None) -> bool:
        """
        Get or set dry run mode.

        When set to true, no messages are produced.

        Parameters
        ----------
        dry_run_mode : bool, optional
            Set the dry-run mode, by default None

        Returns
        -------
        bool
            Get dry-run mode.
        """
        if dry_run_mode is not None:
            self._dry_run_mode = dry_run_mode

        return self._dry_run_mode

    def get_dlq_id(self):
        """
        Get the ID for the DLQ headers.

        Returns
        -------
        str
            If KAFKA_ROUTER_DLQ_ID is provided. If not provided will be set
            to KAFKA_CONSUMER_CLIENT_ID (if present) or KAFKA_CONSUMER_GROUP_ID.
        """
        if os.getenv('KAFKA_ROUTER_DLQ_ID', None):
            return os.environ['KAFKA_ROUTER_DLQ_ID']
        elif os.getenv('KAFKA_CONSUMER_CLIENT_ID', None):
            return os.environ['KAFKA_CONSUMER_CLIENT_ID']

        return os.environ['KAFKA_CONSUMER_GROUP_ID']

    def get_rules(self) -> None:
        """
        Get the rules from the environment variables.

        Returns
        -------
        list
            A list of KafkaRouterRules objects.
        """
        rules = []
        keys = []

        for key in os.environ.keys():
            if key.startswith('KAFKA_ROUTER_RULE_'):
                keys.append(key)

        keys.sort()

        for key in keys:
            self.add_rule(
                KafkaRouterRule(key, os.environ[key])
            )

        return rules

    def handler(self, signum: int, frame: types.FrameType) -> None:
        """Catch signals."""
        signame = signal.Signals(signum).name
        logger.warning(f'Caught signal {signame} ({signum}).')
        sys.exit(0)

    def headers(self, headers: list = None) -> list:
        """
        Get or set the headers of the message being processed.

        Parameters
        ----------
        headers : list, optional
            If provided, a list of tuples to set as headers for the message, by default None

        Returns
        -------
        list
            A list of tuples that represent the headers of the message.
        """
        if headers is not None:
            self._headers = headers

        return self._headers

    def match_message_to_rule(self, message: Message) -> None:
        """
        Match the given message to the configured rules.

        Parameters
        ----------
        message : Message
            The message to be matched.
        """
        destination_topic = self.DLQ_topic_name
        message_matched_to_rule = False
        self.headers(message.headers())

        for rule in self.rules:
            try:
                if rule.match_message(message):
                    destination_topic = rule.destination_topic
                    message_matched_to_rule = True
                    break
            except json.decoder.JSONDecodeError as ex:
                destination_topic = self.DLQ_topic_name
                self.upsert_header(f'__{self.get_dlq_id()}.topic', message.topic())
                self.upsert_header(f'__{self.get_dlq_id()}.partition', message.partition())
                self.upsert_header(f'__{self.get_dlq_id()}.offset', message.offset())
                self.upsert_header(f'__{self.get_dlq_id()}.message', ex)
                self.upsert_header(f'__{self.get_dlq_id()}.stacktrace', traceback.format_exc())

                # Keep DLQ headers intact by saying we have matched the message.
                message_matched_to_rule = True

        if destination_topic:
            logger.debug(f'Producing message onto the {destination_topic} topic.')
            self.prepare_headers(message, destination_topic, message_matched_to_rule)
            self.produce(destination_topic, message.value(), message.key(), self.headers())

        self.report_message_matching_status(destination_topic, message_matched_to_rule)

    def prepare_headers(self, message: Message, destination_topic: str, message_matched_to_rule: bool) -> None:
        """
        Prepare headers before producing a message.

        Predominantly used to ensure that a message that has not been
        matched to any rules and is destined for the DLQ topic has
        headers explaining why.

        Parameters
        ----------
        message : Message
            The message to be produced.
        message_matched_to_rule : bool
            Was the message matched to any rule.
        """
        if destination_topic == self.DLQ_topic_name and not message_matched_to_rule:
            self.upsert_header(f'__{self.get_dlq_id()}.topic', message.topic())
            self.upsert_header(f'__{self.get_dlq_id()}.partition', message.partition())
            self.upsert_header(f'__{self.get_dlq_id()}.offset', message.offset())
            self.upsert_header(f'__{self.get_dlq_id()}.message', 'Message not matched to any routing rules.')

    @PROCESS_TIME.time()
    def process_message(self, message: Message):
        """
        Process a message that has been consumed from an input topic.

        Parameters
        ----------
        message : Message
            The consumed message to be processed.

        Raises
        ------
        KafkaError
            If an error occurred in the consumer.
        """
        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                logger.debug('End of partition reached {0}/{1}'.format(message.topic(), message.partition()))
            else:
                raise KafkaException(message.error())
        else:
            logger.debug(f'Consumed message from {message.topic()}: {message.value().decode("utf-8")}')
            self.match_message_to_rule(message)

    def produce(self, topic: str, value: str, key: str, headers: list) -> None:
        """
        Produce a message onto a topic unless dry run and DLQ mode is on.

        Parameters
        ----------
        topic : str
            The topic to be written to.
        value : str
            The value of the message.
        key : str
            The key of the message.
        headers : list
            The headers of the message.
        """
        if not self.dlq_mode() and not self.dry_run_mode():
            self.producer.produce(topic, value, key, headers=self.headers())
            logger.debug('Flushing the producer.')
            self.producer.flush()
            producer_message_count.inc()
        else:
            logger.debug(f'Skipping producing message to {topic} as dry-run mode is on.')

    def report_message_matching_status(self, destination_topic: str, message_matched_to_rule: bool) -> None:
        """
        Report and set metrics for if the message was matched or not.

        Yes, this could be an if statement in match_message_to_rule method,
        but radon is at the limit of how complex that method is already.

        Parameters
        ----------
        destination_topic: str
            The name of the topic that the message is being routed to.
        message_matched_to_rule : bool
            True if the message was successfully matched to a routing rule,
            False otherwise.
        """
        if message_matched_to_rule and destination_topic == self.DLQ_topic_name:
            non_routed_error_count.inc()
        elif message_matched_to_rule:
            logger.debug('The message was successfully matched to a rule.')
        else:
            message = 'The message did not match any configured rules.  '

            if self.DLQ_topic_name:
                message += f'It has been sent to the {self.DLQ_topic_name} topic.'
            else:
                message += 'The message will no longer be processed.'

            logger.warn(message)
            non_routed_error_count.inc()

    def router(self) -> None:
        """
        Consume from the consumer and produce to the producer.

        Exits if SIGINT is caught.
        """
        if len(self.rules) == 0:
            logger.error('There are no KafkaRouter rules defined.')
            sys.exit(0)

        self.validate_consumer_config(self.consumer_conf)
        self.consumer = Consumer(self.consumer_conf)
        self.producer = Producer(self.producer_conf)

        try:
            self.consumer.subscribe(self.source_topics)
            time_of_last_message = time.time() * 1000

            while self.running():
                self.check_for_timeout(time_of_last_message)
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    logger.debug('Message is None.')
                    continue

                time_of_last_message = time.time() * 1000
                consumer_message_count.inc()
                self.process_message(msg)
                logger.debug('Committing the message in the consumer.')
                self.commit(msg)
        except SystemExit:
            logger.warning('SystemExit exception caught.')
        finally:
            logger.info('Closing the consumer.')
            self.consumer.close()

    def running(self, running: bool = None) -> bool:
        """
        Get or set the running state.

        Parameters
        ----------
        running : bool, optional
            Set the running state if not None, by default None

        Returns
        -------
        bool
            Get the running state.
        """
        if running is not None:
            self._running = running

        return self._running

    def upsert_header(self, new_key: str, new_value: str) -> None:
        """
        Update an existing header or insert a new one.

        Parameters
        ----------
        new_key : str
            The key value of the header.
        new_value : str
            The value of the header.
        """
        existing_headers = self.headers()
        new_headers = []

        for key, value in existing_headers:
            if key != new_key:
                new_headers.append((key, value))

        new_headers.append((new_key, str(new_value)))
        self.headers(new_headers)

    def validate_consumer_config(self, config: dict) -> None:
        """
        Validate the consumer config.

        Ensures that enable.auto.commit is disabled.

        Parameters
        ----------
        config : dict
            The consumer config.

        Raises
        ------
        ValueError
            Raised if enable.auto.commit is missing or not set to false.
        """
        is_valid = False

        if 'enable.auto.commit' not in config:
            logger.error('Please set the KAFKA_CONSUMER_ENABLE_AUTO_COMMIT environment variable.')
        elif config['enable.auto.commit'] != 'false':
            logger.error('Please set the KAFKA_CONSUMER_ENABLE_AUTO_COMMIT environment variable to "false".')
        else:
            is_valid = True

        if not is_valid:
            raise ValueError('The consumer must be configured with enable.auto.commit set to false.')


if __name__ == '__main__':
    start_http_server(int(os.getenv('KAFKA_ROUTER_PROMETHEUS_PORT', '8000')))
    router = KafkaRouter(os.getenv('KAFKA_ROUTER_DLQ_TOPIC_NAME', None))
    router.router()
