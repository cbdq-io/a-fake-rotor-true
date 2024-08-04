Feature: The KafkaRouter class.
    In order to route messages
    As a KafkaRouter
    I want to be able to have a viable router

    Scenario Outline: Validate Consumer Config
        Given consumer config to be validated is <config>
        When the consumer config is validated
        Then ValueError exception is raised is <is_true>

        Examples:
            | config                                                                                  | is_true |
            | { "bootstrap.servers": "kafka:9092", "group.id": "foo" }                                | True    |
            | { "bootstrap.servers": "kafka:9092", "group.id": "foo", "enable.auto.commit": "true" }  | True    |
            | { "bootstrap.servers": "kafka:9092", "group.id": "foo", "enable.auto.commit": "false" } | False   |

    Scenario Outline: Check Adding Rules Affects Source Topics
        Given a KafkaRouter with DLQ topic <dlq_topic>
        When rule <rule> is added to the KafkaRouter
        Then KafkaRouter source topics include <source_topic>

        Examples:
            | dlq_topic | rule                                                                                          | source_topic |
            | None      | {"destination_topic":"GB.output","jmespath":"country","regexp":"^GB$","source_topic":"input"} | input        |

    Scenario Outline: DLQ ID
        Given a KafkaRouter with DLQ topic <dlq_topic>
        When OS environment KAFKA_ROUTER_DLQ_ID is <kafka_router_dlq_id>
        And OS environment KAFKA_CONSUMER_CLIENT_ID is <kafka_consumer_client_id>
        And OS environment KAFKA_CONSUMER_GROUP_ID is <kafka_consumer_group_id>
        Then DLQ ID is <expected_value>

        Examples:
            | dlq_topic | kafka_router_dlq_id | kafka_consumer_client_id | kafka_consumer_group_id | expected_value |
            | None      | a                   | b                        | c                       | a              |
            | None      | None                | b                        | c                       | b              |
            | None      | None                | None                     | c                       | c              |

    Scenario: Test Upsert Headers
        Given  a KafkaRouter with DLQ topic None
        And populated headers
        When new headers are appended
        Then headers count is two
