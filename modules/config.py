import yaml

class ConfigManager:
    def __init__(self, config_file):
        """
        Initialize the ConfigManager with a specified configuration file.

        Args:
            config_file (str): The path to the YAML configuration file.
        """
        self.config = self.load_config(config_file)  # Load the configuration from the file

    def load_config(self, config_file):
        """
        Load the configuration from a YAML file.

        Args:
            config_file (str): The path to the YAML configuration file.

        Returns:
            dict: The loaded configuration as a dictionary.
        """
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)  # Parse the YAML file and return the configuration
