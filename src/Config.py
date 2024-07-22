class Config:
    """
    Configuration class for managing model settings, directories, and parameters.
    Adds timestamps to directory names and ensures directories exist. This class
    dynamically accepts configuration parameters and provides verbose output if enabled.

    Attributes:
        verbose (bool): Enable detailed logging of operations if True. Default is False.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new instance of the Config class.

        Args:
            **kwargs: Arbitrary keyword arguments. 'verbose' is used for logging, and
                      others are stored as configuration parameters.
        """
        self.verbose = kwargs.pop('verbose', False)  # Extract verbosity and remove from kwargs
        self.__dict__.update(kwargs)  # Update instance dictionary with remaining kwargs

        if self.verbose:
            print("Initializing configuration with parameters:", kwargs)

    def add_parameter(self, key, value):
        """
        Add or update a key-value pair in the configuration.

        Args:
            key (str): The key for the parameter to add or update.
            value (any): The value for the parameter.

        Example:
            config.add_parameter('learning_rate', 0.01)
        """
        self.__dict__[key] = value
        if self.verbose:
            print(f"Added or updated parameter: {key} = {value}")
