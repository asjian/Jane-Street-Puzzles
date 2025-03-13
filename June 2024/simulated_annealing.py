import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import copy
import random
import itertools
import operator

df = pd.read_csv('census.csv')
pops = df.set_index('State').to_dict()['Population']

pops = {k.lower().replace(' ', ''): v for k, v in pops.items()}
states = list(pops.keys())
freqs = Counter(''.join(states))
letters = list(freqs.keys())

total_sum = sum(freqs.values()) + 7.0 * len(freqs) # + 2.0 for smoothing
prob_dist = {k: (v + 7.0) / total_sum for k, v in freqs.items()}
probs = list(prob_dist.values())

def gridify(s):
    grid = []
    for i in range(0, 25, 5):
        grid.append(list(s[i:i+5]))
    return grid

def make_adjset(grid):
    offset = ord('a')
    adj = [defaultdict(list) for k in range(25)]
    for i in range(25):
        x, y = i//5, i%5
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if not (dx == 0 and dy == 0) and x+dx > -1 and x+dx < 5 and y+dy > -1 and y+dy < 5:
                    adj[i][grid[x+dx][y+dy]].append(5*(x+dx) + (y+dy))
    return adj

def score(grid): #5x5
    startdex = {letter:set() for letter in letters}
    for j in range(len(grid)):
        startdex[grid[j//5][j%5]].add(j)

    adjset = make_adjset(grid)
    visited = {}
    def dfs(state, x, y, idx, option):
        v = visited.get((x,y,idx), None)
        if v or v == option:
            return False
        visited[(x,y,idx)] = option

        gv, sv = grid[x][y], state[idx]
        if idx == len(state) - 1:
            if option:
                return True
            if gv == sv:
                return True
            return False

        if not gv == sv:
            if not option:
                return False
            option = False

        if option:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if not (dx == 0 and dy == 0) and x+dx > -1 and x+dx < 5 and y+dy > -1 and y+dy < 5:
                        if dfs(state, x+dx, y+dy, idx+1, option):
                            return True
        else:
            for grid_idx in adjset[5*x+y][state[idx+1]]:
                if dfs(state, grid_idx//5, grid_idx%5, idx+1, False):
                    return True
        return False
    score = 0
    for state in states:
        visited = {}
        found = False
        starts = startdex[state[0]]
        for j in starts:
            if dfs(state, j//5, j%5, 0, True):
                    score += pops[state]
                    found = True
                    break
        if not found:
            for i in range(25):
                if not i in starts:
                    if dfs(state, i//5, i%5, 0, True):
                        score += pops[state]
                        break
    return score

points = [(i, j) for i in range(1, 25) for j in range(0, i)]
dist_probs = np.array([1/(3 + abs(p[0]//5 - p[1]//5) + abs(p[0]%5 - p[1]%5)) for p in points])
dist_probs /= dist_probs.sum()

def perturb_grid(orig_grid, num_changes=3):
    grid = copy.deepcopy(orig_grid)
    for _ in range(num_changes):
        if random.choice([True, False]):
            i = random.randint(0, 24)
            grid[i//5][i%5] = np.random.choice(letters)
        else:
            #temp = np.random.choice(range(300), replace = True, p = dist_probs)
            i1, i2 = random.sample(range(25), 2)
            grid[i1//5][i1%5], grid[i2//5][i2%5] = grid[i2//5][i2%5], grid[i1//5][i1%5]

    return grid

def sa(curr_grid, T = 10**8, k = 0.9999978, iterations = 3 * 10**6, start_i = 0, filename = 'sagrid.txt'):
    best_grid = copy.deepcopy(curr_grid)
    curr_score = score(curr_grid)
    best_score = curr_score
    iter_since_best, T_best = 0, T
    T *= (k**start_i)

    for i in range(int(start_i), int(iterations)):
        if i%10000 == 0:
            print(i, best_score)

        changed_grid = perturb_grid(curr_grid, np.random.geometric(p = 0.5))
        newscore = score(changed_grid)

        if newscore > curr_score or random.uniform(0, 1) < np.exp((newscore - curr_score)/T):
            curr_grid = copy.deepcopy(changed_grid)
            curr_score = newscore

        if curr_score > best_score:
            best_grid = copy.deepcopy(curr_grid)
            best_score = curr_score
            iter_since_best, T_best = 0, T
            np.savetxt(filename, np.array(curr_grid), fmt='%s')
            with open(filename, 'a') as file:
                file.write(str(curr_score))

        elif i > iterations//2:
            iter_since_best += 1
            if iter_since_best > 200000:
                T = T_best
                iter_since_best = 0
        T *= k

    return best_grid, best_score

def random_init():
    return gridify(np.random.choice(letters, size = 25, p = probs))

print(sa(random_init(), filename='sa.txt'))
#print(sa(gridify('entadwenigyrsortocalahmin'), iterations = 2.5 * 10**6, start_i = 2 * 10**6, filename = 'sa.txt'))
#print(score2(gridify('amonedsihtinacagrolnkeywi')))
