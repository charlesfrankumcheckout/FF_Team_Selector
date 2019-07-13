from collections import defaultdict
import numpy as np

# Chooses the optimal items based on the items' weight and value. There are 2
# Constratints; W represents the total allowed maximum weight and capacity of
# the items and C represents the exact number of items we want returned
# i.e. The optimal n items from the item list

weight = [3,2,1,2,1,3,2]
value = [1,3,2,2,1,2,1]
capacity = 9
maxitems = 4
nbitems = len(weight)

def xknapsack(capacity, nbitems, maxitems):
    #ks_matrix = np.zeros((capacity + 1, nbitems, maxitems + 1))

    ks_matrix = [[[[0,[]] for k in range(maxitems + 1)] for j in range(nbitems)] for i in range(capacity + 1)] 

    for j in range(-1, nbitems - 1):

        for i in range(1, capacity + 1):
            
            for k in range(1, maxitems + 1):
                
                if weight[j] > i: # If adding this object would exceed the current weight limit (i), append the last score to the matrix
                    ks_matrix[i][j+1][k] = ks_matrix[i][j][k]
                    
                else:
                    
                    if j < k: # If the item number is smaller than the current item limit (k), take the maximum value between the value of
                              # the last matrix position and the value of adding this item instead
                        temp = {'1': ks_matrix[i][j][k][0], '2':ks_matrix[i-weight[j]][j][k][0] + value[j]}
                        ks_matrix[i][j+1][k][0] =  max(temp.items())[1]
                        
                        if max(temp.items())[0] == '1':
                            ks_matrix[i][j+1][k][1] = ks_matrix[i][j][k][1]
                        else:
                            ks_matrix[i][j+1][k][1] = ks_matrix[i-weight[j]][j][k][1] + [j]
                            
                            
                    else: # If the item number is exceeded then calculate the values from the item limit matrix before (k-1) where the weight
                          # limit is not exceeded
                        prev = {}
                        
                        for z in range(j+1):
                            prev[z] = {}
                            prev[z]['value'] = ks_matrix[i-weight[j]][z][k-1][0]
                            prev[z]['items'] = ks_matrix[i-weight[j]][z][k-1][1]

                          # Take the max value between the last matrix position and the value of using the old item and new value instead
                        temp = {'1':ks_matrix[i][j][k][0],'2':max([v['value'] for k,v in prev.items()]) + value[j]}
                        ks_matrix[i][j+1][k][0] = max(temp.items())[1]
                        
                        if max(temp.items())[0] == '1':
                            ks_matrix[i][j+1][k][1] = ks_matrix[i][j][k][1]
                        else:       
                            ks_matrix[i][j+1][k][1] = prev[max(prev, key=lambda k: prev[k]['value'])]['items'] + [j]
                            
    return ks_matrix[capacity][nbitems-1][maxitems][0], [x+1 for x in ks_matrix[capacity][nbitems-1][maxitems][1]]

results = xknapsack(capacity, nbitems, maxitems)
