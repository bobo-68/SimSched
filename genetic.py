import random
from copy import deepcopy

def rand_pop(tasks, pop_size = 200):
	pop = []
	for h in range(pop_size):
		os = []
		ms = []
		i = 0
		for job in tasks:
			os += [i]*len(tasks[i])
			job_ms = []
			for k in range(len(job)):
					t = -1
					j = -1
					while(t == -1):
						j = random.choice(range(len(job[k])))
						t = job[k][j]
					job_ms.append(j)
			ms.append(job_ms)
			i += 1
		random.shuffle(os)
		ind = {'os': os, 'ms': ms}
		pop.append(ind)
	return pop

def SPT_sol(tasks, w_t = -1):
    os = []
    ms = []

    if(w_t == -1):
        w_t = [0] * len(tasks[0][0])

    for i in range(len(tasks)):
        ms.append([])

    dyn_tasks = deepcopy(tasks)
    m_ok_time = deepcopy(w_t)
    job_ok_time = [0] * len(tasks)
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


def total_time(ind, tasks, w_t = [0] * 100):
    
    o = ind['os']
    m = ind['ms']
    m_ok_time = deepcopy(w_t)	#反正暂时不会有10台以上的机器吧，先定个10吧
    job_ok_time = [0] * len(m)		#反正暂时不会有20个以上的job吧，先定个20吧
    job_do_times = [0] * len(m)
    for i in range(len(o)):
        
        job = o[i]
        op = job_do_times[job]
        
        mechine_assigned = m[job][op]
        processing_time = tasks[job][op][mechine_assigned]
        
        job_do_times[job] += 1
        
        ok_time = max(job_ok_time[job], m_ok_time[mechine_assigned]) + processing_time
        
        job_ok_time[job] = ok_time
        m_ok_time[mechine_assigned] = ok_time
    return max(job_ok_time)

def mean_remaining_flow_time(ind, tasks, w_t = [0] * 100, w_t_j = [0] * 100):
    # print(ind)
    o = ind['os']
    m = ind['ms']
    remaining_job_num = 0
    for job in tasks:
        if(job != []):
            remaining_job_num += 1

    job_ok_time = deepcopy(w_t_j)
    job_do_times = [0] * len(m)
    m_ok_time = deepcopy(w_t)

    for i in range(len(o)):

        job = o[i]
        op = job_do_times[job]

        # if(job>=len(m)):
        #     print(ind)
        #     print("job="+str(job))
        # elif(op >= len(m[job])):
        #     print(ind)

        mechine_assigned = m[job][op]
        processing_time = tasks[job][op][mechine_assigned]

        job_do_times[job] += 1

        ok_time = max(job_ok_time[job], m_ok_time[mechine_assigned]) + processing_time
        
        job_ok_time[job] = ok_time
        m_ok_time[mechine_assigned] = ok_time

    return sum(job_ok_time)



def select(time_takens):
    i = random.choice(range(len(time_takens)))
    j = random.choice(range(len(time_takens)))
    if(time_takens[i] > time_takens[j]):
        return j
    else:
        return i
    

def cross(p1, p2, cross_rate):

        r = random.random()
        if(r>cross_rate):

            return [p1, p2]
        else:
            if(random.choice([True, False])):
                os1 = p1['os']
                os2 = p2['os']
                ms1 = p1['ms']
                ms2 = p2['ms']
                os_choosed_job_num = int(len(ms1)/3) #random.randint(1, len(ms1)-2)
                os_choosed_jobs = random.sample(range(len(ms1)), os_choosed_job_num)
                ch_os1 = [-1] * len(os1)
                ch_os2 = [-1] * len(os1)
                rest1 = []
                rest2 = []
                for i in range(len(os1)):
                    if(os1[i] in os_choosed_jobs):
                        ch_os1[i] = os1[i]
                    else:
                        rest1.append(os1[i])
                    if(os2[i] in os_choosed_jobs):
                        ch_os2[i] = os2[i]
                    else:
                        rest2.append(os2[i])
                for i in range(len(os1)):
                    if(ch_os1[i] == -1):
                        ch_os1[i] = rest2.pop(0)
                    if(ch_os2[i] == -1):
                        ch_os2[i] = rest1.pop(0)
            else:
                os1 = p1['os']
                os2 = p2['os']
                ms1 = p1['ms']
                ms2 = p2['ms']
                os_choosed_job_num = int(len(ms1)/3)
                os_choosed_jobs = random.sample(range(len(ms1)), os_choosed_job_num)
                ch_os1 = [-1] * len(os1)
                ch_os2 = [-1] * len(os1)
                rest1 = []
                rest2 = []
                for i in range(len(os1)):
                    if(os1[i] in os_choosed_jobs):
                        ch_os1[i] = os1[i]
                        rest1.append(os1[i])
                    if(os2[i] not in os_choosed_jobs):
                        ch_os2[i] = os2[i]
                        rest2.append(os2[i])
                for i in range(len(os1)):
                    if(ch_os1[i] == -1):
                        ch_os1[i] = rest2.pop(0)
                    if(ch_os2[i] == -1):
                        ch_os2[i] = rest1.pop(0)


            ch_ms1 = deepcopy(ms1)
            ch_ms2 = deepcopy(ms2)
            ms_choosed_job_num = int(len(ms1)/3) #random.randint(1, len(ms1)-2)
            ms_choosed_jobs = random.sample(range(len(ms1)), ms_choosed_job_num)
            for job in ms_choosed_jobs:
                for i in range(len(ch_ms1[job])):
                    m1 = ch_ms1[job][i]
                    m2 = ch_ms2[job][i]
                    if(random.choice([True, False])):
                        ch_ms1[job][i] = m2
                        ch_ms2[job][i] = m1

        return [{'os':ch_os1, 'ms':ch_ms1}, {'os':ch_os2, 'ms':ch_ms2}]

def mutate(ind, mut_rate, tasks):

    r = random.random()
    
    if(r>mut_rate):
        return ind
    else:
        m_os = deepcopy(ind['os'])
        m_ms = deepcopy(ind['ms'])
        
        if(random.choice([True, False])):
            if(len(m_os)>=2):
                os_m_index1 = random.randint(0, len(m_os)-1)
                os_m_index2 = random.randint(0, len(m_os)-1)                            
                while(os_m_index1 == os_m_index2):
                    os_m_index2 = random.randint(0, len(m_os)-1)
                j = m_os[os_m_index1]         
                m_os[os_m_index1] = m_os[os_m_index2]
                m_os[os_m_index2] = j
        else:
            if(len(m_os)>=3):
                poses = random.sample(range(len(m_os)), 3)
                c = random.randint(1, 5)
                if(c == 1):
                    op = m_os[poses[0]]
                    m_os[poses[0]] = m_os[poses[1]]
                    m_os[poses[1]] = op
                elif(c == 2):
                    op = m_os[poses[0]]
                    m_os[poses[0]] = m_os[poses[2]]
                    m_os[poses[2]] = op
                elif(c == 3):
                    op = m_os[poses[1]]
                    m_os[poses[1]] = m_os[poses[2]]
                    m_os[poses[2]] = op
                elif(c == 4):
                    op = m_os[poses[1]]
                    m_os[poses[1]] = m_os[poses[2]]
                    m_os[poses[2]] = op
                    op = m_os[poses[0]]
                    m_os[poses[0]] = m_os[poses[2]]
                    m_os[poses[2]] = op
                else:
                    op = m_os[poses[0]]
                    m_os[poses[0]] = m_os[poses[1]]
                    m_os[poses[1]] = op
                    op = m_os[poses[0]]
                    m_os[poses[0]] = m_os[poses[2]]
                    m_os[poses[2]] = op
                    
        ms_m_job_num = round(len(m_ms)/1.4)
        ms_m_jobs = random.sample(range(len(m_ms)), ms_m_job_num)
        for ms_m_index_job in ms_m_jobs:
            if(len(m_ms[ms_m_index_job])>0):
                ms_m_index_ops = random.sample(range(len(m_ms[ms_m_index_job])), round(len(m_ms[ms_m_index_job])/1.4))
                for ms_m_index_op in ms_m_index_ops:							#从一半job中选一半operation改变选择的机台
                    t = -1
                    j = -1
                    while(t == -1):
                        j = random.choice(range(len(tasks[ms_m_index_job][ms_m_index_op])))
                        t = tasks[ms_m_index_job][ms_m_index_op][j]
                        m_ms[ms_m_index_job][ms_m_index_op] = j
                        
    return {'os':m_os, 'ms':m_ms}

def evolve_ms(pop, tasks, mut_rate = 0.1, cross_rate = 0.8, elite = 2, eliminate = 0, w_t = [0 for i in range(100)]):

    current_size = len(pop)
    time_takens = []
    
    for ind in pop:
        time_taken = total_time(ind, tasks, w_t)

        time_takens.append(time_taken)
    scored_pop = list(zip(time_takens, pop))
    scored_pop.sort(key = lambda scored_ind: scored_ind[0])
    children = []

    for i in range(elite):
        children.append(scored_pop[i][1])

    while(len(children)<(current_size-eliminate)):
        parent1 = pop[select(time_takens)]
        parent2 = pop[select(time_takens)]
        
        twins = cross(parent1, parent2, cross_rate)
        
        twins[0] = mutate(twins[0], mut_rate, tasks)
        twins[1] = mutate(twins[1], mut_rate, tasks)

        children.append(twins[0])
        children.append(twins[1])
        
    while(len(children)>(current_size-eliminate)):
        children.pop()

    return children

def evolve_ft(pop, tasks, mut_rate = 0.1, cross_rate = 0.8, elite = 2, eliminate = 0, w_t = [0 for i in range(100)], w_t_j = [0] * 100):

    current_size = len(pop)
    time_takens = []
    
    for ind in pop:
        time_taken = mean_remaining_flow_time(ind, tasks, w_t, w_t_j)

        time_takens.append(time_taken)
    scored_pop = list(zip(time_takens, pop))
    scored_pop.sort(key = lambda scored_ind: scored_ind[0])
    children = []

    for i in range(elite):
        children.append(scored_pop[i][1])

    count = 0
    while(len(children)<(current_size-eliminate)):
        parent1 = pop[select(time_takens)]
        parent2 = pop[select(time_takens)]
        
        twins = cross(parent1, parent2, cross_rate)
        
        twins[0] = mutate(twins[0], mut_rate, tasks)
        twins[1] = mutate(twins[1], mut_rate, tasks)

        if((twins[0] not in children) or (count>5)):
            children.append(twins[0])
            count = 0
        else:
            count += 1
        if((twins[1] not in children) or (count>5)):
            children.append(twins[1])
            count = 0
        else:
            count += 1
        
    while(len(children)>(current_size-eliminate)):
        children.pop()

    return children









