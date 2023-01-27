# vle-api

[![CI](https://github.com/sunnamed434/UIElementsUnturned/workflows/CI/badge.svg)](https://github.com/CHAMPMOON/vle-api/actions)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy.readthedocs.io/en/stable/)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

## Docker

```sh
$ docker-compose up -d
```

## Poetry hash problem in docker
If you ran the command:
```sh
$ docker-compose up -d
```
and you have problems with hash, do these commands:
```sh
$ docker-compose down
$ poetry cache clear . --all
$ rm poetry.lock
$ poetry install --no-root
$ docker-compose up -d
```
