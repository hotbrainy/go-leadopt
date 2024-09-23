# Lead Optimizer Backend with Dj!

### Create database

`psql -h $(minikube ip) -p 30002 -U postgres`
Password for user postgres: 
psql (16.4 (Ubuntu 16.4-1.pgdg24.04+1))
Type "help" for help.

postgres=# CREATE DATABASE leadopt;
CREATE DATABASE
postgres=# \l
                                                      List of databases
   Name    |  Owner   | Encoding | Locale Provider |  Collate   |   Ctype    | ICU Locale | ICU Rules |   Access privileges   
-----------+----------+----------+-----------------+------------+------------+------------+-----------+-----------------------
 leadopt   | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
 postgres  | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | 
 template0 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |            |           | =c/postgres          +
           |          |          |                 |            |            |            |           | postgres=CTc/postgres
(3 rows)

### Migration and Create Superuser

`kubectl exec -it $(kubectl get pods | grep django | awk '{print $1}')  -- bash`

root@leadopt-optimizer-django-76845fb7c6-kcxd6:/app# `poetry shell`
Spawning shell within /root/.cache/pypoetry/virtualenvs/lead-optimizer-9TtSrW0h-py3.11
root@leadopt-optimizer-django-76845fb7c6-kcxd6:/app# . /root/.cache/pypoetry/virtualenvs/lead-optimizer-9TtSrW0h-py3.11/bin/activate

(lead-optimizer-py3.11) root@leadopt-optimizer-django-79cbddfb85-d7vgv:/app# `python manage.py migrate`
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, lo_interpreter, lo_profile, lo_user, sessions
Running migrations:
  No migrations to apply.

(lead-optimizer-py3.11) root@leadopt-optimizer-django-76845fb7c6-kcxd6:/app# `python manage.py createsuperuser`
Username: nic
Email address: nic@aerialempire.com
Password: 
Password (again): 
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: Y
Superuser created successfully.
(lead-optimizer-py3.11) root@leadopt-optimizer-django-76845fb7c6-kcxd6:/app# 


