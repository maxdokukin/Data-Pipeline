from DataPipeline import DataPipeline

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

def function5(input_directory, output_directory):
    # Implementation for stage 2
    print("function 4 called")
# Usage
pipeline = DataPipeline(
    base_directory=r'C:\Users\mdokukin1\Desktop\GitHub\Data-Pipeline\data',
    start_folder='original',
    verbose=True,
    stacked_stages_names_output=False
)

pipeline.add_stage('train', function0, 'training_checkpoints')
pipeline.add_stage('test_tf', function1, '')
pipeline.add_stage('optimize', function2, 'optimized')
pipeline.add_stage('convert_tf_tflite', function3, 'tflite')
pipeline.add_stage('test_tflite', function4, '')
pipeline.add_stage('convert_tflite_c', function5, 'converted')

pipeline.execute()

