

import math
import scipy.cluster.hierarchy as sc
import matplotlib.pyplot as py
import matplotlib
from pylab import savefig
import csv

'''
The program is about implementing agglomerative clustering with the total number of clusters to be fprmed is tgree
central linkage is used to find the two closet cluster and the distance is found using EUclidiean distance.
The program being a part of an assignment I cannot share the data,
how does the input look like,

There were 13 coloumns. 1st coloumn is unique trasaction ID and is not used as features the remaining 12 coloumns 
is used as features.
Although the program works for 12 input feature it can work for any number of input feature with minor modification
'''


def original_weights(inputs):
    '''

    :param inputs: inputs- It is the given input in the formof list os list, inputs are basically attributes
    :return: Distance- It is a Distance matrix,
    '''


    distance=[]

    '''
    The for loop calculates the euclidean distance betweem each id or each customer
    '''
    for item_x in range(len(inputs)):
        distance_x=[]
        for item_y in range(len(inputs)):
            squaresum=0
            for item in range(1,13):
                squaresum=squaresum+math.pow((inputs[item_x][item]-inputs[item_y][item]),2)

            euclidean_dist= math.sqrt(squaresum)
            distance_x.append(euclidean_dist)
        distance.append(distance_x)
    return distance


def computeNewWeights(inputs,item_x,item_y):

        '''

        :param inputs: The original matrix on which the calculation needs to be performed
        :param item_x: one of the point between whom the lowest distance needs to be found
        :param item_y: another point of the lowest i=distance
        :return: inputs- the updated matrix

        This function basically perform the central linkage process
        '''
        #for loop for finding the new centroid between two points
        for items in range(1,13):
            inputs[item_x][items]=(inputs[item_x][items]+inputs[item_y][items])/2

        inputs.pop(item_y)
        return inputs




def calculateDistance(inputs,dictForgroup,number_of_cluster):

    '''

    :param inputs: the original matrix
    :param dictForgroup: It keep track of which cluster is been merged with which existing cluster/member and gives final three cluster

    :param number_of_cluster: Keeps track of the number of cluster
    :return: inputs, number_of_cluster, dictForgroup,dict
    '''

    distances=[]
    dict={}

    min_x=0
    min_y=0
    min_euclideian=math.inf


    for item_x in range(len(inputs)):
        '''
        For loop calculates the euclidiean distance and gives the two points having lowest euclidiean distance
        '''
        distance_x=[]
        for item_y in range(item_x+1,len(inputs)):
            squaresum=0
            '''
            actual calculation of the euclidiean distance
            '''
            for item in range(1,13):
                squaresum=squaresum+math.pow((inputs[item_x][item]-inputs[item_y][item]),2)

            euclidean_dist= math.sqrt(squaresum)
            '''
            returning the point with minimum distance
            '''
            if euclidean_dist<min_euclideian:
                min_x=item_x
                min_y=item_y

                min_euclideian=euclidean_dist

            distance_x.append([inputs[item_y][0],euclidean_dist])
        distances.append(distance_x)

        dict[inputs[item_x][0]]=distance_x



    '''
    The code below merges the two custers and calls the function for finding new centroids
    '''
    values=dictForgroup.get(inputs[min_x][0])
    values_y=dictForgroup.get(inputs[min_y][0])
    for cluster in range(len(values_y)):
        values.append(values_y[cluster])
    print("Length of the previous cluster appended",len(values_y))
    dictForgroup[inputs[min_x][0]]=values
    dictForgroup.pop(inputs[min_y][0])


    inputs = computeNewWeights(inputs, min_x, min_y)
    number_of_cluster=number_of_cluster-1
    return inputs, number_of_cluster, dictForgroup,dict



def doAglomeration(inputs_original,inputs,dictForgroup,number):
    '''

    :param inputs_original:
    :param inputs: The input data without any updates or weights
    :param dictForgroup: the number of cluster currently present
    :param number: the number of cluster that needs to be formed
    :return: none
    '''
    number_of_cluster=len(inputs)
    inputs_main=original_weights(inputs)


    '''
    whike loop runs untill the desire number of cluster is formed
    '''
    while number_of_cluster>number:
        inputs, number_of_cluster,dictForgroup,dict=calculateDistance(inputs, dictForgroup,number_of_cluster)


    print("clusters formed",dictForgroup)
    print('final centroids of three clusters')
    for item in range (len(inputs)):
        print("cluster number",item,"centroid values",inputs[item])
        print('length of final centroid',len(inputs[item]))
    print('The clusters are as follows')
    for keys in dictForgroup:
        print("Cluster ",keys,"number of elements",len(dictForgroup.get(keys)) )
        print("The Keys of the Clusters are",(dictForgroup.get(keys)))

    '''
    the Following code forms the dendrograms
    '''

    linkage=sc.linkage(inputs_main,method='average')
    py.figure()
    dendohgram=sc.dendrogram(linkage,p=30,truncate_mode='lastp',count_sort=True)
    py.show()






def main():
    flag=False
    inputs=[]
    input_orignal=[]
    with open("your file name") as myfile:
        for lines in myfile:
            if flag==False:
                flag=True
            else:
                lines=lines.strip().split(",")
                lines=list(map(int,lines))
                inputs.append(lines)

    print("input",inputs)

    dictForgroup={}
    for item in range(len(inputs)):
        dictForgroup[item+1]=[inputs[item][0]]


    doAglomeration(input_orignal,inputs,dictForgroup,3)




if __name__ == '__main__':
    main()