import matplotlib.pyplot as plt
import numpy as np

def graphmaker(data):
    # 記録された日数
    len_d = len(data)
    

    # 日のデータと時間のデータのリストを用意
    d_data = []
    h_data = []

    # リスト要素をintに変換
    [d_data.append(int(data[d][0])) for d in range(len_d)]
    [h_data.append(int(data[d][1])) for d in range(len_d)]

    # 31日分のデータを用意
    d_data_ = []
    d_data_int = []
    h_data_ = [0]*31

    # 31日で日にちを埋める
    for m in range(0,31):
        d_data_.append(str(m))
        d_data_int.append(m)
        for d in range(len_d):
            if(data[d][0][-2:] == str(m).zfill(2)):
                h_data_[m-1] = h_data[d]/60
    

    
    print(len(d_data_int),"\n-------\n",len(h_data_),"\n-------\n",d_data_)

    plt.plot()
    plt.title(data[0][0][0:4]+ "_" + data[0][0][4:6])
    plt.xlabel("day")
    plt.xlim(0,31)
    plt.ylim(0,24)
    plt.ylabel("hours")
    plt.bar(d_data_int, h_data_)

    plt.show()
    
    return 1

if __name__ == "__main__":
    data = [["20210405","400"],["20210407","500"],["20210428","900"],["20210409","460"]]

    graph = graphmaker(data)