import yaml
import os

HOME = os.getenv("HOME")
CONFIG_FOLDER = HOME + "/.logbuch"
CONFIG = CONFIG_FOLDER + '/config.yml'
INITIAL_CONFIG = "task_repo: " + CONFIG_FOLDER + "/data/current.json \n"


def create_config_if_not_exists():
    if not os.path.exists(CONFIG_FOLDER):
        os.makedirs(CONFIG_FOLDER)
    if not os.path.exists(CONFIG):
        with open(CONFIG, 'w') as f:
            f.write(INITIAL_CONFIG)


def read_config(config_file):
    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


class Conf(object):
    def __init__(self, logbuch_path):
        create_config_if_not_exists()
        self.logbuch_path = logbuch_path
        config_dict = read_config(CONFIG)
        self.task_repo_file_path = config_dict['task_repo']
