#inventory-service

##build docker image
>docker build . -t inventory-service:latest

##run docker image in a container
>docker run -itd --network redis_default -p 8000:8000 --name inventory-service-container -e inventory-db-name=inventory-db -e inventory-db-pass=invDbPass  -e eventq-host-name=eventq -e eventq-pass=eventqPass inventory-service:latest