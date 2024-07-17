import os
from datetime import datetime

class DataPipeline:
    def __init__(self, base_directory, start_folder, verbose=False, stacked_stages_names_output=False):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.base_directory = os.path.join(base_directory, f"pipeline_output_{timestamp}")
        self.stages = []
        self.current_directory = os.path.join(base_directory, start_folder)
        self.verbose = verbose
        self.stage_control = {}
        self.stack_stages_names = stacked_stages_names_output
        self.executed_stages_stack = []

    def add_stage(self, stage_name, function_pointer, output_name=""):
        stage_id = len(self.stages)
        self.stages.append(
            {'id': stage_id, 'name': stage_name, 'function': function_pointer, 'output_name': output_name})
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
