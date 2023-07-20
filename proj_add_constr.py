import gurobipy as gp
from gurobipy import GRB

# Data
exams=[] # Set of exams
f = open("C:\\Users\kvend\Downloads\DODMproject2023-main\DODMproject2023-main\instances\instance01.exm", "r")
for x in f:
    try:
        [exam_ID, number_of_students]=x.split()
        exams.append(exam_ID)
    except:
        pass
f.close()

f = open("C:\\Users\kvend\Downloads\DODMproject2023-main\DODMproject2023-main\instances\instance01.slo", "r")
time_slots=range(1,int(f.readline().split()[0])+1) # Set of time slots. Number from 1 to T.
distance=range(1,min(6,len(time_slots))) # The distance between conflicting exams.
f.close()

enrollment_matrix=dict() # Dictionary for the enrolments of the students.
conflicting_exams=dict() # Dictionary for the conflicting exams.
f = open("C:\\Users\kvend\Downloads\DODMproject2023-main\DODMproject2023-main\instances\instance01.stu", "r")
for x in f:
    try:
        enrollment_matrix[x.split()[0]].append(x.split()[1])
    except:
        enrollment_matrix[x.split()[0]]=[x.split()[1]]
f.close()
students=enrollment_matrix.keys()

for e1 in exams:
    for e2 in exams:
        if e1!=e2 and (e2,e1) not in enrollment_matrix.keys():
            for s in students:
                if e1 in enrollment_matrix[s] and e2 in enrollment_matrix[s]:
                    if (e1,e2) not in enrollment_matrix.keys():
                        conflicting_exams[(e1,e2)]=1
                    else:
                        conflicting_exams[(e1,e2)]=conflicting_exams[(e1,e2)]+1

# Data
#exams = ['e1', 'e2', 'e3','e4']  # List of exams
#students = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8',]  # List of students
#time_slots = range(1,7)  # List of time slots
#conflicting_exams = {('e1', 'e2'): 2, ('e1', 'e3'): 3, ('e2', 'e3'): 2}  # Conflicting exams
#enrollment_matrix ={'s1': ['e1', 'e2', 'e3'],'s2': ['e1', 'e3'],'s3': ['e4'],'s4': ['e3'],'s5': ['e1', 'e3'],'s6': ['e4'],'s7': ['e2', 'e3'],'s8': ['e1', 'e2']}
#distance=range(min(6,len(time_slots)))


# Create the model
model = gp.Model()

# Variables
x = model.addVars(time_slots, exams, vtype=GRB.BINARY, name='x')  # Binary variables for time slot-exam pairs
y = model.addVars(distance, time_slots, exams, exams, vtype=GRB.BINARY, name='y')  # Binary variables for exam distances
u = model.addVars(exams, exams, vtype=GRB.INTEGER, name='u') # Penalty for pair of exams
u6_t=model.addVars(time_slots[:-5], vtype=GRB.BINARY, name='u6_t') # 6 consecutive time slots contain conflicting exams
u2_t=model.addVars(time_slots[:-1], vtype=GRB.BINARY, name='u2_t') # 2 consecutive time slots contain conflicting exams
u3_t=model.addVars(time_slots[:-2], vtype=GRB.BINARY, name='u3_t') # 3 consecutive time slots contain conflicting exams


# Constraints

# Constraint 1: Each exam is scheduled exactly once during the examination period
model.addConstrs((x.sum('*',e) == 1 for e in exams), name='exams_once')

# Constraint 2: Two conflicting exams are not scheduled in the same time-slot
for t in time_slots:
  for (e1,e2) in conflicting_exams.keys():
    if conflicting_exams[(e1,e2)]>0:
      model.addConstr((x[t, e1] + x[t, e2]<= 1), name='no_conflict')

# Constraint: At most 3 consecutive time slots can have conflicting exams

for (e1,e2) in conflicting_exams.keys():
    for t in time_slots[:-1]:
        model.addConstr(x[t, e1] + x[t+1, e2]<= 1)
        model.addConstr(x[t+1, e1] + x[t, e2]<= 1)

# Constraint: If two consecutive time slots contain conflicting exams, then no conflicting exam can be scheduled in the next 3 time slots.

for t in time_slots[:-1]:
    for (e1,e2) in conflicting_exams.keys():
        for t1 in range(t,t+2):
            for t2 in range(t,t+2):
                model.addConstr(u2_t[t] >= x[t1, e1] + x[t2, e2]-1)
for t in time_slots[:-2]:
    for (e1,e2) in conflicting_exams.keys():
        for t1 in range(t,t+3):
            for t2 in range(t,t+3):
                model.addConstr(u3_t[t] >= x[t1, e1] + x[t2, e2]-1)
for t in time_slots[:-4]:
    model.addConstr(u2_t[t]+u3_t[t+2]<=1)


# Constraint: Include a bonus profit each time no conflicting exams are scheduled for 6 consecutive time slots.

for t in time_slots[:-5]:
    for (e1,e2) in conflicting_exams.keys():
        for t1 in range(t,t+6):
            for t2 in range(t,t+6):
                model.addConstr(u6_t[t] >= x[t1, e1] + x[t2, e2]-1)
            


# Constraint 3: Expressing u variables with x variables
for i in distance:
    for t in time_slots:
        for (e1,e2) in conflicting_exams.keys():
            if t+i<=len(time_slots):
                model.addConstr(u[e1,e2] >= (2**(5-i) * x[t,e1]  + 2**(5-i) * x[t+i, e2]  - 2**(5-i))*conflicting_exams[(e1,e2)])
                model.addConstr(u[e1,e2] >= (2**(5-i) * x[t+i,e1]  + 2**(5-i) * x[t, e2]  - 2**(5-i))*conflicting_exams[(e1,e2)])

b=0.1 # Weight of the bonus points
# Objective function
model.setObjective((gp.quicksum(u)+b*gp.quicksum(u6_t))/len(students), GRB.MINIMIZE)

# Solve the model
model.optimize()

# Print the optimal solution
if model.status == GRB.OPTIMAL:
    sol=model.getAttr('X', x)
    for key in sol.keys():
      if sol[key]==1:
        print(key[1]," : ", key[0])
else:
    print('No solution found.')
