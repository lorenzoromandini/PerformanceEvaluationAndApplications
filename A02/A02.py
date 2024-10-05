import numpy as np

inter_arrival_trace = np.loadtxt("Logger1.csv")
service_time_trace = np.loadtxt("Logger2.csv")
C = service_time_trace.shape[0]

A_T = np.zeros((C, 1))
C_T = np.zeros((C, 1))


def calculate_metrics(alpha, beta):
    inter_arrival_new = inter_arrival_trace * alpha
    service_time_new = service_time_trace * beta

    A_T[:, 0] = np.cumsum(inter_arrival_new)

    C_T[0, 0] = service_time_new[0] + A_T[0, 0]
    for i in range(1, C):
        C_T[i, 0] = max(C_T[i - 1, 0], A_T[i, 0]) + service_time_new[i]

    r_i = C_T - A_T
    R = np.mean(r_i)

    return R


def computation(fraction_alpha, fraction_beta, question):
    R = calculate_metrics(fraction_alpha, fraction_beta)

    if question == 1:
        simulation_lambda(R, fraction_alpha)
    elif question == 2:
        simulation_beta(R, fraction_alpha, fraction_beta)


def simulation_lambda(R, alpha):
    lower_bound = 19.999
    upper_bound = 20.001
    step = 0.00001
    print("Solving Exercise 1...")
    while not (lower_bound < R < upper_bound):
        if R < lower_bound:
            alpha -= step
        elif R > upper_bound:
            alpha += step

        R = calculate_metrics(alpha, 1)

    lambda_max = 1 / np.mean(inter_arrival_trace * alpha)

    print(f"Exercise 1: R = {R}, lambda_max = {lambda_max}, alpha = {alpha}")


def simulation_beta(R, alpha, beta):
    bound_2 = 15
    step = 0.0001
    print("Solving Exercise 2...")
    while R > bound_2:
        beta -= step
        R = calculate_metrics(alpha, beta)

    print(f"Exercise 2: R = {R}, beta = {beta}, alpha = {alpha}")


# Exercise 1
fraction_alpha_1 = 1
fraction_beta = 1

computation(fraction_alpha_1, fraction_beta, 1)

# Exercise 2
lambda_original = 1 / np.mean(inter_arrival_trace)
lambda_target_2 = 1.2
fraction_alpha_2 = lambda_original / lambda_target_2

computation(fraction_alpha_2, fraction_beta, 2)
