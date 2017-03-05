import time
from collections import defaultdict
import operator
# Below are two codes to read the file, we will be going with the non list comprehension version
def readtext(filename):
    with open(filename) as f:
        txtlines = [[str(s) for s in line.rstrip("\n").split(" ")] for line in f]
    return txtlines

def readtext2(filename):
    data = open(filename, "r")
    txtlines = list()
    for line in data:
        line = line.rstrip("\n")
        lst = [str(s) for s in line.split(" ")]
        # print(lst)
        txtlines.append(lst)
    return txtlines

def getdictoffreqwords(listoflines):
    fullwordlist = defaultdict(int)
    for line in listoflines:
        for word in line:
            fullwordlist[word] +=1
    return fullwordlist

def getreducedwordlist(worddict,minsup):
    return {k:v for k,v in worddict.items() if v >= minsup}

def getpatternsgivenline(line):
    linelen = len(line)
    # print(linelen)
    patterns = set()
    for i in range(1,linelen):
        for j in range(0,linelen-i+1):
            patterns.add(" ".join(line[j:j+i]))
    # print(patterns)
    # print(len(patterns))
    return(patterns)


def getpatternsforeachline(alltext):
    listoflinesets = []
    i = 0
    for line in alltext:
        listoflinesets.append(getpatternsgivenline(line))
        print(i)
        i += 1
    return listoflinesets

def getphrasefreq(listoflinesets):
    # print(listoflinesets)
    phrasedict = defaultdict(int)
    for lineset in listoflinesets:
        # print(lineset)
        if lineset is not None:
            # print("inside")
            for element in lineset:
                phrasedict[element] +=1
    return phrasedict


def filterbyfrequency(phrasefrequencydict,minsup):
    return {k:v for k,v in phrasefrequencydict.items() if v >= minsup}


def filterbywordlength(phrasefrequencydict,minlength):
    return {k: v for k, v in phrasefrequencydict.items() if len(k.split(" ")) >= minlength}


def printreturnfile(inputdict,outputfile):
    # inputlist.sort(key=lambda x: -x[1])
    inputlist = [(k,v) for k,v in inputdict.items()]
    print(inputlist)
    inputlist.sort(key=operator.itemgetter(1),reverse=True)
    with open(outputfile, 'w') as the_file:
        for element in inputlist:
            the_file.write(str(element[1]) + ":" + element[0].replace(" ",";") + '\n')


if __name__ == "__main__":
    #testing time for reading
    # times = time.time()
    txtlines = readtext2("rawdata/yelp_reviews.txt")
    # print("timetaken by longer code = ",time.time() - times)
    # time taken by the list comprehension is 0.18secs
    # times = time.time()
    # txtlines = readtext("rawdata/yelp_reviews.txt")
    # print("timetaken by shorter code = ", time.time() - times)
    # time taken by normal loop is 0.15secs
    # going with normal code
    # print(txtlines)

    worddict = getdictoffreqwords(txtlines)
    # print("worddict is ",worddict )
    # print("len of worddict is ", len(worddict))


    worddict = getreducedwordlist(worddict,100)
    # print("reduced worddict is ", worddict)
    # print("len of reduced worddict is ", len(worddict))

    # Test whether single line comprehension works
    # getpatternsgivenline(txtlines[0])
    # Get list of sets for each line
    times = time.time()
    listoflinesets = getpatternsforeachline(txtlines)
    print("Got list of line phrases in ", time.time() - times, "seconds")
    # Get list of all phrases
    times = time.time()
    phrasesfreq = getphrasefreq(listoflinesets)
    frequentphrases = filterbyfrequency(phrasesfreq,100)
    # print(frequentphrases)
    print(len(frequentphrases))

    frequentphrases = filterbywordlength(frequentphrases, 2)
    # print(frequentphrases)
    print(len(frequentphrases))
    print("Got Worddict in ", time.time() - times, "seconds")

    printreturnfile(frequentphrases, "output/yelpcontiguouspatterns.txt")
