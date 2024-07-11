from kfp import dsl

@dsl.component(base_image='python:3.7',
               target_image='gcr.io/my-project/my-component:v1')
def add_number(a: int, b: int) -> int:
    return a + b

# light weight component
@dsl.component
def sub_number(a: int, b: int) -> int:
    return a - b

@dsl.component(packages_to_install=['numpy==1.21.6'])
def sin(val: float=3.14)->float:
    import numpy as np
    return np.sin(val).item()
