import numpy as np
from scipy import linalg

P = np.array(
    [
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        # [0.05, 0.0, 0.35, 0.6, 0.0, 0.0],  we suppose that 0 is the Ref station, so values in the first column must be all equal to 0.0
        [0.0, 0.0, 0.35, 0.6, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.9, 0.0, 0.0, 0.0, 0.1],
        [0.0, 0.9, 0.0, 0.0, 0.1, 0.0],
    ]
)

l = np.zeros(6)
l[0] = 1  # Ref station

S1 = 40
S2 = 0.05
S3 = 0.002
S4 = 0.08
S5 = 0.08
S6 = 0.1

Sk = np.array([S1, S2, S3, S4, S5, S6])

I = np.eye(6)

v = linalg.solve((I - P).T, l)
print("Visits:", v)
