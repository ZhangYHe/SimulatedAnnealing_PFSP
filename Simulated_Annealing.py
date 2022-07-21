import numpy as np
import csv
import random
import math
import matplotlib.pyplot as plt
import seaborn as sns

class My_Simulated_Annealing:

    def __init__(self,alpha,step,T_threshold,temperature=0):
        #定义工件数量和机器数量
        self.component_num=0
        self.machine_num=0

        #初始化降温过程的alpha和每个温度下执行次数
        self.alpha=alpha
        self.step=step

        #读入样例
        self.Read_time()

        #初始化起始温度和停止退火的温度阈值,选择选取初始温度的方法
        #若没有指定初始温度则使用改进方法选取初始温度
        self.T0=temperature
        self.temperature=self.Chose_temperature()
        self.T_threshold=T_threshold

        #初始化结束条件
        #初始化连续不接纳邻域解的次数阈值、当前不接纳邻域解次数、总接纳邻域解次数、总尝试次数、acceptance ratio阈值
        self.naccepted_threshold=10000
        self.currect_naccepted=0
        self.total_accepted=0
        self.total_try=0
        self.acceptance_ratio_threshold=0.00001

        #随机选定初始解，计算初始解完工时间
        #为便于处理，将工件序号均-1
        sequence=[i for i in range(self.component_num)]
        random.shuffle(sequence)
        self.current_sequence = sequence
        self.current_processing_time=self.Processing_time(self.current_sequence)

        #定义邻域解完工时间
        self.neighbor_sequence=[]
        self.neighbor_processing_time=0

        #定义接纳的邻域解列表和退火过程时间变化列表
        self.accepted_time_list=[]
        self.time_list=[]


    #读入样例函数
    def Read_time(self):

        print("请输入样例")
        self.instance_name=input()

        #读入工件数量、机器数量
        read_string = input()
        ls = read_string.split(' ')
        ls = [i for i in ls if i != '']
        self.component_num = eval(ls[0])
        self.machine_num = eval(ls[1])

        #初始化样例对应的时间表
        self.time_table = np.zeros((self.machine_num,self.component_num), dtype=int)

        for i in range(self.component_num):
            read_string=input()
            ls=read_string.split(' ')
            ls = [i for i in ls if i != '']
            for j in range(self.machine_num):
                self.time_table[j][i]=eval(ls[2*j+1])
        '''
        样例说明：
            以 instance 0 为例
            第一行为样例序号
            第二行为工件数量、机器数量
            从第三行开始表示加工时间
                0 375 1  12 2 142 3 245 4 412
                第三行数据依次表示第一个工件在机器0上加工时间为375，在机器1上加工时间为12......
        '''


    #使用动态规划思想计算完工时间
    def Processing_time(self,sequence):

        #初始化dp表第一行
        self.dp_table=np.zeros((self.machine_num,self.component_num),dtype=int)
        for i in range(self.machine_num):
            if i==0:
                self.dp_table[0][0]=self.time_table[0][sequence[0]]
            else:
                self.dp_table[i][0]=self.dp_table[i-1][0]+self.time_table[i][sequence[0]]

        #初始化dp表第一列
        for i in range(1,self.component_num):
                self.dp_table[0][i]=self.dp_table[0][i-1]+self.time_table[0][sequence[i]]

        for i in range(1,self.machine_num):
            for j in range(1,self.component_num):
                self.dp_table[i][j]=max(self.dp_table[i-1][j],self.dp_table[i][j-1])+self.time_table[i][sequence[j]]

        #dp表最后一行最后一列即为当前加工序列最小总完工时间
        return self.dp_table[self.machine_num-1][self.component_num-1]


    #随机选择邻域解
    #随机选取当前加工顺序的一个位置，与下一位置工件序号交换
    def Random_select(self,sequence):

        temp_sequence=[item for item in sequence]
        #随机选取待交换的位置
        pos=random.randint(0,self.component_num-1)

        #交换当前解序列中相邻两数位置
        #若随机选取的位置为当前加工顺序的最末位，则与第一位工件序号交换
        if pos==(self.component_num-1):
            temp=temp_sequence[self.component_num-1]
            temp_sequence[self.component_num-1]=temp_sequence[0]
            temp_sequence[0]=temp
        else:
            temp = temp_sequence[pos]
            temp_sequence[pos] = temp_sequence[pos+1]
            temp_sequence[pos+1] = temp
        return temp_sequence


    #选定初始温度
    def Chose_temperature(self):
        #若没有给定初始温度则采用改进方法选取初始温度
        if self.T0==0:
            #初始化接纳质量较差解的概率,随机选取解的个数
            P0=0.98
            N=360

            Pmax=0
            Pmin=0
            sequence = [i for i in range(self.component_num)]

            #记录随机选取的N个解总完工时间的最大最小值
            for i in range(N):
                random.shuffle(sequence)
                time=self.Processing_time(sequence)
                if i==0:
                    Pmax=time
                    Pmin=time
                else:
                    if Pmax<time:
                        Pmax=time
                    elif Pmin>time:
                        Pmin=time

            #按照公式计算初始温度取值
            T0=(Pmin-Pmax)/(math.log(P0,math.e))
            print("N={},Choose T0 as {:.5f}".format(N,T0))
            return T0
        else:
            return self.T0


    #判断是否结束退火
    def End_annealing(self):

        #温度小于阈值，结束退火
        if self.temperature<self.T_threshold:
            print("End annealing because T<T_threshold")
            return True
       #连续不接纳邻域解的次数超过限制
        elif self.currect_naccepted>self.naccepted_threshold:
            print("End annealing because currect_naccepted>threshold")
            self.currect_naccepted=0
            return True
        #acceptance ratio低于阈值
        elif self.total_try!=0 and self.total_accepted/self.total_try<self.acceptance_ratio_threshold:
            print("End annealing because acceptance ratio<threshold")
            return True
        else:
            return False

    #退火过程
    def Annealing(self):

        while not self.End_annealing():
            #初始化当前温度下不接纳邻域解次数
            self.currect_naccepted=0

            for process_time in range(self.step):

                self.time_list.append(self.current_processing_time)
                #选定邻域解
                self.neighbor_sequence=self.Random_select(self.current_sequence)
                self.neighbor_processing_time=self.Processing_time(self.neighbor_sequence)

                #计算delta E并判断是否接纳邻域解
                delta_E =  self.current_processing_time-self.neighbor_processing_time
                # 接受邻域解
                if delta_E>=0:
                    self.current_sequence=self.neighbor_sequence
                    self.current_processing_time=self.neighbor_processing_time
                    self.total_accepted+=1
                    self.accepted_time_list.append(self.neighbor_processing_time)
                else:
                    #捕获计算概率时的异常
                    try:
                        Pr=math.exp(delta_E/self.temperature)
                    except OverflowError:
                        Pr=1

                    P=random.random()
                    # 接受邻域解
                    if P<Pr:
                        self.current_sequence=self.neighbor_sequence
                        self.current_processing_time = self.neighbor_processing_time
                        self.accepted_time_list.append(self.neighbor_processing_time)
                        self.total_accepted += 1
                    # 拒绝邻域解
                    else:
                        self.currect_naccepted+=1

                self.total_try += 1
            #执行Step次选择邻域解后降低温度
            self.temperature*=self.alpha

        #退火结束，绘制图像
        self.Draw_image()

        return self.current_sequence,self.current_processing_time


    #绘制图像
    def Draw_image(self):

        id=[i for i in range(len(self.time_list))]

        plt.plot(id, self.time_list, linewidth=0.05,color="orange")

        #将图片名保存为样例名--总完工时间
        plt.savefig(self.instance_name+"--"+str(self.current_processing_time)+".png")
        plt.show()



#.......................我佛慈悲.....................
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -卍-|||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#..................佛祖开光 ,永无BUG...................




