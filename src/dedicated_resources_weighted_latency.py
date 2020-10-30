"""
	This file is part of the basic_periodic_scheduling_problems program.
	basic_periodic_scheduling_problems is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	CC_Scheduling_WithJitter is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
	GNU General Public License for more details.
	You should have received a copy of the GNU General Public License
	along with basic_periodic_scheduling_problems. If not, see <http://www.gnu.org/licenses/>.
"""

from z3 import *
import numpy as np

def abs(x):
    return If(x >= 0,x,-x)

print("Copyright 2020-2021 Anna Minaeva and Zdenek Hanzalek.");
print("The program is distributed under the terms of the GNU General Public License.\n");

# data -----------------------------------------------------
n_transactions = 2
tasks = {
    0: {'r': 0, 'D': 12, 'T': 6, 'jit':4, 'p':2, 'fix':1, 'pred': [], 'succ': [2], 'transaction':0},
    1: {'r': 0, 'D': 16, 'T': 8, 'jit':4, 'p':2, 'fix':1, 'pred': [], 'succ': [4], 'transaction':1},
    2: {'r': 0, 'D': 12, 'T': 6, 'jit':4, 'p':2, 'fix':2, 'pred': [0], 'succ': [3], 'transaction':0},
    3: {'r': 0, 'D': 12, 'T': 6, 'jit':4, 'p':2, 'fix':3, 'pred': [2], 'succ': [], 'transaction':0},
    4: {'r': 0 , 'D': 16, 'T': 8, 'jit':4, 'p':4, 'fix':2, 'pred': [1], 'succ': [5], 'transaction':1},
    5: {'r': 0 , 'D': 16, 'T': 8, 'jit':4, 'p':4, 'fix':3, 'pred': [4], 'succ': [], 'transaction':1}}
latency_bound = [14, 14]
latency_weight = [1, 100]

# processed data
n_tasks = len(tasks)
H = int(np.lcm.reduce([tasks[i]['T'] for i in range(n_tasks)]))
print("The hyper-period is {}".format(H))
nJobs = [int(H / tasks[i]['T']) for i in range(n_tasks)]

# solver
opt = Optimize()

# create variables
s = [ [Int("s_%s_%s" % (i+1, k+1)) for k in range(nJobs[i])]
      for i in range(n_tasks)]

# formulate constraints

# relative time window constraints 1
r = [ [Int("r_%s_%s" % (i+1, k+1)) for k in range(nJobs[i])]
      for i in range(n_tasks)]
D = [ [Int("D_%s_%s" % (i+1, k+1)) for k in range(nJobs[i])]
      for i in range(n_tasks)]
for i in range(n_tasks):
    for k in range(nJobs[i]):
        opt.add(r[i][k] == tasks[i]['r'] + k * tasks[i]['T'])
        opt.add(D[i][k] == tasks[i]['D'] + k * tasks[i]['T'])
        opt.add(r[i][k] <= s[i][k],
                s[i][k] <= D[i][k] - tasks[i]['p'])

# jitter constraints 2 and 3
jit = [Int("jit_%s" % (i+1)) for i in range(n_tasks)]
for i in range(n_tasks):
    for k in range(nJobs[i]):
        for l in range(k+1, nJobs[i]):
            opt.add(jit[i] >= abs((s[i][k] - (k - 1) * tasks[i]['T']) - (s[i][l] - (l - 1) * tasks[i]['T'])))
    opt.add(jit[i] <= tasks[i]['jit'])

# precedence constraints 8
for i in range(n_tasks):
    for j in tasks[i]['pred']:
        for k in range(nJobs[i]):
            opt.add(s[j][k] + tasks[j]['p'] <= s[i][k])

# end-to-end latency constraints 9 and 10
lat = [Int("lat_%s" % (i+1)) for i in range(n_transactions)]
for i in range(n_transactions):
    sources = [t for t in range(n_tasks) if tasks[t]['transaction'] == i and not tasks[t]['pred']]
    destinations = [t for t in range(n_tasks) if tasks[t]['transaction'] == i and not tasks[t]['succ']]
    for source in sources:
        for dest in destinations:
            for k in range(nJobs[source]):
                opt.add(lat[i] >= s[dest][k] + tasks[dest]['p'] - s[source][k])
    opt.add(lat[i] <= latency_bound[i])

# resource constraints 11
D = [tasks[i]['D'] + k * tasks[i]['T'] for k in range(nJobs[i]) for i in range(n_tasks)]
n_H_max = int(np.ceil(max(D)/H))
for i in range(n_tasks):
    for j in range(i, n_tasks):
        for k in range(nJobs[i]):
            for l in range(nJobs[j]):
                for f in range(n_H_max):
                    for h in range(n_H_max):
                        if tasks[i]['fix'] == tasks[j]['fix']:
                            if i != j or k != l:
                                opt.add(
                                    Xor(
                                        ((s[i][k] + f*H) + tasks[i]['p']) <= (s[j][l] + h*H),
                                        ((s[j][l] + h*H) + tasks[j]['p']) <= (s[i][k] + f*H)
                                    )
                                )


# create objective function ------------------------------------
h = opt.minimize(sum([lat[i] * latency_weight[i] for i in range(n_transactions)]))

# solve the model ----------------------------------------------
if opt.check() == sat:
    opt.lower(h)
    m = opt.model()
    print("\nOptimal objective value is", m.evaluate(opt.objectives()[0]))
    start_times = [[m.evaluate(s[i][j]) for j in range(nJobs[i])]
                   for i in range(n_tasks)]
    print("\nMatrix of the start times is ")
    print_matrix(start_times)
    print("\nVector of task mappings to resources")
    print([tasks[i]['fix'] for i in range(n_tasks)])
else:
    print("Failed to solve")


