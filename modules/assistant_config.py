import os
import yaml
from dpath import util as dpath_util

DEFAULT_CONFIG_PATH = "assistant_config.yml"


def get_config(dot_path_key: str, config_path: str = DEFAULT_CONFIG_PATH) -> str:
    """
    Load a field from the YAML config file using dot notation path.

    Args:
        dot_path_key: The key path to look up in the config (e.g. 'parent.child.key')
        config_path: Path to the YAML config file, defaults to assistant_config.yml

    Returns:
        str: The value for the requested key path

    Raises:
        FileNotFoundError: If config file doesn't exist
        KeyError: If ke{y path not found in config
    """
    # Get absolute path from current working directory
    abs_config_path = os.path.join(os.getcwd(), config_path)

    if not os.path.exists(abs_config_path):
        raise FileNotFoundError(f"Config file not found at {abs_config_path}")

    with open(abs_config_path) as f:
        config = yaml.safe_load(f)

    try:
        return dpath_util.get(config, dot_path_key, separator=".")
    except KeyError:
        raise KeyError(f"Key path '{dot_path_key}' not found in config")


def get_config_file(config_path: str = DEFAULT_CONFIG_PATH) -> str:
    """
    Get the config file as a string.
    """
    with open(config_path, "r") as f:
        return f.read()
