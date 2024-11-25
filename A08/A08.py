import numpy as np
from scipy import linalg

data = np.loadtxt("Data.csv", delimiter=";", encoding="utf-8-sig")

probNextSongs = (100 - data[:, 1] - data[:, 2]) / (data[:, 0] * 100)
probExtendSongs = data[:, 1] / (data[:, 0] * 100)
probSkipSongs = data[:, 2] / (data[:, 0] * 100)
probSkipNextIfExtended = data[:, 4] / (data[:, 3] * 100)
probNextSongIfExtended = (100 - data[:, 4]) / (data[:, 3] * 100)

nSongs = len(data)

Q = np.zeros((2 * nSongs, 2 * nSongs))

for i in range(nSongs):
    #### Unextended state i ####

    # Self-transition
    Q[2 * i, 2 * i] = -probNextSongs[i] - probSkipSongs[i] - probExtendSongs[i]
    # Transition to extended state i'
    Q[2 * i, 2 * i + 1] = probExtendSongs[i]
    # Transition to next state
    Q[2 * i, 2 * (i + 1) % (2 * nSongs)] = probNextSongs[i]
    # Transition to skip state
    Q[2 * i, 2 * (i + 2) % (2 * nSongs)] = probSkipSongs[i]

    #### Extended state i' ####

    # Self-transition for extended state
    Q[2 * i + 1, 2 * i + 1] = -probNextSongIfExtended[i] - probSkipNextIfExtended[i]
    # Transition to next state
    Q[2 * i + 1, 2 * (i + 1) % (2 * nSongs)] = probNextSongIfExtended[i]
    # Transition to skip state
    Q[2 * i + 1, 2 * (i + 2) % (2 * nSongs)] = probSkipNextIfExtended[i]


Q2 = Q.copy()
Q2[:, 0] = np.ones(2 * nSongs)
u = np.zeros(2 * nSongs)
u[0] = 1
pi = linalg.solve(Q2.T, u)


a_songs = [
    np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # 1st song
    np.array([0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # 2nd song
    np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),  # 5th song
    np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]),  # 9th song
    np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]),  # 10th song
]

probabilities = [pi @ a for a in a_songs]

for i, prob in enumerate(probabilities, 1):
    print(f"Probability of song {i} being played:", prob)

# Average cost of songs
a_cost = [float(value) for row in data for value in [row[5], row[5]]]
avgCost = pi @ a_cost
print("Average cost of the songs:", avgCost)


xi0 = np.zeros((2 * nSongs, 2 * nSongs))
xi0[2 * nSongs - 2, 0] = 1
xi0[2 * nSongs - 1, 0] = 1

RTLP = ((Q * xi0) @ np.ones(2 * nSongs)) @ pi

print("Number of shows per day:", RTLP * 60 * 60 * 24)
print("Average show duration [min.]:", 1 / (RTLP * 60))
