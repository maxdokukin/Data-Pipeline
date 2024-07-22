
# DataPipelineController README

## Overview
The `DataPipelineController` class is designed to manage and execute a data processing pipeline consisting of multiple stages. It facilitates the organization, execution, and tracking of various data processing tasks, ensuring a streamlined and efficient workflow.

## Class: DataPipelineController

### Attributes
- `base_directory` (str): The root directory for the dataset.
- `current_directory` (str): The current working directory within the pipeline.
- `verbose` (bool): Enables verbose output for detailed processing information.
- `stack_stages_names` (bool): Controls the naming of output directories.
- `stages` (list): List to store stages with their corresponding details.
- `stage_control` (dict): Dictionary to control the execution of stages by their IDs.
- `executed_stages_stack` (list): List to keep track of executed stage names for stacked naming.
- `prestage_function` (callable): Function to be executed before each stage.
- `poststage_function` (callable): Function to be executed after each stage.
- `full_pipeline_execution` (bool): Indicates if the entire pipeline is executed without skipping stages.

### Methods
#### `__init__(self, base_directory, start_folder, config=None, verbose=False, stacked_stages_names_output=False)`
Initializes the DataPipelineController with the specified parameters.

- `base_directory` (str): The root directory for the dataset.
- `start_folder` (str): The starting folder within the base directory.
- `config` (dict, optional): Configuration dictionary for additional settings.
- `verbose` (bool, optional): Enables verbose output, default is False.
- `stacked_stages_names_output` (bool, optional): Controls the naming of output directories, default is False.

#### `add_stage(self, stage_name, function_pointer, output_name="")`
Adds a processing stage to the pipeline.
- `stage_name` (str): The name of the stage.
- `function_pointer` (callable): The function to execute for this stage.
- `output_name` (str, optional): The name for the output directory of this stage.

#### `disable_stage(self, stage_name)`
Disables a specific stage based on its name.
- `stage_name` (str): The name of the stage to disable.

#### `set_prestage_function(self, f)`
Sets the function to be executed before each stage.
- `f` (callable): The function to execute before each stage.

#### `set_poststage_function(self, f)`
Sets the function to be executed after each stage.
- `f` (callable): The function to execute after each stage.

#### `execute(self)`
Executes the pipeline by processing each stage in the order they were added.

## Usage Example

### Sample Configuration for Preprocessing
```python
import os.path
from config.config import config
from classes.DataPipelineController import DataPipelineController
from functions.rename import rename_as_folders
from functions.trim import trim_silence_split
from functions.normalize import normalize_volume_dbfs
from functions.slice import slice_to_onesecond
from functions.augment import augment_by_volume
from functions.visualize import visualize_datasets

# Initialize the data processing pipeline controller
pipeline = DataPipelineController(
    base_directory=config.datasets_dir,
    start_folder=config.dataset_name,
    config=config,
    verbose=config.verbose,
    stacked_stages_names_output=True
)

# Add stages to the pipeline
pipeline.add_stage('rename', rename_as_folders, 'renamed')
pipeline.add_stage('trim', trim_silence_split, 'trimmed')
pipeline.add_stage('normalize', normalize_volume_dbfs, 'normalized')
pipeline.add_stage('slice', slice_to_onesecond, 'sliced')
pipeline.add_stage('augment', augment_by_volume, 'augmented')

# Disable stages based on configuration
if not config.perform_renaming:
    pipeline.disable_stage('rename')
if not config.perform_silence_trimming:
    pipeline.disable_stage('trim')
if not config.perform_normalization:
    pipeline.disable_stage('normalize')
if not config.perform_slicing:
    pipeline.disable_stage('slice')
if not config.perform_augmentation:
    pipeline.disable_stage('augment')

# Set post-stage function if required
if config.generate_figures:
    pipeline.set_poststage_function(visualize_datasets)

# Execute the pipeline
pipeline.execute()
```

### Key Functions in the Pipeline
- `rename_as_folders`: Renames files as folders.
- `trim_silence_split`: Trims silence from audio files.
- `normalize_volume_dbfs`: Normalizes the volume of audio files to a specified dBFS.
- `slice_to_onesecond`: Slices audio files into one-second segments.
- `augment_by_volume`: Augments audio files by altering their volume.
- `visualize_datasets`: Generates visualizations of the datasets.

## Notes
- Ensure all required functions and configurations are properly imported and set up.
- Adjust the stages and their configurations based on your specific data processing needs.
- Verbose output can be enabled for detailed processing information by setting `verbose=True` during initialization.
