set -e
kafka-topics --bootstrap-server kafka:29092 --list
kafka-topics --bootstrap-server kafka:29092 --create --topic input_topic --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic input_topic.dlq --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic output_topic --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --list
cat /mnt/data/input-data.txt | kafka-console-producer --bootstrap-server kafka:29092 --topic input_topic
