# -*- coding: utf-8 -*-
import yaml


def load_yml_config(config_file):
    with open(config_file, 'r') as stream:
        return yaml.safe_load(stream)
