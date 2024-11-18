import matplotlib.pyplot as plt
import numpy as np
from scipy.special import factorial

N = 10000

t = np.r_[1 : N + 1] / 200

############### Exponential ###############
u = np.random.rand(N)
lexp = 0.25

Xexp = -np.log(u) / lexp
Xexp.sort()

Fexp = 1 - np.exp(-lexp * t)

############### Pareto ###############
u = np.random.rand(N)
alpha_pareto = 2.5
m_pareto = 3

Xpareto = m_pareto / (u ** (1 / alpha_pareto))
Xpareto.sort()

Fpareto = np.maximum(0, 1 - ((m_pareto / t) ** alpha_pareto))

############### Erlang ###############
kerlang = 8
lerlang = 0.8

u = np.random.rand(kerlang, N)

Xerlang = -np.sum(np.log(u), axis=0) / lerlang

Xerlang.sort()

Ferlang = 1 - np.sum(
    [
        ((lerlang * t) ** n) * np.exp(-lerlang * t) / factorial(n)
        for n in range(0, kerlang)
    ],
    axis=0,
)

############### Hypo Exp ###############
u1 = np.random.rand(N)
u2 = np.random.rand(N)

l1_hypo = 0.25
l2_hypo = 0.4
Xhypo = -np.log(u1) / l1_hypo - np.log(u2) / l2_hypo
Xhypo.sort(0)

Fhypo = 1 - (l2_hypo * np.exp(-l1_hypo * t) - l1_hypo * np.exp(-l2_hypo * t)) / (
    l2_hypo - l1_hypo
)

############### Hyper Exp ###############
u1 = np.random.rand(N)
u2 = np.random.rand(N)

l1_hyper = 1
l2_hyper = 0.05
p1_hyper = 0.75

Xhyper = [0.0] * N
for i in range(0, N):
    if u1[i] < p1_hyper:
        Xhyper[i] = -np.log(u2[i]) / l1_hyper
    else:
        Xhyper[i] = -np.log(u2[i]) / l2_hyper
Xhyper.sort()

Fhyper = 1 - p1_hyper * np.exp(-t * l1_hyper) - (1 - p1_hyper) * np.exp(-t * l2_hyper)

############### CDF ###############

yp = np.r_[1 : N + 1] / N

distributions = [Fexp, Fpareto, Ferlang, Fhypo, Fhyper]
generated = [Xexp, Xpareto, Xerlang, Xhypo, Xhyper]
titles = ["Exponential", "Pareto", "Erlang", "Hypo Exponential", "Hyper Exponential"]

for i in range(len(distributions)):
    plt.figure(figsize=(10, 7))

    plt.plot(generated[i], yp, ".", label="Random variable generation", color="blue")
    plt.plot(t, distributions[i], label=titles[i] + " CDF", color="red")

    plt.xlim([-1, 25])
    plt.title(titles[i])
    plt.grid(True)
    plt.legend(loc="lower right", fontsize="medium", frameon=True)
    plt.show()
