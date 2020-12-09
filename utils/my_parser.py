

def parse(path):
    file = open(path, 'r')

    firstLine = file.readline()
    firstLineValues = list(map(int, firstLine.split()[0:2]))

    jobsNb = firstLineValues[0]
    machinesNb = firstLineValues[1]

    jobs = []

    for i in range(jobsNb):
        currentLine = file.readline()
        currentLineValues = list(map(int, currentLine.split()))

        operations = []

        j = 1
        while j < len(currentLineValues):
            k = currentLineValues[j]
            j = j+1

            operation = []

            for ik in range(k):
                machine = currentLineValues[j]
                j = j+1
                processingTime = currentLineValues[j]
                j = j+1

                operation.append({'machine': machine, 'processingTime': processingTime})

            operations.append(operation)

        jobs.append(operations)

    file.close()

    return {'machinesNb': machinesNb, 'jobs': jobs}

def my_parse(path):
	his_parse = parse(path)

	task_list = []
	mechinesNb = his_parse['machinesNb']
	jobs = his_parse['jobs']
	for j in jobs:
		job = []
		for o in j:
			operation = [-1] * mechinesNb
			for m_t in o:
				operation[m_t['machine']-1] = m_t['processingTime']
			job.append(operation)
		task_list.append(job)

	return task_list


	