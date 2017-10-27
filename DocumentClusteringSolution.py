# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 20:00:23 2017

@author: Jyoti
"""
import urllib
import re
import math
from bs4 import BeautifulSoup

def readWebPageContent(url):
    """Read the webpage contents and strip the html tags"""
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "lxml" )
    # remove all script and style elements
    for script in soup(["script", "style"]):
            script.extract()    
    # now retrieve text
    text = soup.get_text()
    return text.lower()

def convertContentToWordList(content):
    #strip the punctuations and split it into a list
    return re.compile(r'\W+', re.UNICODE).split(content)
   
def stripCommonWords(wordsList):
    """Remove the common stop words from words list"""
    commonWords = ["the","for","of","if","to","are","a","is","as","at","any","in","on","can","an","or","not","that","than","which",'very','well','was','that','then','and','be','also','such','from','into']
    return [w for w in wordsList if w not in commonWords]
        
def calcTermFrequency(termList):
        """Calculate the term frequency in the given word list"""
        termFrequency = [termList.count(p) for p in termList]
        return dict(zip(termList,termFrequency))
        
def calcCosineSimNum(dict1,dict2):
        sum = 0
        for key in dict1:
            if key in dict2:
                sum = sum + dict1[key]*dict2[key]
        return sum

def summationOfCount(inputDict):
        inputStrSum = 0
        for key in inputDict:
            inputStrSum = inputStrSum + (inputDict[key])*(inputDict[key])
        return inputStrSum         

def calculateCosineSimilarity(url1,url2):
    """Calculats Cosine Similarity between given two webpages"""
    webContent1 = readWebPageContent(url1)
    webContent2 = readWebPageContent(url2)
    
    wordList1 = convertContentToWordList(webContent1)
    #remove common words
    wordList1=stripCommonWords(wordList1)
    
    wordList2 = convertContentToWordList(webContent2)
    #remove common words
    wordList2=stripCommonWords(wordList2)
    
    termFreqDict1 = calcTermFrequency(wordList1)
    termFreqDict2 = calcTermFrequency(wordList2)
    
    cosineNumerator = calcCosineSimNum(termFreqDict1,termFreqDict2)
    
    summationStr1 = summationOfCount(termFreqDict1)
    summationStr2=  summationOfCount(termFreqDict2)
    
    cosineDenom= math.sqrt(summationStr1)*math.sqrt(summationStr2)
    cosineSimilarity = (cosineNumerator/cosineDenom)                  
    return cosineSimilarity

def readInputFile(fileName):
    """Read the URLs from input file and store them in a dict"""
    try:
        f = open(fileName,"r")
    except IOError:
        print("Error encountered, unable to find the given file : " ,fileName)
        return
    except:
        print("Error while trying to open the given file")
        return
    key=1 
    urlDict={}
    for str in f:
        urlDict[key]=str
        key=key+1   
    f.close()
    return urlDict    
    
def calcCosineSimilarityUsingInputFile():
    webPagesDict={}
    webPagesDict=readInputFile("input.txt")
    try:
        outputFile=open("output.txt","w")
    except:
        print("Error while trying to write output to file")    
        
    webPageList= list()
    outputList=list()
    cosineSimList=list()
    maxValueList=list()
    highestValueList=list()
    
    outputFile.write("Following webpages have been processed to find the cosine similarity : " + "\n")
    
    for key in webPagesDict.keys():
        outputFile.write(str(key) + " : " + webPagesDict[key])
        outputFile.write("\n" + "\n")
        webPageList.append(key)
        if(len(cosineSimList) != 0):
            outputList.append(cosineSimList)
            highestValueList.append(maxValueList)
        cosineSimList=[]
        maxValueList=[]
        for j in range(1,key+1):
            cosineSimList.append("")
            maxValueList.append(0)
        for i in range(key+1,(len(webPagesDict)+1)):  
            print("\n" + "Calculating cosine similarity for webpages {} and {}".format(webPagesDict[key],webPagesDict[i]) )  
            cosineSimilarity= calculateCosineSimilarity(webPagesDict[key],webPagesDict[i])
            print("Cosine Similarity between webpage {} and webpage {} is : {}".format(key,i,cosineSimilarity))
            cosineSimList.append(round(cosineSimilarity,2))
            maxValueList.append(round(cosineSimilarity,2))
        if(key != len(webPagesDict)):
            for k in range(0,(key-1)):
                maxValueList[k] = outputList[k][key-1]
        
    #appending the values for Last key
    for k in range(0,(key-1)):
                maxValueList[k] = outputList[k][key-1]
    highestValueList.append(maxValueList)
    
    highestValueDict = dict(zip(webPageList,highestValueList))
    
    highestMatchDict={}
    for key in webPagesDict.keys():
        tempItrList=highestValueDict[key]
        max=0
        index=0
        for temp in range(0,len(tempItrList)):
            if(tempItrList[temp] > max):
                max=tempItrList[temp]
                index=temp
        highestMatchDict[key] = index+1        

    tempList=[]        
    for i in range(0,len(webPagesDict)):
            tempList.append("")        
    outputList.append(tempList)              
    
    outputFile.write("\n" + "Cosine similarity for the above webpages is : " + "\n")        
    for key in webPagesDict.keys():
        outputFile.write("\n" + str(key) + " : " + str(outputList[key-1]))
    row_format ="{:>15}" * (len(webPageList) + 1)
    outputFile.write("\n" +  "\n"+"Cosine Similarity Matrix for the above list of webpages is as follows : " + "\n" + "\n")
    outputFile.write(row_format.format("", *webPageList))
    outputFile.write("\n")
    for team, row in zip(webPageList, outputList):
        outputFile.write(row_format.format(team, *row))
        outputFile.write("\n")
    outputFile.write("\n" + "Highest matches for each webpage : " + "\n")    
    for key in highestMatchDict.keys():
        outputFile.write("\n" + str(key) + " : " + webPagesDict[(highestMatchDict[key])])
    outputFile.close() 
        
def calcCosineSimilarity(url1,url2):
        print("Cosine Sim is : " , calculateCosineSimilarity(url1,url2))

#Calculate COsine Similarity of webpages listed in input file        
calcCosineSimilarityUsingInputFile()





