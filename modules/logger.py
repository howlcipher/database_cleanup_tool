import logging

class Logger:
    def __init__(self, log_file, server, database_name=None):
        """
        Initialize the Logger with log file, server, and optional database name.

        Args:
            log_file (str): The path to the log file where logs will be written.
            server (str): The name or IP address of the server being logged.
            database_name (str, optional): The name of the database (if applicable).
        """
        self.log_file = log_file  # Store the log file path
        self.server = server  # Store the server information
        self.database_name = database_name  # Store the database name (optional)
        self.setup_logger()  # Call method to set up logging configuration

    def setup_logger(self):
        """
        Set up the logging configuration.
        This method configures the logging level, format, and handlers.
        """
        logging.basicConfig(
            level=logging.INFO,  # Set the logging level to INFO
            format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format
            handlers=[  # Specify the handlers for logging output
                logging.FileHandler(self.log_file),  # Log messages to the specified log file
                logging.StreamHandler()  # Optional: also log messages to the console
            ]
        )

    def info(self, message):
        """
        Log an informational message.

        Args:
            message (str): The message to log.
        """
        logging.info(f"{self.get_database_info()} {message}")  # Log info message with server and database info

    def error(self, message):
        """
        Log an error message.

        Args:
            message (str): The message to log.
        """
        logging.error(f"{self.get_database_info()} {message}")  # Log error message with server and database info

    def warning(self, message):
        """
        Log a warning message.

        Args:
            message (str): The message to log.
        """
        logging.warning(f"{self.get_database_info()} {message}")  # Log warning message with server and database info

    def get_database_info(self):
        """
        Retrieve the server and database information for logging.

        Returns:
            str: A string containing server and database information, if available.
        """
        # Format the database information if database_name is provided
        return f"[{self.server}] [{self.database_name}] " if self.database_name else f"[{self.server}] "
