"""Simple Base API config loader"""
from os import environ as environment
import yaml

HOME = environment["HOME"]
CONFIG_PATH = HOME + "/data/seckc_mhn_api/shared/config/settings.yaml"

with open(CONFIG_PATH, "r") as f:
    SETTINGS = yaml.load(f)