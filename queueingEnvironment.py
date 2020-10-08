import numpy as np
import simpy
import matplotlib.pyplot as plt

# RANDOM_SEED = 42
NUM_QUEUES = 2  # Number of test takers in the center
FIRST_TEST_TIME = 6      # Minutes it takes to test for first time test takers
RETURN_TEST_TIME = 3      # Minutes it takes to test for return time test takers
T_INTER = 5       # A new student comes every ~7 minutes
SIM_TIME = 60     # Simulation time in minutes
NUM_FIRST_TIME_TESTERS = 800
NUM_RETURN_TESTERS = 200


class TestCenter(object):
    def __init__(self, env, num_queue):
        self.env = env
        self.testing_queue = simpy.Resource(env, num_queue)

    def take_test(self,mean_test_time):
        test_time=np.random.exponential(mean_test_time)
        yield self.env.timeout(test_time)


def student(env, name, tc,wait_times):
    # print('%s arrives at the center at %.2f.' % (name, env.now))
    arrival_time=env.now
    state= np.random.uniform(0,1)

    if state<NUM_FIRST_TIME_TESTERS*1./(NUM_RETURN_TESTERS+NUM_FIRST_TIME_TESTERS):
        # new tester
        with tc.testing_queue.request() as request:
            yield request
            wait_time=env.now-arrival_time
            # print('%s new tester starts the test at %.2f.' % (name, env.now))
            yield env.process(tc.take_test(FIRST_TEST_TIME))
            # print('%s new tester leaves the center at %.2f.' % (name, env.now))
    else:
        # return tester
        with tc.testing_queue.request() as request:
            yield request
            wait_time=env.now-arrival_time
            # print('%s return tester starts the test at %.2f.' % (name, env.now))
            yield env.process(tc.take_test(RETURN_TEST_TIME))
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


def execute_one_day():
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
    wait_times=execute_one_day()
    all_wait_times+=wait_times
print(all_wait_times)
plt.hist(all_wait_times, bins='auto')  # arguments are passed to np.histogram
plt.title("Two queues with mixed students ")
plt.xlabel("Waiting time in minute")
plt.ylabel("Counts")
plt.show()