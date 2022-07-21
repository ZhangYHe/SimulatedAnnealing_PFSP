import Simulated_Annealing

#改变Step与T0取值
for S in [5,10,15,25,50]:
    for T0 in [5,10,15,50,100]:
        run=Simulated_Annealing.My_Simulated_Annealing(alpha=0.8,step=S,T_threshold=0.1,temperature=T0)
        final_sequence,final_time=run.Annealing()

        print("-------{}---{}----".format(S,T0))
        print(run.instance_name)
        print(final_sequence)
        print(final_time)

#改变Step和Alpha取值
for S in [5,10,15,25,50]:
    for Alpha in [0.3,0.5,0.6,0.8,0.9]:
        run=Simulated_Annealing.My_Simulated_Annealing(alpha=Alpha,step=S,T_threshold=0.1,temperature=50)
        final_sequence,final_time=run.Annealing()

        print("-------{}---{}----".format(S,Alpha))
        print(run.instance_name)
        print(final_sequence)
        print(final_time)