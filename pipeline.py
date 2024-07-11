from kfp import dsl,compiler
from my_component import *

@dsl.pipeline
def hello_pipeline():
    say_hello()

compiler.Compiler().compile(hello_pipeline, 'pipeline.yaml')

from kfp.client import Client
client = Client(host='http://localhost:8080')
client.create_run_from_pipeline_package('pipeline.yaml', arguments={})