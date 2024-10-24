import warnings

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.special import factorial, gamma

warnings.filterwarnings("ignore")

trace_1 = np.loadtxt("Trace1.csv")
trace_2 = np.loadtxt("Trace2.csv")


def computation(trace, index):
    print(f"**Solutions for Trace{index}:**")

    N = trace.shape[0]

    if index == 1:
        t = np.r_[1 : N + 1] / 1000
    else:
        t = np.r_[1 : N + 1] / 100

    M1t = np.mean(trace)
    M2t = np.mean(trace**2)
    M3t = np.mean(trace**3)
    print(f"moment_1 = {M1t}, moment_2 = {M2t}, moment_3 = {M3t}")

    ############### Uniform ###############
    a_uniform = M1t - 0.5 * (np.sqrt(12 * (M2t - (M1t**2))))
    b_uniform = M1t + 0.5 * (np.sqrt(12 * (M2t - (M1t**2))))
    print(f"a_uniform = {a_uniform}, b_uniform = {b_uniform}")

    Funif = np.maximum(
        np.array([0.0] * N),
        np.minimum(np.array([1.0] * N), (t - a_uniform) / (b_uniform - a_uniform)),
    )
    ############### Exponential ###############
    lambda_exp = 1 / M1t
    print(f"lambda_exp = {lambda_exp}")

    Fexp = 1 - np.exp(-lambda_exp * t)

    ############### Erlang ###############
    VAR = M2t - (M1t**2)
    std = np.sqrt(VAR)
    cv = std / M1t
    k_erl = int(np.round(1 / (cv**2)))
    lambda_erlang = k_erl / M1t
    print(f"lambda_erl = {lambda_erlang}, k_erl = {k_erl}")

    Ferlang = 1 - np.sum(
        [
            ((lambda_erlang * t) ** n) * np.exp(-lambda_erlang * t) / factorial(n)
            for n in range(0, k_erl)
        ],
        axis=0,
    )

    srt = trace.copy()
    srt.sort(0)

    ############### Weibull ###############
    initial_guess_weibull = np.array([1, 1])
    bounds_weibull = ((0.001, 100.0), (0.1, 100.0))
    constraints_weibull = "N"
    lambda_weibull, k_weibull = optimization(
        fun_MM,
        initial_guess_weibull,
        bounds_weibull,
        constraints_weibull,
        srt,
        "weibull",
    )
    print(f"lambda_weibull = {lambda_weibull}, k_weibull = {k_weibull}")

    Fweibull = 1 - np.exp(-((t / lambda_weibull) ** k_weibull))

    ############### Pareto ###############
    initial_guess_pareto = np.array([1, 1])
    bounds_pareto = ((2.001, 100.0), (1, 100.0))
    constraints_pareto = "N"
    alpha_pareto, m_pareto = optimization(
        fun_MM, initial_guess_pareto, bounds_pareto, constraints_pareto, srt, "pareto"
    )
    print(f"alpha_pareto = {alpha_pareto}, m_pareto = {m_pareto}")

    Fpareto = np.maximum(np.array([0.0] * N), 1 - ((m_pareto / t) ** alpha_pareto))

    ############### Hyper Exp ###############
    initial_guess_hyper = np.array([0.8 / M1t, 1.2 / M1t, 0.4])
    bounds_hyper = ((0.001, 100.0), (0.001, 100.0), (0.001, 0.999))
    constraints_hyper = "Y"
    l1d_hyper, l2d_hyper, p1d = optimization(
        fun_hyper_MLE, initial_guess_hyper, bounds_hyper, constraints_hyper, srt
    )
    p2d = 1 - p1d
    print(f"lambda_1_hyper = {l1d_hyper}, lambda_2_hyper = {l2d_hyper}")
    print(f"p1_hyper = {p1d}, p2_hyper = {p2d}")

    # M1d_hyper, M2d_hyper, M3d_hyper = compute_moments("hyper", [l1d_hyper, l2d_hyper, p1d, p2d])
    # print(f"moment_1_hyper = {M1d_hyper}, moment_2_hyper = {M2d_hyper}, moment_3_hyper = {M3d_hyper}")

    Fhyper = 1 - p1d * np.exp(-t * l1d_hyper) - p2d * np.exp(-t * l2d_hyper)

    ############### Hypo Exp ###############

    initial_guess_hypo = np.array([1 / (0.7 * M1t), 1 / (0.3 * M1t)])
    bounds_hypo = ((0.001, 100.0), (0.1, 100.0))
    constraints_hypo = "Y"
    l1d_hypo, l2d_hypo = optimization(
        fun_hypo_MLE, initial_guess_hypo, bounds_hypo, constraints_hypo, srt
    )
    print(f"lambda_1_hypo = {l1d_hypo}, lambda_2_hypo = {l2d_hypo}")

    # M1d_hypo, M2d_hypo, x = compute_moments("hypo", [l1d_hypo, l2d_hypo])
    # print(f"moment_1_hypo = {M1d_hypo}, moment_2_hypo = {M2d_hypo}")

    Fhypo = 1 - (
        l2d_hypo * np.exp(-l1d_hypo * t) - l1d_hypo * np.exp(-l2d_hypo * t)
    ) / (l2d_hypo - l1d_hypo)

    ############### CDF ###############

    probV = np.r_[1 : N + 1] / N

    fig, axs = plt.subplots(3, 3, figsize=(10, 14))
    axs = axs.flatten()
    distributions = []
    titles = []

    # If cv <= 1 include Erlang, otherwise exclude it
    if cv <= 1:
        distributions = [Funif, Fexp, Ferlang, Fweibull, Fpareto, Fhyper, Fhypo]
        titles = [
            "Uniform",
            "Exponential",
            "Erlang",
            "Weibull",
            "Pareto",
            "Hyper Exponential",
            "Hypo Exponential",
        ]
    else:
        distributions = [Funif, Fexp, Fweibull, Fpareto, Fhyper, Fhypo]
        titles = [
            "Uniform",
            "Exponential",
            "Weibull",
            "Pareto",
            "Hyper Exponential",
            "Hypo Exponential",
        ]

    xlim = [0, 0]

    for i in range(len(distributions)):
        # Adjust the x-axis limits for Uniform CDF plot when dealing with the second trace
        if i == 0 and index == 2:
            xlim = [-1, 50]
        else:
            xlim = [-1, 25]

        axs[i].plot(srt, probV, ".", label="Data Trace", color="blue")
        axs[i].set_xlim(xlim)
        axs[i].plot(t, distributions[i], label=titles[i], color="red")

        axs[i].set_title(titles[i])
        axs[i].grid()
        axs[i].legend(loc="lower right", fontsize="medium", frameon=True)

    # Turn off any unused subplots to avoid empty spaces
    for j in range(len(distributions), len(axs)):
        axs[j].axis("off")

    # Adjust layout and spacing between subplots for better visualization
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.3)

    plt.show()


# Find the ideal optimal parameters of distributions that minimize the difference w.r.t. data in the trace
def optimization(fun, initial_guess, bounds, constraints, srt, type=None):
    sx = opt.minimize(
        lambda x: fun(x, srt, type),
        initial_guess,
        bounds=bounds,
        # We use constraints only on Hyper Exp and Hypo Exp, as their own lambda parameters have to be similar
        constraints=[{"type": "ineq", "fun": lambda x: x[1] - x[0] - 0.001}]
        if constraints == "Y"
        else [],
    )
    return sx.x


# Compute parameters of distribution through Method of Moments (combined with optimization() function)
def fun_MM(x, srt, type):
    M1t = np.mean(srt)
    M2t = np.mean(srt**2)
    M1d, M2d, f = compute_moments(type, [x[0], x[1]])
    return np.abs(M1d / M1t - 1) ** 2 + np.abs(M2d / M2t - 1) ** 2
    # return np.abs(M1d / M1t - 1) ** 2 + np.abs(M2d / M2t - 1) // we use the formula above without the 2/n exp (always exp 2)


# Compute parameters of Hyper Exp distribution through Maximum Likelyhood Estimation (combined with optimization() function)
def fun_hyper_MLE(x, srt, none):
    l1 = x[0]
    l2 = x[1]
    p1 = x[2]
    p2 = 1 - p1

    return -np.sum(np.log(p1 * l1 * np.exp(-l1 * srt) + p2 * l2 * np.exp(-l2 * srt)))


# Compute parameters of Hypo Exp distribution through Maximum Likelyhood Estimation (combined with optimization() function)
def fun_hypo_MLE(x, srt, none):
    l1 = x[0]
    l2 = x[1]

    if l1 == l2:
        return -1000000 - l1 - l2
    else:
        return -np.sum(
            np.log(l1 * l2 / (l1 - l2) * (np.exp(-l2 * srt) - np.exp(-l1 * srt)))
        )


# Compute moments of distributions
def compute_moments(type, params):
    M1d, M2d, M3d = 0, 0, 0
    if type == "hyper":
        M1d = params[2] / params[0] + params[3] / params[1]
        M2d = 2 * (params[2] / params[0] ** 2 + params[3] / params[1] ** 2)
        M3d = 6 * (params[2] / params[0] ** 3 + params[3] / params[1] ** 3)
    elif type == "hypo":
        M1d = 1 / params[0] + 1 / params[1]
        M2d = 2 * (
            1 / (params[0] ** 2) + 1 / (params[0] * params[1]) + 1 / (params[1] ** 2)
        )
    elif type == "weibull":
        M1d = params[0] * gamma(1 + 1 / params[1])
        M2d = (params[0] ** 2) * gamma(1 + 2 / params[1])
    elif type == "pareto":
        M1d = params[0] * params[1] / (params[0] - 1)
        M2d = params[0] * (params[1] ** 2) / (params[0] - 2)
    return M1d, M2d, M3d


# Execute program, first with trace 1 and then with trace 2
for index, trace in enumerate([trace_1, trace_2]):
    computation(trace, index + 1)
    print("-" * 100)
