import gurobipy as gp
from gurobipy import GRB

# Data
exams=[]
f = open("C:\\Users\kvend\Downloads\DODMproject2023-main\DODMproject2023-main\instances\instance01.exm", "r")
for x in f:
    try:
        [exam_ID, number_of_students]=x.split()
        exams.append(exam_ID)
    except:
        pass
f.close()

f = open("C:\\Users\kvend\Downloads\DODMproject2023-main\DODMproject2023-main\instances\instance01.slo", "r")
time_slots=range(1,int(f.readline().split()[0])+1)
distance=range(1,min(6,len(time_slots)))
f.close()

enrollment_matrix=dict()
conflicting_exams=dict()
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

# Csak azok, amelyek ütküznek és csak az egyik sorrend.

# Data
#exams = ['e1', 'e2', 'e3','e4']  # List of exams
#students = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8',]  # List of students
#time_slots = range(1,7)  # List of time slots
#conflicting_exams = {('e1', 'e2'): 2, ('e1', 'e3'): 3, ('e2', 'e3'): 2}  # Conflicting exams
#enrollment_matrix ={'s1': ['e1', 'e2', 'e3'],'s2': ['e1', 'e3'],'s3': ['e4'],'s4': ['e3'],'s5': ['e1', 'e3'],'s6': ['e4'],'s7': ['e2', 'e3'],'s8': ['e1', 'e2']}
#distance=range(min(6,len(time_slots))) # Distances of the pairs of the exams which has not larger distance than 5 (or the number of timeslots if it is lower than 5)


# Create the model
model = gp.Model()

# Variables
x = model.addVars(time_slots, exams, vtype=GRB.BINARY, name='x')  # Binary variables for time slot-exam pairs
y = model.addVars(distance, time_slots, exams, exams, vtype=GRB.BINARY, name='y')  # Binary variables for exam distances
u_s=model.addVars(students, vtype=GRB.BINARY, name='u_s') # Binary variable for students with back-to-back exams

# Constraints
# Constraint 1: Each exam is scheduled exactly once during the examination period
model.addConstrs(x.sum('*',e) == 1 for e in exams)

# Constraint 2: Two conflicting exams are not scheduled in the same time-slot
for t in time_slots:
  for (e1,e2) in conflicting_exams.keys():
    if conflicting_exams[(e1,e2)]>0:
      model.addConstr(x[t, e1] + x[t, e2]<= 1)

# Constraint 3: Expressing u_s variables with x variables
for s in students:
    for t in range(1,len(time_slots)):
        for (e1,e2) in conflicting_exams.keys():
            u_s[s] >= x[t, e1] + x[t+1, e2]-1
            u_s[s] >= x[t+1, e1] + x[t, e2]-1

# Objective function
model.setObjective(gp.quicksum(u_s), GRB.MINIMIZE)

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
