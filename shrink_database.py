# Import necessary libraries
import pyodbc  # Library to connect to databases using ODBC
import logging  # Library for logging information, warnings, and errors
import yaml  # Library to read and parse YAML configuration files

# Configure logging to display messages with a specific format and level
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file):
    """
    Load the configuration from a YAML file.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        dict: The loaded configuration as a dictionary.
    """
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)  # Parse and return the YAML content as a dictionary

def shrink_database(config):
    """
    Shrink the specified databases as defined in the configuration.

    Args:
        config (dict): The loaded configuration containing database details.
    """
    conn = None  # Initialize connection variable
    cursor = None  # Initialize cursor variable

    try:
        # Iterate over each database defined in the configuration
        for database in config['database']['databases']:
            logging.info(f"Connecting to the database {database}...")  # Log connection attempt
            conn = pyodbc.connect(
                f"Driver={config['database']['driver']};"  # Specify ODBC driver
                f"Server={config['database']['server']};"  # Specify server address
                f"Database={database};"  # Specify database name
                f"UID={config['database']['uid']};"  # Specify user ID
                f"PWD={config['database']['pwd']};",  # Specify password
                autocommit=True  # Set autocommit to True for immediate effect of commands
            )
            
            cursor = conn.cursor()  # Create a cursor object to execute SQL commands
            
            # Prepare and execute the shrink command
            shrink_sql = f'DBCC SHRINKDATABASE ({database});'
            logging.info(f"Executing shrink command for database {database}...")  # Log execution
            cursor.execute(shrink_sql)  # Execute the shrink command
            logging.info(f"Shrink command executed successfully for database: {database}.")  # Log success

    except pyodbc.Error as e:
        logging.error(f"Failed to shrink database: {str(e)}")  # Log any errors that occur
    finally:
        # Ensure resources are released regardless of success or failure
        if cursor:  # Check if the cursor was created
            cursor.close()  # Close the cursor
        if conn:  # Check if the connection was created
            conn.close()  # Close the connection

# Entry point of the script
if __name__ == "__main__":
    config = load_config('config.yaml')  # Load the configuration from the specified file
    shrink_database(config)  # Call the function to shrink databases based on the loaded configuration
