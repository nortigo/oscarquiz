# Oscar Quiz

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Play with your friends by guessing which movies will be nominated during the Oscar.

## How to play?

Rules are simple:

1. Add the nominated movies/actors/directors/etc. for each category
2. Add your friends
3. Send a unique link to each of your friend
4. Your friends guess the winner of each category before the Oscar ceremony
5. Update the board every time a winner is being revealed.

The winner is the person who has the most point.

## Requirements

* Python 3.8
* Django 4
* Postgresql or the database of your choice :)

## Setup

1. Go to `configs/`
2. Copy `.env.example` to `.env`
3. Edit `.env` and add your own credential
4. Create virtual environment (you can use [pyenv](https://github.com/pyenv/pyenv))
5. Install poetry
6. Run `poetry install`

## Run the database on docker

```bash
docker-compose up -d
```

## Run project

```bash
$ python manage.py runserver
```

## Checkout Oscar Quiz SPA project

[https://github.com/nortigo/oscarquiz_app](https://github.com/nortigo/oscarquiz_app)

## Changelog

2023-01-31:

* Update to Django 4.1.5
* Migrate to Restful API
* Remove all templates

2022-05-19:

* Replace pipenv with poetry
* Format code with black
* Update packages

2021-07-30:

* Update to Django 3.2.5

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
* Update bootstrap to the latest version
* Update HTML to fit new bootstrap version

2018-03-03:

* create unique link to send to players
* remove category model
* hide form from the other players to avoir cheating