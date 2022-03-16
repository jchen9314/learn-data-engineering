# Docker Command

## Docker images

- list images
  
  ```shell
  docker images

  # list untagged images
  docker images -f "dangling=true"
  ```

- pull image: download image from docker hub

  ```shell
  # docker pull [image]
  docker pull mysql
  ```

- search image

  ```shell
  docker search mysql

  # see the layers inside an image (an image is built on several layers)
  docker image history REPO_NAME:TAG_NAME
  docker image history IMAGE_ID

  # check details about certain image
  docker image inspect IMAGE_ID
  ```

- remove images

  - __before removing images, should stop running containers first__
    - `docker container rm CONTAINER_ID`

  ```shell
  # remove images with None tag
  docker image prune
  # remove all images
  docker rmi $(docker images -a -q)
  ```

## Docker container

- run container
  
  - if launching multiple microservices, use different local ports
  - `-d`: detached mode, give the terminal window back to us

  ```shell
  docker container run -p 5000:5000 REPO_NAME/IMAGE_NAME:TAG/VERSION
  # -p: publish
  # 5000:5000 localhost port: container port
  # -p 5000:5000 publish a container port onto a local port
  ```

- operations on container
  - `CONTAINER_ID`: first 3-4 chars of the actual container id

  ```shell
  # check logs
  docker container logs CONTAINER_ID
  # pause container
  docker container pause CONTAINER_ID
  # stop running container
  docker container stop CONTAINER_ID
  # kill running container: kill will immediately stop the container
  docker container kill CONTAINER_ID
  # check details
  docker container inspect CONTAINER_ID
  # remove all stopped containers
  docker container prune
  ```

- list container (running containers by default)

  ```shell
  docker ps
  # -a: all, list all containers
  docker ps -a
  ```

  - `docker ps` lists all running containers in docker engine
  - `docker-compose ps` lists containers related to __images declared in docker-compose file__

- remove container

  ```shell
  # remove all exited containers
  docker rm $(docker ps -a -f status=exited -q)
  # stop and remove all containers
  docker stop $(docker ps -a -q)
  docker rm $(docker ps -a -q)
  ```

- run docker-compose

  ```shell
  docker-compose up -d
  # -d: detached mode, means the terminal is back to us
  ```

## Docker system

```shell
# show docker disk usage
docker system df
# get real-time events from the server
docker system events
# remove all stopped containers and all images w/o at least one container associated with them
docker system prune -a
```

```shell
# check stats of container
docker container stats CONTAINER_ID
# set container configuration
# memory: 512MB, cpu: 50000, total is 100000
docker container run -m 512m --cpu-quota=50000
```

## Reference

1. https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes
2. https://www.edureka.co/blog/interview-questions/docker-interview-questions/
3. https://www.udemy.com/course/devops-with-docker-kubernetes-and-azure-devops/learn/lecture/18087007?start=0#content