#経路変更の閾値1.5,2,2.5でグラフに出した、さらに日本語対応した
#buffer、patternの順で回せるようにした
#ある一つのノードからの通信量が２倍になる

import statistics
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
import fairnessIndex

mpl.rcParams['font.family'] = 'AppleGothic'#漢字を出せるようにする、数という漢字は対応していない


#figure()でグラフを表示する領域をつくり，figというオブジェクトにする．
fig = plt.figure()
#add_subplot()でグラフを描画する領域を追加する．引数は行，列，場所
ax_buffer = fig.add_subplot(2, 1, 1,xlabel="受信バッファ[%]",ylabel="IoT GWへのトラヒック量[packet]")
ax_stdev = fig.add_subplot(2, 1, 2,)


def show_network():

    ssgw_sample=[]#実験終了時のSSGW受信バッファ使用率を格納
    #print("{:<3}".format(buffer_control),"%:")

    print("Threshold:", Threshold)
    for SSGW in SSGW_list:
        if SSGW.id == 0:
            print("SSGW(0)の受信バッファは{:.3g}%".format((SSGW.current_packet_size/SSGW.max_packet_size)*100))
            ssgw_sample.append((SSGW.current_packet_size/SSGW.max_packet_size)*100)
        if SSGW.id == 1:
            print("SSGW(1)の受信バッファは{:.3g}%".format((SSGW.current_packet_size/SSGW.max_packet_size)*100))
            ssgw_sample.append((SSGW.current_packet_size/SSGW.max_packet_size)*100)
        if SSGW.id == 2:
            print("SSGW(2)の受信バッファは{:.3g}%".format((SSGW.current_packet_size/SSGW.max_packet_size)*100))
            ssgw_sample.append((SSGW.current_packet_size/SSGW.max_packet_size)*100)
        if SSGW.id == 3:
            print("SSGW(3)の受信バッファは{:.3g}%".format((SSGW.current_packet_size/SSGW.max_packet_size)*100))
            ssgw_sample.append((SSGW.current_packet_size/SSGW.max_packet_size)*100)
        if SSGW.id == 4:
            print("SSGW(4)の受信バッファは{:.3g}%".format((SSGW.current_packet_size/SSGW.max_packet_size)*100))
            ssgw_sample.append((SSGW.current_packet_size/SSGW.max_packet_size)*100)
    
    #fairness_index = fairnessIndex.FairnessFunc(ssgw_sample)
    #print("fairness_index:",fairness_index)

    for IoTGW in IoTGW_list:
        if IoTGW.id == 0:
            print("IoTGW(0)の所持パケットは",IoTGW.storage_packet_size)

            if Threshold ==15:
                iot_packet_list15.append(IoTGW.storage_packet_size)
                #f_index_list15.append(fairness_index)
            elif Threshold ==20:
                iot_packet_list20.append(IoTGW.storage_packet_size)               
                #f_index_list20.append(fairness_index)
            elif Threshold ==25:
                iot_packet_list25.append(IoTGW.storage_packet_size)                
                #f_index_list25.append(fairness_index)

    #stdev = statistics.stdev(ssgw_stdev)
    #print("標本標準偏差は:{:.1f}".format(stdev))
   


def node_control(ssgw):#ssgwの受信バッファの状態によってnodeに経路変更or広告window制限をかける関数
    if (ssgw.current_packet_size/ssgw.max_packet_size) <= (buffer_control/100):  #受信バッファの90%ならば制御モード
        pass
    else:
        ave_packet_size = ssgw.current_packet_size / len(ssgw.mynodes)#該当SSGWに接続しているnodeの平均送信量
        #print(ave_packet_size,ssgw.id)
        #Threshold=2#経路変更のための閾値(上に書いた)
        control_flag=False#通信量が増えた特定nodeを経路変更した場合、広告ウィンドウを下げないようにするため
        for node in ssgw.mynodes:
            if node.send_packet_size > ave_packet_size * (Threshold/10):#閾値倍以上のnodeが存在するか確認、あれば経路変更、なければ該当するSSGWに接続している全nodeの広告windowを下げる
                ssgw_current_packet_list= []
                #print("SSGW({})に平均通信量の{}倍以上のnode({})あり:".format(ssgw.id,Threshold,node.id),node.send_packet_size)
                for minssgw in SSGW_list:#一度リストにパケットサイズを格納して、そこから最も小さいssgwを探す
                   ssgw_current_packet_list.append(minssgw.current_packet_size)
                for sendssgw in SSGW_list:

                    if sendssgw.current_packet_size == min(ssgw_current_packet_list):

                        if sendssgw.id==ssgw.id:#元と送信先のSSGWが同じならば変更しない
                            pass
                        else:
                            if control_flag==False:
                                ssgw.mynodes.remove(node)#ここで元のSSGWからnodeの登録を消す
                                node.set_myssgw(sendssgw)#ここでnodeに接続先のnodeを登録
                                sendssgw.add_mynode(node)#ここで接続先SSGWにnodeを登録
                                #print("接続先SSGWのid:",sendssgw.id)
                        control_flag=True
                            
        if control_flag==False:
        #else: #受信バッファは閾値を越えているが、単品のnodeからの送信が爆増しているわけではない
            for node in ssgw.mynodes:
                node.control_switch=1
            #print("SSGW({})の全nodeへ広告ウィンドウ制御".format(ssgw.id))
                #pass
                #print("接続されている全nodeの送信量を抑える")


ssgw_number=2

with open("tusin1-packet.txt","a")as f:#aは追記、wは上書
    print("SSGWの数は:",ssgw_number,file=f)
print("SSGWの数は:",ssgw_number)
send_packet_size_kikaku1=500 #通信規格1-3を設定しておく
send_packet_size_kikaku2=300
send_packet_size_kikaku3=100
increase=2 #バーストモードの時、nodeが何倍の送信量になるか
timerange=4 #何秒間送信するか、バースト前と後で時間は同じにしている

buffer_control_list=[] #何割で制御を開始するかを決める閾値％を入れるリスト
for plus in range(50,105,5):#50~100までで5刻みの値をlistに入れる
    buffer_control_list.append(plus)

for buffer_control in buffer_control_list: #ここでバッファの回し
    iot_packet_list15=[]#SSGWの受信バッファ%ごとのIoT総パケット数の値を入れるThreshold=15
    iot_packet_list20=[]#IoTの総パケット数の値を入れるThreshold=20    
    iot_packet_list25=[]  
    print("%:",buffer_control)

    for pattern in range(1):#ここで乱数のパターンの数を決めることができる 
        send_list=[]#ここにnodeの接続先SSGWのidを入れていく
        random.seed(pattern)
        print("seed:",pattern)


        for i in range(30):
            x= random.randint(0, ssgw_number-1)#ここで送信先のSSGWの番号を指定できる(0,4)ならばSSGWの数が5個の場合である
            send_list.append(x) 
        

        for Threshold in range(15,30,5):#ここで何倍で特定ノードを経路変更するか(÷10されている)
            #if Threshold==20:
            x_list=[]

            y_list=[] 

            IoTGW_list=[]
            SSGW_list=[]
            Node_list=[]

            class IoTGW():
                def __init__(self,id):
                    self.id = id  #識別id
                    self.name = "iotgw_"+str(id) #名前をつける
                    self.current_packet_size = 0 #1s間に受信しているパケット総数
                    self.storage_packet_size = 0 #ストレージ
                    self.trash_packet_size = 0 #廃棄したパケットの総数
                    self.max_packet_size = 10000 #受信ウィンドウサイズと同義、一度に受信できるパケットの上限

                def ReceivePacket(self, packet):
                    if self.max_packet_size < self.current_packet_size + packet: #もし受信バッファより大きかった場合、超えた分をtrashに捨てる
                        over_size = self.current_packet_size + packet - self. max_packet_size
                        self.trash_packet_size += over_size #溢れた分を加算

                    else :
                        self.current_packet_size += packet
                        self.storage_packet_size += packet
            
            class SSGW():
                def __init__(self,id):
                    self.id = id  #識別id         
                    self.name = "ssgw_"+str(id) #名前をつける  
                    self.current_packet_size = 0 #1s間に受信しているパケット総数
                    self.storage_packet_size = 0 #ストレージ
                    self.trash_packet_size = 0 #廃棄したパケットの総数
                    self.max_packet_size = 5000 #受信ウィンドウサイズと同義、一度に受信できるパケットの上限
                    self.send_packet_size = 5000 #SSGWから1sで送るパケット数
                    self.current_packet_size_for_control= 0
                    self.mynodes = [] #ここに自分に送信しているnodeのオブジェクトを登録する

                def ReceivePacket(self, packet):
                    if self.max_packet_size < self.current_packet_size + packet: #もし受信バッファより大きかった場合、超えた分をtrashに捨てる
                        over_size = self.current_packet_size + packet - self. max_packet_size
                        self.trash_packet_size += over_size #溢れた分を加算

                    else :
                        self.current_packet_size += packet
                
                def SendPacket(self) :
                    for IoTGW in IoTGW_list:
                        if self.send_packet_size < self.current_packet_size:
                            IoTGW.ReceivePacket(self.send_packet_size)      
                        else :
                            IoTGW.ReceivePacket(self.current_packet_size)

                def add_mynode(self,node):   
                    self.mynodes.append(node)

            class Node():
                #SSGW_listからID=0を見つける
                #そのSSGWを指定してReceivePacketを使う
                def __init__(self,id):
                    self.id = id
                    self.name = "node_"+str(id) #名前をつける
                    self.send_packet_size=0
                    self.control_switch=0
            
                def set_myssgw(self,ssgw) :#ここで送信先のSSGWのオブジェクトを代入
                    self.myssgw = ssgw   

                def SendPacket(self,state):
                    if self.control_switch ==0:#広告window下げるか、どうか0はしない、1で広告window下げる
                        if state == 0:#通常状態
                            if self.id < 10: #idによって送信パケット数を割り振る
                                self.send_packet_size = send_packet_size_kikaku1
                            elif self.id >=10 and self.id <20:
                                self.send_packet_size = send_packet_size_kikaku2
                            else:
                                self.send_packet_size = send_packet_size_kikaku3
                        elif state==1: #異常
                            if self.id < 10: #idによって送信パケット数を割り振る
                                self.send_packet_size = send_packet_size_kikaku1*increase
                            elif self.id >=10 and self.id <20:
                                self.send_packet_size = send_packet_size_kikaku2*increase
                            else:
                                self.send_packet_size = send_packet_size_kikaku3*increase   
                    elif self.control_switch ==1:
                        if state == 0:#通常状態
                            if self.id < 10: #idによって送信パケット数を割り振る
                                self.send_packet_size = send_packet_size_kikaku1*0.8
                            elif self.id >=10 and self.id <20:
                                self.send_packet_size = send_packet_size_kikaku2*0.8
                            else:
                                self.send_packet_size = send_packet_size_kikaku3*0.8
                        elif state==1: #異常
                            if self.id < 10: #idによって送信パケット数を割り振る
                                self.send_packet_size = send_packet_size_kikaku1*increase*0.8
                            elif self.id >=10 and self.id <20:
                                self.send_packet_size = send_packet_size_kikaku2*increase*0.8
                            else:
                                self.send_packet_size = send_packet_size_kikaku3*increase*0.8

                    self.myssgw.ReceivePacket(self.send_packet_size) #myssgeにSSGW(0)とかのオブジェクト自体を持ってこれているので、そのままそのオブジェの関数を使用することができる

            #SSGWとnodeの数を決め、インスタンスをlist追加

            IoTGW_list.append(IoTGW(0))

            for i in range(ssgw_number):
                ssgw = SSGW(i)
                SSGW_list.append(ssgw)  #インスタンスを作成、それをlistに追加


            for i in range(30):
                node = Node(i)
                for ssgw in SSGW_list:            
                    if ssgw.id == send_list[i]:
                            node.set_myssgw(ssgw)#ここで相互に接続先のオブジェクトを登録することで、情報（数値）のやりとりを円滑にしている
                            ssgw.add_mynode(node)
                Node_list.append(node)

            #パケット送信制御部分

            for time in range(timerange): #何秒間やるか

                #print(time,"秒目")

                for ssgw in SSGW_list:
                    node_control(ssgw) #ここでssgwに関数をnode_control関数を用いて制御をする

                for ssgw in SSGW_list:
                    ssgw.current_packet_size=0 #ここで受信バッファを0にする（毎回処理するので）

                for node in Node_list: #nodeは30個ある
                    node.SendPacket(0)#0が入っている場合は通常状態、1ならばバースト
                    #print("接続先SSGW({})".format(node.myssgw.id))
                for ssgw in SSGW_list:
                    ssgw.SendPacket() #IoTGW(0)に送信
                
                for iotgw in IoTGW_list:
                    iotgw.current_packet_size=0
                #if time == 0:
                    #show_network()



            for time_burst in range(timerange): #バーストを何秒間やるか

                #print(time_burst+timerange,"秒目(バーストモード)")

                for ssgw in SSGW_list:
                    node_control(ssgw)

                for ssgw in SSGW_list:
                    ssgw.current_packet_size=0 #ここで受信バッファを0にする（毎回処理するので）


                for node in Node_list: #nodeは30個ある、idは0-29
                    if node.id ==1:#バーストするnodeを指定
                        node.SendPacket(1)
                        #print("接続先SSGW({})".format(node.myssgw.id))
                    else:
                        node.SendPacket(0)
                

                for ssgw in SSGW_list:
                    ssgw.SendPacket() #IoTGW(0)に送信
                    
                
                for iotgw in IoTGW_list:
                    iotgw.current_packet_size=0
            
                #show_network()

            x_list.append(buffer_control)
            for IoTGW in IoTGW_list:
                if IoTGW.id == 0:
                    y_list.append(IoTGW.storage_packet_size)
            show_network()
        if Threshold == 15:#1.5倍で経路変更
            y2_list=[]
            for y in y_list:
                y2_list.append(y-35)
            ax_buffer.plot(x_list,y2_list,color="Green", marker="o")
        elif Threshold ==20:#2倍で経路変更
            y2_list=[]
            for y in y_list:
                y2_list.append(y-70)
            ax_buffer.plot(x_list,y2_list,color="Blue", marker="o")
        elif Threshold ==25:
            ax_buffer.plot(x_list,y_list,color="Red", marker="o")
        #elif Threshold ==30:#意味なかった（25と同じ）
           #plt.plot(x_list,y_list,color="Pink")
    ax_buffer.legend( ("1.5倍", "2倍","2.5倍"), loc=2)

    #plt.show()   
    def average(xs):
        return sum(xs) / len(xs)

    with open("tusin1-packet.txt","a")as f:#aは追記、wは上書
        
        print("buff(%):",buffer_control,file=f)
        print("Thr=15",average(iot_packet_list15),file=f)
        print("Thr=20",average(iot_packet_list20),file=f)
        print("Thr=25",average(iot_packet_list25),file=f)


    #print("f_index_list15:",f_index_list15,"\n",average(f_index_list15))

    #print("f_index_list20:",f_index_list20,"\n",average(f_index_list20))

    #print("f_index_list25:",f_index_list25,"\n",average(f_index_list25))


