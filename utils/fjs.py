import random

#按照scheduling and rescheduling中的4.2和5.2的方式生成新任务
#6台机器
#每个任务4、5、6个操作
#每个操作花1~7的时间
#所以平均每个任务花p = 20的时间
#新任务到来时间间隔为指数分布，且均值为20/(6*utilization_rate)
def generate_job(minm_per_p = 1, maxm_per_p = 4, machine_num = 6):
	machine_sets = list(range(machine_num))
	job = []
	op_num = random.randint(4, 6)
	for i in range(op_num):
		op = [-1] * machine_num
		m_per_p = random.randint(minm_per_p, maxm_per_p)
		available_machines = random.sample(machine_sets, m_per_p)
		for j in available_machines:
			op[j] = random.randint(1, 7)
		job.append(op)
	return job

