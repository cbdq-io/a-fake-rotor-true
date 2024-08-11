
@system
Feature: System Tests
    Scenario Outline: Load Test Data
        Given Kafka producer message value is <message_value>
        And Kafka producer headers
        When Kafka producer header <header_key> is <header_value>
        Then Kafka producer should produce to <topic>

        Examples:
        | message_value                                                                                                                      | header_key | header_value | topic      |
        | { "given_name": "John", "family_name": "Smith", "company_name": "John Smith & Associates" }                                        | test       | TEST01A      | input.json |
        | { "given_name": "John", "family_name": "Smith", "company_name": "John Smith & Associates", "vat_number": "WTF", "country": "WTF" } | test       | TEST01B      | input.json |
        | { "given_name": "John", "family_name": "Smith", "company_name": "John Smith & Associates", "vat_number": "GB999 9999 73" }         | test       | TEST01C      | input.json |
        | { "given_name": "John", "family_name": "Smith", "company_name": "John Smith & Associates", "country": "GB" }                       | test       | TEST01D      | input.json |
        | { "given_name": "Seána", "family_name": "Murphy", "company_name": "Seána Murphy & Associates", "vat_number": "IE1234567FA"}        | test       | TEST01E      | input.json |
        | { "given_name": "Seána", "family_name": "Murphy", "company_name": "Seána Murphy & Associates", "country": "IE"}                    | test       | TEST01F      | input.json |
        | Hello, world!                                                                                                                      | test       | TEST02A      | input.json |


    Scenario: Verify the Container Build
        Given the TestInfra host with URL "docker://router" is ready
        When the TestInfra user is "router"
        And the TestInfra group is "router"
        Then the TestInfra user is present
        And the TestInfra user group is router
        And the TestInfra user home is /home/router
        And the TestInfra user shell is /usr/sbin/nologin
        And the TestInfra group is present
        And the TestInfra pip check is OK

    Scenario Outline: Docker Container Files
        Given the TestInfra host with URL "docker://router" is ready
        When the TestInfra file is <file>
        Then the TestInfra file is present
        And the TestInfra file owner is router
        And the TestInfra file group is router
        And the TestInfra file type is <file_type>
        And the TestInfra file mode is <file_mode>

        Examples:
        | file                          | file_type | file_mode |
        | /home/router                  | directory | 0o700     |
        | /home/router/router.py        | file      | 0o755     |
        | /home/router/rule-schema.json | file      | 0o644     |

    Scenario Outline: Latest Python Packages
        Given the TestInfra host with URL "docker://router" is ready
        When the TestInfra pip package is <package>
        Then the TestInfra pip package is present
        And the TestInfra pip package is latest

        Examples:
        | package           |
        | confluent-kafka   |
        | prometheus_client |
        | redmx             |
        | sentry-sdk        |

    Scenario Outline: System Test Outcomes
        Given the TestInfra host with URL "docker://router" is ready
        When the TestInfra command is "curl --fail http://localhost:8000"
        Then the TestInfra command return code is 0
        And the TestInfra command stdout contains "<expected_output>"

        Examples:
        | expected_output                                   |
        | docker_consumer_message_count_total 8.0           |
        | docker_consumer_message_committed_count_total 8.0 |
        | docker_producer_message_count_total 8.0           |
        | docker_non_routed_error_count_total 4.0           |

    Scenario Outline: Track Test Message Destinations
        Given a Kafka Consumer Config
        And the Kafka Topic Name is <topic_name>
        When the Kafka Consumer Config Setting bootstrap.servers is localhost:9092
        And the Kafka Consumer Config Setting enable.auto.commit is false
        And the Kafka Consumer Config Setting group.id is test_consumer
        And the Kafka Consumer Config Setting auto.offset.reset is earliest
        Then the Kafka Topic Contains a Message With a Header Called <header_name> Set to <header_value>

        Examples:
        | header_name | header_value | topic_name     |
        | test        | TEST01A      | router.dlq     |
        | test        | TEST01B      | router.dlq     |
        | test        | TEST01C      | GB.output.json |
        | test        | TEST01D      | GB.output.json |
        | test        | TEST01E      | IE.output.json |
        | test        | TEST01F      | IE.output.json |
        | test        | TEST02A      | router.dlq     |

    Scenario: Stop The Router Container
        Given the TestInfra host with URL "local://" is ready
        When the TestInfra command is "docker compose stop router"
        Then the TestInfra command return code is 0

    Scenario Outline: Ensure Graceful Shutdown of the Kafka Consumer
        Given the TestInfra host with URL "local://" is ready
        When the TestInfra command is "docker compose logs router"
        Then the TestInfra command stdout contains "<expected_output>"

        Examples:
        | expected_output                             |
        | WARNING:router:Caught signal SIGTERM (15).  |
        | WARNING:router:SystemExit exception caught. |
        | INFO:router:Closing the consumer.           |
