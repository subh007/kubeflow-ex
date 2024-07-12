from typing import List

from kfp import client
from kfp import dsl
from kfp.dsl import Dataset
from kfp.dsl import Input
from kfp.dsl import Model
from kfp.dsl import Output
from src.math_utils import sum

@dsl.component(base_image='python:3.8',
               target_image='gcr.io/my-project/my-component:v2')
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

@dsl.component
def say_hello_name(name: str) -> str:
    return f"hi {name}" 


@dsl.component(packages_to_install=['pandas==1.3.5'])
def get_dataset(iris_dataset: Output[Dataset]):
    import pandas as pd

    csv_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
    col_names = [
        'Sepal_Length', 'Sepal_Width', 'Petal_Length', 'Petal_Width', 'Labels'
    ]
    df = pd.read_csv(csv_url, names=col_names)

    with open(iris_dataset.path, 'w') as f:
        df.to_csv(f)