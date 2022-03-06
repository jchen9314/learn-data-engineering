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

  # see the layers inside an image
  docker image history REPO_NAME:TAG_NAME
  docker image history IMAGE_ID

  # check details about certain image
  docker image inspect IMAGE_ID
  ```

- remove images

  - before removing images, should stop running containers first
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
  docker run -p 5000:5000 REPO_NAME/IMAGE_NAME:TAG/VERSION
  # -p: publish
  # 5000:5000 localhost port: container port
  # -p 5000:5000 publish a container port onto a local port
  ```

- operations on container
  - `CONTAINER_ID`: first 4 chars of the actual container id

  ```shell
  # check logs
  docker logs CONTAINER_ID
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
  - `docker-compose ps` lists containers related to **images declared in docker-compose file**

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

## Reference

1. https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes
2. https://www.edureka.co/blog/interview-questions/docker-interview-questions/