#Import all Modules
import sys
import math
import matplotlib.pyplot as plt

#Take all arguments
dataFile=sys.argv[1] #Input Data file
k=int(sys.argv[2])   #No. of clusters
loops=int(sys.argv[3])  # no. of iterations to converge
initialPoints=sys.argv[4]  #Initial Points

#Global Variables
myDict={}
category=4
isPrint=False
main=0
func=1
sepal=0
petal=2
catList=[]
myNewDict={}



#Define all functions
def getLineList(lines):
    temp=[]
    lineList=[]
    for line in lines:
        tempLine=[]
        temp=[]
        tempLine=line.split(",")
        for i in range(len(tempLine)-1):
            attribute=tempLine[i]
            tempAttribute=float(attribute)                
            temp.append(tempAttribute)
        temp.append(tempLine[len(tempLine)-1])
        lineList.append(temp)
    return lineList

def euclidDistance(list1,list2):
    d=0
    for i in range(len(list1)-1):
        d+=(list1[i]-list2[i])**2
    d=math.sqrt(d)
    #return d,list2[category]
    return d

def getMin(myDict):
    smallest=50000.00
    smallestKey=''
    for key in myDict:
        if myDict[key]<smallest:
            smallest=myDict[key]
            smallestKey=key
    resetPrint()
    if isPrint==True:
        print "smallest:%f , key:%s "%(smallest,smallestKey)
    return smallest,smallestKey


def getCategories(inList):       
    for i in range(len(inList)):
        myDict[i]=[]
    return myDict
    

def setPrint():
    global isPrint
    isPrint=True

def resetPrint():
    global isPrint
    isPrint=False

def getCentroids(myDict):
    masterList=[]
    for key in myDict:
        x=[]
        for eachList in myDict[key]:
            if x==[]:
                for i in range(len(eachList)-1):
                    x.append(eachList[i])
            else:
                for i in range(len(eachList)-1):
                    x[i]+=eachList[i]
        for i in range(len(x)):
            x[i]=x[i]/len(myDict[key])
        x.append(key)
        masterList.append(x)
    resetPrint()
    if isPrint==True:
        print
        print "Printing New Centroids:"
        print masterList
    return masterList

def resetDict(myDict,typeDS=0):
    for key in myDict:
        if typeDS==main:
            myDict[key]=[]
        else:
            myDict[key]=0
    return myDict

def getCategory(inDict):
    count=-1
    cat=""
    for key in inDict:
        if count<inDict[key]:
            count=inDict[key]
            cat=key
    #print cat
    return cat

def getWrongCount(inDict,cat):
    count=0
    #print inDict
    for key in inDict:
        if key !=cat:
            count+=inDict[key]
    #print count
    return count

def getCategoryAndWrongCount(inDict):
    count=0
    cat=getCategory(inDict)
    count=getWrongCount(inDict,cat)
    return cat,count

def getWrongClusterCount(myDict):
    global func
    count=0
    tempVal=0
    tempDict={}
 #   myNewDict={}
    for key in myDict:
        tempDict=resetDict(tempDict,func)
        for eachList in myDict[key]:
##            if key != eachList[category]:                
##                count+=1
##    return count
            if eachList[category] not in tempDict:
                tempDict[eachList[category]]=1
            else:
                tempDict[eachList[category]]+=1
        #print tempDict
        cat,tempVal=getCategoryAndWrongCount(tempDict)
        myNewDict[cat]=key
        #print myNewDict[cat]
        count+=tempVal
    return count,myNewDict
            
def getCat(inDict):
    tempList=[]
    for key in inDict:
        tempList.append(key)
    return tempList
        

def scatterPlot(inDict,color,feature) :
    L=[]
    W=[]
    count=0
    maxL=maxW=0
    for key in catList:
        L=[]
        W=[]
        for eachList in myDict[myNewDict[key]]:
            L.append(eachList[0+feature])
            W.append(eachList[1+feature])
        if maxL<max(L):
            maxL=max(L)
        if maxW<max(W):
            maxW=max(W)
        #print "maxL:%f maxW:%f"%(maxL,maxW)
        if count==0:
            plt.scatter (L,W,color="r")
            
        elif count==1:
            plt.scatter(L,W,color="g")
            
        else:
            plt.scatter(L,W,color="b")
            
        count+=1
    plt.text(maxL+0.35,maxW-1.25,"Red : %s"%catList[0],bbox=dict(boxstyle="round",color="pink"))
    plt.text(maxL+0.35,maxW-1.5,"Green : %s"%catList[1],bbox=dict(boxstyle="round",color="pink"))
    plt.text(maxL+0.35,maxW-1.75,"Blue : %s"%catList[2],bbox=dict(boxstyle="round",color="pink"))
    
    if feature==sepal:
        plt.title("Sepal Length vs. Sepal Width")
    else:
        plt.title("Petal Length vs. Petal Width")
    

if __name__=="__main__":
    lineListIP=[]                       
    myFileIP=open(initialPoints,"r+")
    lines=myFileIP.read()
    lines=lines.split()
    lineListCentroids=getLineList(lines)   #Get the initial centroids
    if  len(lineListCentroids)!=k:         #Check if the K and no. of initial centoids are same    
        print "Equality between no. of Initial points and input K value"
        sys.exit()

    lines=[]
    myFile=open(dataFile,"r+")              
    lines=myFile.read()
    lines=lines.split()
    lineList=getLineList(lines)				#Get the list of data points
    
    
    
    resetPrint()
    if isPrint==True:
        print lineListCentroids

    #myDict=getCategories(lineList)
    myDict=getCategories(lineListCentroids)   #Get the class of the flowers from the data set
    resetPrint()
    if isPrint==True:
        print myDict

    count=0
    while (count<loops):
        tempDict={}
        myDict=resetDict(myDict)
        for i in range(len(lineList)):            
            for j in range(len(lineListCentroids)):               
               d=euclidDistance(lineList[i],lineListCentroids[j])  #Calculate the Euclidean distance of each data point from the centroids
               tempDict[j]=d
            resetPrint()
            if isPrint==True:
                print tempDict
            minD,cat=getMin(tempDict)             #Calculate the min distance and assign the data point ro the cluster
            myDict[cat].append(lineList[i])
        #print myDict
        lineListCentroids=getCentroids(myDict)
        count+=1    
    
    wrongCluster,myNewDict=getWrongClusterCount(myDict)  #Get the count of wrong clusters
    catList=getCat(myNewDict)
    catList.sort()
    
    for key in catList:      #Print the clusters and their points
        #key=myNewDict[i]
        print "Cluster %s"%(key)
        for eachList in myDict[myNewDict[key]]:
            print eachList
        print 
    
    print "Number of points assigned to wrong cluster:"   #Print the no. of points assigned to wrong cluster
    print wrongCluster

##    print
##    print catList
##    print
##    print myDict
    plt.subplot(2,1,1)
    scatterPlot(myDict,sepal,sepal)
    plt.subplot(2,1,2)
    scatterPlot(myDict,petal,petal)
    plt.show()
    
    myFile.close()
    myFileIP.close()
