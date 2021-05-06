import numpy as np
import matplotlib.pyplot as plt
from split_txt import split_txt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'AppleGothic'#漢字を出せるようにする、数という漢字は対応していない
plt.rcParams['xtick.direction'] = 'in'  # x軸の目盛線を内向きへ
plt.rcParams['ytick.direction'] = 'in'  # y軸の目盛線を内向きへ

#キーワード zorder を使用して、図の描画順序を設定できます。plot と scatter に異なる順序を割り当て、順序を逆にして異なる描画順序の動作を示します。 
#↑可能

#一言で言うと、 if __name__=='__main__': はこのPythonファイルが「python ファイル名.py というふうに実行されているかどうか」を判定するif文です。



def generate_graph(num):
    data = np.load("splited_text"+str(num)+".npy")
    fig, ax = plt.subplots()
    t = data[:,0]
    y1 = data[:,1]
    y2 = data[:,2]
    y3 = data[:,3]

    c1,c2,c3 = "blue","green","red"
    l1,l2,l3 = "Threshold:1.5倍","Threshold:2.0倍","Threshold:2.5倍" # 各ラベル

    #plt.rcParams["font.size"] = 14#文字の大きさを全て大きくする
    plt.ylim([0.85,1]) #y軸範囲
    ax.set_xlabel('受信バッファ使用率[%]')  # x軸ラベル
    ax.set_ylabel('Firness index')  # y軸ラベル
    #ax.set_ylabel('IoTGW到達通信量')  # y軸ラベル    
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.edgecolor'] = 'black' 
    plt.rcParams["font.size"] = 14#文字の大きさを全て大きくする

    #ax.set_title(r"SSGWの受信バッファ使用率の公平性(SSGW:{} Pt:1)".format(2)) # グラフタイトル
    #ax.set_aspect('equal') # スケールを揃える
    #ax.grid()            # 罫線
    ax.set_xlim([50, 100]) # x方向の描画範囲を指定
    #ax.set_ylim([0, 1])    # y方向の描画範囲を指定
    #ax.scatter(t,y1,color=c1,label=l1,s=13,marker="^")
    ax.plot(t, y1, color=c1, linewidth = 3.0,label=l1, linestyle = "dotted",markersize=10,marker="^",clip_on=False,zorder=3)
    #ax.scatter(t,y2,color=c2,s=13,marker=",")
    ax.plot(t, y2, color=c2, linewidth = 3.0,label=l2, linestyle = "dashed",markersize=14,marker="*",clip_on=False,zorder=3)
    #ax.scatter(t,y3,color=c3,s=13)    
    ax.plot(t, y3, color=c3, linewidth = 3.0,label=l3, linestyle = "dashdot",markersize=10,marker="o",clip_on=False,zorder=3)
    ax.legend(loc=0)    # 凡例
    fig.tight_layout()  # レイアウトの設定
    plt.savefig("スライドSSGWtusin1" + str(num) + ".pdf")# 画像の保存
    #plt.show()
if __name__ == "__main__":
    for i in range(2,6):
        split_txt(i)

    for i in range(1,6):
        generate_graph(i)