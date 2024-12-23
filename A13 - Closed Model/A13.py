import numpy as np
from scipy import linalg

P = np.array(
    [
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        # [0.05, 0.0, 0.35, 0.6, 0.0, 0.0],  we suppose that the first is the Ref station, so values in the first column must be all equal to 0.0
        [0.0, 0.0, 0.35, 0.6, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.65, 0.35],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.9, 0.0, 0.0, 0.0, 0.1],
        [0.0, 0.9, 0.0, 0.0, 0.1, 0.0],
    ]
)

l = np.zeros(6)
l[0] = 1  # Reference station

S1 = 40
S2 = 0.05
S3 = 0.002
S4 = 0.08
S5 = 0.08
S6 = 0.1

Sk = np.array([S1, S2, S3, S4, S5, S6])

I = np.eye(6)

v = linalg.solve((I - P).T, l)

Dk = v * Sk
print("Demands [ms]: \n\t-Disk1:", Dk[4] * 1000, "\n\t-Disk2:", Dk[5] * 1000)

Z = Dk[0]

N = 100
Nk = np.zeros(6)
Nk[0] = N  # Terminal station

for n in range(1, N + 1):
    Rk = Dk * (1 + Nk)
    Rk[0] = 0

    R = sum(Rk[1:])

    X = n / (Z + R)

    Nk = Rk * X

    Uk = Dk * X

    Xk = v * X

    if n == N:
        print("Throughput of the system [job/s]:", X)
        print("Average Response time of the system [ms]:", R * 1000)
        print(
            "Utilization:\n\t-Application Server:",
            Uk[1],
            "\n\t-DBMS:",
            Uk[3],
            "\n\t-Disk1:",
            Uk[4],
            "\n\t-Disk2:",
            Uk[5],
        )
        print("Throughput [job/s]:\n\t-Disk1:", Xk[4], "\n\t-Disk2:", Xk[5])
