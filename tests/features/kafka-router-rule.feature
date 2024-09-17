Feature: Kafka Router Rule
    In order to route a message
    As a Kafka Router
    I want a Kafka Router Rule engine

    Scenario Outline: Test How a Message Will Be Routed
        Given  a KafkaRouter with DLQ topic "dlq_topic"
        And a message with a value of <message_value>
        And with message topic <topic>
        And a Kafka Router Rule of <rule>
        When the message is checked
        And append message header status with value TEST
        And append message header __router.errors.topic with value input
        Then message is a match is <expected_outcome>

        Examples:
        | message_value                                                                                                | topic     | rule                                                                                                                                      | expected_outcome |
        | { "given_name": "John", "family_name": "Smith", "company_name": "John Smith & Associates" }                  | input     | {"destination_topics":"GB.output","jmespath":"country","regexp":"^GB$","source_topic":"input"}                                             | False            |
        | { "given_name": "John", "family_name": "Smith", "company_name": "John Smith & Associates", "country": "GB" } | input     | {"destination_topics":"GB.output","jmespath":"country","regexp":"^GB$","source_topic":"input"}                                             | True             |
        | { "given_name": "John", "family_name": "Smith", "company_name": "John Smith & Associates", "country": "GB" } | input     | {"destination_topics":"GB.output","jmespath":"country","source_topic":"input"}                                                             | True             |
        | Country: England                                                                                             | input     | {"destination_topics":"GB.output","regexp":"Scotland","source_topic":"input"}                                                              | False            |
        | Country: Scotland                                                                                            | input     | {"destination_topics":"GB.output","regexp":"Scotland","source_topic":"input"}                                                              | True             |
        | Hello, world!                                                                                                | input     | {"destination_topics":"GB.output","source_topic":"input"}                                                                                  | True             |
        | Hello, world!                                                                                                | input.dlq | {"destination_topics":"GB.output","source_topic":"input.dlq","header":"__router.errors.topic","header_regexp":"^input$"}                   | True             |
        | Hello, world!                                                                                                | input.dlq | {"destination_topics":"GB.output","source_topic":"input.DLQ","header":"__router.errors.topic","header_regexp":"^input$"}                   | False            |
        | Hello, world!                                                                                                | input.dlq | {"destination_topics":"GB.output","source_topic":"input.dlq","header":"__router.errors.topic","header_regexp":"^foo$"}                     | False            |
        | Hello, world!                                                                                                | input.dlq | {"destination_topics":"GB.output","source_topic":"input.dlq","header":"__router.errors.topic","header_regexp":"^input$","regexp":"^Hello"} | True             |
        | Goodbye Cruel World, Elvis Costello                                                                          | input.dlq | {"destination_topics":"GB.output","source_topic":"input.dlq","header":"__router.errors.topic","header_regexp":"^foo$","regexp":"^Hello"}   | False            |

    Scenario Outline: Rule Exceptions
        Given an Invalid Kafka Router Rule of <rule>
        When the rule is initialised
        Then the SystemExit is 2

        Examples:
        | rule                            |
        | Invalid JSON.                   |
        | { "message": "Invalid schema" } |
