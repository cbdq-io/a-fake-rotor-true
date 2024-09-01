# a-fake-rotor-true
A configurable router for Kafka messages.  Can also be used to replay
selected messages from a dead letter queue (DLQ) topic.  See the
[DLQ replay examples](./examples/README.md) for more details.

[What's with the name](docs/that-aint-an-anagram-dude.png)
a-fake-rotor-true? The official explanation __now__ is that it's just a
random name :blush:

## Configuration

We use the
[Confluent Kafka
Python](https://docs.confluent.io/kafka-clients/python/current/overview.html)
client, so the consumer and producer need to be configured with settings
that will be recognised by that package.  All configuration settings are
provided by environment variables.

### Kafka Consumer

Any environment variable that is prefixed with `KAFKA_CONSUMER_` is
considered to be a configuration setting for the consumer.  This will then:

- Remove the `KAFKA_CONSUMER_` prefix.
- Substitute any occurrence of "`_`" with "`.`".
- Change all uppercase letters to lowercase.

For example, an environment variable called
`KAFKA_CONSUMER_BOOTSTRAP_SERVERS` that is set to `host1:9092,host2:9092`
will configure `bootstrap.servers=host1:9092,host2:9092` in the consumer.

Please not that `KAFKA_CONSUMER_ENABLE_AUTO_COMMIT` **MUST** be set to "false".

### Kafka Producer

A similar method of configuration for the consumer, except using a prefix
of `KAFKA_PRODUCER_`.  So `KAFKA_PRODUCER_BOOTSTRAP_SERVERS` will configure
`bootstrap.servers` in the producer configuration.

### Routing Rules

Routing rules (of which at least one is required) have a prefix of
`KAFKA_ROUTER_RULE_`.  These are added and processed alphabetically, sorted
on the name of the environment variable.  For more details on configuring
rules, see [docs/rules.md](docs/rules.md) and an example configuration
can be seen in the `router` service in
`docker-compose.yml`.

### Other Configuration Items

If no default is provided, the configuration item is mandatory.

| Configuration | Default | Notes |
| ------------- | ------- | ----- |
| KAFKA_ROUTER_DLQ_ID | "" | If not provided will be set to KAFKA_CONSUMER_CLIENT_ID (if present) or KAFKA_CONSUMER_GROUP_ID. |
| KAFKA_ROUTER_DLQ_MODE | False | If True, obeys KAFKA_ROUTER_TIMEOUT_MS and will not commit on the consumer. |
| KAFKA_ROUTER_DLQ_TOPIC_NAME | "" | Will attempt to write messages that no rules apply to this topic.  If blank, the router warn no matches were found for the message and continue. |
| KAFKA_ROUTER_DRY_RUN_MODE | False | If True AND KAFKA_ROUTER_DLQ_MODE is True then don't produce any messages. |
| KAFKA_ROUTER_PROMETHEUS_PORT | 8000 | The port for Prometheus metrics. |
| KAFKA_ROUTER_PROMETHEUS_PREFIX | "" | A prefix name to add to the prometheus metrics (e.g. "dev_"). |
| KAFKA_ROUTER_TIMEOUT_MS | 500 | Exit if no message is available for consumption for the specified interval.  Ignored unless KAFKA_ROUTER_DLQ_MODE is "True" |
| LOG_LEVEL     | WARN    | Can be DEBUG, INFO, WARN or ERROR. |
| SENTRY_DSN    | "" | If configured in the environment, will be used to configure the DSN in [Sentry](www.sentry.io). |

### Headers of Messages Placed on the DLQ Topic

If a message is placed upon the DLQ topic, we follow the example as set in
[Confluent Cloud Dead Letter Queue](https://docs.confluent.io/cloud/current/connectors/dead-letter-queue.html).
In this example we have set KAFKA_ROUTER_DLQ_ID to "router" and the headers will look something like this:

| Key | Example Value | Description |
| --- | ------------- | ----------- |
| __router.errors.topic | input | The name of the topic tha the message was consumed from. |
| __router.errors.partition | 1 | The partition number that the consumed message was on. |
| __router.errors.offset | 8583 | The offset of the consumed consumed message within the partition. |
| __router.errors.exception.message | No matching rules for message. | The exception message of why the message is on the DLQ. |
| __router.errors.exception.stacktrace | json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0) | Any stack trace (if available) associated with the exception. |
