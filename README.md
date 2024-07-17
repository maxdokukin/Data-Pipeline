
# Data Pipeline Class

A Python class for managing and executing a data processing pipeline with multiple stages. This class allows you to add, enable, disable, and execute stages dynamically, with support for verbose output and flexible naming of output directories.

## Features

- Dynamic addition of processing stages
- Enable or disable specific stages by name
- Verbose output for detailed processing information
- Option to stack stage names for output directory naming
- Unique directory naming for each pipeline execution using timestamps

## Installation

Ensure you have Python installed. Then, clone this repository or copy the `DataPipeline` class into your project.

## Usage

### Import the necessary modules

```python
import os
from datetime import datetime
```

### Define your external functions

These functions will be used as the processing stages of the pipeline. Each function should take `input_directory` and `output_directory` as parameters and perform the necessary processing.

```python
def function0(input_directory, output_directory):
    # Implementation for stage 0
    pass

def function1(input_directory, output_directory):
    # Implementation for stage 1
    pass

def function2(input_directory, output_directory):
    # Implementation for stage 2
    pass

def function3(input_directory, output_directory):
    # Implementation for stage 3
    pass

def function4(input_directory, output_directory):
    # Implementation for stage 4
    pass

def function5(input_directory, output_directory):
    # Implementation for stage 5
    pass
```

### Create an instance of DataPipeline

Initialize the `DataPipeline` with the base directory, start folder, and optional settings for verbosity and stacked stage names.

```python
pipeline = DataPipeline('data', 'ESC50', verbose=True, stacked_stages_names_output=True)
```

### Add stages to the pipeline

Add stages with their respective names, functions, and optional output directory names.

```python
pipeline.add_stage('train', function0, 'training_checkpoints')
pipeline.add_stage('test_tf', function1, '')  # No output directory change
pipeline.add_stage('optimize', function2, 'optimized')
pipeline.add_stage('convert_tf_tflite', function3, 'tflite')
pipeline.add_stage('test_tflite', function4, '')  # No output directory change
pipeline.add_stage('convert_tflite_c', function5, 'converted')
```

### Enable or disable specific stages

Enable or disable stages by their name. All enabled by default.

```python
pipeline.enable_stage('train')  # Enable stage 'train'
pipeline.disable_stage('test_tf')  # Disable stage 'test_tf'
pipeline.enable_stage('optimize')  # Enable stage 'optimize'
```

### Execute the pipeline

Execute the pipeline to process each stage in the order they were added.

```python
pipeline.execute()
```

## Example

```python
import os
from datetime import datetime

class DataPipeline:
    def __init__(self, base_directory, start_folder, verbose=False, stacked_stages_names_output=False):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.base_directory = os.path.join(base_directory, f"pipeline_output_{timestamp}")
        self.current_directory = os.path.join(base_directory, start_folder)
        self.verbose = verbose
        self.stack_stages_names = stacked_stages_names_output
        self.stages = []
        self.stage_control = {}
        self.executed_stages_stack = []

    def add_stage(self, stage_name, function_pointer, output_name=""):
        stage_id = len(self.stages)
        self.stages.append({'id': stage_id, 'name': stage_name, 'function': function_pointer, 'output_name': output_name})
        self.stage_control[stage_id] = True  # Enable the stage by default

    def disable_stage(self, stage_name):
        found = False
        for stage in self.stages:
            if stage['name'] == stage_name:
                self.stage_control[stage['id']] = False
                found = True
                break
        if not found:
            print(f"Stage name {stage_name} does not exist.")

    def enable_stage(self, stage_name):
        found = False
        for stage in self.stages:
            if stage['name'] == stage_name:
                self.stage_control[stage['id']] = True
                found = True
                break
        if not found:
            print(f"Stage name {stage_name} does not exist.")

    def execute(self):
        for stage_info in self.stages:
            stage_id = stage_info['id']
            if not self.stage_control.get(stage_id, False):
                if self.verbose:
                    print(f"Stage {stage_id} ({stage_info['name']}) is skipped.")
                continue

            stage_name = stage_info['name']
            function = stage_info['function']
            output_name = stage_info['output_name']

            if output_name:
                if self.stack_stages_names:
                    self.executed_stages_stack.append(output_name)
                    next_directory = os.path.join(self.base_directory, '_'.join(self.executed_stages_stack))
                else:
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
            function(self.current_directory, next_directory)
            self.current_directory = next_directory

# Define your external functions
def function0(input_directory, output_directory):
    # Implementation for stage 0
    pass

def function1(input_directory, output_directory):
    # Implementation for stage 1
    pass

def function2(input_directory, output_directory):
    # Implementation for stage 2
    pass

def function3(input_directory, output_directory):
    # Implementation for stage 3
    pass

def function4(input_directory, output_directory):
    # Implementation for stage 4
    pass

def function5(input_directory, output_directory):
    # Implementation for stage 5
    pass

# Create an instance of DataPipeline
pipeline = DataPipeline('data', 'ESC50', verbose=True, stacked_stages_names_output=True)
pipeline.add_stage('train', function0, 'training_checkpoints')
pipeline.add_stage('test_tf', function1, '')  # No output directory change
pipeline.add_stage('optimize', function2, 'optimized')
pipeline.add_stage('convert_tf_tflite', function3, 'tflite')
pipeline.add_stage('test_tflite', function4, '')  # No output directory change
pipeline.add_stage('convert_tflite_c', function5, 'converted')

# Execute the pipeline
pipeline.execute()
```
