import os
from datetime import datetime


class DataPipelineController:
    """
    A class to manage and execute a data processing pipeline with multiple stages.

    Attributes:
        base_directory (str): The root directory for the dataset.
        current_directory (str): The current working directory within the pipeline.
        verbose (bool): Enables verbose output for detailed processing information.
        stack_stages_names (bool): Controls the naming of output directories.
        stages (list): List to store stages with their corresponding details.
        stage_control (dict): Dictionary to control the execution of stages by their IDs.
        executed_stages_stack (list): List to keep track of executed stage names for stacked naming.
        prestage_function (callable): Function to be executed before each stage.
        poststage_function (callable): Function to be executed after each stage.
        full_pipeline_execution (bool): Indicates if the entire pipeline is executed without skipping stages.
    """

    def __init__(self, base_directory, start_directory, config=None, verbose=False, stacked_stages_names_output=False):
        """
        Initializes the DataPipelineController with a base directory, start folder, and configuration options.

        Args:
            base_directory (str): The root directory for the dataset.
            start_folder (str): The starting folder within the base directory.
            config (dict, optional): Configuration dictionary for additional settings.
            verbose (bool, optional): Enables verbose output, default is False.
            stacked_stages_names_output (bool, optional): Controls the naming of output directories, default is False.
        """
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.base_directory = os.path.join(base_directory, f"pipeline_output_{self.timestamp}")

        if start_directory is not None:
            self.start_directory = start_directory
            self.executed_stages_stack = [os.path.basename(start_directory)]

        else:
            self.start_directory = base_directory
            self.executed_stages_stack = []
        self.current_directory = self.start_directory

        self.verbose = verbose
        self.stack_stages_names = stacked_stages_names_output

        self.stages = []
        self.stage_control = {}
        self.prestage_function = None
        self.poststage_function = None
        self.config = config
        self.full_pipeline_execution = True

        if config is not None:
            self.config.add_parameter('logs_dir', os.path.join(self.base_directory, 'logs'))
            if not os.path.exists(config.logs_dir):
                os.makedirs(config.logs_dir)

            self.config.add_parameter('timestamp', self.timestamp)




    def add_stage(self, stage_name, function_pointer, output_name=""):
        """
        Adds a processing stage to the pipeline.

        Args:
            stage_name (str): The name of the stage.
            function_pointer (callable): The function to execute for this stage.
            output_name (str, optional): The name for the output directory of this stage, default is an empty string.
        """
        stage_id = len(self.stages)
        self.stages.append({
            'id': stage_id, 'name': stage_name, 'function': function_pointer, 'output_name': output_name
        })
        self.stage_control[stage_id] = True  # Enable the stage by default

    def disable_stage(self, stage_name):
        """
        Disables a specific stage based on its name.

        Args:
            stage_name (str): The name of the stage to disable.
        """
        for stage in self.stages:
            if stage['name'] == stage_name:
                self.stage_control[stage['id']] = False
                self.full_pipeline_execution = False
                if self.verbose:
                    print(f"Stage {stage_name} disabled.")
                return
        if self.verbose:
            print(f"Stage name {stage_name} does not exist.")

    def set_prestage_function(self, f):
        """
        Sets the function to be executed before each stage.

        Args:
            f (callable): The function to execute before each stage.
        """
        self.prestage_function = f

    def set_poststage_function(self, f):
        """
        Sets the function to be executed after each stage.

        Args:
            f (callable): The function to execute after each stage.
        """
        self.poststage_function = f

    def execute(self):
        """
        Executes the pipeline by processing each stage in the order they were added.
        """
        for stage_info in self.stages:
            stage_id = stage_info['id']
            if not self.stage_control.get(stage_id, False):
                if self.verbose:
                    print(f"Stage {stage_id} ({stage_info['name']}) is skipped.")
                continue

            stage_name = stage_info['name']
            function = stage_info['function']
            output_name = stage_info['output_name']

            if self.prestage_function:
                if self.verbose:
                    print("Executing pre-stage function.")
                self.prestage_function(self.config, self.current_directory)

            if output_name:
                if self.stack_stages_names:
                    self.executed_stages_stack.append(output_name)
                    next_directory = os.path.join(self.base_directory, '_'.join(self.executed_stages_stack))
                else:
                    # if self.starting_dir is not None:
                    #     # next_directory = os.path.join(self.base_directory, f"{self.start_folder}_{output_name}")
                    #     next_directory = self.starting_dir
                    #     starting_dir = None
                    # else:
                    next_directory = os.path.join(self.base_directory, output_name)

                if not os.path.exists(next_directory):
                    os.makedirs(next_directory)
            else:
                next_directory = self.current_directory

            if self.verbose:
                print(f"Stage {stage_id}: {stage_name}, {output_name}")
                print(f" - Input directory: {self.current_directory}")
                if output_name:
                    print(f" - Output directory: {next_directory}")

            # Call the processing function with current and next directories
            function(self.config, self.current_directory, next_directory)
            self.current_directory = next_directory

            if self.poststage_function:
                if self.verbose:
                    print("Executing post-stage function.")
                self.poststage_function(self.config, self.current_directory)

        if self.verbose:
            print("Pipeline execution complete.")
