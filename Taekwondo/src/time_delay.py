import time
import numpy as np

def custom_delay():
    n_seconds = np.random.poisson(68)
    time.sleep(n_seconds)

    return
