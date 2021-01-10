import os

# Api Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 5000))

# Configuration folder
DEFAULT_CONFIG_DIR = os.getenv("DEFAULT_CONFIG_DIR", "/mnt/config/")

# Path to active services' configuration
SERVICE_CONFIG_PATH = os.path.join(DEFAULT_CONFIG_DIR, "json", "service_config.json")