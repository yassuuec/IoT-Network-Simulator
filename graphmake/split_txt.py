#謎にtext[0]に前の100が入るから[1:]で消してる
import numpy as np

def split_txt(num):
    text = np.empty(4)
    flag = False
    with open("./tusin1.txt", "r") as rf:
        while True:
            data = rf.readline()
            if data == "": #readlineで上から読み込んで何も読み込めなくなったら終了
                break
            if data == "SSGWの数は: "+str(num)+"\n":
                flag = True
            elif data == "SSGWの数は: "+str(num+1)+"\n":
                break
            elif flag == True
                data = np.array(int(data.split(" ")[1].replace("\n","")))
                for i in range(3):
                    data = np.append(data,float(rf.readline().split(" ")[1].replace("\n","")))
                text = np.concatenate([text,data],0)#concatenateでデータを重ねていく
    text = text.reshape(-1,4) #-1はオプションで、無限に区切ってくれる(何個になるか,一個あたりなんこか)
    np.save("splited_text"+str(num),text[1:])
if __name__ == "__main__":
    for i in range(2,6):
        split_txt(i)


#   while 条件式:
#    条件式が真の時に実行する文1
#    条件式が真の時に実行する文2
#    条件式が真の時に実行する文3