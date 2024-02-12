# logs.py

import os
from datetime import datetime

def create_log_directory():
    log_directory = 'data/logs/'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

def get_log_filename():
    now = datetime.now()
    log_directory = 'data/logs/'
    return f"{log_directory}{now.strftime('%Y-%m-%d_%H')}.log"

def log_action(action, success=True, error_message=None):
    log_filename = get_log_filename()
    with open(log_filename, 'a') as log_file:
        log_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Action: {action}\n")
        log_file.write(f"Success: {'Yes' if success else 'No'}\n")
        if not success and error_message:
            log_file.write(f"Error: {error_message}\n")
        log_file.write("\n")

