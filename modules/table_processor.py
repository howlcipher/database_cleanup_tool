import logging

class TableProcessor:
    def __init__(self, connection):
        """
        Initialize the TableProcessor with a database connection.

        Args:
            connection: The database connection object used to interact with the database.
        """
        self.cursor = connection.cursor()  # Create a cursor object to execute SQL commands

    def process_table(self, table_name):
        """
        Process a table by inserting its data into a temporary table, truncating the original table,
        and then reinserting the data back from the temporary table.

        Args:
            table_name (str): The name of the table to process.
        """
        try:
            self.insert_to_temp_table(table_name)  # Insert data into temporary table
            self.truncate_table(table_name)  # Truncate the original table
            self.reinsert_from_temp_table(table_name)  # Reinsert data back from temporary table
            self.drop_temp_table()  # Drop the temporary table
        except Exception as e:
            # Log any errors that occur during processing
            logging.error(f"Error processing table {table_name}: {str(e)}")
            self.cursor.connection.rollback()  # Rollback the transaction on error

    def insert_to_temp_table(self, table_name):
        """
        Insert the top 1000 rows from the specified table into a temporary table.

        Args:
            table_name (str): The name of the table from which to select rows.
        """
        temp_table_sql = f'''
            SELECT TOP 1000 *
            INTO ##TempTable  -- Create a global temporary table
            FROM {table_name} ORDER BY (SELECT NULL);  -- Select rows without a specific order
        '''
        self.cursor.execute(temp_table_sql)  # Execute the SQL command to insert rows
        self.cursor.connection.commit()  # Commit the transaction to save changes
        logging.info(f"Inserted first 1000 rows from {table_name} into ##TempTable.")

    def truncate_table(self, table_name):
        """
        Truncate the specified table, removing all rows.

        Args:
            table_name (str): The name of the table to truncate.
        """
        truncate_sql = f'TRUNCATE TABLE {table_name};'  # SQL command to truncate the table
        self.cursor.execute(truncate_sql)  # Execute the truncation
        self.cursor.connection.commit()  # Commit the transaction
        logging.info(f"Truncated table {table_name}.")

    def reinsert_from_temp_table(self, table_name):
        """
        Reinsert rows from the temporary table back into the specified table.

        Args:
            table_name (str): The name of the table to which to reinsert data.
        """
        insert_sql = f'INSERT INTO {table_name} SELECT * FROM ##TempTable;'  # SQL command to reinsert data
        self.cursor.execute(insert_sql)  # Execute the insertion
        self.cursor.connection.commit()  # Commit the transaction
        logging.info(f"Reinserted rows back into {table_name}.")

    def drop_temp_table(self):
        """
        Drop the temporary table if it exists.

        This method ensures that the temporary table is removed after processing.
        """
        drop_temp_sql = 'DROP TABLE IF EXISTS ##TempTable;'  # SQL command to drop the temporary table
        self.cursor.execute(drop_temp_sql)  # Execute the drop command
        self.cursor.connection.commit()  # Commit the transaction
        logging.info(f"Dropped temporary table ##TempTable.")
