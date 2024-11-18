import numpy as np

M = 5000
K0 = 70
DeltaK = 10
MaxK = 200000
MaxRelErr = 0.02


def computation(index):
    print(f"**Solutions for Scenario {index}:**")

    K = K0
    Krange = K0

    U1 = U2 = X1 = X2 = R1 = R2 = N1 = N2 = 0
    Ul = Uu = Xl = Xu = Rl = Ru = Nl = Nu = RelErrU = RelErrX = RelErrR = RelErrN = 0.0

    while K < MaxK:
        for k in range(Krange):
            Xarr, Xsrv = setArrivalService(index)

            A = np.zeros(M)
            C = np.zeros(M)

            A[0] = Xarr[0]
            C[0] = Xarr[0] + Xsrv[0]

            for j in range(1, M):
                A[j] = A[j - 1] + Xarr[j]
                C[j] = max(A[j], C[j - 1]) + Xsrv[j]

            T = C[M - 1] - A[0]

            B = np.sum(Xsrv)
            Uk = B / T

            Xk = M / T

            Rk = np.mean(C - A)
            Nk = Xk * Rk

            U1, U2 = update_accumulators(Uk, U1, U2)
            X1, X2 = update_accumulators(Xk, X1, X2)
            R1, R2 = update_accumulators(Rk, R1, R2)
            N1, N2 = update_accumulators(Nk, N1, N2)

        Ul, Uu, RelErrU = calculate_statistics(U1, U2, K)
        Xl, Xu, RelErrX = calculate_statistics(X1, X2, K)
        Rl, Ru, RelErrR = calculate_statistics(R1, R2, K)
        Nl, Nu, RelErrN = calculate_statistics(N1, N2, K)

        if (
            RelErrU < MaxRelErr
            and RelErrX < MaxRelErr
            and RelErrR < MaxRelErr
            and RelErrN < MaxRelErr
        ):
            break

        K += DeltaK
        Krange = DeltaK

    print(f"Utilizazion: [{Ul}, {Uu}]\t Relative error: {RelErrU}")
    print(f"Throughput: [{Xl}, {Xu}]\t Relative error: {RelErrX}")
    print(f"Number of jobs: [{Nl}, {Nu}]\t Relative error: {RelErrN}")
    print(f"Response time: [{Rl}, {Ru}]\t Relative error: {RelErrR}")
    print(f"Solution obtained in K = {K} iterations")
    print("-" * 100)


def setArrivalService(index):
    if index == 1:
        u1 = np.random.rand(M)
        u2 = np.random.rand(M)

        l1_hyper = 0.025
        l2_hyper = 0.1
        p1_hyper = 0.35

        Ahyper = np.zeros(M)
        for i in range(M):
            if u1[i] < p1_hyper:
                Ahyper[i] = -np.log(u2[i]) / l1_hyper
            else:
                Ahyper[i] = -np.log(u2[i]) / l2_hyper

        kweibull = 0.333
        lweibull = 2.5
        u = np.random.rand(M)
        Sweibull = lweibull * ((-np.log(u)) ** (1 / kweibull))

        return Ahyper, Sweibull

    elif index == 2:
        kerlang = 8
        lerlang = 1.25
        u = np.random.rand(kerlang, M)
        Aerlang = -np.sum(np.log(u), axis=0) / lerlang

        a = 1
        b = 10
        u = np.random.rand(M)
        Sunif = a + (b - a) * u

        return Aerlang, Sunif


def calculate_statistics(accumulator_1, accumulator_2, K):
    mean = accumulator_1 / K
    mean_square = accumulator_2 / K
    variance = mean_square - mean**2
    delta = 1.96 * np.sqrt(variance / K)  # 1.96 for 95% confidence level
    lower_bound = mean - delta
    upper_bound = mean + delta
    relative_error = 2 * (upper_bound - lower_bound) / (upper_bound + lower_bound)
    return lower_bound, upper_bound, relative_error


def update_accumulators(value, sum_acc, sum_sq_acc):
    sum_acc += value
    sum_sq_acc += value**2
    return sum_acc, sum_sq_acc


computation(1)
computation(2)
