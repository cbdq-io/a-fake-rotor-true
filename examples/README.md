# Dead Letter Queue (DLQ) Replay Examples

To run these exercises, first, follow the
[contributing guide](../CONTRIBUTING.md) and run the end-to-end tests.  After
they have completed successfully, run the following command to show the
contents of the **replay_example.dlq** topic:

```shell
docker compose exec kafka kafka-console-consumer  \
    --bootstrap-server kafka:9092 \
    --from-beginning \
    --timeout-ms=500 \
    --property print.headers=true \
    --topic replay_example.dlq
```

This will give you the following output:

```
__example_errors.topic:example1	{"message": "DLQ Message 1."}
__example_errors.topic:example2	{"message": "DLQ Message 2."}
__example_errors.topic:example2	{"message": "DLQ Message 3."}
[2024-08-11 12:13:59,927] ERROR Error processing message, terminating consumer process:  (kafka.tools.ConsoleConsumer$)
org.apache.kafka.common.errors.TimeoutException
Processed a total of 3 messages
```

One can ignore the message `org.apache.kafka.common.errors.TimeoutException`
in this instance.  From the output, we can see that we have messages that
can be summarised as:

| # | Offset | Header Key             | Header Value | Message                       |
| - | ------ | ---------------------- | ------------ | ----------------------------- |
| 1 | 0/0    | __example_errors.topic | example1     | {"message": "DLQ Message 1."} |
| 2 | 0/1    | __example_errors.topic | example2     | {"message": "DLQ Message 2."} |
| 3 | 0/2    | __example_errors.topic | example2     | {"message": "DLQ Message 3."} |

These examples are executed from the directory where you cloned this repo to
and utilise both the `docker-compose.yml` in the root of the project and
another `docker-compose.yml` in the `examples` directory.  In the services
configured in `examples/docker-compose.yml`, please note the following:

1. KAFKA_ROUTER_DLQ_MODE is set to 1 (for True).
1. KAFKA_ROUTER_DRY_RUN_MODE can be set on the command line (an example of
   this is provided below).
1. We have set KAFKA_ROUTER_TIMEOUT_MS to 3000 (3 seconds) so that the
   router doesn't close before all messages are processed.

## Use Case 1: Replay All Messages From a DLQ Topic and a Dry Run Example

Normally the routing rules are provided as minimised JSON, but to make these
examples more readable, we will also provide well formatted JSON.  In this
example, we are going to:

1. Run in dry-run mode to preview what is going to happen.
1. Run the same job without dry-run mode.
1. Confirm the contents of the destination topic.

In this example, the rule is the most basic it can be:

```JSON
{
    "destination_topic": "replay_example1",
    "source_topic": "replay_example.dlq"
}
```

This simply takes any message found on the topic **replay_example.dlq** and
routes them to **replay_examples1**.  First let us run the container in
dry-run mode:

```shell
KAFKA_ROUTER_DRY_RUN_MODE=1 docker compose -f docker-compose.yml \
                                           -f examples/docker-compose.yml \
                                           run --rm example1
```

This should give you output similar to the following:

```
INFO:router:Log level has been set to "DEBUG".
INFO:router:DLQ mode - True
INFO:router:Dry run mode - True
DEBUG:router:Timeout - 3000ms.
DEBUG:router:Message on topic "replay_example.dlq" (0/0) matches rule "REPLAY_ALL_DLQ_MESSAGES" (replay_example1).
DEBUG:router:Message on topic "replay_example.dlq" (0/1) matches rule "REPLAY_ALL_DLQ_MESSAGES" (replay_example1).
DEBUG:router:Message on topic "replay_example.dlq" (0/2) matches rule "REPLAY_ALL_DLQ_MESSAGES" (replay_example1).
DEBUG:router:No messages to consume.
DEBUG:router:No messages to consume.
DEBUG:router:No messages to consume.
WARNING:router:Timeout (3000ms) since last message consumed.
DEBUG:router:No messages to consume.
INFO:router:Closing the consumer.
INFO:router:Consumed 3 messages.
INFO:router:Produced 0 messages.
```

This tells us:

- The log level is DEBUG.
- We are running in DLQ mode (do not commit on the consumer so that we can start from the beginning of the topic in the consumer group).
- We are running in dry-run mode (no messages will be produced).
- The timeout has been configured to 3000ms (3 seconds).
- The rule REPLAY_ALL_DLQ_MESSAGES matched 3 messages.
- We had 3 seconds when no messages were received.
- The router timed out waiting for new messages (as configured) and closed the consumer.
- We consumed 3 messages.
- We produced 0 messages (dry-run mode).

No let's run the command without dry-run mode on:

```shell
docker compose -f docker-compose.yml \
               -f examples/docker-compose.yml \
               run --rm example1
```

This time the output is:

```
INFO:router:Log level has been set to "DEBUG".
INFO:router:DLQ mode - True
INFO:router:Dry run mode - False
DEBUG:router:Timeout - 3000ms.
DEBUG:router:Message on topic "replay_example.dlq" (0/0) matches rule "REPLAY_ALL_DLQ_MESSAGES" (replay_example1).
DEBUG:router:Message on topic "replay_example.dlq" (0/1) matches rule "REPLAY_ALL_DLQ_MESSAGES" (replay_example1).
DEBUG:router:Message on topic "replay_example.dlq" (0/2) matches rule "REPLAY_ALL_DLQ_MESSAGES" (replay_example1).
DEBUG:router:No messages to consume.
DEBUG:router:No messages to consume.
DEBUG:router:No messages to consume.
WARNING:router:Timeout (3000ms) since last message consumed.
DEBUG:router:No messages to consume.
INFO:router:Closing the consumer.
INFO:router:Consumed 3 messages.
INFO:router:Produced 3 messages.
```

Telling us that dry-run mode was disabled and that this time, we produced 3
messages onto the **replay_example1** topic.

We can confirm this with the following command:

```shell
docker compose exec kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic replay_example1 --from-beginning --timeout-ms 250
```

Which should give you output similar to the following:

```
{"message": "DLQ Message 1."}
{"message": "DLQ Message 2."}
{"message": "DLQ Message 3."}
[2024-08-11 12:46:10,481] ERROR Error processing message, terminating consumer process:  (kafka.tools.ConsoleConsumer$)
org.apache.kafka.common.errors.TimeoutException
Processed a total of 3 messages
```

## Use Case 2: Replay Messages Depending on the Content of Message Headers

In this example, the rule to be applied is:

```JSON
{
  destination_topic: "replay_example2",
  header: "__example_errors.topic",
  header_regexp: "^example2$",
  source_topic: "replay_example.dlq"
}
```

1. The destination topic will be **replay_example2**.
1. The message must contain a header called **__example_errors.topic**
   that matches the regular expression `^example2$`.
1. The source topic must be **replay_example.dlq**.

Please not that these rules must **ALL** match (and logic).

Run the example container:

```shell
docker compose -f docker-compose.yml \
               -f examples/docker-compose.yml \
               run --rm example2
```

Which will give you output similar to the following:

```
INFO:router:Log level has been set to "DEBUG".
INFO:router:DLQ mode - True
INFO:router:Dry run mode - False
DEBUG:router:Timeout - 3000ms.
DEBUG:router:Message on topic "replay_example.dlq" (0/1) matches rule "REPLAY_EXAMPLE2_HEADER" (replay_example2).
DEBUG:router:Message on topic "replay_example.dlq" (0/2) matches rule "REPLAY_EXAMPLE2_HEADER" (replay_example2).
DEBUG:router:No messages to consume.
DEBUG:router:No messages to consume.
DEBUG:router:No messages to consume.
WARNING:router:Timeout (3000ms) since last message consumed.
DEBUG:router:No messages to consume.
INFO:router:Closing the consumer.
INFO:router:Consumed 3 messages.
INFO:router:Produced 2 messages.
```

This can be confirmed with:

```shell
docker compose exec kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic replay_example2 --from-beginning --timeout-ms 250
```

Which will give output similar to:

```
{"message": "DLQ Message 2."}
{"message": "DLQ Message 3."}
[2024-08-11 12:56:20,341] ERROR Error processing message, terminating consumer process:  (kafka.tools.ConsoleConsumer$)
org.apache.kafka.common.errors.TimeoutException
Processed a total of 2 messages
```

Showing us that messages 2 and 3 were routed from the DLQ topic.

## Use Case 3: Replay Messages Depending on the Content of Message Headers and Message Content

In this example, the rule to be applied is:

```JSON
{
  destination_topic: "replay_example2",
  header: "__example_errors.topic",
  header_regexp: "^example2$",
  regexp: "Message 2",
  source_topic: "replay_example.dlq"
}
```

This sets the same rules as in example 2 except with the additional condition
that the message value must match the regular expression `Message 2` (this is
message 2 in our test data).

Run the container:

```shell
docker compose -f docker-compose.yml \
               -f examples/docker-compose.yml \
               run --rm example3
```

Which should give output similar to the following:

```
INFO:router:Log level has been set to "DEBUG".
INFO:router:DLQ mode - True
INFO:router:Dry run mode - False
DEBUG:router:Timeout - 3000ms.
DEBUG:router:Message on topic "replay_example.dlq" (0/1) matches rule "REPLAY_EXAMPLE2_HEADER_AND_MESSAGE_2" (replay_example2).
DEBUG:router:No messages to consume.
DEBUG:router:No messages to consume.
DEBUG:router:No messages to consume.
WARNING:router:Timeout (3000ms) since last message consumed.
DEBUG:router:No messages to consume.
INFO:router:Closing the consumer.
INFO:router:Consumed 3 messages.
INFO:router:Produced 1 messages.
```

Confirm the outcome:

```shell
docker compose exec kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic replay_example3 --from-beginning --timeout-ms 250
```

Which will give output similar to the following:

```
{"message": "DLQ Message 2."}
[2024-08-11 13:05:52,757] ERROR Error processing message, terminating consumer process:  (kafka.tools.ConsoleConsumer$)
org.apache.kafka.common.errors.TimeoutException
Processed a total of 1 messages
```
