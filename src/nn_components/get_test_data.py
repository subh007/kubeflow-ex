from kfp import dsl
from kfp.dsl import Dataset, Input

@dsl.component(base_image='python:3.10',
               packages_to_install=['pandas'],
               target_image='ghcr.io/subh007/get_test_data:v1')
def getTestData(data: Input[Dataset]):
    import pandas as pd

    with open(data.path, "r") as f:
        df = pd.read_csv(f)
    
    print(df.first)