docker-compose build

mkdir docker_images

docker image save -o  docker_images/db-server-auth.tar db-server-auth:latest
docker image save -o  docker_images/db-server-users.tar db-server-users:latest
docker image save -o  docker_images/db-server-data.tar db-server-data:latest
docker image save -o  docker_images/db-server-nginx.tar db-server-nginx:latest

scp docker_images/* 139:/home/vht/duonghdt/db-server