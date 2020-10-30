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
    0: {'r': 0, 'd': 6, 'T': 6, 'jit':0, 'p':2},
    1: {'r': 0, 'd': 24, 'T': 24, 'jit':0, 'p':2},
    2: {'r': 0, 'd': 3, 'T': 3, 'jit':0, 'p':1},
    3: {'r': 0, 'd': 8, 'T': 8, 'jit':0, 'p':3},
    4: {'r': 0 , 'd': 4, 'T': 4, 'jit':0, 'p':2}}

# processed data
n_tasks = len(tasks)
H = np.lcm.reduce([tasks[i]['T'] for i in range(n_tasks)])
print("The hyper-period is {}".format(H))
nJobs = [int(H / tasks[i]['T']) for i in range(n_tasks)]

# solver
opt = Optimize()

# create variables
s = [ [Int("s_%s_%s" % (i+1, k+1)) for k in range(nJobs[i])]
      for i in range(n_tasks)]
fix = [ Int("fix_%s" % (i+1)) for i in range(n_tasks)]

# mapping variable is positive
for i in range(n_tasks):
    opt.add(fix[i] >= 1)

R = Int("R")

# formulate constraints

# relative time window constraints 1
r = [ [Int("r_%s_%s" % (i+1, k+1)) for k in range(nJobs[i])]
      for i in range(n_tasks)]
d = [ [Int("d_%s_%s" % (i+1, k+1)) for k in range(nJobs[i])]
      for i in range(n_tasks)]
for i in range(n_tasks):
    for k in range(nJobs[i]):
        opt.add(r[i][k] == tasks[i]['r'] + k * tasks[i]['T'])
        opt.add(d[i][k] == tasks[i]['d'] + k * tasks[i]['T'])
        opt.add(r[i][k] <= s[i][k],
                s[i][k] <= d[i][k] - tasks[i]['p'])

# jitter constraints 2 and 3
jit = [Int("jit_%s" % (i+1)) for i in range(n_tasks)]
for i in range(n_tasks):
    for k in range(nJobs[i]):
        for l in range(k+1, nJobs[i]):
            opt.add(jit[i] >= abs((s[i][k] - (k - 1) * tasks[i]['T']) - (s[i][l] - (l - 1) * tasks[i]['T'])))
        opt.add(jit[i] <= tasks[i]['jit'])


# resource constraints 5
for i in range(n_tasks):
    for j in range(i+1, n_tasks):
        for k in range(nJobs[i]):
            for l in range(nJobs[j]):
                opt.add(Implies(fix[i] == fix[j],
                                Or(s[i][k] + tasks[i]['p'] <= s[j][l],
                                    s[j][l] + tasks[j]['p'] <= s[i][k])

                ))

# R setting constraints 7
for i in range(n_tasks):
    opt.add(R >= fix[i])

# criterion 6
h = opt.minimize(R)

# solve the model
if opt.check() == sat:
    opt.lower(h)
    m = opt.model() 
    print("Number of resources is", m.evaluate(opt.objectives()[0]).as_long())
    start_times = [[m.evaluate(s[i][j]) for j in range(nJobs[i])]
         for i in range(n_tasks)]
    print("\nMatrix of the start times is ")
    print_matrix(start_times)
    fix = [m.evaluate(fix[i]) for i in range(n_tasks)]
    print("\nVector of task mappings to resources")
    print(fix)
else:
    print("Failed to solve")

