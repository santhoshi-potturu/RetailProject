import configparser
import os
from pyspark import SparkConf


# Helper function to get absolute path for configs/
def get_config_path(filename):
    # Go up one level from 'lib' folder → project root → configs/
    base_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_path, "configs", filename)


# Load the application configs into a Python dictionary
def get_app_config(env):
    config = configparser.ConfigParser()
    config_path = get_config_path("application.conf")
    config.read(config_path)

    app_conf = {}
    if env not in config:
        raise KeyError(f"Environment '{env}' not found in {config_path}")

    for (key, val) in config.items(env):
        app_conf[key] = val
    return app_conf


# Load PySpark configs and create a SparkConf object
def get_pyspark_config(env):
    config = configparser.ConfigParser()
    config_path = get_config_path("pyspark.conf")
    config.read(config_path)

    pyspark_conf = SparkConf()
    if env not in config:
        raise KeyError(f"Environment '{env}' not found in {config_path}")

    for (key, val) in config.items(env):
        pyspark_conf.set(key, val)
    return pyspark_conf
