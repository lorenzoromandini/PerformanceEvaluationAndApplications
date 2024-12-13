import numpy as np
from scipy import linalg

P = np.array(
    [
        [0.0, 0.7, 0.0, 0.0],
        [0.0, 0.0, 0.25, 0.45],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
    ]
)

lamIN = np.zeros(4)
lamIN[0] = 2.5
lamIN[1] = 2

lam = sum(lamIN)
l = lamIN / lam

S1 = 2
S2 = 0.02
S3 = 0.1
S4 = 0.07

Sk = np.array([S1, S2, S3, S4])

I = np.eye(4)

v = linalg.solve((I - P).T, l)

print(
    "Visits : \n- Application server =", v[1], "\n- Storage =", v[2], "\n- DBMS =", v[3]
)

Dk = v * Sk

X = lam
print("Throughput of the system =", X)

Uk = X * Dk

Rk = np.zeros(4)
Rk[0] = Dk[0]
for i in range(1, len(Rk)):
    Rk[i] = Dk[i] / (1 - Uk[i])

Nk = np.zeros(4)
Nk[0] = Uk[0]
for i in range(1, len(Nk)):
    Nk[i] = Uk[i] / (1 - Uk[i])

N = sum(Nk)
print("Average number of jobs in the system =", N)

R = sum(Rk)
print("Average system Response time [ms] =", R * 1000)

MaxLam = 1 / max(Dk)
print("Maximum Arrival rate =", MaxLam)
