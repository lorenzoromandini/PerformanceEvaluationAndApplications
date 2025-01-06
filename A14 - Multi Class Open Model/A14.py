import numpy as np
from scipy import linalg

PA = np.array(
    [
        [0.0, 1.0],
        [0.1, 0.0],
    ]
)

PB = np.array(
    [
        [0.0, 1.0],
        [0.08, 0.0],
    ]
)

PC = np.array(
    [
        [0.0, 1.0],
        [0.12, 0.0],
    ]
)

lamINA = np.zeros(2)
lamINB = np.zeros(2)
lamINC = np.zeros(2)

lamINA[0] = 1.5 / 60
lamINB[0] = 2.5 / 60
lamINC[0] = 2 / 60

lamA = sum(lamINA)
lamB = sum(lamINB)
lamC = sum(lamINC)

lA = lamINA / lamA
lB = lamINB / lamB
lC = lamINC / lamC

I = np.eye(2)

vkA = linalg.solve((I - PA).T, lA)
vkB = linalg.solve((I - PB).T, lB)
vkC = linalg.solve((I - PC).T, lC)

SkA = [8, 10]
SkB = [3, 2]
SkC = [4, 7]

XA = lamA
XB = lamB
XC = lamC

X = XA + XB + XC

XkA = vkA * XA
XkB = vkB * XB
XkC = vkC * XC

Xk = [XkA[0] + XkB[0] + XkC[0], XkA[1] + XkB[1] + XkC[1]]

DkA = vkA * SkA
DkB = vkB * SkB
DkC = vkC * SkC

UkA = XA * DkA
UkB = XB * DkB
UkC = XC * DkC

Uk = [UkA[0] + UkB[0] + UkC[0], UkA[1] + UkB[1] + UkC[1]]
print("Utilisation of the production station:", Uk[0])
print("Utilisation of the packaging station:", Uk[1])

RkA = [DkA[0] / (1 - Uk[0]), DkA[1] / (1 - Uk[1])]
RkB = [DkB[0] / (1 - Uk[0]), DkB[1] / (1 - Uk[1])]
RkC = [DkC[0] / (1 - Uk[0]), DkC[1] / (1 - Uk[1])]

RA = sum(RkA)
RB = sum(RkB)
RC = sum(RkC)
print("Average system response time (Class A - RA [min]):", RA)
print("Average system response time (Class B - RB [min]):", RB)
print("Average system response time (Class C - RC [min]):", RC)

Rk = [
    XA / X * RkA[0] + XB / X * RkB[0] + XC / X * RkC[0],
    XA / X * RkA[1] + XB / X * RkB[1] + XC / X * RkC[1],
]

R = sum(Rk)
print("Class independent average system response time (R [min]):", R)


NkA = [XA * RkA[0], XA * RkA[1]]
NkB = [XB * RkB[0], XB * RkB[1]]
NkC = [XC * RkC[0], XC * RkC[1]]

NA = sum(NkA)
NB = sum(NkB)
NC = sum(NkC)
print("Average number of jobs in the system (Class A - NA):", NA)
print("Average number of jobs in the system (Class B - NB):", NB)
print("Average number of jobs in the system (Class C - NC):", NC)

Nk = [NkA[0] + NkB[0] + NkC[0], NkA[1] + NkB[1] + NkC[1]]

N = sum(Nk)
print("Class independent average number of jobs in the system (N):", N)
