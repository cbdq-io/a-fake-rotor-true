set -e
kafka-topics --bootstrap-server kafka:29092 --list
kafka-topics --bootstrap-server kafka:29092 --create --topic input --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic input.dlq --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic IE.output --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic GB.output --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --list
cat /mnt/data/input-data.txt | kafka-console-producer --bootstrap-server kafka:29092 --topic input
