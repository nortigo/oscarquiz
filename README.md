# Oscar Quiz

## Requirements

* Python 3+
* Django 3+
* Database of your choice :)

## Setup

Go to `configs/`

1. Copy `project_config.yml.sample` to `project_config.yml`
1. Edit `project_config.yml` and add your own credential
1. Copy `uwsgi.ini.sample` to `uwsgi.ini`
1. Edit `uwsgi.ini` and set `OSCARQUIZ_CONFIG` path to YML config

## Run project

```bash
$ OSCARQUIZ_CONFIG=/path/to/yml/configs python manage.py runserver
```

You can ommit `OSCARQUIZ_CONFIG` If you keep `project_config.yml` in the configs folder.

```bash
$ python manage.py runserver
```

## Changelog

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