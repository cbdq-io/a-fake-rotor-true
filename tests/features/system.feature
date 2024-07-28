
@system
Feature: System Tests
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

    Scenario Outline: System Test Outcomes
        Given the TestInfra host with URL "docker://router" is ready
        When the TestInfra command is "curl --fail http://localhost:8000"
        Then the TestInfra command return code is 0
        And the TestInfra command stdout contains "<expected_output>"

        Examples:
        | expected_output                            |
        | consumer_message_count_total 6.0           |
        | consumer_message_committed_count_total 6.0 |
        | producer_message_count_total 6.0           |
