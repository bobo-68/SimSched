import random
from copy import deepcopy


def se1(ind, gmax):
	op_num = len(ind['os'])
	neighbor = deepcopy(ind)
	for i in range(gmax):
		i1 = random.randint(0, op_num-2)
		o = neighbor['os'][i1]
		neighbor['os'][i1] = neighbor['os'][i1+1]
		neighbor['os'][i1+1] = o
	return neighbor

def se2(ind, job_num):
	if(job_num<2):
		return ind
	else:
		neighbor = deepcopy(ind)
		jobs = random.sample(range(job_num), 2)
		op_num1 = neighbor['os'].count(jobs[0])
		op_num2 = neighbor['os'].count(jobs[1])
		if(op_num1==op_num2):
			for i in range(len(neighbor['os'])):
				if(neighbor['os'][i]==jobs[0]):
					neighbor['os'][i]=jobs[1]
				elif(neighbor['os'][i]==jobs[1]):
					neighbor['os'][i]=jobs[0]
		elif(op_num1>op_num2):
			for i in range(len(neighbor['os'])):
				if(neighbor['os'][i]==jobs[0]):
					if(op_num2>0):
						neighbor['os'][i] = jobs[1]
						op_num2 -= 1
				elif(neighbor['os'][i]==jobs[1]):
					neighbor['os'][i]=jobs[0]
		elif(op_num1<op_num2):
			for i in range(len(neighbor['os'])):
				if(neighbor['os'][i]==jobs[1]):
					if(op_num1>0):
						neighbor['os'][i] = jobs[0]
						op_num1 -= 1
				elif(neighbor['os'][i]==jobs[0]):
					neighbor['os'][i]=jobs[1]
	return neighbor

def a_s(ind, amax, tasks):
	job_num = len(ind['ms'])
	machine_num = len(tasks[0][0])
	neighbor = deepcopy(ind)
	for i in range(amax):
		job = random.randint(0, job_num-1)
		op = random.randint(0, len(neighbor['ms'][job])-1)
		
		while(sum([(t>0) for t in tasks[job][op]]) < 2):
			job = random.randint(0, job_num-1)
			op = random.randint(0, len(neighbor['ms'][job])-1)

		current_machine = neighbor['ms'][job][op]
		new_machine = random.randint(0, machine_num-1)
		while((new_machine==current_machine) or (tasks[job][op][new_machine] < 0)):
			new_machine = random.randint(0, machine_num-1)
		neighbor['ms'][job][op] = new_machine
	
	return neighbor

def co(ind, gmax, amax, tasks):
	neighbor = se1(ind, gmax)
	neighbor = a_s(neighbor, amax, tasks)
	return neighbor

def i1(ind, tasks):
	job_num = len(tasks)
	machine_num = len(tasks[0][0])
	machine_loads = [0] * machine_num
	job_do_times = [0] * job_num
	for i in range(len(ind['os'])):
		job = ind['os'][i]
		op = job_do_times[job]
		machine_assigned = ind['ms'][job][op]
		machine_loads[machine_assigned] += tasks[job][op][machine_assigned]
		job_do_times[job] += 1
	max_load = max(machine_loads)
	min_load = min(machine_loads)
	max_machines = []
	min_machines = []

	for i in range(machine_num):
		if (machine_loads[i] == max_load):
			max_machines.append(i)
		if(machine_loads[i] == min_load):
			min_machines.append(i)
	m1 = random.choice(max_machines)
	m2 = random.choice(min_machines)

	job = random.randint(0, job_num-1)
	op = random.randint(0, len(ind['ms'][job])-1)
	while(ind['ms'][job][op] != m1):
		job = random.randint(0, job_num-1)
		op = random.randint(0, len(ind['ms'][job])-1)
	if(tasks[job][op][m2]>0):
		neighbor = deepcopy(ind)
		neighbor['ms'][job][op] = m2
	else:
		if(sum([(t>0) for t in tasks[job][op]]) < 2):
			return ind
		else:
			neighbor = deepcopy(ind)
			new_machine = random.randint(0, machine_num-1)
			while((new_machine==m1) or (tasks[job][op][new_machine] < 0)):
				new_machine = random.randint(0, machine_num-1)
			neighbor['ms'][job][op] = new_machine
	return neighbor


def i2(ind, tasks):
	job_num = len(tasks)
	machine_num = len(tasks[0][0])
	machine_starts = [-1] * machine_num
	machine_ends = [0] * machine_num
	job_do_times = [0] * job_num
	job_ok_time = [0] * job_num

	for i in range(len(ind['os'])):
		job = ind['os'][i]
		op = job_do_times[job]
		machine_assigned = ind['ms'][job][op]
		processing_time = tasks[job][op][machine_assigned] 

		if(machine_starts[machine_assigned]==-1):
			machine_starts[machine_assigned] = job_ok_time[job]

		job_do_times[job] += 1

		ok_time = max(job_ok_time[job], machine_ends[machine_assigned]) + processing_time
		
		job_ok_time[job] = ok_time
		machine_ends[machine_assigned] = ok_time
	
	machine_spans = []
	for i in range(machine_num):
		machine_spans.append(machine_ends[i]-machine_starts[i])

	max_span = max(machine_spans)
	min_span = min(machine_spans)
	max_machines = []
	min_machines = []
	for i in range(machine_num):
		if (machine_spans[i] == max_span):
			max_machines.append(i)
		if(machine_spans[i] == min_span):
			min_machines.append(i)
	m1 = random.choice(max_machines)
	m2 = random.choice(min_machines)

	job = random.randint(0, job_num-1)
	op = random.randint(0, len(ind['ms'][job])-1)
	while(ind['ms'][job][op] != m1):
		job = random.randint(0, job_num-1)
		op = random.randint(0, len(ind['ms'][job])-1)
	if(tasks[job][op][m2]>0):
		neighbor = deepcopy(ind)
		neighbor['ms'][job][op] = m2
	else:
		if(sum([(t>0) for t in tasks[job][op]]) < 2):
			return ind
		else:
			neighbor = deepcopy(ind)
			new_machine = random.randint(0, machine_num-1)
			while((new_machine==m1) or (tasks[job][op][new_machine] < 0)):
				new_machine = random.randint(0, machine_num-1)
			neighbor['ms'][job][op] = new_machine
	return neighbor


