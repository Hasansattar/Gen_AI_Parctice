# POETRY COMMANDS

 **1) poetry add sqlmodel fastapi**
**2) poetry run uvicorn 03_dev_containers.main:app --host 127.0.0.1 --port 8000**







# DOCKER COMMANDS


#### Building the Image:
```
docker build -f Dockerfile.dev -t my-dev-image .
```

#### Check Images:
```docker images```

#### Verify the config:
```docker inspect my-dev-image```


#### Running the Container:
```docker run -d --name dev-cont1 -p 8000:8000 my-dev-image```

#### Check container logs
```docker logs container_name -f```


#### List Running Containers
``` docker ps```


#### Running the Container and start a Bash shell:
##### it will run the container and will take you inside the container 
``` docker run -it my-dev-image /bin/bash```


#### Running the Container At the Backgroud of Terminal and start a Bash shell:
##### If you want to leave the container running but detach from it, you should have started the container with the -d flag for detached mode.
``` docker run -d -it my-dev-image /bin/bash```



#### Exit the running container
```exit ```


#### Opening the command line in the container:
```docker exec -it dev-cont1_name  /bin/bash```


#### Stop the running container
```docker stop container_ID ```



#### Remove the running container
```docker rm container_ID ```

