# dd

Some dbt debugging (dd) tools.

## Setup/Installation

Clone and install into a python virtual env:

```sh
$ git clone https://github.com/jeremyyeo/dd.git
$ cd dd
$ python -m venv venv
$ source venv/bin/activate
$ pip install .
$ dd --help

usage: dd [-h] {extract} ...

positional arguments:
  {extract}
    extract   Extract model specific log lines from debug logs.

options:
  -h, --help  show this help message and exit
```

## Extract

Extract model specific log lines from debug logs.

```sh
$ dd extract --model model.analytics.foo --from-file debug.log
```

Note that the debug logs normally contain multiple lines in a single thread for SQL queries - for example:

```
2025-08-14 22:54:06.906486 (Thread-4 (worker)): 22:54:06  On model.analytics.foo: create or replace transient table db.dbt_jyeo.foo



    as (select 1 c
    )

/* {"app": "dbt", "dbt_version": "2025.8.12+a8d4e26", "profile_name": "user", "target_name": "default", "node_id": "model.analytics.foo"} */;
```

In the extracted logs, we will only see log lines that start with `Thread-X`

```
2025-08-14 22:54:06.906486 (Thread-4 (worker)): 22:54:06  On model.analytics.foo: create or replace transient table db.dbt_jyeo.foo
```
