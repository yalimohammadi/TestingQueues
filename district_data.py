from simple_plots import find_number_of_student
import numpy as np
import matplotlib.pyplot as plt

Carver={"W":[9.5]*5,"Nurse":[2]*5}
Foshay={"W":[9.5]*5,"Nurse":[2]*5}
Franklin={"W":[8.5,9,9,8.5,9.25],"Nurse":[2]*5}
Marshal={"W":[9.25,9.5,9.25,9.5,4.75],"Nurse":[2]*5}
Roybal={"W":[8.5,9.33,8.75,8.5,8.5],"Nurse":[2]*5}
WestAdams= {"W":[8.5,9,8.5,9.5,9],"Nurse":[2,2,2,1,2]}
Central = [Carver,Foshay,Franklin,Marshal,Roybal,WestAdams]





def find_num_students_tested_for_school_week(school,CS,CA,P):
    working_hours=school["W"]
    num_personell=school["Nurse"]
    num_students_shared=[]
    num_students_separate = []
    for i in range(5): #days of week
        shared= find_number_of_student(CA, CS, W=working_hours[i], L=num_personell[i], P=P, max_wait_time=5, shared_queue=True)
        separate = find_number_of_student(CA, CS, W=working_hours[i], L=num_personell[i], P=P, max_wait_time=5, shared_queue=False)
        num_students_separate.append(separate)
        num_students_shared.append(shared)

    return np.array(num_students_shared),np.array(num_students_separate)






def find_num_students_tested_for_district_week(district,CS,CA,P):
    total_separate = np.zeros(5)
    total_shared = np.zeros(5)
    for school in district:
        shared_s,separate_s=find_num_students_tested_for_school_week(school, CS, CA, P)
        print(shared_s)
        print(separate_s)
        print(total_separate)
        print(total_shared)
        total_separate+=separate_s
        total_shared+=shared_s
    return total_shared,total_separate


def plot_school(data,label):
    plt.plot(days,data,label=label)

days=["Mon","Tue","Wed","Thu","Fri"]
total_shared,total_spsarate= find_num_students_tested_for_district_week(Central,CS=.18,CA=1.,P=2.5)
plot_school(total_shared,"Central, Shared Queues")
plot_school(total_spsarate,"Central, Separate Queues")
plt.ylabel("number of tests")
plt.xlabel("days of week")
plt.legend()
plt.show()

