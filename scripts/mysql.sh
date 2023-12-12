#!/usr/bin/env sh

docker-compose exec mysql mysql -u$DB_USER -p$DB_PASSWORD
