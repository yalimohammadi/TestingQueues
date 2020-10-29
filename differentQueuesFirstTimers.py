import numpy as np
import simpy
import matplotlib.pyplot as plt

NUM_FAST_TRACKS=2
NUM_Regular_QUEUES = 6  # Number of registrars in the center
NUM_TENTS= 4  # Number of testing tents in the center
FIRST_CHECKIN_TIME = 3
RETURN_CHECKIN_TIME = 2
FIRST_TEST_TIME = 6./6    # Minutes it takes to test for first time test takers
RETURN_TEST_TIME = 3./2      # Minutes it takes to test for return time test takers
WORKING_TIME = 10     # Simulation time in minutes
NUM_FIRST_TIME_TESTERS = 250
NUM_RETURN_TESTERS = 250
SIM_TIME= 120
class MonitoredResource(simpy.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = [(0,0)]

    def request(self, *args, **kwargs):
        self.data.append((self._env.now, len(self.queue)))
        # print("queues",self.queue)
        return super().request(*args, **kwargs)

    def release(self, *args, **kwargs):
        self.data.append((self._env.now, len(self.queue)))
        return super().release(*args, **kwargs)

class TestCenter(object):
    def __init__(self, env):
        self.env = env
        self.checking_queue = MonitoredResource(env, capacity=NUM_Regular_QUEUES)
        self.check_in_queue_fast = MonitoredResource(env, capacity=NUM_FAST_TRACKS)
        # self.testing_queue = MonitoredResource(env, capacity=NUM_TENTS)

    def check_in(self, mean_check_in_time,mean_test_time):
        # checkin_time=np.random.exponential(mean_check_in_time)

        yield self.env.timeout(mean_check_in_time)
    # def take_test(self, mean_test_time):
    #     # test_time=np.random.exponential(mean_test_time)
    #     test_time=mean_test_time
    #     yield self.env.timeout(test_time)



def student(env, name, tc,wait_times):
    # print('%s arrives at the center at %.2f.' % (name, env.now))
    arrival_time=env.now
    state= np.random.uniform(0,1)

    if state<NUM_FIRST_TIME_TESTERS*1./(NUM_RETURN_TESTERS+NUM_FIRST_TIME_TESTERS):
        # new tester
        if tc.check_in_queue_fast.data[-1][1] ==0:

            with tc.check_in_queue_fast.request() as request:
                yield request
                wait_time = env.now - arrival_time
                yield env.process(tc.check_in(FIRST_CHECKIN_TIME, FIRST_TEST_TIME))
        else:
            with tc.checking_queue.request() as request:
                yield request
                wait_time=env.now-arrival_time
                yield env.process(tc.check_in(FIRST_CHECKIN_TIME,FIRST_TEST_TIME))
    else:
        # return tester
        if tc.check_in_queue_fast.data[-1][1] < 2*tc.checking_queue.data[-1][1]:

            with tc.check_in_queue_fast.request() as request:
                yield request
                wait_time=env.now-arrival_time
                # print('%s return tester starts the test at %.2f.' % (name, env.now))
                yield env.process(tc.check_in(RETURN_CHECKIN_TIME,RETURN_TEST_TIME))
                # print('%s return tester leaves the center at %.2f.' % (name, env.now))
        else:
            with tc.checking_queue.request() as request:
                yield request
                wait_time = env.now - arrival_time
                # print('%s return tester starts the test at %.2f.' % (name, env.now))
                yield env.process(tc.check_in(RETURN_CHECKIN_TIME, RETURN_TEST_TIME))

    wait_times.append(wait_time)

def setup(env,  t_inter,wait_times):
    """Create a center, a number of initial students and keep creating students
    approx. every ``t_inter`` minutes."""

    testCenter = TestCenter(env)

    # Create 4 initial students
    for i in range(4):
        env.process(student(env, 'student %d' % i, testCenter,wait_times))


    # Create more student while the simulation is running
    while True:
        yield env.timeout(np.random.exponential(t_inter))
        i += 1
        env.process(student(env, 'student %d' % i, testCenter,wait_times))


def execute_one_day( Working_Time):
    # Create an environment and start the setup process
    wait_times = []
    env = simpy.Environment()
    T_INTER= Working_Time*1./(NUM_FIRST_TIME_TESTERS+NUM_RETURN_TESTERS)
    env.process(setup(env,  T_INTER, wait_times))

    # Execute!
    env.run(until=SIM_TIME)
    # print(wait_times)

    return wait_times

waiting_times=[]
Working_Times=list(range(180, 1200,10))
for W in Working_Times:
    all_wait_times=[]
    for i in range(100):
        wait_times=execute_one_day(WORKING_TIME)
        all_wait_times+=wait_times
    avg_waiting=np.mean(all_wait_times)
    print(avg_waiting)
    waiting_times.append(avg_waiting)

plt.plot(Working_Times, waiting_times)
plt.show()
# print(all_wait_times)
# plt.hist(all_wait_times, bins='auto')  # arguments are passed to np.histogram
# plt.title("Two queues with mixed students ")
# plt.xlabel("Waiting time in minute")
# plt.ylabel("Counts")
# plt.show()