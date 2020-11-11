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


Hunting={"W":[8.5,9,9,9,9],"Nurse":[2]*5}
Acad={"W":[8.5,8.5,8.5,7.3,8.5],"Nurse":[5,4,4,4,4]}
Perez={"W":[9]*5,"Nurse":[2]*5}
SGate={"W":[8.25,8.16,8.5,8.5,8.5],"Nurse":[4,3,3,3,3]}
Stevenson={"W":[8.5,8.5,8.5,7,8.5],"Nurse":[3]*5}
Wilson={"W":[8.1,8.5,8.5,8.5,8.5],"Nurse":[5,4,4,4,4]}
East=[Hunting,Acad,Perez,SGate,Stevenson,Wilson]

Pacioma={"W":[7.5,8.3,8.35,8.3,8.75],"Nurse":[4,3,4,4,4]}
Madison={"W":[8.8,8.7,8.8,7.1,7],"Nurse":[3,3,3,3,2]}
Romer={"W":[9.5,9.16,9.16,9,9],"Nurse":[2,3,3,2,2]}
SanFernando={"W":[9.1,9.1,9.1,9,9],"Nurse":[3,3,3,2,2]}
Gleason={"W":[7.25,9.5,9.5,7.25,9.5],"Nurse":[2]*5}
Vista={"W":[9.5]*5,"Nurse":[2]*5}
NEast=[Pacioma,Madison,Romer,SanFernando,Gleason,Vista]


Frost={"W":[8.5]*5,"Nurse":[2]*5}
Holmes={"W":[8.8,8.8,9, 8.8,8.8],"Nurse":[3,3,2,3,3]}
Lawrence={"W":[9,8.5,8.5,8.5,8.5],"Nurse":[2]*5}
Northridge={"W":[9,9,8.5,8.5,8.8],"Nurse":[2,2,3,3,3]}
Reseda={"W":[8.5]*5,"Nurse":[2]*5}
Woodland={"W":[8.8,8.8,8.8,9,9],"Nurse":[3,3,3,2,2]}
NWest=[Frost, Holmes, Lawrence, Northridge,Reseda,Woodland]



Bancroft={"W":[7.25,7.25,7.25,7.25,8],"Nurse":[2]*5}
Crenshaw={"W":[8.5,8.5,8.16,8.5,8.5],"Nurse":[3]*5}
Fairfax={"W":[8.5]*5,"Nurse":[3]*5}
Grandview={"W":[8.5]*5,"Nurse":[2]*5}
Hawkins={"W":[8.5]*5,"Nurse":[2]*5}
LosAngeles= {"W":[8.5,8.5,8.67,8.67,8.5],"Nurse":[2,2,3,3,2]}
Palms={"W":[9.5]*5,"Nurse":[2]*5}
RaymondAve={"W":[8.67,8.5,8.5,8.5,8.5],"Nurse":[3]*5}
Wright= {"W":[8.83]*5,"Nurse":[3]*5}
West = [Bancroft,Crenshaw,Fairfax,Grandview,Hawkins,LosAngeles,Palms,RaymondAve,Wright]

S112th ={"W":[8.5]*5,"Nurse":[2]*5}
Bethune ={"W":[9,9,8,9,8],"Nurse":[2,2,3,2,3]}
Bridges ={"W":[8.1,8.5,8,8.1,8.5],"Nurse":[5,4,4,5,4]}
Carnegie ={"W":[8,7.75,8,8,8.5],"Nurse":[3,2,3,3,1]}
Dodson ={"W":[8.75]*5,"Nurse":[2]*5}
Drew = {"W":[9]*5,"Nurse":[2]*5}
Gardena ={"W":[8.6,8.5,8.25,8.67,8.1],"Nurse":[5,6,6,6,5]}
President ={"W":[8.25,7.5,8.25,8.25,8.75],"Nurse":[2]*5}
South = [S112th ,Bethune ,Bridges ,Carnegie ,Dodson ,Drew ,Gardena ,President]
def find_num_students_tested_for_school_week(school,CS,CA,P):
    working_hours=school["W"]
    num_personell=school["Nurse"]
    num_students_shared=[]
    num_students_separate = []
    for i in range(5): #days of week
        # print(school)
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
        # print(shared_s)
        # print(separate_s)
        # print(total_separate)
        # print(total_shared)
        total_separate+=separate_s
        total_shared+=shared_s
    return total_shared,total_separate

def find_avg_num_nurses(district):
    num_personell=[]
    for school in district:
        num_personell = school["Nurse"]
        num_personell.append(np.mean(num_personell))
    return sum(num_personell)

def plot_school(data,label):
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    plt.plot(days,data,label=label)


def district_plot(district,name):
    total_shared, total_spsarate = find_num_students_tested_for_district_week(district, CS=.3, CA=1., P=3.2)
    # plot_school(total_shared, name+", Shared Queues")

    print(name,sum(total_spsarate),sum(total_shared))
    plot_school(total_spsarate, name+"")

all_districts=[Central,East,NEast,NWest,West,South]
i=1
for district in all_districts:
    print(i)

    i+=1
    print(find_avg_num_nurses(district))
district_plot(Central,"C")
district_plot(East,"E")
district_plot(NEast,"NE")
district_plot(NWest,"NW")
district_plot(West,"West")
district_plot(South,"South")
plt.ylabel("number of students tested")
plt.xlabel("days of week")
plt.title("Shared Queues vs Separate Queues")
plt.legend()
plt.show()



S=[ 10.8, 18.0, 15.6, 12.0, 25.2,12.0]
S= [79364,
71767,
78178,
72966,
81440,
82058]

print(np.array(S)/sum(S))
