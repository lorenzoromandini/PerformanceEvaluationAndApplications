from collections import deque

import numpy as np


def computation():
    s = 1
    t = 0

    tMax = 24000

    tS1 = 0
    tS2 = 0
    tS3 = 0
    tS4 = 0
    C = 0

    cash = 0.0
    time20h = 1200

    while t < tMax:
        if s == 1:
            u = np.random.rand()
            if u < 0.2:
                ns = 1
                C += 1
            elif u < 0.48:
                ns = 2
            else:
                ns = 3
            dt = 0
            dt += setDistribution(1)
            tS1 += dt
        if s == 2:
            ns = 4
            dt = 0
            dt += setDistribution(2)
            tS2 += dt
            uCash = np.random.rand()
            if uCash < 0.9:
                cash += 2.50
            elif uCash < 0.96:
                cash += 4
            else:
                cash += 6
        if s == 3:
            ns = 4
            dt = 0
            dt += setDistribution(3)
            tS3 += dt
        if s == 4:
            ns = 1
            dt = 0
            dt += setDistribution(4)
            tS4 += dt
            C += 1

        s = ns
        t += dt

    pS1 = tS1 / t
    pS2 = tS2 / t
    pS3 = tS3 / t
    pS4 = tS4 / t
    avgTranDuration = t / C
    avgCash20h = cash * time20h / t

    print("Prob(Waiting): ", pS1)
    print("Prob(Cash transaction): ", pS2)
    print("Prob(Electronic transaction): ", pS3)
    print("Prob(Printing): ", pS4)
    print("Average duration of a transaction: ", avgTranDuration, "min")
    print("Average cash in 20 hours: ", avgCash20h, "€")


def setDistribution(state):
    if state == 1:
        u1 = np.random.rand()
        u2 = np.random.rand()
        l1_hyperexp = 0.4
        l2_hyperexp = 0.1
        p1_hyperexp = 0.8
        XhyperExp = 0.0
        if u1 < p1_hyperexp:
            XhyperExp = -np.log(u2) / l1_hyperexp
        else:
            XhyperExp = -np.log(u2) / l2_hyperexp
        return XhyperExp
    elif state == 2:
        u = np.random.rand()
        lexp = 0.4
        Xexp = -np.log(u) / lexp
        return Xexp
    elif state == 3:
        lerlang = 2
        kerlang = 4
        u = np.random.rand(kerlang)
        Xerlang = -np.sum(np.log(u)) / lerlang
        return Xerlang
    elif state == 4:
        l1_hypererl = 10
        l2_hypererl = 0.1
        k1_hypererl = 2
        k2_hypererl = 1
        p1_hypererl = 0.95
        u = np.random.rand()
        XhyperErl = 0.0
        if u < p1_hypererl:
            u1 = np.random.rand(k1_hypererl)
            XhyperErl = -np.sum(np.log(u1)) / l1_hypererl
        else:
            u2 = np.random.rand(k2_hypererl)
            XhyperErl = -np.sum(np.log(u2)) / l2_hypererl
        return XhyperErl


computation()
