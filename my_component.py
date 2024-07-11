from kfp import dsl
from src.math_utils import sum

@dsl.component(base_image='python:3.7',
               target_image='gcr.io/my-project/my-component:v1')
def add_number(a: int, b: int) -> int:
    sum(a, b)

# light weight component
@dsl.component
def sub_number(a: int, b: int) -> int:
    return a - b

@dsl.component(packages_to_install=['numpy==1.21.6'])
def sin(val: float=3.14)->float:
    import numpy as np
    return np.sin(val).item()


# Containerized Python Component functions can depend on symbols 
# defined outside of the function, imports outside of the function, 
# code in adjacent Python modules, etc. To achieve this, the KFP 
# SDK provides a convenient way to package your Python code into a container.

"""
Container Components, unlike Python Components, enable component authors to set 
the image, command, and args directly. This makes it possible to author components 
that execute shell scripts, use other languages and binaries, etc., all from within 
the KFP Python SDK.
"""
@dsl.container_component
def say_hello():
    return dsl.ContainerSpec(image='alpine', command=['echo'], args=['hello'])