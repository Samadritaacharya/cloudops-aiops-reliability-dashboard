import pandas as pd
import numpy as np

SERVICES = ["checkout", "payments"]

def hello():
    return pd.DataFrame({"service": SERVICES, "value": np.arange(2)})
