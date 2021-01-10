import json
import configuration.environment_config as env_config


def load_service_config():
    """ Returns the current active services """
    with open(env_config.SERVICE_CONFIG_PATH, "r") as config_file:
        service_config = json.load(config_file)
    return service_config["ACTIVE_SERVICES"]


def load_timeout():
    """ Returns the maximum processing time allowed """
    with open(env_config.SERVICE_CONFIG_PATH, 'r') as config_file:
        service_config = json.load(config_file)
    return service_config["TIMEOUT"]

