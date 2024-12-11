from math import factorial

import numpy as np

lam_D = 100
k_D = 4
D = k_D / lam_D
Cv = 1 / np.sqrt(k_D)


def compute_mg1(lam_A):
    print("**** M/G/1 ****")

    rho = lam_A * D
    U = rho

    print("Utilization =", U)

    R = D + (rho * D / (1 - rho)) * (1 + Cv**2) / 2
    N = rho + rho**2 * (1 + Cv**2) / (2 * (1 - rho))

    print("(Exact) Average Response time [ms] =", R * 1000)
    print("(Exact) Average Number of jobs in the system =", N)

    print("-" * 100)


def compute_ggc(l1, l2, p1):
    print("**** G/G/c ****")

    mu = p1 / l1 + (1 - p1) / l2
    lam = 1 / mu
    m2 = 2 * p1 / l1**2 + 2 * (1 - p1) / l2**2
    std = np.sqrt(m2 - mu**2)
    Ca = std / mu

    c = 1
    while True:
        rho = lam * D / c
        Ub = rho

        if Ub <= 1 and Ub >= 0:
            break
        c += 1

    print("Minimum number of servers c for which the considered system is stable =", c)

    Ub = rho

    print("Average Utilization =", Ub)

    denominator = 1 + (1 - rho) * (factorial(c) / ((c * rho) ** c)) * sum(
        (c * rho) ** k / factorial(k) for k in range(c)
    )
    N = c * rho + (rho / (1 - rho)) / denominator

    R = N / lam
    Th = R - D
    Rapprox = D + (Cv**2 + Ca**2) / 2 * Th
    print("(Approximate) Average Response time [ms] =", Rapprox * 1000)

    Napprox = lam * Rapprox
    print("(Approximate) Average Number of jobs in the system =", Napprox)


compute_mg1(lam_A=20)
compute_ggc(l1=40, l2=240, p1=0.8)
