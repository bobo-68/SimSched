import time
import threading
import genetic
import random
import utils.fjs as fjs
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from utils.my_parser import my_parse
from utils.dispatching_rules import SPT_sol, FIFO_sol

################# params decl
task_list = []
new_task_list = []

job_num = 0
machine_num = 0

proc_dsc = 0    #多少次
total_dsc = 0

real_records = []
theo_records = {'os':[], 'ms':[]}

next_step = {'machine':-1, "job":-1}
new_arriving_jobs = []
tasks_just_done = []

job_state = []
machine_state = []
wait_time = []

time_unit = 0

very_begin = time.time() 
################# locks decl
job_num_lock = threading.Lock()
task_list_lock = threading.Lock()
new_arriving_jobs_lock = threading.Lock()
tasks_just_done_lock = threading.Lock()
next_step_lock = threading.Lock()

theo_records_lock = threading.Lock()

job_state_locks = []
machine_state_locks = []
wait_time_locks = []

####################################################################################################################### participant classes define
class Display(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while(True):
            if(proc_dsc==total_dsc):                                                 
                # print(real_records)
                break
                

class Machine(threading.Thread):
    def __init__(self, ID):
        threading.Thread.__init__(self)
        self.ID = ID

    def run(self):
        global task_list, tasks_just_done, real_records, theo_records, wait_time, next_step, proc_dsc
        while(proc_dsc<total_dsc):                                                  
            
            next_step_lock.acquire()

            if(next_step['machine']==self.ID):   #被叫到
                job_index = next_step['job']

                job_state_locks[job_index].acquire()
                if(job_state[job_index]==1):            #任务有人正在做，则还没法做
                    job_state_locks[job_index].release()
                    next_step_lock.release()
                    continue

                #开始接单
                theo_records_lock.acquire()

                theo_records['os'].append(job_index)
                theo_records['ms'][job_index].append(self.ID)

                theo_records_lock.release()

                next_step = {'machine':-1, 'job':-1}

                machine_state_locks[self.ID].acquire()
                machine_state[self.ID] = 1
                machine_state_locks[self.ID].release()

                job_state[job_index] = 1

                task_list_lock.acquire()
                tasks_just_done_lock.acquire()
                wait_time_locks[self.ID].acquire() 

                tasks_just_done.append(job_index)

                # print("\n\tMachine-"+str(self.ID)+" starts to process job-"+str(job_index)+".")
                
                processing_time = task_list[job_index][0][self.ID] * time_unit 
                                                                                                   #processing time !!!
                task_list[job_index].pop(0) 

                # print("\n\tprocessing_time: "+str(processing_time))
                wait_time[self.ID] = processing_time + time.time()                              #wait time edited

                wait_time_locks[self.ID].release()
                task_list_lock.release()
                tasks_just_done_lock.release()

                job_state_locks[job_index].release()
                next_step_lock.release()

                #接单完成，以删除掉task_list中的该operation，并在tasks_just_done中添加了它
                
                proc_begin = round(time.time() - very_begin, 1)

                time.sleep(processing_time)

                machine_state_locks[self.ID].acquire()
                machine_state[self.ID] = 0
                machine_state_locks[self.ID].release()

                job_state_locks[job_index].acquire()
                wait_time_locks[self.ID].acquire()

                job_state[job_index] = 0
                wait_time[self.ID] = time.time()                                             ##wait time edited

                wait_time_locks[self.ID].release()
                job_state_locks[job_index].release()

                proc_end = round(time.time() - very_begin, 1)
                real_records[self.ID].append({'job':job_index, 'begin': proc_begin, 'end': proc_end})

                proc_dsc += 1
                print("\t"+str(proc_dsc)+"/"+str(total_dsc)+" finished.")

                # print("\n\tMachine-"+str(self.ID)+" has just finished an operation of job-"+str(job_index)+".\n")

            else:
                next_step_lock.release()


#evolving the population using GA is another thread (Scheduler class)
class Scheduler(threading.Thread):
    def __init__(self, init_pop):
        threading.Thread.__init__(self)
        self.pop = init_pop
        
        self.op_num = len(init_pop[0]['os'])

        task_list_lock.acquire()
        self.tasks = deepcopy(task_list)
        task_list_lock.release()

        time_takens = []
        for ind in self.pop:
            time_taken = genetic.total_time(ind, self.tasks)
            time_takens.append(time_taken)
        scored_pop = list(zip(time_takens, self.pop))
        scored_pop.sort(key = lambda scored_ind: scored_ind[0])
        self.best = scored_pop[0][1]
        self.wait_time = [0] * 100
        
        self.ev_time = 0
    
    def evolve(self, mut_rate = 0.1, cross_rate = 0.7, elite = 2, eliminate = 0):

        self.pop = genetic.evolve_ms(self.pop, self.tasks, mut_rate, cross_rate, elite, eliminate, self.wait_time)

        time_takens = []
        for ind in self.pop:
            time_taken = genetic.total_time(ind, self.tasks, self.wait_time)
            time_takens.append(time_taken)

        scored_pop = list(zip(time_takens, self.pop))
        scored_pop.sort(key = lambda scored_ind: scored_ind[0])
        self.best = scored_pop[0][1]

        self.ev_time += 1
    
    def delete_op(self, job_index):

        new_pop = []
        for ind in self.pop:
            os = deepcopy(ind['os'])
            ms = deepcopy(ind['ms'])
            os.remove(job_index)
            ms[job_index].pop(0)
            new_ind = {'os':os, 'ms':ms}
            new_pop.append(new_ind)

        return new_pop
    
    def add_job(self, new_job): #new_job is in the same format in task_list

        new_pop = []
        time_takens = []
        for ind in self.pop:
            time_taken = genetic.total_time(ind, self.tasks, self.wait_time)
            time_takens.append(time_taken)
        scored_pop = list(zip(time_takens, self.pop))
        scored_pop.sort(key = lambda scored_ind: scored_ind[0])

        while(len(new_pop)<20):                                     #20个：随机插在优选出的20个中间
            ind_to_h = deepcopy(self.pop[genetic.select(time_takens)])
            new_job_ms = []
            for i in range(len(new_job)):
                k = random.randint(0, self.op_num-1+i)
                ind_to_h['os'].insert(k, job_num-1)
                t = -1
                j = -1
                while(m < 0):
                    j = random.choice(range(len(new_job[i])))
                    t = new_job[i][j]
                new_job_ms.append(j)
            ind_to_h['ms'].append(new_job_ms)
            new_pop.append(ind_to_h)

        while(len(new_pop)<26):                                     #6个：SPT新解
            spt_ind = genetic.SPT_sol(self.tasks, self.wait_time)
            new_pop.append(spt_ind)

        random_new_pop = genetic.rand_pop(self.tasks, 24)
        new_pop += random_new_pop

        for i in range(len(self.pop)-50):                           #50个：随机接在最优秀的50个后面
            ind = scored_pop[i][1]
            new_job_ms = []
            for i in range(len(new_job)):
                t = -1
                j = -1
                while(t < 0):
                    j = random.choice(range(len(new_job[i])))
                    t = new_job[i][j]
                new_job_ms.append(j) 
            new_ind = {'os':(ind['os'][:]+[job_num-1]*len(new_job)), 'ms':(ind['ms'][:]+[new_job_ms])}
            new_pop.append(new_ind)

        return new_pop
    
    def run(self):
        global new_arriving_jobs, tasks_just_done, task_list, next_step#, in_machine, in_scheduler, in_manager
        while(proc_dsc<total_dsc): 
                                                         #run time limit of Scheduler
            task_list_lock.acquire()
            tasks_just_done_lock.acquire()
            new_arriving_jobs_lock.acquire()
            for lock in wait_time_locks:
                lock.acquire()

            self.tasks = deepcopy(task_list)
            t_j_d = deepcopy(tasks_just_done)
            n_a_j = deepcopy(new_arriving_jobs)
            abs_wait_times = wait_time
            
            task_list_lock.release()  
            tasks_just_done_lock.release()
            new_arriving_jobs_lock.release()

            for lock in wait_time_locks:
                lock.release()

            for i in range(len(abs_wait_times)):
                t = abs_wait_times[i] - time.time()
                if(t > 0):
                    self.wait_time[i] = rount(t/time_unit)
                else:
                    self.wait_time[i] = 0

            if(len(t_j_d)):

                job_indexs = []
                while(len(tasks_just_done)):
                    job_indexs.append(t_j_d.pop(0))

                    tasks_just_done_lock.acquire()
                    tasks_just_done.pop(0)
                    tasks_just_done_lock.release()  

                for job_index in job_indexs:

                    self.pop = self.delete_op(job_index)
                    self.op_num -= 1
  
            if(len(n_a_j)):
                new_jobs = []
                while(len(n_a_j)>0):
                    new_arriving_jobs_lock.acquire()
                    new_arriving_jobs.pop(0)
                    new_arriving_jobs_lock.release()
                    new_jobs.append(n_a_j.pop(0))

                for new_job in new_jobs:
                    self.pop = self.add_job(new_job)
                    self.op_num += len(new_job)

            self.evolve()

            if(len(self.best['os'])==0):
                continue

            next_step_lock.acquire()

            tasks_just_done_lock.acquire()
            new_arriving_jobs_lock.acquire()

            if((tasks_just_done==[])&(new_arriving_jobs==[])):
                k = 0
                n_j = self.best['os'][k]

                n_m = self.best['ms'][n_j][0]

                for j_lock in job_state_locks:
                    j_lock.acquire()

                for m_lock in machine_state_locks:
                    m_lock.acquire()

                while((job_state[n_j]!=0)or(machine_state[n_m]!=0)):           #job 没人在做才能发送请求！！！不然如果机器1在做job1，又让机器2去做job1可不行
                    k += 1
                    if(k==len(self.best['os'])):
                        break
                    n_j = self.best['os'][k]

                    n_m = n_m = self.best['ms'][n_j][0]
                    

                if(k<len(self.best['os'])):
                    next_step = {'machine': n_m, 'job':n_j}

                else:
                    next_step = {'machine': -1, 'job':-1}
                
                for m_lock in machine_state_locks:
                    m_lock.release()

                for j_lock in job_state_locks:
                    j_lock.release()

            tasks_just_done_lock.release()
            new_arriving_jobs_lock.release()

            next_step_lock.release()


class Manager(threading.Thread):
    def __init__(self, new_job_freq):
        threading.Thread.__init__(self)
        self.new_job_batch = new_job_freq[0]
        self.new_job_time = new_job_freq[1]
    
    def run(self):
        global new_arriving_jobs, job_num, task_list, wait_time, wait_time_locks
        while(proc_dsc<total_dsc):   
                                                                #run time limit of Manager
            time.sleep((self.new_job_time) * time_unit) 
                                                                                                    #new jobs arriving time   
            for i in range(self.new_job_batch):
                if(new_task_list == []):
                    break
                else:
                    wait_time.append(0)
                    wait_lock = threading.Lock()
                    wait_time_locks.append(wait_lock)

                    new_job = new_task_list.pop(0)
                    
                    task_list_lock.acquire()
                    new_arriving_jobs_lock.acquire()
                    job_num_lock.acquire()

                    task_list.append(deepcopy(new_job))
                    job_state.append(0)
                    new_job_state_lock = threading.Lock()
                    job_state_locks.append(new_job_state_lock)
                    new_arriving_jobs.append(new_job)
                    job_num += 1

                    job_num_lock.release()
                    new_arriving_jobs_lock.release()
                    task_list_lock.release()
                    
                    # print("\n\tA new job with "+str(len(new_job))+" operations arrived:")
                    # print("\t"+str(new_job))


######################################################################################################################################## the function

def oga_fjs(static_path, dynamic_path = None, time_unit_param = 10, new_job_freq = (1, 5)):
    global task_list, new_task_list, job_num, machine_num, proc_dsc, total_dsc, real_records, theo_records, job_state, machine_state, wait_time, job_state_locks, machine_state_locks, wait_time_locks, time_unit, very_begin, tasks_just_done, new_arriving_jobs, next_step

################# params redecl

    new_task_list = []

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

    task_list = my_parse(static_path)

    # print(task_list)

    job_num = len(task_list)
    machine_num = len(task_list[0][0])

    if(dynamic_path):
        new_task_list = my_parse(dynamic_path)
        if(len(new_task_list[0][0])>machine_num):
            machine_num = new_task_list[0][0]

    all_the_jobs = deepcopy(task_list)+deepcopy(new_task_list)
    for job in all_the_jobs:
        total_dsc += len(job)


    for i in range(machine_num):
        real_records.append(["Machine-"+str(i)])

    for i in range(len(all_the_jobs)):
        theo_records['ms'].append([])

    # print(theo_records)

    job_state = [0] * job_num
    machine_state = [0] * machine_num
    wait_time = [0] * machine_num

################# locks

    for i in range(job_num):
        job_lock = threading.Lock()
        job_state_locks.append(job_lock)

    for i in range(machine_num):
        machine_lock = threading.Lock()
        machine_state_locks.append(machine_lock)

    for i in range(len(task_list[0][0])):
        wait_lock = threading.Lock()
        wait_time_locks.append(wait_lock)

################# initial population
    t000 = time.time()

    population = []

    shortest_ms = []
    for job in task_list:
        job_ms = []
        for op in job:
            opp = deepcopy(op)
            shortest_machines = []
            for i in range(len(opp)):
                if(opp[i]<0):
                    opp[i] = 1000
            shortest_time = min(opp)
            for i in range(len(opp)):
                if(opp[i] == shortest_time):
                    shortest_machines.append(i)
            job_ms.append(shortest_machines)
        shortest_ms.append(job_ms)

####  24个全局最短加工时间
    for i in range(24):
        ms = []
        os = []
        i = 0
        for job in shortest_ms:
            os += [i]*len(job)
            i += 1
            job_ms = []
            for shortest_machines in job:
                m = random.choice(shortest_machines)
                job_ms.append(m)
            ms.append(job_ms)
        
        random.shuffle(os)
        population.append({'os':os, 'ms':ms})

####  56个随机
    for i in range(56):
        os = []
        ms = []
        i = 0
        for job in task_list:
            os += [i]*len(task_list[i])
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
        population.append(ind)

#### 10个SPT
    for i in range(10):
        ind = SPT_sol(task_list)
        population.append(ind)

#### 10个FIFO
    for i in range(10):
        ind = FIFO_sol(task_list)
        population.append(ind)


################# participants init
    machines = []
    for i in range(machine_num):
    	machine = Machine(i)
    	machines.append(machine)
    # print("\tMachines are ready.\n")


    scheduler = Scheduler(population)
    # print("\tScheduler is ready.\n")

    if(dynamic_path):
        manager = Manager(new_job_freq)

    very_begin = time.time() 

    t001 = time.time()

    print("!!!!!!!WT = "+str(t001 - t000))

################# participants start
    for m in machines:
    	m.start()
    scheduler.start()
    
    if(dynamic_path):
        manager.start()

    for m in machines:
        m.join()
    scheduler.join()
    
    if(dynamic_path):
        manager.join()

#################
    proc_begins = []
    proc_ends = []
    for real_record in real_records:
        for proc in real_record[1:]:
            proc_begins.append(proc['begin'])
            proc_ends.append(proc['end'])
    real_makespan = max(proc_ends) - min(proc_begins)

    theo_makespan = genetic.total_time(theo_records, all_the_jobs)

    return {'real_records':real_records, 'theo_records':theo_records, 'real_makespan':real_makespan, 'theo_makespan':theo_makespan}


print(oga_fjs("bran/Mk10.fjs",time_unit_param = 1))
















