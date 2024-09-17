set -e
kafka-topics --bootstrap-server kafka:29092 --list
kafka-topics --bootstrap-server kafka:29092 --create --topic input.json --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic both.json --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic router.dlq --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic IE.output.json --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic GB.output.json --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic replay_example.dlq --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic replay_example1 --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic replay_example2 --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic replay_example3 --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --list

# We add this message with no messages as a test for bug #28.
echo 'Plain text message with no header.' | kafka-console-producer --bootstrap-server kafka:29092 --topic input.json
cat /mnt/data/replay_example.dlq.txt \
  | kafka-console-producer \
        --bootstrap-server kafka:29092 \
        --property parse.headers=true \
        --property headers.delimiter=\| \
        --topic replay_example.dlq
