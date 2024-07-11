from kfp import dsl,compiler
from my_component import *

@dsl.pipeline
def hello_pipeline():
    say_hello()

compiler.Compiler().compile(hello_pipeline, 'pipeline.yaml')