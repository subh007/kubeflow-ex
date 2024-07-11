from kfp import dsl,compiler
from my_component import *

@dsl.pipeline
def addition_pipeline(x: int, y: int) -> int:
    task1 = add_number(a=x, b=y)
    task2 = add_number(a=task1.output, b=x)
    return task2.output

compiler.Compiler().compile(addition_pipeline, 'pipeline.yaml')