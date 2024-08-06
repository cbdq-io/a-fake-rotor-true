Feature: Kafka Router Rule
    In order to route a message
    As a Kafka Router
    I want a Kafka Router Rule engine

    Scenario Outline: Test How a Message Will Be Routed
        Given  a KafkaRouter with DLQ topic "dlq_topic"
        And a message with a value of <message_value>
        And a Kafka Router Rule of <rule>
        When the message is checked
        Then message is a match is <expected_outcome>

        Examples:
        | message_value                                                                                                | rule                                                                                          | expected_outcome |
        | { "given_name": "John", "family_name": "Smith", "company_name": "John Smith & Associates" }                  | {"destination_topic":"GB.output","jmespath":"country","regexp":"^GB$","source_topic":"input"} | False            |
        | { "given_name": "John", "family_name": "Smith", "company_name": "John Smith & Associates", "country": "GB" } | {"destination_topic":"GB.output","jmespath":"country","regexp":"^GB$","source_topic":"input"} | True             |
        | { "given_name": "John", "family_name": "Smith", "company_name": "John Smith & Associates", "country": "GB" } | {"destination_topic":"GB.output","jmespath":"country","source_topic":"input"}                 | True             |
        | Country: England                                                                                             | {"destination_topic":"GB.output","regexp":"Scotland","source_topic":"input"}                  | False            |
        | Country: Scotland                                                                                            | {"destination_topic":"GB.output","regexp":"Scotland","source_topic":"input"}                  | True             |
        | Hello, world!                                                                                                | {"destination_topic":"GB.output","source_topic":"input"}                                      | True             |

    Scenario Outline: Rule Exceptions
        Given an Invalid Kafka Router Rule of <rule>
        When the rule is initialised
        Then the SystemExit is 2

        Examples:
        | rule                            |
        | Invalid JSON.                   |
        | { "message": "Invalid schema" } |
