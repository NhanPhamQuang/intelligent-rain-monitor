import numpy as np
import pandas as pd

def gen_temp(n):
    return pd.DataFrame({
        "Min": np.random.randint(10, 20, n),
        "Max": np.random.randint(20, 35, n)
    })

def gen_rain():
    return np.random.randint(0, 100, 10)

def gen_scatter():
    return pd.DataFrame({
        "Humidity": np.random.randint(40, 100, 50),
        "Rain": np.random.randint(0, 10, 50)
    })