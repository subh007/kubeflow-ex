from kfp import dsl,compiler
from my_component import *
from kfp import kubernetes


@dsl.pipeline
def hello_pipeline():
    say_hello()

@dsl.pipeline
def hello_name_pipeline(name: str)-> str:
    return say_hello_name(name=name).output

@dsl.pipeline
def add_number_pipeline(a: int, b: int)-> int:
    return add_number(a=a, b=b).output

@dsl.pipeline
def get_iris_dataset()->dsl.Model:
    comp = get_dataset()
    kubernetes.set_image_pull_policy(comp, "IfNotPresent")


    train = train_model(normalized_iris_dataset=comp.output, n_neighbors=3)

    return train.outputs['model']

# compiler.Compiler().compile(hello_pipeline, 'pipeline.yaml')
# compiler.Compiler().compile(hello_name_pipeline, 'pipeline.yaml')
# compiler.Compiler().compile(add_number_pipeline, 'pipeline.yaml')
compiler.Compiler().compile(get_iris_dataset, 'pipeline.yaml')


from kfp.client import Client
client = Client(host='http://localhost:8080')
# client.upload_pipeline_version(pipeline_package_path='pipeline.yaml',pipeline_version_name='v2', pipeline_name='sample-pipeline')
result = client.create_run_from_pipeline_package('pipeline.yaml', arguments={})

