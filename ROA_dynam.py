import time
import genetic
import random
import utils.fjs as fjs
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from utils.my_parser import my_parse
from utils.vns_dynam import se1, se2, a_s, co, i1, i2, total_flow_time, search
import indicators
from utils.dispatching_rules import SPT_sol, AT_sol, FIFO_sol

################# params decl
sol = {}
gen=0

task_list = []
all_the_tasks = []

job_num = 0
total_job_num = 0
machine_num = 0

proc_dsc = 0    #多少次
total_dsc = 0

real_records = []
theo_records = {'os':[], 'ms':[]}

next_step = {'machine':-1, "job":-1}
new_arriving_jobs = []
tasks_just_done = []
job_arrival_time = []

job_state = []
machine_state = []
wait_time = []

time_unit = 0

very_begin = time.time() 

######################################################################################################################################## the function
def roa(task_list, wait_time):
    population = []

####  30个SPT
    for i in range(30):
        s = SPT_sol(task_list, wait_time)
        population.append(s)
####  30个AT
    for i in range(30):
        s = AT_sol(task_list, wait_time)
        population.append(s)
####  30个FIFO
    for i in range(30):
        s = FIFO_sol(task_list, wait_time)
        population.append(s)

    time_takens = []
    for ind in population:
        time_taken = total_flow_time(ind, task_list, wait_time)
        time_takens.append(time_taken)
    scored_pop = list(zip(time_takens, population))
    scored_pop.sort(key = lambda scored_ind: scored_ind[0])

    return scored_pop[0][1]


def ovns_fjs(utilization_rate, max_job_num, a_t_t, j_a_t, time_unit_param = 1):
    global sol, job_arrival_time, task_list, all_the_tasks, total_job_num, job_num, machine_num, proc_dsc, total_dsc, real_records, theo_records, job_state, machine_state, wait_time, job_state_locks, machine_state_locks, wait_time_locks, time_unit, very_begin, tasks_just_done, new_arriving_jobs, next_step

################# params redecl
    total_job_num = max_job_num

    # mean_interval = 20/(6*utilization_rate)

    all_the_tasks = a_t_t
    arriving_time = 0
    job_arrival_time = j_a_t

    proc_dsc = 0    #多少次
    total_dsc = 0

    real_records = []
    theo_records = {'os':[], 'ms':[]}

    next_step = {'machine':-1, "job":-1}
    new_arriving_jobs = []
    tasks_just_done = []

################# locks clear

    job_state_locks = []
    machine_state_locks = []
    wait_time_locks = []


################# params
    time_unit = time_unit_param

    task_list = []

    # print(task_list)

    machine_num = 6

    for i in range(machine_num):
        real_records.append(["Machine-"+str(i)])
    for i in range(total_job_num):
        theo_records['ms'].append([])

################# locks

    for i in range(total_job_num):
        job = all_the_tasks[i]
        total_dsc += len(job)
    print(job_arrival_time)

################# participants init

    computing_time = 0
    job_state = []
    job_do_times = []
    machine_state = [-1] * machine_num #-1表示空闲，其他表示job编号
    wait_time = [0] * machine_num
    i = 0
    t = 0

    s = {'os':[], 'ms':[]}
    while(proc_dsc<total_dsc):

        if(i<len(all_the_tasks)):
            if(t>=job_arrival_time[i]):
                t1 = time.time()
                task_list.append(deepcopy(all_the_tasks[i]))
                i += 1
                s = roa(task_list, wait_time)
                job_state.append(0)
                job_do_times.append(0)
                t2 = time.time()
                computing_time += (t2-t1)
        finished_op = []
        for j in range(len(s['os'])):
            job = s['os'][j]
            if(job_state[job] == 0):
                op = job_do_times[job]

                machine_assigned = s['ms'][job][0]
                if(machine_state[machine_assigned]==-1):
                    finished_op.append(j)
                    s['ms'][job].pop(0)
                    processing_time = task_list[job][0][machine_assigned]
                    if(processing_time<=0):
                        print("wrong!")
                    task_list[job].pop(0)
                    job_state[job] = processing_time
                    machine_state[machine_assigned] = job
                    job_do_times[job] += 1
                    theo_records['os'].append(job)
                    theo_records['ms'][job].append(machine_assigned)
        for p in range(len(finished_op)):
            s['os'].pop(finished_op[p]-p)
        
        t += 1
        for m in range(machine_num):
            if(machine_state[m] >= 0):
                job = machine_state[m]
                job_state[job] -= 1
                if(job_state[job] == 0):
                    machine_state[m] = -1
                    proc_dsc += 1
                    print("\t"+str(proc_dsc)+"/"+str(total_dsc)+"finished")


#################
    mft = indicators.mean_flow_time(theo_records, all_the_tasks, job_arrival_time)

    return {'computing_time':computing_time, 'theo_mft':mft, 'theo_records': theo_records, 'job_arriving_time': job_arrival_time, 'all_the_tasks':all_the_tasks}

# for i in range(5):
# print(ovns_fjs(0.6, 5, time_unit_param = 1))
















