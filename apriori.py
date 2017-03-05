import time
import random, copy
from collections import defaultdict
import itertools
import operator


def readtransactions(filename):
    data = open(filename, "r")
    trns = list()
    for line in data:
        line = line[:-1]
        lst = {str(s) for s in line.split(";")}
        # print(lst)
        trns.append(lst)
    return trns

def buildskus(trns):
    skus = defaultdict(int)
    for transaction in trns:
        for element in transaction:
            skus[element] += 1
    return (skus,sum(skus.values()))

def getlevel0frequent(skus,minsup):
    l0 = defaultdict(int)
    for sku in skus:
        if skus[sku]>minsup:
            l0[sku] = skus[sku]
    # print("length is",len(l0))
    return(l0)

def printreturnfile(inputdict,outputfile):
    g = sorted(inputdict, key=inputdict.get, reverse=True)
    with open(outputfile, 'w+') as the_file:
        for element in g:
            the_file.write(str(inputdict[element])+":"+element+'\n')
    g = None

def getlevelwisefrequent(skus,minsup,trns):
    level = 2
    answerlist = [(k,v) for k,v in skus.items()]
    thislevel = dict()
    lastlevel = {frozenset({k}):v for k,v in skus.items()}
    # i = 0
    while(len(lastlevel)!=0):
        thislevel = dict()
        for skucombo in itertools.combinations(lastlevel.keys(), level):
            # print("insideskucombo is",skucombo)
            # print("insideset().union(skucombo) is", set().union(skucombo))
            # print("insidelen(set().union(skucombo)) is", len(set().union(skucombo)))
            setunion = set().union(*skucombo)
            if len(setunion) == level:
                # print(i)
                newitem = setunion
                newitem = frozenset(newitem)
                thislevel[newitem] = 0
                for transaction in trns:
                    if newitem.issubset(transaction):
                        thislevel[newitem] +=1
                # i+=1

        thislevel = {k: v for k, v in thislevel.items() if v > minsup}
        # print("thislevelis",str(thislevel))
        print("level:",level,"size of answer here is", len(thislevel))
        if len(thislevel) != 0: answerlist += [(k,v) for k,v in thislevel.items()]
        lastlevel = thislevel
        level +=1
    return answerlist



def appendreturnfile(inputlist,outputfile):
    # inputlist.sort(key=lambda x: -x[1])
    inputlist.sort(key=operator.itemgetter(1),reverse=True)
    with open(outputfile, 'w') as the_file:
        for element in inputlist:
            # print(element)
            if(type(element[0]) != frozenset):the_file.write(str(element[1])+":"+str(element[0])+'\n')
            else: the_file.write(str(element[1])+":"+";".join(map(str,[x for x in element[0]]))+'\n')



if __name__ == "__main__":
    timenow = time.time()
    trns = readtransactions("rawdata/categories.txt")
    (skus,total_skus) = buildskus(trns)
    returndict = getlevel0frequent(skus, 771)
    printreturnfile(returndict,"output/myfile.txt")
    answerlist = getlevelwisefrequent(returndict, 771,trns)
    appendreturnfile(answerlist, "output/myfile2.txt")
    timetaken=time.time() - timenow
    print("Time taken for ",len(trns)," transactions with ",total_skus," skus is ",timetaken ,"seconds")

