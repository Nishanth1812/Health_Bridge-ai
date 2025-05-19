
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Preventive Healthcare Chatbot"
    openai_api_key: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
"""
Configuration utility functions.
"""
import os
import yaml
import logging

logger = logging.getLogger(__name__)

def load_config(config_path):
    """
    Load configuration from YAML file.
    
    Args:
        config_path (str): Path to the configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            return config
        else:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return {}
    except Exception as e:
        logger.error(f"Error loading config from {config_path}: {str(e)}")
        return {}
