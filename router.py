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
import logging
import os
import signal
import sys

from confluent_kafka import (Consumer, KafkaError, KafkaException, Message,
                             Producer)
from prometheus_client import Counter, Info, Summary, start_http_server

__version__ = '0.1.0'
PROG = os.path.basename(sys.argv[0]).removesuffix('.py')
logging.basicConfig()
logger = logging.getLogger(PROG)
log_level = os.getenv('LOG_LEVEL', 'WARN')
logger.setLevel(log_level)
logger.debug(f'Log level has been set to "{log_level}".')

""" Prometheus Metrics. """
PROCESS_TIME = Summary('processing_time_seconds', 'Time spent processing message.')
VERSION_INFO = Info('run_version', 'The currently running version.')
VERSION_INFO.info({'version': __version__})
consumer_message_count = Counter('consumer_message_count', 'The count of messages consumed.')
consumer_message_committed_count = Counter(
    'consumer_message_committed_count',
    'The count of messages consumed and committed.'
)
producer_message_count = Counter('producer_message_count', 'The count of messages produced.')


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
                message = f'Converted environment variable "{key}" to '
                key = key.removeprefix(prefix).replace('_', '.').lower()
                message += f' config item "{key}".'
                logger.debug(message)
                response[key] = value

        return response


class KafkaRouter:
    """A class for routing Kafka traffic to/from topics according to configurable rule."""

    def __init__(self, DLQ_topic_name: str = None) -> None:
        env_config = EnvironmentConfig()
        self.consumer_conf = env_config.get_config('KAFKA_CONSUMER_')
        self.producer_conf = env_config.get_config('KAFKA_PRODUCER_')
        self.DLQ_topic_name = DLQ_topic_name

    def handler(signum: int, frame):
        """Catch fish."""
        signame = signal.Signals(signum).name
        logger.debug(f'frame is of type ({type(frame)}).')
        logger.warn(f'Caught signal {signame} ({signum}).')
        sys.exit(0)

    def router(self) -> None:
        """
        Consume from the consumer and produce to the producer.

        Exits if SIGINT is caught.
        """
        self.validate_consumer_config(self.consumer_conf)
        consumer = Consumer(self.consumer_conf)
        producer = Producer(self.producer_conf)
        signal.signal(signal.SIGINT, self.handler)
        input_topic = 'input_topic'

        try:
            consumer.subscribe([input_topic])

            while True:
                msg = consumer.poll(timeout=1.0)

                if msg is None:
                    logger.debug('Message is None.')
                    continue

                consumer_message_count.inc()
                self.process_message(msg, producer)
                logger.debug('Committing the message in the consumer.')
                consumer.commit(msg)
                consumer_message_committed_count.inc()
        except SystemExit:
            logger.warning('SystemExit exception caught.')
        finally:
            logger.info('Closing the consumer.')
            consumer.close()

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

    @PROCESS_TIME.time()
    def process_message(self, message: Message, producer: Producer):
        """
        Process a message that has been consumed from an input topic.

        Parameters
        ----------
        message : Message
            The consumed message to be processed.
        producer : confluent_kafka.Producer

        Raises
        ------
        KafkaError
            If an error occurred in the consumer.
        """
        output_topic = 'output_topic'

        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                logger.debug('End of partition reached {0}/{1}'.format(message.topic(), message.partition()))
            else:
                raise KafkaException(message.error())
        else:
            logger.debug(f'Consumed message from {message.topic()}: {message.value().decode("utf-8")}')
            logger.debug(f'Producing message onto the {output_topic} topic.')
            producer.produce(output_topic, message.value())
            logger.debug('Flushing the producer.')
            producer.flush()
            producer_message_count.inc()


if __name__ == '__main__':
    start_http_server(int(os.getenv('KAFKA_ROUTER_PROMETHEUS_PORT', '8000')))
    router = KafkaRouter(os.getenv('KAFKA_ROUTER_DLQ_TOPIC_NAME', None))
    router.router()
