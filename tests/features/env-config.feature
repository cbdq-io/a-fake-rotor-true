Feature: Environment Config
    In order to configure a Kafka producer or consumer
    As a role
    I want a feature that will extract the config from the environment.

    Scenario Outline: Kafka Consumer
        Given an EnvironmentConfig object
        And the EnvironmentConfig prefix setting is <prefix>
        When the environment variable <key> is set to <value>
        Then config <config_key> has a value of <value>

        Examples:

            | prefix          | key                             | value          | config_key       |
            | KAFKA_CONSUMER_ | KAFKA_CONSUMER_BOOTSTRAP_SERVER | localhost:9092 | bootstrap.server |
