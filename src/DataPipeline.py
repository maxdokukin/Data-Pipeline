import os


class DatasetPipeline:
    def __init__(self, base_directory, verbose=False):
        self.base_directory = base_directory
        self.stages = []
        self.current_directory = f"{base_directory}_original"
        self.verbose = verbose
        self.stage_control = {}

    def add_stage(self, stage_name, function_pointer, description=""):
        stage_id = len(self.stages)
        self.stages.append(
            {'id': stage_id, 'name': stage_name, 'function': function_pointer, 'description': description})
        self.stage_control[stage_id] = True  # Enable the stage by default

    def execute_stage(self, stage_id, execute):
        if stage_id in self.stage_control:
            self.stage_control[stage_id] = execute
        else:
            print(f"Stage ID {stage_id} does not exist.")

    def preprocess(self):
        for stage_info in self.stages:
            stage_id = stage_info['id']
            if not self.stage_control.get(stage_id, False):
                if self.verbose:
                    print(f"Stage {stage_id} ({stage_info['name']}) is skipped.")
                continue

            stage_name = stage_info['name']
            function = stage_info['function']
            description = stage_info['description']
            next_directory = f"{self.base_directory}_{description}" if description else f"{self.base_directory}_{stage_name}"

            if not os.path.exists(next_directory):
                os.makedirs(next_directory)

            if self.verbose:
                print(f"Stage {stage_id}: {stage_name}")
                print(f" - Input directory: {self.current_directory}")
                print(f" - Output directory: {next_directory}")

            # Call the processing function with current and next directories
            function(self.current_directory, next_directory)
            self.current_directory = next_directory

    def execute_pipeline(self, data):
        # Placeholder for the main execution flow of the pipeline
        pass


# Define your external functions
def function0(input_directory, output_directory):
    # Implementation for stage 0
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for filename in os.listdir(input_directory):
        src = os.path.join(input_directory, filename)
        dst = os.path.join(output_directory, filename)
        # Implement the renaming logic
        # For example:
        os.rename(src, dst)


def function1(input_directory, output_directory):
    # Implementation for stage 1
    pass


def function2(input_directory, output_directory):
    # Implementation for stage 2
    pass


# Usage
pipeline = DatasetPipeline('ESC50', verbose=True)
pipeline.add_stage('rename', function0, 'renamed')
pipeline.add_stage('trim', function1, 'trimmed')
pipeline.add_stage('normalize', function2, 'normalized')

# Enable or disable specific stages
pipeline.execute_stage(0, True)  # Execute stage 0
pipeline.execute_stage(1, False)  # Skip stage 1
pipeline.execute_stage(2, True)  # Execute stage 2

pipeline.preprocess()
data = ...  # Load your data here
processed_data = pipeline.execute_pipeline(data)
