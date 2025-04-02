"""Example configuration settings - Copy to config.py and edit."""

# Camera connection settings
CAMERA_CONFIG = {
    "ip": "192.168.1.60",  # Replace with your camera's IP
    "port": 80,  # HTTP port - usually 80
    "username": "admin",  # Camera username
    "password": "password",  # Camera password
}

# Directory for storing WSDL files
WSDL_DIR = "./wsdl"

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"
