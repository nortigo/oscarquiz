# Oscar Quiz

## Requirements

* Python 3.8
* Django 3
* Database of your choice :)

## Setup

1. Go to `configs/`
1. Copy `.env.example` to `.env`
1. Edit `.env` and add your own credential

## Run docker

```bash
docker-compose up -d
```

## Run project

```bash
$ python manage.py runserver
```

## Changelog

2021-03-18:

* Add Pipenv and environs
* Update requirements
* Update settings
* Add docker

2020-02-21:

* Update to Django 3.0.3

2020-01-17:

* Update to Django 3.0.2
* Update requirements
* Update settings

2019-12-16:

* Update to Django 3.0
* Update requirements
* Update settings

2019-02-17:

* Update requirements
* Remove SECRET_KEY from settings

2018-06-05:

* Replace self-hosted bootstrap to CDN
* Update bootstrap to latest version
* Update HTML to fit new bootstrap version

2018-03-03:

* create unique link to send to players
* remove category model
* hide form from the other players to avoir cheating