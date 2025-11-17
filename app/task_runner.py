"""
docstring
"""
from queue import Queue
from threading import Thread, Event, Lock
import os
import multiprocessing
import json


class ThreadPool:
    """
    this class 
    """
    def __init__(self, data_ingestor):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task

        #setez cate thread-uri pot avea
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.nr_threads = os.environ['TP_NUM_OF_THREADS']
        else:
            self.nr_threads = multiprocessing.cpu_count()


        self.jobs = 1
        self.queue_jobs = Queue()
        self.threads_list = []
        self.jobs_done = {}
        self.lock = Lock()
        self.event = Event()
        self.webserver_event = Event()
        self.up = True

        for i in range(0, self.nr_threads):
            self.threads_list.append(TaskRunner(i, self, data_ingestor))

        for i in self.threads_list:
            i.start()


class TaskRunner(Thread):
    """
    this class 
    """
    def __init__(self, id, master, data_ingestor):
        super().__init__()
        self.id = id
        self.lock = Lock()
        self.master = master
        self.data_ingestor = data_ingestor
        # init necessary data structures
        self.queue = self.master.queue_jobs

    def run(self):
        while True:
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            if self.master.queue_jobs.empty() is False:
                item = self.master.queue_jobs.get()
                #In functie de ID-ul cererii care e reprezentat
                #de item[0] se apeleaza o diferita functie.
                aux = None
                if item[0] == 0:
                    aux = states_mean(item[1], self.data_ingestor)
                elif item[0] == 1:
                    aux = state_mean(item[1], self.data_ingestor)
                elif item[0] == 2:
                    aux = best5(item[1], self.data_ingestor)
                elif item[0] == 3:
                    aux = worst5(item[1], self.data_ingestor)
                elif item[0] == 4:
                    aux = global_mean(item[1], self.data_ingestor)
                elif item[0] == 5:
                    aux = diff_from_mean(item[1], self.data_ingestor)
                elif item[0] == 6:
                    aux = state_diff_from_mean(item[1], self.data_ingestor)
                elif item[0] == 7:
                    aux = mean_by_category(item[1], self.data_ingestor)
                elif item[0] == 8:
                    aux = state_mean_by_category(item[1], self.data_ingestor)
                elif item[0] == 9:
                    join_all(self.id, self)
                    self.master.webserver_event.set()
                    self.master.webserver_event.set()
                    self.master.up = False
                    break
                with self.master.lock:
                    self.master.jobs += 1

                with open(f"results/job_id_{item[2]}.json", "w", encoding='utf-8') as fout:
                    json.dump(aux, fout)
                self.master.jobs_done[item[2]] = aux
            else:
                if self.master.event.is_set():
                    break

def join_all(id, thread):
    """
    metoda ce face join dintr-un thread pe celelalte
    """
    for i in thread.master.threads_list:
        if i.id != id:
            i.join()


def states_mean(data, data_ingestor):
    """
    se face o lista in care se calculeaza pentru fiecare stat un tuplu de suma totala
    si numarul de studii, iar apoi imparte in rezultat suma la numar
    """
    dict_data = data
    returned_list = {}

    for lines in data_ingestor.data:
        if dict_data['question'] == lines['Question']:
            if lines['LocationDesc'] in returned_list:
                a = returned_list[lines['LocationDesc']]
                b = (float(a[0]) + float(lines['Data_Value']), float(a[1]) + float(1))
                returned_list[lines['LocationDesc']] = b

            else:
                returned_list[lines['LocationDesc']] = (float(lines['Data_Value']), 1)


    result = [(a, b[0] / b[1] ) for (a, b) in list(returned_list.items())]

    dict5 = {}
    for i in result:
        dict5[i[0]] = i[1]
    return dict5


def state_mean(data, data_ingestor):
    """
    metoda ce calculeaza doar pentru un singur stat, analog ca mai sus
    """
    dict_data = data
    returned_list = {}

    for lines in data_ingestor.data:
        if dict_data['question'] == lines['Question'] and \
            dict_data['state'] == lines['LocationDesc']:
            if lines['LocationDesc'] in returned_list:
                a = returned_list[lines['LocationDesc']]
                b = (float(a[0]) + float(lines['Data_Value']), float(a[1]) + float(1))
                returned_list[lines['LocationDesc']] = b

            else:
                returned_list[lines['LocationDesc']] = (float(lines['Data_Value']), 1)

    result = [(a, b[0] / b[1] ) for (a, b) in list(returned_list.items())  ]

    dict5 = {}
    for i in result:
        dict5[i[0]] = i[1]
    return dict5


def best5(data, data_ingestor):
    """
    metoda ce calculeaza primele 5, analog ca mai sus doar ca le ia pe primele
    """
    dict_data = data
    returned_list = {}

    for lines in data_ingestor.data:
        if dict_data['question'] == lines['Question']:
            if lines['LocationDesc'] in returned_list:
                a = returned_list[lines['LocationDesc']]
                b = (float(a[0]) + float(lines['Data_Value']), float(a[1]) + float(1))
                returned_list[lines['LocationDesc']] = b

            else:
                returned_list[lines['LocationDesc']] = (float(lines['Data_Value']), 1)


    result = [(a, b[0] / b[1] ) for (a, b) in list(returned_list.items())  ]
    if dict_data['question'] in data_ingestor.questions_best_is_max:
        result_sorted = sorted(result, key = lambda x: -x[1])
    else:
        result_sorted = sorted(result, key = lambda x: x[1])
    result_sorted = result_sorted[0:5]

    dict5 = {}
    for i in result_sorted:
        dict5[i[0]] = i[1]
    return dict5



def worst5(data, data_ingestor):
    """
    metoda ce calculeaza ultimele 5, analog ca mai sus doar ca le ia pe ultimele
    """
    dict_data = data
    returned_list = {}

    for lines in data_ingestor.data:
        if dict_data['question'] == lines['Question']:
            if lines['LocationDesc'] in returned_list:
                a = returned_list[lines['LocationDesc']]
                b = (float(a[0]) + float(lines['Data_Value']), float(a[1]) + float(1))
                returned_list[lines['LocationDesc']] = b

            else:
                returned_list[lines['LocationDesc']] = (float(lines['Data_Value']), 1)

    items_list = list(returned_list.items())
    result = [(a, b[0] / b[1] ) for (a, b) in items_list  ]

    if dict_data['question'] in data_ingestor.questions_best_is_min:
        result_sorted = sorted(result, key = lambda x: -x[1])
    else:
        result_sorted = sorted(result, key = lambda x: x[1])

    result_sorted = result_sorted[0:5]
    dict5 = {}
    for i in result_sorted:
        dict5[i[0]] = i[1]
    return dict5



def global_mean(data, data_ingestor):
    """
    metoda ce calculeaza global_mean, ia o variabila unde tine suma si un counter
    """
    dict_data = data
    mean = 0.0
    number_states = 0.0
    for lines in data_ingestor.data:
        if dict_data['question'] == lines['Question']:
            mean += float(lines['Data_Value'])
            number_states += 1.0

    mean = float(mean/number_states)
    dict5 = {}
    dict5["global_mean"] = mean
    return dict5


def diff_from_mean(data, data_ingestor):
    """
    se face media globala si media pentru fiecare stat ca mai sus
    si se face diferenta lor
    """
    dict_data = data
    returned_list = {}

    mean = 0.0
    nr_states = 0.0

    for lines in data_ingestor.data:
        if dict_data['question'] == lines['Question']:
            if lines['LocationDesc'] in returned_list:
                a = returned_list[lines['LocationDesc']]
                b = (float(a[0]) + float(lines['Data_Value']), float(a[1]) + float(1))
                returned_list[lines['LocationDesc']] = b
                mean += float(lines['Data_Value'])
                nr_states += 1.0

            else:
                returned_list[lines['LocationDesc']] = (float(lines['Data_Value']), 1)
                mean += float(lines['Data_Value'])
                nr_states += 1.0


    mean = float(mean/nr_states)
    result = [(a, mean - (b[0] / b[1])) for (a, b) in list(returned_list.items())  ]

    dict5 = {}
    for i in result:
        dict5[i[0]] = i[1]
    return dict5


def state_diff_from_mean(data, data_ingestor):
    """
    metoda ce calculeaza analog ca mai sus doar ca pentru un stat.
    """
    dict_data = data
    returned_list = {}

    mean = 0.0
    nr_states = 0.0
    for lines in data_ingestor.data:
        if dict_data['question'] == lines['Question'] and \
            dict_data['state'] == lines['LocationDesc']:
            if lines['LocationDesc'] in returned_list:
                a = returned_list[lines['LocationDesc']]
                b = (float(a[0]) + float(lines['Data_Value']), float(a[1]) + float(1))
                returned_list[lines['LocationDesc']] = b

            else:
                returned_list[lines['LocationDesc']] = (float(lines['Data_Value']), 1)

        if dict_data['question'] == lines['Question']:
            mean += float(lines['Data_Value'])
            nr_states += 1.0


    mean = mean/nr_states

    result = [(a, mean - b[0] / b[1] ) for (a, b) in list(returned_list.items())  ]

    dict5 = {}
    for i in result:
        dict5[i[0]] = i[1]
    return dict5



def mean_by_category(data, data_ingestor):
    """
    metoda ce calculeaza media dupa categorie, functioneaza ca states_mean
    doar ca cheia din lista e si in functie de categorie.
    """
    dict_data = data
    returned_list = {}

    for lines in data_ingestor.data:
        if dict_data['question'] == lines['Question'] and \
            lines['StratificationCategory1'] != '' and lines['Stratification1'] != '':
            if (lines['LocationDesc'], lines['StratificationCategory1'], lines['Stratification1'])\
                  in returned_list:
                a = returned_list[(lines['LocationDesc'], lines['StratificationCategory1'], \
                                   lines['Stratification1'])]
                b = (float(a[0]) + float(lines['Data_Value']), float(a[1]) + float(1))
                returned_list[(lines['LocationDesc'], lines['StratificationCategory1'], \
                               lines['Stratification1'])] = b

            else:
                returned_list[(lines['LocationDesc'], lines['StratificationCategory1'], \
                               lines['Stratification1'])] \
                    = (float(lines['Data_Value']), 1)

    result = [(a, b[0] / b[1] ) for (a, b) in list(returned_list.items()) ]

    result_sorted = sorted(result, key = lambda x: x[0])

    dict5 = {}
    for i in result_sorted:
        dict5[str(i[0])] = i[1]
    return dict5

def state_mean_by_category(data, data_ingestor):
    """
    metoda ce calculeaza analog ca mai sus doar ca pentru un stat
    """
    dict_data = data
    returned_list = {}

    for lines in data_ingestor.data:
        if dict_data['question'] == lines['Question'] and lines['StratificationCategory1'] != '' \
            and lines['Stratification1'] != '' and dict_data['state'] == lines['LocationDesc']:
            if ( lines['StratificationCategory1'], lines['Stratification1']) \
                in returned_list:
                a = returned_list[( lines['StratificationCategory1'], lines['Stratification1'])]
                b = (float(a[0]) + float(lines['Data_Value']), float(a[1]) + float(1))
                returned_list[( lines['StratificationCategory1'], lines['Stratification1'])] = b

            else:
                returned_list[( lines['StratificationCategory1'], lines['Stratification1'])] \
                    = (float(lines['Data_Value']), 1)


    result = [(a, b[0] / b[1] ) for (a, b) in list(returned_list.items()) ]

    result_sorted = sorted(result, key = lambda x: x[0])
    dict5 = {}
    for i in result_sorted:
        dict5[str(i[0])] = i[1]
    return {dict_data['state'] : dict5}
