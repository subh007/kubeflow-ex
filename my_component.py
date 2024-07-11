from kfp import dsl

@dsl.component(base_image='python:3.7',
               target_image='gcr.io/my-project/my-component:v1')
def add_number(a: int, b: int) -> int:
    sum(a,b)