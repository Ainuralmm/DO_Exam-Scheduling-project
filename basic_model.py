import gurobipy as gp
from gurobipy import GRB


# Data
exams = ['e1', 'e2', 'e3']  # List of exams
students = ['s1', 's2', 's3']  # List of students
time_slots = range(1,4)  # List of time slots
conflicting_exams = {('e1', 'e2'): 2, ('e2', 'e3'): 0, ('e1', 'e3'): 1}  # Conflicting exams
enrollment_matrix = {'s1': ['e1', 'e2'], 's2': ['e1','e2'], 's3': ['e1', 'e3']}  # Enrollment matrix
distance=range(1,min(6,len(time_slots))) # Distances of the pairs of the exams which has not larger distance than 5 (or the number of timeslots if it is lower than 5)

# Create the model
model = gp.Model()

# Variables
x = model.addVars(time_slots, exams, vtype=GRB.BINARY, name='x')  # Binary variables for time slot-exam pairs
y = model.addVars(distance, time_slots, exams, exams, vtype=GRB.BINARY, name='y')  # Binary variables for exam distances
y_prime = model.addVars(distance, time_slots, exams, exams, vtype=GRB.BINARY, name='y_prime')  # Binary variables for exam distances
u = model.addVars(distance, exams, exams, vtype=GRB.INTEGER, name='u') # Penalty for pair of exams

# Constraints
# Constraint 1: Each exam is scheduled exactly once during the examination period
model.addConstrs((x.sum('*', e) == 1 for e in exams), name='exams_once')

# Constraint 2: Two conflicting exams are not scheduled in the same time-slot
model.addConstrs((x[t, e1] + x[t, e2]<= 1 for t in time_slots for e1, e2 in conflicting_exams if conflicting_exams[(e1,e2)]!=0),
                 name='no_conflict')

# Constraint 3: Expressing yi variables with x variables
model.addConstrs((y[i, t, e1, e2] >= x[t, e1] + x[t+i, e2] - 1 for i in distance for t in time_slots
                 for e1 in exams for e2 in exams if e1 != e2 and t+i<=len(time_slots)), name='y_expr')
model.addConstrs((y_prime[i, t, e1, e2] >= x[t+i, e1] + x[t, e2] - 1 for i in distance for t in time_slots
                 for e1 in exams for e2 in exams if e1 != e2 and t+i<=len(time_slots)), name='y_prime_expr')
for i in distance:
  for e1 in exams:
    for e2 in exams:
      if e1!=e2:
        model.addConstr((u[i, e1, e2]==sum(y[i,t,e1,e2]+y_prime[i,t,e1,e2] for t in range(1,len(time_slots)-i+1))),name='u_expr')
#model.addConstr((u[i, e1, e2]==sum(y[i,t,e1,e2]+y_prime[i,t,e1,e2] for t in range(1,len(time_slots)-i)) for i in distance
                                 #for e1 in exams for e2 in exams if e1 != e2), name='u_expr')

# Objective function
objective = sum(u[i,e1,e2] * (2**(5-i)) * (conflicting_exams.get((e1, e2), 0) / len(students))
                for i in distance
                for e1 in exams
                for e2 in exams if e1 != e2)
model.setObjective(objective, GRB.MINIMIZE)

# Solve the model
model.optimize()

# Print the optimal solution
if model.status == GRB.OPTIMAL:
    #for var in model.getVars():
        #print(f'{var.varName} = {var.x}')
    #print(f'Objective value: {model.objVal}')
    sol=model.getAttr('X', x)
    for key in sol.keys():
      if sol[key]==1:
        print(key[1]," : ", key[0])
else:
    print('No solution found.')
