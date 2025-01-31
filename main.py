# Import necessary modules
from modules.config import ConfigManager  # To handle configuration loading
from modules.database_cleanup import DatabaseCleanup  # To manage database cleanup operations

# Entry point of the script
if __name__ == "__main__":
    # Load the configuration from the specified YAML file
    config_manager = ConfigManager('config.yaml')
    
    # Create an instance of the DatabaseCleanup class with the loaded configuration
    cleanup = DatabaseCleanup(config_manager.config)
    
    # Run the cleanup process, which includes processing tables and shrinking databases
    cleanup.run()
