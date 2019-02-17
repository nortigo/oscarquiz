# Oscar Quiz

## Requirements

* Python 3+
* Django 2+
* Database of your choice :)

## Setup

Go to `configs/`

1. Copy `project.env.sample` to `project.env`
1. Edit `project.env` and add your own credential
1. Copy `uwsgi.ini.sample` to `uwsgi.ini`
1. Edit `uwsgi.ini` and add the same credential from `project.env`

## Changelog

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