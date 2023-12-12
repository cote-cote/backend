#!/bin/sh

container_name=backend-mysql-1
username=$DB_USER
password=$DB_PASSWORD
db_name=$DB_NAME

docker exec $container_name \
  bash -c "mysql -h localhost -P 3306 --protocol=tcp -u$username -p$password \
   -e \"CREATE DATABASE IF NOT EXISTS $db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;\"; exit;"
