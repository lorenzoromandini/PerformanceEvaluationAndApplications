from math import factorial

import numpy as np

D = 0.2
K = 16


def compute_mm1k(lam):
    print("**** M/M/1/K ****")
    rho = lam * D

    U = (rho - rho ** (K + 1)) / (1 - rho ** (K + 1))
    print("Utilization =", U)

    LossProb = (rho**K - rho ** (K + 1)) / (1 - rho ** (K + 1))
    print("Loss Probability =", LossProb)

    N = rho / (1 - rho) - (K + 1) * rho ** (K + 1) / (1 - rho ** (K + 1))
    print("Average number of jobs =", N)

    DropRate = lam * LossProb
    print("Drop rate [req/min] =", DropRate * 60)

    X = lam - DropRate

    R = N / X
    print("Average Response Time [ms] =", R * 1000)

    W = R - D
    print("Average Time Spent in Queue [ms] =", W * 1000)
    print("-" * 100)


def compute_mmck(lam, find_c):
    c = 1 if find_c else 2
    rho = lam * D / c

    while True:
        pi = np.zeros(K + 1)
        pi[0] = 1 / (
            ((c * rho) ** c) / factorial(c) * (1 - rho ** (K - c + 1)) / (1 - rho)
            + sum(((c * rho) ** k / factorial(k)) for k in range(c))
        )

        for i in range(1, K + 1):
            if i < c:
                pi[i] = pi[0] / factorial(i) * (c * rho) ** i
            else:
                pi[i] = pi[0] * (c * rho) ** i / (factorial(c) * c ** (i - c))

        LossProb = pi[K]

        if find_c and LossProb < 0.01:
            break

        if not find_c:
            break

        c += 1
        rho = lam * D / c

    print("**** M/M/c/K ****")
    if find_c:
        print("Servers required to achieve Loss Probability < 1% :", c)
    else:
        print("Number of Servers (c):", c)

    U = sum(i * pi[i] for i in range(1, c + 1)) + c * sum(
        pi[i] for i in range(c + 1, K + 1)
    )
    print("Total Utilization =", U)

    Ub = rho
    print("Average Utilization =", Ub)

    print("Loss Probability =", LossProb)

    N = sum(i * pi[i] for i in range(K + 1))
    print("Average Number of Jobs =", N)

    DropRate = lam * LossProb
    print("Drop Rate [req/min] =", DropRate * 60)

    X = lam - DropRate
    R = N / X
    print("Average Response Time [ms] =", R * 1000)

    W = R - D
    print("Average Time Spent in Queue [ms] =", W * 1000)
    print("-" * 100)


compute_mm1k(lam=4)
compute_mmck(lam=6, find_c=False)
compute_mmck(lam=16, find_c=True)
