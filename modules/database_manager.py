import pyodbc

class DatabaseManager:
    def __init__(self, config, database_name):
        """
        Initialize the DatabaseManager with configuration and database name.

        Args:
            config (dict): Configuration dictionary containing database connection details.
            database_name (str): The name of the database to connect to.
        """
        self.config = config  # Store the configuration
        self.database_name = database_name  # Store the database name
        self.connection = None  # Initialize connection as None

    def connect(self):
        """
        Establish a connection to the specified database using the configuration settings.
        
        Raises:
            Exception: If the connection fails, an exception is raised with the error message.
        """
        try:
            # Build the connection string using the provided configuration
            connection_string = (
                f"Driver={self.config['database']['driver']};"
                f"Server={self.config['database']['server']};"
                f"Database={self.database_name};"
                f"UID={self.config['database']['uid']};"
                f"PWD={self.config['database']['pwd']};"
            )
            # Connect to the database with autocommit enabled
            self.connection = pyodbc.connect(connection_string, autocommit=True)
        except pyodbc.Error as e:
            # Raise an exception if the connection fails
            raise Exception(f"Failed to connect to database {self.database_name}: {str(e)}")

    def close(self):
        """
        Close the database connection if it is open.
        """
        if self.connection:
            self.connection.close()  # Close the connection if it exists
