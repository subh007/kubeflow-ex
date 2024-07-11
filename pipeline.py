from kfp import dsl,compiler
from my_component import *

@dsl.pipeline
def hello_pipeline():
    say_hello()

@dsl.pipeline
def hello_name_pipeline(name: str)-> str:
    return say_hello_name(name=name).output

# compiler.Compiler().compile(hello_pipeline, 'pipeline.yaml')
compiler.Compiler().compile(hello_name_pipeline, 'pipeline.yaml')

from kfp.client import Client
client = Client(host='http://localhost:8080')
client.create_run_from_pipeline_package('pipeline.yaml', arguments={'name': 'sweety'})