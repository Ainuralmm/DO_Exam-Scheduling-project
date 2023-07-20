# **Exam Scheduling with Gurobi**

## **Description**

This project presents an integer programming model to optimize the scheduling of exams during the examination period while minimizing the penalties associated with conflicting exams. The model ensures that each exam is scheduled exactly once, no conflicting exams are held in the same time slot, and other equity measures are considered to enhance the overall quality of the schedule.

## **Table of Contents**

1. **Introduction**
2. **Data**
3. **Requirements**
4. **Usage**
5. **Optimization Model**
6. **Results**


## **Introduction**

The Exam Scheduling project aims to create an optimal schedule for exams during an examination period. It takes into account various constraints and equity measures to ensure fair and efficient scheduling.

## **Data**

The project utilizes the following data:

- **`exams`**: A list of exams (e.g., ['e1', 'e2', 'e3']).
- **`students`**: A list of students (e.g., ['s1', 's2', 's3']).
- **`time_slots`**: A list of time slots (e.g., ['t1', 't2', 't3']).
- **`conflicting_exams`**: A dictionary representing the conflicts between exams (e.g., {('e1', 'e2'): 1, ('e2', 'e3'): 0, ('e1', 'e3'): 1}).
- **`enrollment_matrix`**: A dictionary representing the enrollment matrix of students and exams (e.g., {'s1': ['e1', 'e2'], 's2': ['e2', 'e3'], 's3': ['e1', 'e3']}).

## **Requirements**

To run the code, you need to have Gurobi installed on your machine. Gurobi is a mathematical optimization solver that will be used to find the optimal exam schedule.

## **Usage**

1. Install Gurobi on your machine.
2. Update the data in the provided Python script (e.g., exams, students, time_slots, conflicting_exams, enrollment_matrix) to match your specific case.
3. Run the Python script in your terminal/command prompt using **`python your_script.py`**.

## **Optimization Model**

The project formulates the exam scheduling problem as an integer programming model. It introduces binary variables to represent the scheduling of exams in each time slot. Constraints are added to ensure that each exam is scheduled exactly once, conflicting exams are not held in the same time slot, and other equity measures are taken into account.

## **Results**

Upon execution, the script will provide the optimal exam schedule and the objective value, which represents the minimized penalties.
