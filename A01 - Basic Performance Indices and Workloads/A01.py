import matplotlib.pyplot as plt
import numpy as np

traceIn = np.loadtxt("Logger1.csv")
traceOut = np.loadtxt("Logger2.csv")
C = traceIn.shape[0]

A_T = np.zeros((C, 1))
A_T[:, 0] = traceIn

C_T = np.zeros((C, 1))
C_T[:, 0] = traceOut

T = C_T[-1, 0]

lambda_ = C / T
print(f"Arrival rate = {lambda_} cars/min")

X = C / T
print(f"Throughput = {X} cars/min")

avg_inter_arrival = 1 / lambda_
print(f"Average arrival rate = {avg_inter_arrival} min")

s_i = [0] * C
s_i[0] = C_T[0] - A_T[0]
for i in range(1, C):
    s_i[i] = C_T[i] - max(A_T[i], C_T[i - 1])

B = np.sum(s_i)

U = B / T
print(f"Utilization = {U}")

S = B / C
print(f"Average service time = {S} min")

r_i = C_T - A_T

R = np.mean(r_i)
print(f"Average response time = {R} min")

N = X * R
print(f"Average number of cars = {N}")


AC_T = np.block([[A_T, np.ones((C, 1))], [C_T, -np.ones((C, 1))]])
AC_T = AC_T[AC_T[:, 0].argsort()]
AC_T[:, 1] = np.cumsum(AC_T[:, 1])
AC_T = np.c_[[AC_T[1:-1, 0] - AC_T[0:-2, 0], AC_T[1:-1, 1]]].T

# Distribution of the number of cars in the road segment (from 0 to 25)
x_1 = [0] * 26
y_1 = [0] * 26
for i in range(0, 26):
    x_1[i] = i
    y_1[i] = np.sum(AC_T[AC_T[:, 1] == i, 0]) / T

plt.bar(x_1, y_1)
plt.xlabel("Cars")
plt.suptitle("Distribution of the number of cars in the road segment")
plt.show()

# Response time distribution (between 1 and 40 minutes, with a granularity of 1 min.)
x_2 = [0] * 40
y_2 = [0] * 40
for i in range(1, 41):
    x_2[i - 1] = i
    y_2[i - 1] = np.sum(r_i < x_2[i - 1]) / C

plt.plot(x_2, y_2)
plt.xticks([1, 5, 10, 15, 20, 25, 30, 35, 40])
plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
plt.xlabel("Response time")
plt.suptitle("Response time distribution")
plt.show()

# Service time distribution (between 0.1 and 5 minutes, with a granularity of 0.1 minutes)
x_3 = np.arange(0.1, 5.1, 0.1)
y_3 = [0] * 50
for i in range(1, 51):
    y_3[i - 1] = np.sum(s_i < x_3[i - 1]) / C

plt.plot(x_3, y_3)
plt.xticks([0.1, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
plt.xlabel("Service time")
plt.suptitle("Service time distribution")
plt.show()
