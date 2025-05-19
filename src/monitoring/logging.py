# logging setup
"""
Logging configuration for the application.
"""
import os
import logging
import logging.config
import yaml
from datetime import datetime

def setup_logging(config_path='config/logging.yaml', default_level=logging.INFO):
    """
    Set up logging configuration
    
    Args:
        config_path (str): Path to the logging configuration file
        default_level (int): Default logging level
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d')
    log_filename = f'logs/app_{timestamp}.log'
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            try:
                config = yaml.safe_load(f)
                # Update log filename in configuration
                for handler in config.get('handlers', {}).values():
                    if 'filename' in handler:
                        handler['filename'] = log_filename
                
                logging.config.dictConfig(config)
                return
            except Exception as e:
                print(f"Error in logging configuration: {e}")
                print("Using default logging configuration")
    
    # Default configuration if file not found or error occurred
    logging.basicConfig(
        level=default_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )