import random
from copy import deepcopy
import genetic

def is_overlap(node1, node2):
	if((node1[0] >= (node2[0]+node2[2])) | ((node2[0] >= (node1[0]+node1[2])))):
		return False
	else:
		return True

def graph2o(machine_nodes, op_num, job_num):
	machine_nodes = deepcopy(machine_nodes)
	op_real = 0

	n_o = []
	job_do_times = [0] * job_num
	n_o_length = 0
	while(len(n_o) < op_num):
		
		for machine_chain in machine_nodes:
			if(machine_chain != []):
				if(job_do_times[machine_chain[0][3]]==machine_chain[0][4]):
					job_do_times[machine_chain[0][3]] += 1
					n_o.append((machine_chain.pop(0))[3])
		if(len(n_o) == n_o_length):
			return []
		n_o_length = len(n_o)

	return n_o

def nopt1(ind, tasks, w_t = [0 for i in range(100)]):

	o = deepcopy(ind['os'])
	m = deepcopy(ind['ms'])

	op_num = len(o)
	job_num = len(m)

	m_ok_time = deepcopy(w_t)	#反正暂时不会有10台以上的机器吧，先定个10吧
	job_ok_time = [0] * job_num		#反正暂时不会有20个以上的job吧，先定个20吧
	job_do_times = [0] * job_num

	job_nodes = []
	for i in range(len(m)):
		job_nodes.append([])	#这里每一个[]代表一个job，里面将按顺序存放每个op的节点，节点格式为[earliest, latest, processing_time, job, op_index, machine]
	machine_nodes = []
	for i in range(len(tasks[0][0])):
		machine_nodes.append([])

	for i in range(len(o)):

		machine_assigned = m[o[i]][job_do_times[o[i]]]
		processing_time = tasks[o[i]][job_do_times[o[i]]][machine_assigned] #* (1-i/(len(o)*2))


		earliest = max(job_ok_time[o[i]], m_ok_time[machine_assigned])

		node = [earliest, 1000, processing_time, o[i], job_do_times[o[i]], machine_assigned]

		job_do_times[o[i]] += 1

		if(job_nodes[o[i]] != []) :
			job_nodes[o[i]][-1][1] = min(earliest-job_nodes[o[i]][-1][2], job_nodes[o[i]][-1][1])
		if(machine_nodes[machine_assigned] != []):
			machine_nodes[machine_assigned][-1][1] = earliest
		
		job_nodes[o[i]].append(node)
		machine_nodes[machine_assigned].append(node)


		ok_time = earliest + processing_time
		
		job_ok_time[o[i]] = ok_time
		m_ok_time[machine_assigned] = ok_time

	tt = max(job_ok_time)

	times_do_job = [1] * job_num
	times_do_machine = [1] * len(tasks[0][0])
	for i in range(len(o)-1, -1, -1):
		machine_assigned = m[o[i]][-times_do_job[o[i]]]
		if(times_do_machine[machine_assigned] == 1 & times_do_job[o[i]] == 1):
			job_nodes[o[i]][-times_do_job[o[i]]][1] = tt - job_nodes[o[i]][-times_do_job[o[i]]][2]
		elif(times_do_machine[machine_assigned] > 1):
			job_nodes[o[i]][-times_do_job[o[i]]][1] = job_nodes[o[i]][1-times_do_job[o[i]]][1] - job_nodes[o[i]][-times_do_job[o[i]]][2]
		else:
			machine_nodes[machine_assigned][-times_do_machine[machine_assigned]][1] = machine_nodes[machine_assigned][1-times_do_machine[machine_assigned]][1] - machine_nodes[machine_assigned][-times_do_machine[machine_assigned]][2]

		times_do_job[o[i]] += 1
		times_do_machine[machine_assigned] += 1


	critical_nodes = []

	for job in job_nodes:
		for node in job:
			if (node[1]==-1):
				node[1] = tt-node[2]
			if(node[0]==node[1]):
				critical_nodes.append(node)

	to_delete_list = []

	for node1 in critical_nodes:
		for node2 in critical_nodes:
			if(node1==node2):
				continue
			if(is_overlap(node1, node2)):
				to_delete_list.append(node1)
				break


	for node in to_delete_list:
		critical_nodes.remove(node)

	

	neighbors = []

	for node in critical_nodes:
		
		chain1 = deepcopy(machine_nodes[node[5]])
		machine_nodes[node[5]].remove(node)

###
		

		######
		for machine in range(len(tasks[0][0])):
			if(machine == node[5]):
				if(machine_nodes[machine] == []):
					break
				if((machine_nodes[machine][-1][1]-machine_nodes[machine][-1][0])>=node[2]):
					# if(in_job_sequence(node, machine_nodes[machine], 0)):
					chain2 = deepcopy(machine_nodes[machine])
					machine_nodes[machine].insert(0, node)
					if(machine_nodes[node[5]]==chain1):
						n_o = graph2o(machine_nodes, op_num, job_num)
						if(n_o):
							n_m = deepcopy(m)
							n_m[node[3]][node[4]] = machine
							neighbors.append({'os': n_o, 'ms': n_m})
					machine_nodes[machine] = chain2
				if((machine_nodes[machine][0][1]-machine_nodes[machine][0][0])>=node[2]):					
					chain2 = deepcopy(machine_nodes[machine])
					machine_nodes[machine].append(node)
					if(machine_nodes[node[5]]==chain1):
						n_o = graph2o(machine_nodes, op_num, job_num)
						if(n_o):
							n_m = deepcopy(m)
							n_m[node[3]][node[4]] = machine
							neighbors.append({'os': n_o, 'ms': n_m})
					machine_nodes[machine] = chain2
				for i in range(len(machine_nodes[machine])-1):
					if((machine_nodes[machine][i+1][1]-machine_nodes[machine][i][0]-machine_nodes[machine][i][2])>=node[2]):						
						chain2 = deepcopy(machine_nodes[machine])
						machine_nodes[machine].insert(i+1, node)
						if(machine_nodes[node[5]]==chain1):
							n_o = graph2o(machine_nodes, op_num, job_num)
							if(n_o):
								n_m = deepcopy(m)
								n_m[node[3]][node[4]] = machine
								neighbors.append({'os': n_o, 'ms': n_m})
						machine_nodes[machine] = chain2
			else:
				if(tasks[node[3]][node[4]][machine] > 0):
					if(machine_nodes[machine] == []):
						machine_nodes[machine] = [node]
						n_o = graph2o(machine_nodes, op_num, job_num)
						if(n_o):
							n_m = deepcopy(m)
							n_m[node[3]][node[4]] = machine
							neighbors.append({'os': n_o, 'ms': n_m})
						machine_nodes[machine] = []
						break
					if((machine_nodes[machine][-1][1]-machine_nodes[machine][-1][0])>=node[2]):
						chain2 = deepcopy(machine_nodes[machine])
						machine_nodes[machine].insert(0, node)
						n_o = graph2o(machine_nodes, op_num, job_num)
						if(n_o):
							n_m = deepcopy(m)
							n_m[node[3]][node[4]] = machine
							neighbors.append({'os': n_o, 'ms': n_m})
						machine_nodes[machine] = chain2
					if((machine_nodes[machine][0][1]-machine_nodes[machine][0][0])>=node[2]):
						chain2 = deepcopy(machine_nodes[machine])
						machine_nodes[machine].append(node)
						n_o = graph2o(machine_nodes, op_num, job_num)
						if(n_o):
							n_m = deepcopy(m)
							n_m[node[3]][node[4]] = machine
							neighbors.append({'os': n_o, 'ms': n_m})
						machine_nodes[machine] = chain2
					for i in range(len(machine_nodes[machine])-1):
						if((machine_nodes[machine][i+1][1]-machine_nodes[machine][i][0]-machine_nodes[machine][i][2])>=node[2]):
							chain2 = deepcopy(machine_nodes[machine])
							machine_nodes[machine].insert(i+1, node)
							n_o = graph2o(machine_nodes, op_num, job_num)
							if(n_o):
								n_m = deepcopy(m)
								n_m[node[3]][node[4]] = machine
								neighbors.append({'os': n_o, 'ms': n_m})
							machine_nodes[machine] = chain2
		machine_nodes[node[5]] = chain1
	

	return neighbors

def tabu_search(ind, tasks, iter_size, list_size, w_t = [0 for i in range(100)]):
	current = ind
	best = ind
	best_score = genetic.total_time(ind['os'], ind['ms'], tasks, w_t)
	tabu_list = [current]

	neighbors = []
	for i in range(iter_size):
		neighbors = nopt1(current, tasks, w_t)
		if(neighbors == []):
			return best

		scores = []
		for neighbor in neighbors:
			score = genetic.total_time(neighbor['os'], neighbor['ms'], tasks, w_t)
			scores.append(score)

		index = scores.index(min(scores))
		candidate = neighbors[index]

		# print("i="+str(i)+", best_score="+str(best_score))


		while(candidate in tabu_list):
			if(scores[index] < best_score):
				break
			else:
				neighbors.pop(index)
				scores.pop(index)
				if(neighbors == []):
					candidate = tabu_list[0]
					tabu_list.pop(0)
					break
				index = scores.index(min(scores))
				candidate = neighbors[index]
		
		score = genetic.total_time(candidate['os'], candidate['ms'], tasks, w_t)
		if(score < best_score):
			# print("a change")
			if(candidate in tabu_list):
				tabu_list.remove(candidate)
			current = candidate
			best = current
			best_score = score
			tabu_list.append(candidate)
			if(len(tabu_list)>list_size):
				tabu_list.pop(0)
		else:
			current = candidate		
			tabu_list.append(candidate)
			if(len(tabu_list)>list_size):
				tabu_list.pop(0)

	return best
			






	
