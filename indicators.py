
from copy import deepcopy

def makespan(records):
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


def mean_flow_time(theo_schedule, tasks, job_arriving_time):

    o = deepcopy(theo_schedule['os'])
    m = deepcopy(theo_schedule['ms'])
    m_ok_time = [0] * len(tasks[0][0])   
    job_num = len(m)
    job_ok_time = deepcopy(job_arriving_time)      
    job_do_times = [0] * job_num

    for i in range(len(o)):

        job = o[i]
        op = job_do_times[job]
        mechine_assigned = m[job][op]
        processing_time = tasks[job][op][mechine_assigned]

        job_do_times[job] += 1

        ok_time = max(job_ok_time[job], m_ok_time[mechine_assigned]) + processing_time
        
        job_ok_time[job] = ok_time
        m_ok_time[mechine_assigned] = ok_time
    flow_time = []
    for i in range(job_num):
        flow_time.append(job_ok_time[i] - job_arriving_time[i])
    return sum(flow_time)/job_num

# print(mean_flow_time({'os': [0, 0, 0, 1, 1, 0, 1, 2, 3, 1, 2, 0, 3, 2, 3, 0, 3, 4, 3, 2, 4, 4, 2, 4, 4, 4], 'ms': [[0, 2, 5, 4, 1, 3], [0, 2, 0, 0], [1, 4, 2, 4, 0], [3, 5, 5, 4, 1], [0, 2, 2, 5, 3, 3]]}, [[[4, -1, -1, 6, -1, 5], [7, -1, 4, -1, -1, -1], [7, 6, -1, -1, 6, 6], [-1, -1, 7, -1, 4, -1], [-1, 2, 3, -1, -1, 4], [-1, -1, -1, 4, -1, 7]], [[1, -1, -1, -1, 1, 3], [4, -1, 1, -1, -1, 4], [3, -1, 3, 4, 4, -1], [2, -1, 6, 2, 5, -1]], [[6, 5, -1, -1, -1, -1], [-1, 1, 7, 7, 3, -1], [-1, 6, 5, -1, -1, -1], [5, -1, 7, 2, 6, -1], [5, 7, -1, -1, -1, 5]], [[-1, 3, -1, 3, -1, 1], [6, -1, -1, 4, 5, 2], [-1, -1, -1, 7, -1, 2], [2, 5, -1, 4, 1, -1], [-1, 2, -1, -1, 7, -1]], [[1, -1, 2, 2, -1, -1], [-1, -1, 3, -1, -1, 4], [-1, 7, 4, 7, -1, -1], [-1, 7, -1, 7, 7, 6], [-1, -1, -1, 1, 4, -1], [7, -1, 6, 2, 5, -1]]], [27, 19, 40, 28, 46, 0.1244349479675293, 12.000122785568237, 16.002575874328613, 18.000075101852417, 29.01197385787964]))