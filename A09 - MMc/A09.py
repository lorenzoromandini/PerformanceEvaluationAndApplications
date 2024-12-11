from math import factorial

import numpy as np

D = 1.6


def compute_mm1(lam):
    rho = lam * D
    U = rho
    print("**** M/M/1 ****")
    print("Utilization =", U)

    pi = [(1 - rho) * (rho**i) for i in range(20)]
    pNgti = [rho ** (i + 1) for i in range(20)]

    print("p(N = 2) =", pi[2])
    print("p(N < 5) =", 1 - (pNgti[5] + pi[5]))

    N = rho / (1 - rho)
    Nq = N - U
    print("Average queue length =", Nq)

    R = D / (1 - rho)
    print("Average Response time =", R)

    pRgt2 = np.exp(-2 / R)
    print("p(R > 2) =", pRgt2)

    perc95 = -np.log(1 - 0.95) * R
    print("95th Percentile =", perc95)
    print("-" * 100)


def compute_mm2(lam):
    print("**** M/M/2 ****")
    c = 2
    rho = lam * D / c
    U = rho * c
    Ub = rho
    print("Total Utilization =", U)
    print("Average Utilization =", Ub)

    pi = np.zeros(20)
    pNlei = np.zeros(20)

    pi[0] = (1 - rho) / (1 + rho)
    pNlei[0] = pi[0]

    for i in range(1, 20):
        pi[i] = 2 * pi[0] * (rho**i)
        pNlei[i] = pNlei[i - 1] + pi[i]

    print("p(N = 2) =", pi[2])
    print("p(N < 5) =", pNlei[4])

    N = 2 * rho / (1 - rho**2)
    Nq = N - U
    print("Average queue length =", Nq)

    R = D / (1 - rho**2)
    print("Average Response time =", R)
    print("-" * 100)


def compute_mmc(lam):
    c = 1

    while True:
        rho = lam * D / c
        Ub = rho
        U = rho * c

        if Ub <= 1 and Ub >= 0:
            break
        c += 1

    print("**** M/M/c ****")
    print("c =", c)
    print("Total Utilization =", U)
    print("Average Utilization =", Ub)

    pi = np.zeros(20)
    pNlei = np.zeros(20)

    pi[0] = 1 / (
        (((c * rho) ** c) / factorial(c)) * (1 / (1 - rho))
        + sum(((c * rho) ** k / factorial(k)) for k in range(c))
    )
    pNlei[0] = pi[0]

    for i in range(1, 20):
        if i < c:
            pi[i] = pi[0] * (c * rho) ** i / factorial(i)
        else:
            pi[i] = pi[0] * (c**c) * (rho**i) / factorial(c)
        pNlei[i] = pNlei[i - 1] + pi[i]

    print("p(N = 2) =", pi[2])
    print("p(N < 5) =", pNlei[4])

    denominator = 1 + (1 - rho) * (factorial(c) / ((c * rho) ** c)) * sum(
        (c * rho) ** k / factorial(k) for k in range(c)
    )
    N = c * rho + (rho / (1 - rho)) / denominator
    Nq = N - U
    print("Average queue length = ", Nq)

    Th = (D / (c * (1 - rho))) / denominator
    R = D + Th
    print("Average Response time =", R)
    print("-" * 100)


def compute_mminf(lam):
    print("**** M/M/∞ ****")
    rho = lam * D
    U = rho
    print("Total Utilization =", U)

    pi = np.zeros(20)
    pNlei = np.zeros(20)

    pi[0] = np.exp(-rho)
    pNlei[0] = pi[0]

    for i in range(1, 20):
        pi[i] = pi[0] * (rho**i) / factorial(i)
        pNlei[i] = pNlei[i - 1] + pi[i]

    print("p(N = 2) =", pi[2])
    print("p(N < 5) =", pNlei[4])

    R = D
    print("Average Response time =", R)


compute_mm1(lam=0.5)
compute_mm2(lam=1)
compute_mmc(lam=4)
compute_mminf(lam=10)
