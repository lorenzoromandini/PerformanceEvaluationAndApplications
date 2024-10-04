import matplotlib.pyplot as plt
import numpy as np

trace_1 = np.loadtxt("Trace1.csv")
trace_2 = np.loadtxt("Trace2.csv")
trace_3 = np.loadtxt("Trace3.csv")

def computation(trace, i):
    print(f"**Solutions for Trace{i}:**")
    N = trace.shape[0]

    EX = np.mean(trace)
    EX2 = np.mean(trace ** 2)
    EX3 = np.mean(trace ** 3)
    EX4 = np.mean(trace ** 4)
    print(f"Mean = {EX}, moment_2 = {EX2}, moment_3 = {EX3}, moment_4 = {EX4}")

    CX2 = np.mean((trace - EX) ** 2)
    CX3 = np.mean((trace - EX) ** 3)
    CX4 = np.mean((trace - EX) ** 4)
    print(f"Variance = {CX2}, centered_moment_3 = {CX3}, centered_moment_4 = {CX4}")

    sigma = np.sqrt(CX2)
    
    SX3 = np.mean(((trace - EX) / sigma) ** 3)
    SX4 = np.mean(((trace - EX) / sigma) ** 4)
    print(f"Skewness = {SX3}, standardized_moment_4 = {SX4}")

    c_v = sigma / EX
    beta = SX4 - 3
    print(f"Standard deviation = {sigma}, Coefficient of Variation = {c_v}, Excess Kurtosis = {beta}")

    q1 = calculate_percentile(trace, 25)
    q2 = calculate_percentile(trace, 50)
    q3 = calculate_percentile(trace, 75)
    p05 = calculate_percentile(trace, 5)
    p90 = calculate_percentile(trace, 90)
    print(f"Median = {q2}, quartile_1 = {q1}, quartile_3 = {q3}, percentile_5 = {p05}, percentile_90 = {p90}")

    # Pearson Correlation Coefficient for lags m=1 to m=100
    x_axis = [0] * 100
    pearson_cc = [0] * 100
    for m in range(1, 101):
        x_axis[m-1] = m
        cross_cov = ((trace[m:] - EX)*(trace[:-m] - EX)).sum() / (N-m)
        pearson_cc[m-1] = cross_cov/CX2

    plt.plot(x_axis, pearson_cc)
    plt.xticks([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xlabel("m")
    plt.suptitle(f"Trace{i}: Pearson Correlation Coefficient")
    plt.show()

    # Approximated CDF of the corresponding distribution
    yp = np.r_[1:N+1] / N
    plt.plot(np.sort(trace), yp)
    if (i == 1):
        plt.xlim(0, 35)
    elif (i == 2):
        plt.xlim(0, 6)
    elif (i == 3): 
        plt.xlim(0, 140)
    plt.suptitle(f"Trace{i}: Approximated CDF")
    plt.show()

def calculate_percentile(trace, P):
    N = trace.shape[0]
    trace = np.sort(trace)
    h = (N-1) * P/100
    if (h == N):
        return trace[h]
    elif (h < N):
        h_int = np.floor(h)
        return trace[int(h_int)] + (h - h_int) * (trace[int(h_int)+1] - trace[int(h_int)])

for index, trace in enumerate([trace_1, trace_2, trace_3]):
    computation(trace, index+1)
    
