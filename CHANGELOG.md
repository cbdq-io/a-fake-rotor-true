# Changelog


## 0.1.1

### New

* Documentation of DLQ message headers. [Ben Dalling]

### Fix

* Ensure that the container catches signals correctly and shutsdown gracefully. [Ben Dalling]

* Ensure metrics for DLQ messages are recorded correctly. [Ben Dalling]

* Allow Kafka metrics to be prefixed. [Ben Dalling]

* We have correct headers on messages on the DLQ topic. Also ensure we handle deserialisation errors properly. [Ben Dalling]

* Ensure input message headers and keys and replicated in output messages. [Ben Dalling]


## 0.1.0 (2024-07-28)

### New

* Add documentation about the rules configuration. [Ben Dalling]

* Add non_routed_error_count to Prometheus metrics. [Ben Dalling]

* Route Kafka topics based upon configurable rules. [Ben Dalling]

* Add Prometheus metrics. [Ben Dalling]

* Add Trivy scan. [Ben Dalling]

* Add a Docker Kafka broker as part of the test rig. [Ben Dalling]

* Add the EnvironmentConfig class. [Ben Dalling]

### Other

* Fix; dev: Rename the CI workflow to Pipeline. [Ben Dalling]

* Initial commit. [Ben Dalling]


