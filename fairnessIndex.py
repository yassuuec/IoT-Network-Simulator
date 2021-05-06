#端末間の公平性を測る指標として，Jain の Fairness Index を用いる 
#0.0 から 1.0 で表し，1.0 に近い程，公平な値であることを示す.


#sample_list=[64,78,38]
def FairnessFunc(data_list):
    x = sum(data_list)
    under = 0
    y= 0
    for j in data_list:
        under=j**2
        y += under 
    
    n = len(data_list)
    fairness_index= x**2/(n*y)

    return fairness_index
    #print("Fairness Index:" ,fairnessIndex)
    #print("x,y,n",x**2,y,n)
    
#FairnessFunc(sample_list)


