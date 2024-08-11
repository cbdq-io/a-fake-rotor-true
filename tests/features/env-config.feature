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

    Scenario Outline: Boolean Environment Variable
        Given an EnvironmentConfig object
        When the environment variable <key> is set to <value>
        Then env config boolean for <key> is <boolean>

        Examples:

            | key       | value          | boolean    |
            | BOOL_TEST | Yarp           | ValueError |
            | BOOL_TEST | True           | True       |
            | BOOL_TEST | TRUE           | True       |
            | BOOL_TEST | T              | True       |
            | BOOL_TEST | 1              | True       |
            | BOOL_TEST | Yes            | True       |
            | BOOL_TEST | YES            | True       |
            | BOOL_TEST | Y              | True       |
            | BOOL_TEST | Narp           | ValueError |
            | BOOL_TEST | False          | False      |
            | BOOL_TEST | FALSE          | False      |
            | BOOL_TEST | F              | False      |
            | BOOL_TEST | 0              | False      |
            | BOOL_TEST | No             | False      |
            | BOOL_TEST | NO             | False      |
            | BOOL_TEST | N              | False      |
