import logging.config
import os
import yaml


def setup_logging(path='config/logging.yaml',
                  level=logging.INFO,
                  env_key='LOG_CFG'):

    value = os.getenv(env_key, path)
    if value and os.path.exists(value):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)
