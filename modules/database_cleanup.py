import pyodbc  
from modules.config import ConfigManager
from modules.logger import Logger
from modules.database_manager import DatabaseManager
from modules.table_processor import TableProcessor
import time

class DatabaseCleanup:
    def __init__(self, config):
        """
        Initialize the DatabaseCleanup class with the provided configuration.

        Args:
            config (dict): The configuration dictionary containing database and logging settings.
        """
        self.config = config

    def run(self):
        """
        Execute the cleanup process for each database specified in the configuration.
        """
        # Iterate over each database in the configuration
        for db_name in self.config['database']['databases']:
            # Create a logger for the current database
            logger = Logger(self.config['logging']['file'], self.config['database']['server'], db_name)
            logger.info(f"Processing database: {db_name}")

            # Create a DatabaseManager for the current database
            db_manager = DatabaseManager(self.config, db_name)
            db_manager.connect()  # Connect to the current database
            
            try:
                self.process_tables(db_manager, logger)  # Process tables and log actions
                self.shrink_database(db_manager, logger)  # Attempt to shrink the database
            finally:
                db_manager.close()  # Ensure the database connection is closed
                logger.info("Database connection closed.")

    def check_database_state(self, cursor, db_name):
        """
        Check the current state of the specified database.

        Args:
            cursor: The database cursor for executing SQL queries.
            db_name (str): The name of the database to check.

        Returns:
            str: The state description of the database.
        """
        query = f"SELECT state_desc FROM sys.databases WHERE name = '{db_name}';"
        cursor.execute(query)
        state = cursor.fetchone()  # Fetch the result of the query
        return state[0] if state else None  # Return the state if it exists

    def process_tables(self, db_manager, logger):
        """
        Process tables in the current database that exceed the row threshold.

        Args:
            db_manager (DatabaseManager): The database manager for managing connections.
            logger (Logger): The logger for logging actions.
        """
        threshold = self.config['row_threshold']  # Row threshold from configuration
        query = f"""
            SELECT t.name AS table_name
            FROM sys.tables t
            JOIN sys.partitions p ON t.object_id = p.object_id
            WHERE p.index_id IN (0, 1)
            GROUP BY t.name
            HAVING SUM(p.rows) > {threshold};
        """
        cursor = db_manager.connection.cursor()  # Create a cursor for executing SQL
        cursor.execute(query)  # Execute the query to find tables exceeding the threshold
        tables = cursor.fetchall()  # Fetch all matching tables

        for table in tables:
            table_name = table[0]  # Extract the table name
            logger.info(f"Processing table: {table_name}")  # Log the processing action
            processor = TableProcessor(db_manager.connection)  # Create a table processor
            processor.process_table(table_name)  # Process the current table

    def shrink_database(self, db_manager, logger):
        """
        Shrink the current database after confirming it's ONLINE.

        Args:
            db_manager (DatabaseManager): The database manager for managing connections.
            logger (Logger): The logger for logging actions.
        """
        try:
            logger.info("Opening a new connection for shrink operation.")
            cursor = db_manager.connection.cursor()  # Create a cursor for the shrink operation
            db_name = db_manager.database_name  # Get the database name from the manager

            logger.info(f"Waiting for database {db_name} to be ONLINE...")
            while True:
                state = self.check_database_state(cursor, db_name)  # Check the database state
                if state == 'ONLINE':
                    logger.info(f"Database {db_name} is ONLINE.")  # Log that the database is ready
                    break
                else:
                    logger.info(f"Current state of database {db_name}: {state}. Waiting...")
                    time.sleep(5)  # Wait before checking again

            # Wait for an additional seconds before attempting to shrink
            logger.info("Waiting before shrink operation...")
            time.sleep(1)  # You can adjust this as necessary

            # Set implicit transactions off to avoid transaction issues during shrink
            cursor.execute("SET IMPLICIT_TRANSACTIONS OFF;")

            # Perform the shrink operation without any open transactions
            shrink_sql = f'DBCC SHRINKDATABASE ({db_name});'
            cursor.execute(shrink_sql)  # Execute the shrink command
            logger.info(f"Shrink command executed on database: {db_name}.")
            
        except pyodbc.Error as e:
            logger.error(f"Failed to shrink database: {str(e)}")  # Log any errors encountered
        finally:
            cursor.close()  # Ensure the cursor is closed
