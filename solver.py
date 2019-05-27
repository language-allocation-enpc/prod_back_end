from pymprog import *
import numpy as np

import random as rd


FALSE_DATA_MODE = False
PROD_MODE = True

if FALSE_DATA_MODE:
    #Generating data
    from random_data import *
    NB_STUDENTS = 300
    COURSES = generate_random_course_list(50)
    NB_VOWS = 3
    NB_COURSES_IN_VOW=3
    #VOWS = generate_vow_dic(COURSES)
    STUDENTS = generate_random_population(COURSES, NB_VOWS, NB_COURSES_IN_VOW, NB_STUDENTS)

def solve(COURSES, STUDENTS):
    print("COURSES = " +str(COURSES))
    print("STUDENTS = " + str(STUDENTS))
    #indexing the set of students
    S=range(len(STUDENTS))

    #indexing the set of courses
    C=range(len(COURSES))
    #Counting vows
    # vow_set = set()
    # for s in S:
    #     for vow in STUDENTS[s].vows:
    #         vow_set.add(vow)
    NB_VOWS = 2
    print("NB_VOWS = "+str(NB_VOWS))
    #indexation of wishes for cartesian product
    V=range(NB_VOWS)

    #cartesian product of S and W
    SxV=iprod(S, V)


    ##solving linear problem

    assignment_model = model("assign")

    # Variables
    course_is_open = assignment_model.var('course is open', C)
    course_headcount = assignment_model.var('course headcount', C)
    student_gets_vow = assignment_model.var('student gets wish', SxV)

    # Objective function
    assignment_model.min(sum(
        STUDENTS[s].vows[v].weight * student_gets_vow[s, v]
        for s, v in SxV
    ))

    # Constraints
    for student in S:
        sum(student_gets_vow[student, v] for v in V) == 1
    for course in C:
        course_is_open[course]<=1
        sum(student_gets_vow[s, v] * int(COURSES[course] in STUDENTS[s].vows[v].courses) for s, v in SxV) == course_headcount[course]
        COURSES[course].min_students*course_is_open[course] <= course_headcount[course]
        COURSES[course].max_students*course_is_open[course] >= course_headcount[course]

    # Solve
    assignment_model.solve()

    ## building results

    result=[0 for student in S]

    for student, vow in SxV:
        if student_gets_vow[student, vow].primal!=0:
            result[student]=vow
            STUDENTS[student].courses = STUDENTS[student].vows[vow].courses
    return result


if __name__ == '__main__':
    ## results display
    from random_data import *
    NB_STUDENTS = 300
    COURSES = generate_random_course_list(50)
    NB_VOWS = 3
    NB_COURSES_IN_VOW=3
    #VOWS = generate_vow_dic(COURSES)
    STUDENTS = generate_random_population(COURSES, NB_VOWS, NB_COURSES_IN_VOW, NB_STUDENTS)
    result = solve(STUDENTS, COURSES)
    print(result)
    print('Rang de voeu moyen : '+str(sum(result)/len(result)+1))
    print('Rang de voeu médian : '+str(np.median(result)+1))
    print('Quartiles : '+str(np.quantile(result, [0.25,0.5,0.75])+np.ones((3,))))
    print('Pire rang de voeu : '+str(np.max(result)+1))
    print('Pourcentage par voeu :')
    for i in range(np.max(result)+1):
        print(str(i+1)+'e voeu : '+str(sum([r==i for r in result])/len(result) * 100)+'%')
    print("Total cost = ", assignment_model.vobj())
