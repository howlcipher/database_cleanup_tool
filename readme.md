# Database Cleanup Tool

This tool is designed to clean up and shrink SQL Server databases based on specified configurations. It processes tables exceeding a defined row threshold and shrinks the database to optimize storage.

## Features

- Connects to multiple SQL Server databases.
- Processes tables based on row thresholds.
- Shrinks databases after processing.

## Requirements

- Python 3.x
- PyODBC
- PyYAML

## Installation

1. Clone this repository or download the source code.
2. Install the required Python packages using `requirements.txt`:
```pip install -r requirements.txt```
    Contents of requirements.txt
    ``` 
    pyodbc
    pyyaml
    ```
## Configuration
The tool requires a configuration file named config.yaml to run. Below is an example configuration:

yaml
```
database:
  driver: '{ODBC Driver 17 for SQL Server}'
  server: 'SERVER'
  databases:
    - 'DATABASE1'
    - 'DATABASE2'  # Add more databases as needed
  uid: 'USERNAME'
  pwd: 'PASSWORD'
logging:
  file: 'db_cleanup.log'
row_threshold: 1000
Configuration Options
driver: ODBC driver for SQL Server.
server: SQL Server address.
databases: List of databases to process.
uid: Database user ID.
pwd: Database password.
logging.file: Path to the log file.
row_threshold: Number of rows to use as a threshold for processing tables.
```
## Usage
Run the script using the command: ```python main.py```
This will process the databases specified in the config.yaml file.

## Building the Executable
To create a standalone executable (.exe) from this project, follow these steps:

Install PyInstaller if you haven't already: ```pip install pyinstaller```
Navigate to your project directory where main.py is located.

Run the following command to build the executable: ```pyinstaller --onefile --add-data "config.yaml;." main.py```
- --onefile: Bundles everything into a single executable.
- --add-data "config.yaml;.": Includes the config.yaml file in the same directory as the executable.
After running the command, locate the dist folder created in your project directory. Inside this folder, you will find the main.exe file.

Run the executable from the command line or by double-clicking it. Ensure the config.yaml file is in the same directory as the executable.

## Notes
The config.yaml file should be adjusted as needed for different database configurations before running the executable.
Make sure you have the necessary permissions to access and modify the databases specified in your configuration.