from kfp import dsl
from kfp.dsl import Dataset, Output
from kfp import local

@dsl.component(packages_to_install=['tensorflow==2.18.0', 'pandas'],
               base_image='python:3.10', target_image='ghcr.io/subh007/pd_test:v1',
               pip_index_urls='http://localhost/simple/')
def prepare_data(boston_data: Output[Dataset]):
    import tensorflow as tf
    import numpy as np
    import pandas as pd
    (train_x, train_y), (test_X, test_Y) = tf.keras.datasets.boston_housing.load_data(test_split=0)
    # Convert to DataFrame
    column_names = [
        "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT", "MEDV"
    ]
    df = pd.DataFrame(np.column_stack((train_x, train_y)), columns=column_names)

    # it is important to save the artifact by writing
    with open(boston_data.path, "wb") as f:
        df.to_csv(f, index=False)

    print(f"Boston Housing dataset saved to {boston_data.path}")



# import kfp
# kfp.local.init(runner=local.DockerRunner())

# prepare_data()
    
from kfp import compiler
compiler.Compiler().compile(prepare_data, 'component.yaml')