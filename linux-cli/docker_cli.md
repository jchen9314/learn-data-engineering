# Docker Command

- list images
  
  ```shell
  docker images

  # list untagged images
  docker images -f "dangling=true"
  ```

- remove images

  ```shell
  # remove images with None tag
  docker image prune
  # remove all images
  docker rmi $(docker images -a -q)
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
  # step and remove all containers
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