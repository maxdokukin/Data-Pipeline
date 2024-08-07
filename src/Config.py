class Config:
    """
    Configuration class for managing model settings, directories, and parameters.
    Adds timestamps to directory names and ensures directories exist. This class
    dynamically accepts configuration parameters and provides verbose output if enabled.

    Attributes:
        verbose (bool): Enable detailed logging of operations if True. Default is False.
    """

    def __init__(self, **kwargs):
        self.verbose = kwargs.pop('verbose', False)
        self.__dict__.update(kwargs)

        if self.verbose:
            print("Initializing configuration with parameters:", kwargs)


    def add_parameter(self, key, value):
        """
        Add or update a key-value pair in the configuration.

        Args:
            key: The key for the parameter.
            value: The value for the parameter.
        """
        self.__dict__[key] = value
        if self.verbose:
            print(f"Added parameter: {key} = {value}")


    def parameters_to_string(self):
        """
        Returns all configuration parameters as a formatted string.

        Returns:
            str: A string representation of all parameters.
        """
        params_str_list = []
        for key, value in self.__dict__.items():
            if isinstance(value, (list, tuple)):
                params_str_list.append(f"{key}:")
                for item in value:
                    params_str_list.append(f"    {item}")
            else:
                params_str_list.append(f"{key}: {value}")
        return "\n".join(params_str_list)
