# Kafka Docker Image Usage Guide

https://github.com/apache/kafka/blob/trunk/docker/examples/README.md

https://github.com/apache/kafka/blob/trunk/docker/examples/jvm/single-node/plaintext/docker-compose.yml

### Check configuration of YAML file
    docker compose config
### Single Node



    docker compose -f docker/examples/jvm/single-node/plaintext/docker-compose.yml up -d
   

   docker compose logs -f