
import matplotlib.pyplot as plt
import numpy as np
Average_waiting_time=[]


def calc_waiting_time(CA,CS, N, W , L, P):
    lambd=  N/(W * 60.)# arrival_rate per minute

    mu = 1./ P
    n = L # number of servers
    # rho= N*P/(W*60. L )
    rho = lambd / (n * mu)  # average utilization
    # print("rho",rho)

    M = np.sqrt(2*n+2)-2
    if rho==1:
        return -1
    avg_wait = (1. / lambd) * (rho ** 2) / (1 - rho) * (CA ** 2 + CS ** 2) / 2. * rho ** M

    return avg_wait
def calc_queue_length(CA,CS, N, W , L, P):
    lambd=  N/(W * 60.)# arrival_rate per minute
    mu = 1./ P
    n = L # number of servers
    # rho= N*P/(W*60. L )
    rho = lambd / (n * mu)  # average utilization
    # print("rho",rho)

    M = np.sqrt(2*n+2)-2
    avg_wait = (1. / lambd) * (rho ** 2) / (1 - rho) * (CA ** 2 + CS ** 2) / 2. * rho ** M

    return avg_wait*lambd

def find_needed_work_hours(CA,CS, N, L, P, max_queue_length=10):
    for W in np.linspace(0.5,12,100):
        avg_length=calc_queue_length(CA, CS, N, W, L, P)

        # print(max_wait_time,avg_wait,L,W)
        if avg_length<0:
            continue
        if avg_length<max_queue_length:
            return W

    return -1

def find_number_of_student(CA,CS, W, L, P, max_wait_time=10,shared_queue=True):
    for N in range(4000,100,-1):
        if shared_queue:
            avg_wait=calc_waiting_time(CA, CS, N, W, L, P)
        else:
            avg_wait = calc_waiting_time(CA, CS, N/L, W, L=1, P=P)

        # print(max_wait_time,avg_wait,L,W)
        if avg_wait<0:
            continue
        if avg_wait<max_wait_time:
            return N

    return -1


def find_number_of_workers(CA,CS, N, W, P, max_wait_time=10,factor=1):
    for L in np.linspace(1,55,1000):
        if factor==1:
            avg_wait=calc_waiting_time(CA, CS, N/L, W, L=1, P=P)
        elif factor==4:
            avg_wait=calc_waiting_time(CA, CS, N, W, L, P)

        # print(max_wait_time,avg_wait,L,W)
        if avg_wait<0:
            continue
        if avg_wait<max_wait_time:
            return L

    return -1

W= 3 # 	Total working hours


# N#Total number of arrivals




# to_plot1=[]
# to_plot2=[]
# to_plot3=[]
# to_plot4=[]
# max_st=300
# N=2000
# min_T=2.8
# L_range=np.linspace(2.5,8,100)
# for W in L_range:
#     CA = 1.
#     CS = .45
#
#     L = 8 # Total Lanes
#     P =2. # Time per person per lane
#     N = find_number_of_student(CA,CS,  W,L,P/2, max_wait_time=5,shared_queue=True) # first strategy
#     to_plot1.append(N)
#     # L = find_number_of_workers(CA,CS, N, W, P, max_wait_time=20,factor=4) # first strategy
#     # to_plot3.append(L)
#
#     # CA = 1.
#     # CS = .45
#     # L1 =int(L/4)  # Total Lanes
#     # P =2.5 # Time per person per lane
#     # N1=int(N/4)
#     # print(calc_waiting_time(CA,CS,N,W,L,P)-calc_waiting_time(CA,CS,N1,W,L,P))
#     N = find_number_of_student(CA,CS, W, L, P, max_wait_time=5,shared_queue=True) # first strategy
#     to_plot2.append(N)
#     # L = find_number_of_workers(CA,CS, N, W, P, max_wait_time=20,factor=1) # first strategy
#     # to_plot4.append(L)
#
#



# print(to_plot)
# plt.plot(list(L_range), to_plot1,label="Separate Queues, Half Service Time",color="red")
# plt.plot(list(L_range), to_plot2,label="Separate Queues, Original Service time.",color="blue")
# # plt.plot(list(L_range), to_plot3,label="Shared Queue",color="red")
# # plt.plot(list(L_range), to_plot4,label="Separate Queues, Usual Service Time",color="blue")
#
# # plt.plot(list(range(4,24,4)), to_plot2,label="First Timers Track  ")
# # plt.plot(list(range(100,max_st)), to_plot 3,label="Shared Queue,  AVG Registration Time = 1:30 min")
# # plt.plot(list(range(100,max_st)), to_plot4,label="Current,  AVG Registration Time = 1:30 min")
#
# # plt.plot(list(range(100,max_st)), to_plot3,label="Slow_track ")
# plt.xlabel("Total Number of Working hours")
# plt.ylabel("Total Number of Student Served  ")
# plt.text(2.5,1800,'~1750 students')
# plt.text(2.5,800,'~800 students')
# plt.hlines(y=1740,xmin=2.5, xmax=4.0, color='black',linestyles="--",alpha=0.2)
# plt.hlines(y=780, xmin=2.5, xmax=4.0, color='black',linestyles="--",alpha=0.2)
# plt.vlines(x=4,ymin=500,ymax=1750,color='black',linestyles="--",alpha=0.2)
# plt.plot(4.,780,'bo')
# plt.plot(4,1740,'ro')
# plt.legend()
# plt.show()
#

