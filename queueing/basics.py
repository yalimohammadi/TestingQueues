import random
import heapq
from numpy import random
import numpy as np



class Student:
    def __init__(self, service_time_rate):
        self.service_rate=service_time_rate
        t=random.exponential(scale=service_time_rate, size=1)[0]
        self.service_time = t

    def set_arrival_time(self,t):
        self.arrival_time=t
    def time_test_starts(self,t):
        self.start_test=t
        self.waiting_time=self.start_test-self.arrival_time
        self.total_process_time=self.waiting_time+self.service_time


def create_exponential_interarrival(arrival_rate,n,max_times=1000):
    inter_arrivals=random.exponential(scale=arrival_rate, size=n)
    arrival_times=np.cumsum(inter_arrivals)
    while arrival_times[-1]>max_times:
        arrival_times=arrival_times[:-1]
    return arrival_times

def assign_arrivals(arrival_times,all_students):
    permuted_students=np.random.permutation(all_students)
    for i in range(len(permuted_students)):
        st=permuted_students[i]
        st.set_arrival_time(arrival_times[i])
    return permuted_students


def create_service_times(service_rates,population):
    #service_rate and population are lists of the same size, that shows how many people have a particular service time
    all_students=[]
    service_data=[]
    num_types=len(service_rates)
    for i in range(num_types):
        service_data+=[{"rate":service_rates[i],"population":population[i],"students":[]}]
    for i in range(num_types):
        # service_times = random.exponential(scale=service_rates[i], size=population[i])
        list_students=[]
        for j in range(population[i]):
            list_students.append(Student(service_rates[i]))
        all_students+=list_students
        service_data[i]["students"]=list_students

    return service_data, all_students


def generate_queue(all_students,num_servers=1):
    # service times and all_students are sorted
    Q=[]
    for st in all_students:
        heapq.heappush(Q,(st.arrival_time,st))
    curr_times=[0 for i in range(num_servers)]
    while Q:
        arrival_time,st = heapq.heappop(Q)
        ind=np.argmin(curr_times)

        if curr_times[ind]<arrival_time:
            # queue was empty for a little while
            curr_times[ind]=arrival_time
        st.time_test_starts(curr_times[ind])
        curr_times[ind]+=st.service_time

def simple_run(n,service_rate,arrival_rate,num_servers=1):

    arrival_times= create_exponential_interarrival(arrival_rate, n)
    service_data, all_students=create_service_times([service_rate], [n])
    all_students=assign_arrivals(arrival_times, all_students) #all students sorted by arrival time
    generate_queue(all_students,num_servers=num_servers)

    # for st in all_students:
    #     print("arrival time",st.arrival_time,"start_test",st.start_test,"service_time",st.service_time)

    return service_data
def compute_average_waiting_time(service_data):
    for i in range(len(service_data)):
        waiting_times = []
        all_students=service_data[i]["students"]
        for st in all_students:
            waiting_times.append(st.waiting_time)
        service_data[i]["avg_wait_t"]=np.mean(waiting_times)

# simple_run(10,2,1)

import matplotlib.pyplot as plt
def increasing_arrival_rates(num_sim=100):
    waiting_times=[]
    arrivals= np.linspace(1.,3,100)
    for arrival_rate in arrivals:
        waiting_tim_fixed_arrival=[]
        for i in range(num_sim):
            service_data=simple_run(10,service_rate=2.5,arrival_rate=arrival_rate)
            compute_average_waiting_time(service_data)
            w_t=service_data[0]["avg_wait_t"]
            waiting_tim_fixed_arrival.append(w_t)
        waiting_times.append(np.mean(waiting_tim_fixed_arrival))
    plt.plot(arrivals,waiting_times)
    plt.show()


def increasing_lanes(num_sim=100):
    waiting_times=[]
    lanes= list(range(1,10))
    for num_servers in lanes:
        waiting_tim_fixed_arrival=[]
        for i in range(num_sim):
            service_data=simple_run(10,service_rate=2.5,arrival_rate=2.,num_servers=num_servers)
            compute_average_waiting_time(service_data)
            w_t=service_data[0]["avg_wait_t"]
            waiting_tim_fixed_arrival.append(w_t)
        waiting_times.append(np.mean(waiting_tim_fixed_arrival))
    plt.plot(lanes,waiting_times)
    plt.show()
increasing_lanes()
