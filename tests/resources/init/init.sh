set -e
kafka-topics --bootstrap-server kafka:29092 --list
kafka-topics --bootstrap-server kafka:29092 --create --topic input.json --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic router.dlq --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic IE.output.json --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic GB.output.json --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic example1 --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --list

# We add this message with no messages as a test for bug #28.
echo 'Plain text message with no header.' | kafka-console-producer --bootstrap-server kafka:29092 --topic input.json
