set -e
kafka-topics --bootstrap-server kafka:29092 --list
kafka-topics --bootstrap-server kafka:29092 --create --topic input --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic input.dlq --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic IE.output --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic GB.output --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --list
TIMESTAMP="$( date -uIseconds )Z"
sed "s/^/timestamp_iso8601:${TIMESTAMP}\t/" /mnt/data/input-data.txt | kafka-console-producer --bootstrap-server kafka:29092 --topic input --property parse.headers=true
