from copy import deepcopy
import random


def SPT_sol(tasks, w_t = -1, w_t_j = -1):
    os = []
    ms = []

    if(w_t == -1 or len(w_t)>30):
        w_t = [0] * len(tasks[0][0])

    if(w_t_j == -1 or len(w_t_j)>80):
        w_t_j = [0] * len(tasks)

    for i in range(len(tasks)):
        ms.append([])

    dyn_tasks = deepcopy(tasks)
    m_ok_time = deepcopy(w_t)
    job_ok_time = deepcopy(w_t_j)
    job_do_times = [0] * len(tasks)

    op_num = 0
    for job in dyn_tasks:
        op_num += len(job)

    while(op_num > 0):
        machine = m_ok_time.index(min(m_ok_time))
        candidates = []
        for i in range(len(dyn_tasks)):
            job = dyn_tasks[i]
            next_op = job_do_times[i]
            if(next_op >= len(job)):
                candidates.append(1000)
            elif(m_ok_time[machine] < job_ok_time[i]):
                candidates.append(1000)
            else:
                # print(job)
                # print(next_op)
                # print(machine)
                # if(machine>=len(job[next_op])):
                #     print(job)
                #     print(next_op)
                #     print(machine)
                if(job[next_op][machine]>0):
                    candidates.append(job[next_op][machine])
                else:
                    candidates.append(1000)
        if(min(candidates) == 1000):
            m_ok_time[machine] += 1
        else:
            choices = []
            min_proc_time = min(candidates)
            for i in range(len(candidates)):
                if(candidates[i] == min_proc_time):
                    choices.append(i)
            next_job = random.choice(choices)
            os.append(next_job)
            ms[next_job].append(machine)
            job_do_times[next_job] += 1
            op_num -= 1
            m_ok_time[machine] += min_proc_time
            job_ok_time[next_job] = m_ok_time[machine]
    return {'os':os, 'ms':ms}

def AT_sol(tasks, w_t = -1, w_t_j = -1):
    os = []
    ms = []

    if(w_t == -1 or len(w_t)>30):
        w_t = [0] * len(tasks[0][0])

    if(w_t_j == -1 or len(w_t_j)>80):
        w_t_j = [0] * len(tasks)


    for i in range(len(tasks)):
        ms.append([])

    dyn_tasks = deepcopy(tasks)
    m_ok_time = deepcopy(w_t)
    job_ok_time = deepcopy(w_t_j)
    job_do_times = [0] * len(tasks)

    op_num = 0
    for job in dyn_tasks:
        op_num += len(job)

    while(op_num > 0):
        machine = m_ok_time.index(min(m_ok_time))
        next_job = -1
        for i in range(len(dyn_tasks)):
            job = dyn_tasks[i]
            next_op = job_do_times[i]
            if(next_op >= len(job)):
                continue
            elif(m_ok_time[machine] < job_ok_time[i]):
                continue
            else:
                if(job[next_op][machine]>0):
                    next_job = i
                else:
                    continue
        if(next_job==-1):
            m_ok_time[machine] += 1
        else:
            os.append(next_job)
            ms[next_job].append(machine)
            job_do_times[next_job] += 1
            op_num -= 1
            m_ok_time[machine] += dyn_tasks[next_job][job_do_times[next_job]-1][machine]
            job_ok_time[next_job] = m_ok_time[machine]
    return {'os':os, 'ms':ms}

def FIFO_sol(tasks, w_t = -1, w_t_j = -1):
    os = []
    ms = []

    if(w_t == -1 or len(w_t)>30):
        w_t = [0] * len(tasks[0][0])

    if(w_t_j == -1 or len(w_t_j)>80):
        w_t_j = [0] * len(tasks)

    for i in range(len(tasks)):
        ms.append([])

    dyn_tasks = deepcopy(tasks)
    m_ok_time = deepcopy(w_t)
    job_ok_time = deepcopy(w_t_j)
    job_do_times = [0] * len(tasks)

    op_num = 0
    for job in dyn_tasks:
        op_num += len(job)

    while(op_num > 0):
        machine = m_ok_time.index(min(m_ok_time))
        candidates = []
        for i in range(len(dyn_tasks)):
            job = dyn_tasks[i]
            next_op = job_do_times[i]
            if(next_op >= len(job)):
                candidates.append(-1)
            elif(m_ok_time[machine] < job_ok_time[i]):
                candidates.append(-1)
            else:
                if(job[next_op][machine]>0):
                    candidates.append((m_ok_time[machine]-job_ok_time[i]))
                else:
                    candidates.append(-1)
        if(max(candidates) == -1):
            m_ok_time[machine] += 1
        else:
            choices = []
            max_wait_time = max(candidates)
            for i in range(len(candidates)):
                if(candidates[i] == max_wait_time):
                    choices.append(i)
            next_job = random.choice(choices)
            os.append(next_job)
            ms[next_job].append(machine)
            job_do_times[next_job] += 1
            op_num -= 1
            m_ok_time[machine] += dyn_tasks[next_job][job_do_times[next_job]-1][machine]
            job_ok_time[next_job] = m_ok_time[machine]
    return {'os':os, 'ms':ms}
