# Docker Command

- list images
  
  ```shell
  docker images

  # list untagged images
  docker images -f "dangling=true"
  ```

- remove images with `<None>` tag:

  ```shell
  docker rmi $(docker images -f "dangling=true" -q) --force
  ```

- list container (running containers by default)

  ```shell
  docker ps
  # -a: all, list all containers
  ```

  - `docker ps` lists all running containers in docker engine
  - `docker-compose ps` lists containers related to **images declared in docker-compose file**
