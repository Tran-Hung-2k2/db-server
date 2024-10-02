docker-compose build

docker image save -o  producer_kafka-kafka_producer.tar producer_kafka-kafka_producer:latest

scp producer_kafka-kafka_producer.tar 139:/home/vht/duonghdt/db-server/docker_images
