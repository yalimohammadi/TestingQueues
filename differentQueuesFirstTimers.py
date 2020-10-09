import numpy as np
import simpy
import matplotlib.pyplot as plt

NUM_QUEUES = 8  # Number of registrars in the center
NUM_TENTS= 4  # Number of testing tents in the center
FIRST_CHECKIN_TIME = 10
RETURN_CHECKIN_TIME = 10
FIRST_TEST_TIME = 10      # Minutes it takes to test for first time test takers
RETURN_TEST_TIME = 3      # Minutes it takes to test for return time test takers
T_INTER = 5       # A new student comes every ~7 minutes
SIM_TIME = 60     # Simulation time in minutes
NUM_FIRST_TIME_TESTERS = 800
NUM_RETURN_TESTERS = 200
class MonitoredResource(simpy.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []

    def request(self, *args, **kwargs):
        self.data.append((self._env.now, len(self.queue)))
        print("queues",self.queue)
        return super().request(*args, **kwargs)

    def release(self, *args, **kwargs):
        self.data.append((self._env.now, len(self.queue)))
        return super().release(*args, **kwargs)

class TestCenter(object):
    def __init__(self, env, num_queue):
        self.env = env
        self.checking_queue = MonitoredResource(env, capacity=num_queue)
        self.testing_queue = MonitoredResource(env, capacity=NUM_TENTS)

    def check_in(self, mean_check_in_time,mean_test_time):
        checkin_time=np.random.exponential(mean_check_in_time)
        yield self.env.timeout(checkin_time)
        with self.testing_queue.request() as request:
            yield request
            yield self.env.process(self.take_test(mean_test_time))
    def take_test(self, mean_test_time):
        test_time=np.random.exponential(mean_test_time)
        yield self.env.timeout(test_time)



def student(env, name, tc,wait_times):
    # print('%s arrives at the center at %.2f.' % (name, env.now))
    arrival_time=env.now
    state= np.random.uniform(0,1)

    if state<NUM_FIRST_TIME_TESTERS*1./(NUM_RETURN_TESTERS+NUM_FIRST_TIME_TESTERS):
        # new tester
        with tc.checking_queue.request() as request:
            yield request
            wait_time=env.now-arrival_time
            # print('%s new tester starts the test at %.2f.' % (name, env.now))
            yield env.process(tc.check_in(FIRST_CHECKIN_TIME,FIRST_TEST_TIME))
            # print('%s new tester leaves the center at %.2f.' % (name, env.now))
    else:
        # return tester
        with tc.checking_queue.request() as request:
            yield request
            wait_time=env.now-arrival_time
            # print('%s return tester starts the test at %.2f.' % (name, env.now))
            yield env.process(tc.check_in(RETURN_CHECKIN_TIME,RETURN_TEST_TIME))
            # print('%s return tester leaves the center at %.2f.' % (name, env.now))

    wait_times.append(wait_time)

def setup(env, num_queues, t_inter,wait_times):
    """Create a center, a number of initial students and keep creating students
    approx. every ``t_inter`` minutes."""

    testCenter = TestCenter(env, num_queues)

    # Create 4 initial students
    for i in range(4):
        env.process(student(env, 'student %d' % i, testCenter,wait_times))

    # Create more student while the simulation is running
    while True:
        yield env.timeout(np.random.exponential(t_inter))
        i += 1
        env.process(student(env, 'student %d' % i, testCenter,wait_times))
    print(testCenter.testing_queue.data)
    print(testCenter.checkin_quque.data)

def execute_one_day(NUM_QUEUES):
    # Create an environment and start the setup process
    wait_times = []
    env = simpy.Environment()
    env.process(setup(env, NUM_QUEUES, T_INTER, wait_times))

    # Execute!
    env.run(until=SIM_TIME)
    # print(wait_times)

    return wait_times

all_wait_times=[]
for i in range(100):
    wait_times=execute_one_day(2)
    all_wait_times+=wait_times

print(all_wait_times)
plt.hist(all_wait_times, bins='auto')  # arguments are passed to np.histogram
plt.title("Two queues with mixed students ")
plt.xlabel("Waiting time in minute")
plt.ylabel("Counts")
plt.show()