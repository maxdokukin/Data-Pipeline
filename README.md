
# DataPipeline

A Python class for managing and executing a data processing pipeline with multiple stages. This class allows you to add, enable, disable, and execute stages dynamically, with support for verbose output and flexible naming of output directories. Additionally, you can specify functions to be executed before and after each stage.

## Features

- Dynamic addition of processing stages
- Enable or disable specific stages by name
- Verbose output for detailed processing information
- Option to stack stage names for output directory naming
- Unique directory naming for each pipeline execution using timestamps
- Specify functions to be executed before and after each stage

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
pipeline = DataPipeline('data', 'original_data', verbose=True, stacked_stages_names_output=True)
```

### Add stages to the pipeline

Add stages with their respective names, functions, and optional output directory names.

```python
pipeline.add_stage('rename', function0, 'renamed')
pipeline.add_stage('trim', function1, 'trimmed')
pipeline.add_stage('normalize', function2, 'normalized')
pipeline.add_stage('split', function3, 'split')
pipeline.add_stage('augment', function4, 'augmented')
```

### Enable or disable specific stages

Enable or disable stages by their name.

```python
pipeline.disable_stage('trim')
pipeline.disable_stage('normalize')
pipeline.disable_stage('split')
```

### Set pre and post stage functions

Set functions to be executed before and after each stage.

```python
def pre_stage_function(stage_name, current_directory):
    print(f"Pre-stage function called for stage: {stage_name}, current directory: {current_directory}")

def post_stage_function(stage_name, current_directory):
    print(f"Post-stage function called for stage: {stage_name}, current directory: {current_directory}")

pipeline.set_prestage_function(pre_stage_function)
pipeline.set_poststage_function(post_stage_function)
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
        self.prestage_function = None
        self.poststage_function = None

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

    def set_prestage_function(self, f):
        self.prestage_function = f

    def set_poststage_function(self, f):
        self.poststage_function = f

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

            if self.prestage_function:
                self.prestage_function(stage_name, self.current_directory)

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

            function(self.current_directory, next_directory)
            self.current_directory = next_directory

            if self.poststage_function:
                self.poststage_function(stage_name, self.current_directory)

# Define your external functions
def function0(input_directory, output_directory):
    print("function 0 called")

def function1(input_directory, output_directory):
    print("function 1 called")

def function2(input_directory, output_directory):
    print("function 2 called")

def function3(input_directory, output_directory):
    print("function 3 called")

def function4(input_directory, output_directory):
    print("function 4 called")

def function5(input_directory, output_directory):
    print("function 5 called")

def pre_stage_function(stage_name, current_directory):
    print(f"Pre-stage function called for stage: {stage_name}, current directory: {current_directory}")

def post_stage_function(stage_name, current_directory):
    print(f"Post-stage function called for stage: {stage_name}, current directory: {current_directory}")

# Create an instance of DataPipeline
pipeline = DataPipeline('models', '', verbose=True, stacked_stages_names_output=True)
pipeline.add_stage('train', function0, 'training_checkpoints')
pipeline.add_stage('test_tf', function1, '')  # No output directory change
pipeline.add_stage('optimize', function2, 'optimized')
pipeline.add_stage('convert_tf_tflite', function3, 'tflite')
pipeline.add_stage('test_tflite', function4, '')  # No output directory change
pipeline.add_stage('convert_tflite_c', function5, 'converted')

pipeline.set_prestage_function(pre_stage_function)
pipeline.set_poststage_function(post_stage_function)

pipeline.disable_stage('train')
pipeline.disable_stage('test_tf')
pipeline.disable_stage('optimize')

pipeline.execute()
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
