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

# input data -----------------------------------------------------
tasks = {
    0: {'r': 4, 'D': 6, 'T': 6, 'jit':4, 'p':2},
    1: {'r': 0, 'D': 4, 'T': 8, 'jit':4, 'p':2}}
    #2: {'r': 0, 'D': 12, 'T': 12, 'jit':0, 'p':2},
    #3: {'r': 0, 'D': 16, 'T': 16, 'jit':0, 'p':1},
    #4: {'r': 0 , 'D': 48, 'T': 48, 'jit':0, 'p':5}}

# processed data
n_tasks = len(tasks)
H = int(np.lcm.reduce([tasks[i]['T'] for i in range(n_tasks)]))
print("The hyper-period is {}".format(H))
nJobs = [int(H / tasks[i]['T']) for i in range(n_tasks)]

# solver
sol = Solver()

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
        sol.add(r[i][k] == tasks[i]['r'] + k * tasks[i]['T'])
        sol.add(D[i][k] == tasks[i]['D'] + k * tasks[i]['T'])
        sol.add(r[i][k] <= s[i][k],
                s[i][k] <= D[i][k] - tasks[i]['p'])

# jitter constraints 2 and 3
jit = [Int("jit_%s" % (i+1)) for i in range(n_tasks)]
for i in range(n_tasks):
    for k in range(nJobs[i]):
        for l in range(k+1, nJobs[i]):
            sol.add(jit[i] >= abs((s[i][k] - (k - 1) * tasks[i]['T']) - (s[i][l] - (l - 1) * tasks[i]['T'])))
    sol.add(jit[i] <= tasks[i]['jit'])

# resource constraints 4
for i in range(n_tasks):
    for j in range(i+1, n_tasks):
        for k in range(nJobs[i]):
            for l in range(nJobs[j]):
                sol.add(Xor(
                    s[i][k] + tasks[i]['p'] <= s[j][l],
                    s[j][l] + tasks[j]['p'] <= s[i][k]
                ))

# solve the model
if sol.check() == sat:
    m = sol.model()
    start_times = [[m.evaluate(s[i][j]) for j in range(nJobs[i])]
         for i in range(n_tasks)]
    print("Matrix of the start times is ")
    print_matrix(start_times)
else:
    print("failed to solve")
