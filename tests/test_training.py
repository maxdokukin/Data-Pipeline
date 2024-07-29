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

def function5(config, input_directory, output_directory):
    # Implementation for stage 2
    print("function 5 called")


# Define pre and post stage functions
def pre_stage_function(stage_name, current_directory):
    print(f"Pre-stage function called")

def post_stage_function(stage_name, current_directory):
    print(f"Post-stage function called")


# Usage
pipeline = DataPipelineController(
    base_directory=r'C:\Users\mdokukin1\Desktop\GitHub\Data-Pipeline\data',
    start_directory='',
    verbose=True,
    stacked_stages_names_output=False
)

pipeline.add_stage('train', function0, 'training_checkpoints')
pipeline.add_stage('test_tf', function1, '')
pipeline.add_stage('optimize', function2, 'optimized')
pipeline.add_stage('convert_tf_tflite', function3, 'tflite')
pipeline.add_stage('test_tflite', function4, '')
pipeline.add_stage('convert_tflite_c', function5, 'converted')

# Set pre and post stage functions
pipeline.set_prestage_function(pre_stage_function)
pipeline.set_poststage_function(post_stage_function)

# pipeline.disable_stage('train')
# pipeline.disable_stage('test_tf')
# pipeline.disable_stage('optimize')

pipeline.execute()
