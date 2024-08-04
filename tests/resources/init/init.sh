set -e
kafka-topics --bootstrap-server kafka:29092 --list
kafka-topics --bootstrap-server kafka:29092 --create --topic input.json --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic router.dlq --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic IE.output.json --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --create --topic GB.output.json --if-not-exists
kafka-topics --bootstrap-server kafka:29092 --list
