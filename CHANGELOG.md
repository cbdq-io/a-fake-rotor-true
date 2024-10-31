# Changelog


## 0.4.5 (2024-10-31)

### Fix

* New release also fixes CVE-2023-49462. [Ben Dalling]

* Bump Sentry SDK from 2.16.0 to 2.17.0. [Ben Dalling]


## 0.4.4 (2024-10-11)

### Fix

* Update (amongst other Python packages) confluent-kafka from 2.5.3 to 2.6.0. [Ben Dalling]


## 0.4.3 (2024-10-08)

### Fix

* Rebuild also removes CVE-2024-41096, CVE-2024-42228, CVE-2024-42314, CVE-2024-44940, CVE-2024-44974, CVE-2024-44983, CVE-2024-44985, CVE-2024-44986, CVE-2024-44987, CVE-2024-44998, CVE-2024-44999, CVE-2024-45026, CVE-2024-46673, CVE-2024-46674, CVE-2024-46722, CVE-2024-46723, CVE-2024-46724, CVE-2024-46725, CVE-2024-46731, CVE-2024-46738, CVE-2024-46740, CVE-2024-46743, CVE-2024-46744, CVE-2024-46746, CVE-2024-46747, CVE-2024-46756, CVE-2024-46757, CVE-2024-46758, CVE-2024-46759, CVE-2024-46782, CVE-2024-46798, CVE-2024-46800, CVE-2024-46804, CVE-2024-46814, CVE-2024-46818, CVE-2024-46821, CVE-2024-46844, CVE-2024-46849, CVE-2024-46852, CVE-2024-46853, CVE-2024-46854, CVE-2024-46858, CVE-2024-46859 and CVE-2024-46865 from the image. [Ben Dalling]

* Bump Sentry SDK from 2.14.0 to 2.15.0. [Ben Dalling]


## 0.4.2 (2024-09-24)

### Changes

* Bump Prometheus Client version from 0.20.0 to 0.21.0. [Ben Dalling]


## 0.4.1 (2024-09-19)

### Fix

* Rebuild to remove CVE-2024-45490, CVE-2024-45491 and CVE-2024-45492 from the image. [Ben Dalling]


## 0.4.0 (2024-09-17)

### Fix

* Rename destination_topic to destination_topics. [Ben Dalling]


## 0.3.6 (2024-09-15)

### Fix

* Rebuild to fix CVE-2023-25652, CVE-2023-29007, CVE-2024-32002, CVE-2024-32004 and CVE-2024-32465. [Ben Dalling]


## 0.3.5 (2024-09-10)

### Changes

* Bump Sentry SDK from 2.13.0 to 2.14.0. [Ben Dalling]


## 0.3.4 (2024-09-03)

### Changes

* Bump Confluent Kafka version from 2.5.0 to 2.5.3. [Ben Dalling]


## 0.3.3 (2024-09-02)

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


