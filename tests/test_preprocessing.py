from DataPipelineController import DataPipelineController

# Define your external functions
def function0(config, input_directory, output_directory):
    # Implementation for stage 0
    print("function 0 called")

def function1(config, input_directory, output_directory):
    # Implementation for stage 1
    print("function 1 called")

def function2(config, input_directory, output_directory):
    # Implementation for stage 2
    print("function 2 called")

def function3(config, input_directory, output_directory):
    # Implementation for stage 2
    print("function 3 called")

def function4(config, input_directory, output_directory):
    # Implementation for stage 2
    print("function 4 called")

# Usage
pipeline = DataPipelineController(
    base_directory=r'C:\Users\mdokukin1\Desktop\GitHub\Data-Pipeline\data',
    start_directory=r'C:\Users\mdokukin1\Desktop\GitHub\Data-Pipeline\data\ESC50',
    verbose=True,
    stacked_stages_names_output=True
)

pipeline.add_stage('rename', function0, 'renamed')
pipeline.add_stage('trim', function1, 'trimmed')
pipeline.add_stage('normalize', function2, 'normalized')
pipeline.add_stage('split', function3, 'split')
pipeline.add_stage('augment', function4, 'augmented')

pipeline.disable_stage('trim')
pipeline.disable_stage('normalize')
pipeline.disable_stage('split')

pipeline.execute()

