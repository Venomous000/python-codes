1️ Docker Overview (Concepts)
==============================

-   **Docker**: runs applications in **isolated containers**, using host kernel

-   **Container**: a running instance of an image

-   **Image**: blueprint / snapshot of your application + dependencies

-   **Volume**: persistent storage mapped between host & container

-   **Namespace**: isolates process IDs, filesystem, network, etc.

-   **cgroups**: resource limits for CPU/memory/disk

-   **Daemon**: `dockerd` --- background service that manages containers and images

    -   Usually runs automatically (`systemctl start docker`)

    -   All `docker` commands talk to it

* * * * *

2️ Docker Daemon Commands
==========================

| Task | Command | Notes |
| --- | --- | --- |
| Start Docker | `sudo systemctl start docker` | Start daemon manually |
| Stop Docker | `sudo systemctl stop docker` | Stop daemon |
| Restart Docker | `sudo systemctl restart docker` | Restart daemon |
| Check status | `sudo systemctl status docker` | See if daemon is running |
| Enable at boot | `sudo systemctl enable docker` | Daemon starts automatically |
| Docker info | `docker info` | Shows daemon version, containers, images, storage driver |

> Most of the time you **don't touch the daemon manually** --- it runs automatically.

* * * * *

3️ Docker Images (Blueprints)
==============================

| Command | Description |
| --- | --- |
| `docker images` | List all images |
| `docker pull <image>` | Download image from Docker Hub |
| `docker build -t <name> .` | Build image from Dockerfile in current folder |
| `docker rmi <image>` | Remove image |
| `docker tag <image> <name>:<tag>` | Add version/tag to image |
| `docker inspect <image>` | Show image metadata/layers |
| `docker history <image>` | Show image layers/history |

* * * * *

4️ Docker Containers (Running apps)
====================================

| Command | Description |
| --- | --- |
| `docker ps` | List **running** containers |
| `docker ps -a` | List **all** containers |
| `docker run -it <image> bash` | Run container interactively |
| `docker run -d --name <name> <image>` | Run container in background (detached) |
| `docker start -ai <name>` | Start a stopped container and attach |
| `docker stop <name>` | Stop running container |
| `docker restart <name>` | Restart container |
| `docker rm <name>` | Delete container |
| `docker exec -it <name> bash` | Enter running container (interactive) |
| `docker logs <name>` | Show container logs |
| `docker logs -f <name>` | Follow container logs in real-time |
| `docker inspect <name>` | Show container metadata (namespace, mounts, IP, etc.) |
| `docker stats` | Show live CPU/memory usage per container |
| `docker attach <name>` | Attach to running container terminal |

* * * * *

5️ Docker Volumes (Persistent storage)
=======================================

| Command | Description |
| --- | --- |
| `docker volume ls` | List volumes |
| `docker volume create <name>` | Create a volume |
| `docker volume inspect <name>` | Inspect volume path/details |
| `docker run -v <host_path>:<container_path>` | Map host folder to container folder |
| `docker run -v <volume_name>:<container_path>` | Map named volume to container folder |
| `docker volume rm <name>` | Remove volume |

> Use volumes to **persist logs, databases, or project files** outside container lifecycle.

* * * * *

6️ Docker Networking (Basics)
==============================

| Command | Description |
| --- | --- |
| `docker network ls` | List networks |
| `docker network inspect <name>` | Show network details |
| `docker run --network=<network>` | Connect container to specific network |
| `docker network create <name>` | Create custom bridge network |

> Most beginner setups use default `bridge` network. Custom networks needed for multi-container communication.

* * * * *

7️ Resource Limits (cgroups)
=============================

| Command | Description |
| --- | --- |
| `docker run --memory="500m" <image>` | Limit RAM to 500MB |
| `docker run --cpus="1.5" <image>` | Limit to 1.5 CPU cores |
| `docker run --memory="500m" --cpus="1.5" <image>` | Limit both CPU & RAM |

> Default: container can use **all host CPU and memory**.

* * * * *

8️ Docker Cleanup
==================

| Command | Description |
| --- | --- |
| `docker container prune` | Delete all stopped containers |
| `docker image prune` | Delete dangling (unused) images |
| `docker volume prune` | Delete unused volumes |
| `docker system prune` | Delete stopped containers, unused images, volumes, and networks |
| `docker system df` | Show disk usage by Docker |

* * * * *

9️ Docker Compose (Multi-container apps)
=========================================

-   File: `docker-compose.yml`

-   Example:

```
version: "3"
services:
  app:
    build: .
    volumes:
      - .:/app
    ports:
      - "5000:5000"
    command: python3 Lists/checking_red.py
  redis:
    image: redis:7`
```

-   Commands:

| Command | Description |
| --- | --- |
| `docker-compose up` | Start all services |
| `docker-compose up -d` | Start in background |
| `docker-compose down` | Stop and remove containers |
| `docker-compose build` | Rebuild images |
| `docker-compose logs` | View logs of all services |
| `docker-compose exec <service> bash` | Enter a service container |

* * * * *

Most commonly used daily Docker commands (practical workflow)
================================================================

1.  **Build image**

`docker build -t python_training_app .`

2.  **Run container interactively**

`docker run -it -v $(pwd):/app python_training_app bash`

3.  **Run a script directly**

`docker run -it -v $(pwd):/app python_training_app python3 Lists/checking_red.py`

4.  **Check running containers**

`docker ps`

5.  **Stop a container**

`docker stop <container_id_or_name>`

6.  **Delete container**

`docker rm <container_id_or_name>`

7.  **Check images**

`docker images`

8.  **Delete unused images**

`docker rmi <image>`

9.  **Follow logs**

`docker logs -f <container>`

10.  **Check resource usage**

`docker stats`

11.  **Clean up everything**

`docker system prune`

12.  **Docker Compose multi-container**

```
docker-compose up -d
docker-compose down
docker-compose logs -f
docker-compose exec app bash`
```

* * * * *

10️ Key Docker Best Practices (Beginner → Daily Use)
=====================================================

-   Always use **Dockerfile** for building images

-   Use **volumes** for any data you want to persist

-   Containers are **ephemeral** → never rely on manual edits inside container

-   Use **tags** for images (versions)

-   Limit resources for production containers

-   Regularly prune stopped containers/images to save space

-   Prefer **docker-compose** for multi-container setups

* * * * *

**Beginner mental model:**

```
Host OS (kernel)
   │
Docker Daemon (manages)
   │
Images (blueprints)
   │
Containers (running apps) → isolated by namespaces + limited by cgroups
   │
Volumes → persistent storage synced with host
```