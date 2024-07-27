Feature: System Tests
    Scenario: Verify the Container Build
        Given the TestInfra host with URL "docker://router" is ready
        When the TestInfra user is "router"
        And the TestInfra group is "router"
        And the TestInfra file is /home/router
        Then the TestInfra user is present
        And the TestInfra user group is router
        And the TestInfra user home is /home/router
        And the TestInfra user shell is /usr/sbin/nologin
        And the TestInfra group is present
        And the TestInfra file type is directory
        And the TestInfra file is present
        And the TestInfra file mode is 0o700
        And the TestInfra pip check is OK

    Scenario: Docker Command File
        Given the TestInfra host with URL "docker://router" is ready
        When the TestInfra file is /home/router/router.py
        Then the TestInfra file owner is router
        And the TestInfra file group is router
        And the TestInfra file is executable

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
