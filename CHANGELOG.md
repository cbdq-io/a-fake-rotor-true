# Changelog


## 0.3.3

### New

* Publish (and check) the UID/GID of the container user. [Ben Dalling]

### Fix

* Rebuild to clear CVE-2024-41030, CVE-2024-41046, CVE-2024-41049, CVE-2024-41057, CVE-2024-41058, CVE-2024-41070, CVE-2024-41073, CVE-2024-41090, CVE-2024-41091, CVE-2024-42271, CVE-2024-42284, CVE-2024-42285, CVE-2024-42301, CVE-2024-42302, CVE-2024-42313, CVE-2024-43858, CVE-2024-43900 and CVE-2024-44934. [Ben Dalling]


## 0.3.2 (2024-08-22)

### New

* Add code of conduct. [Ben Dalling]

### Fix

* CVE-2024-5171. [Ben Dalling]


## 0.3.1 (2024-08-15)

### Changes

* Bump Sentry SDK from 2.12.0 to 2.13.0. [Ben Dalling]

### Fix

* Add a description to the container. [Ben Dalling]

* Patch an edge case issue when DLQ mode is on. [Ben Dalling]


## 0.3.0 (2024-08-12)

### New

* Allow valid messages to be dropped if required. [Ben Dalling]


## 0.2.1 (2024-08-11)

### Fix

* Ensure the router fails completely if unable to produce a message. [Ben Dalling]


## 0.2.0 (2024-08-11)

### New

* Add documentation, tests and logic for DLQ replaying. [Ben Dalling]

* Add contributing guidelines. [Ben Dalling]

### Fix

* Attempt to upgrade libpq-dev and libpq5 to fix CVE-2024-7348. [Ben Dalling]


## 0.1.2 (2024-08-06)

### Fix

* Stop the router crashing a message has no headers. [Ben Dalling]


## 0.1.1 (2024-08-04)

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


