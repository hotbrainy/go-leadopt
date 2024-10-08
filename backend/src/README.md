# Lead Optimizer Backend with Dj!

### Create database

```bash
psql -h $(minikube ip) -p 30002 -U postgres

Password for user postgres:
```

```bash
psql (16.4 (Ubuntu 16.4-1.pgdg24.04+1))
Type "help" for help.

postgres=# CREATE DATABASE leadopt;
CREATE DATABASE
postgres=# \l
List of databases

| Name      | Owner    | Encoding | Locale Provider | Collate    | Ctype      | ICU Locale | ICU Rules | Access privileges                  |
| --------- | -------- | -------- | --------------- | ---------- | ---------- | ---------- | --------- | ---------------------------------- |
| leadopt   | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           |                                    |
| postgres  | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           |                                    |
| template0 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =c/postgres +postgres=CTc/postgres |

(3 rows)
```

### Migration and Create Superuser

```bash
kubectl exec -it $(kubectl get pods | grep django | awk '{print $1}')  -- bash
```

```bash
root@leadopt-optimizer-django-79cbddfb85-d7vgv:/app# poetry shell
Spawning shell within /root/.cache/pypoetry/virtualenvs/lead-optimizer-9TtSrW0h-py3.11
root@leadopt-optimizer-django-79cbddfb85-d7vgv:/app# . /root/.cache/pypoetry/virtualenvs/lead-optimizer-9TtSrW0h-py3.11/bin/activate
```

```bash
(lead-optimizer-py3.11) root@leadopt-optimizer-django-79cbddfb85-d7vgv:/app# python manage.py migrate

Operations to perform:
Apply all migrations: admin, auth, contenttypes, lo_interpreter, lo_profile, lo_user, sessions
Running migrations:
No migrations to apply.

```

```bash
(lead-optimizer-py3.11) root@leadopt-optimizer-django-79cbddfb85-d7vgv:/app# python manage.py createsuperuser

Username: nic
Email address: nic@aerialempire.com
Password:
Password (again):
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: Y
Superuser created successfully.

```
RUN Redis
docker pull redis
docker run -d -p 6379:6379 -v redis-data:/data redis