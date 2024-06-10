import yaml
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())


def load_config(config_path=None):
    """Loads configuration from a YAML file and supplements it with environment variables."""

    if config_path is None:
        base_path = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(base_path, 'config', 'config.yaml')

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    # Add API key from environment variable to the config if it's present
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        config['api'] = {'openai_key': api_key}
    return config
