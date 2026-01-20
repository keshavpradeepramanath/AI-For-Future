import logging
import logging.config
import yaml

def setup_logger():
    with open("config/logging.yaml", "r") as file:
        config = yaml.safe_load(file)

    logging.config.dictConfig(config)
    return logging.getLogger("travel_agent")
