from DataPipelineController import DataPipelineController

# Define your external functions
def function0(input_directory, output_directory):
    # Implementation for stage 0
    # if not os.path.exists(output_directory):
    #     os.makedirs(output_directory)
    # for filename in os.listdir(input_directory):
    #     src = os.path.join(input_directory, filename)
    #     dst = os.path.join(output_directory, filename)
    #     # Implement the renaming logic
    #     # For example:
    #     os.rename(src, dst)
    print("function 0 called")


def function1(input_directory, output_directory):
    # Implementation for stage 1
    print("function 1 called")


def function2(input_directory, output_directory):
    # Implementation for stage 2
    print("function 2 called")

def function3(input_directory, output_directory):
    # Implementation for stage 2
    print("function 3 called")

def function4(input_directory, output_directory):
    # Implementation for stage 2
    print("function 4 called")

# Usage
pipeline = DataPipelineController(
    base_directory=r'C:\Users\mdokukin1\Desktop\GitHub\Data-Pipeline\data',
    start_folder='original',
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

