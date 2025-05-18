from random import random
from math import comb, log2, exp

V = 2
T = 2

# initializes the matrix with random values
def initialize_matrix(n, k):
    matrix = [[int(random()*2) for j in range(k)] for i in range(n)]
    return matrix

# checks the columns pairwise to total missing values
def objective(m, k):
    misses = 0
    for i in range(k-1):
        for j in range(i+1, k):
            pairs = [(0,0), (0,1), (1,0), (1,1)]
            for row in m:
                curr = (row[i], row[j])
                if curr in pairs:
                    pairs.remove(curr)
                if len(pairs) == 0:
                    break
            misses += len(pairs)
    return misses

# generates deep copies of the given matrix with proposed changes
def neighborhood(m, k):
    j = int(random()*k)
    neighbors = []
    for i in range(len(m)):
        m_copy = [list(r) for r in m]
        m_copy[i][j] ^= 1
        neighbors.append(m_copy)
    return neighbors

# conducts the annealing process
def simulated_annealing(k):
    temp = k # temperature
    N = int(pow(V, T) * log2(k)) # calculates N
    matrix = initialize_matrix(N, k) # initial solution
    prev = objective(matrix, k)
    phi = pow(V, T) * comb(k, T) # calculates the frozen factor
    freeze_count = 0

    iteration = 0

    while freeze_count < phi:
        iteration += 1
        possibles = neighborhood(matrix, k)
        new_matrix = possibles[int(random()*len(possibles))]
        curr = objective(new_matrix, k)
        if curr == 0:
            return new_matrix, iteration, "solution"
        delta_e = curr - prev # calculates delta E

        if delta_e < 0:
            matrix = new_matrix
            prev = curr
            freeze_count = 0

        else:
            freeze_count += 1
            if random() < exp(-1*delta_e / temp):
                matrix = new_matrix
                prev = curr
        temp *= 0.99
        

    return None, iteration, "frozen"

def print_matrix(m):
    for row in m:
        print(row)

for k in range(5, 8):
    passes = 0
    print("k =", k)
    for trial in range(30):
        matrix, count, status = simulated_annealing(k)
        if status == "solution":
            passes += 1
        
        if trial == 0:
            print("showing one example")
            print_matrix(matrix)
            print("iterations:", count)
            print("stop criterion:", status)
    print("total successes for this k:", passes, "\n")