docker-compose build
docker image save -o  producer_kafka-zookeeper.tar confluentinc/cp-zookeeper:7.3.2
docker image save -o  producer_kafka-kafka.tar confluentinc/cp-kafka:7.3.2

scp producer_kafka-zookeeper.tar 139:/home/vht/duonghdt/db-server/docker_images
scp producer_kafka-kafka.tar 139:/home/vht/duonghdt/db-server/docker_images