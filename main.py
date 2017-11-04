# -*- coding: utf8 -*- 
'''
Created on 3 Nov 2017

@author: kaho
'''

import sys
import os
import pandas as pd
from functools import partial
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

def save_as_utf8(infilePath,outfilePath):
    if os.path.isfile(outfilePath):
        print "[Skipped]{} already here,please delete it if you want to update ".format(outfilePath.encode('utf8'))
        return
# Decode with UTF-8 and replace errors with "?"
    with open(u"{0}".format(infilePath), 'rb') as in_file:
        with open(u"{0}".format(outfilePath), 'w') as out_file:
            # for byte_fragment in iter(partial(in_file.read, chunksize), b''):
            for byte_fragment in iter(partial(in_file.read), b''):
                byte_file = byte_fragment.decode(encoding='gb18030', errors='replace')
                out_file.write(byte_file.encode('utf8'))
                
def convert_files_utf8(inPath,outPath):
    comment_file_list = os.listdir(u"{0}".format(inPath))
    for fn in comment_file_list:
        save_as_utf8(inPath+"/"+fn,outPath+"/"+fn)

def extract_commentToFile(inFilePath,outFilePath):
    if os.path.isfile(outfilePath):
        print "[Skipped]{} already here,please delete it if you want to update ".format(outfilePath)
        return
    df = pd.read_csv(inFilePath,header = 0)   
    comment = df['postTitle']
    #print comment.head()
    #com_size = comment.size
    with open(outFilePath, 'w') as out_file:
        for row in comment:
            out_file.write(row+'\n')
def get_comment_text(inPath):    
    df = pd.read_csv(inPath,header = 0)   
    comment = df['postTitle']
    #print comment.head()
    #com_size = comment.size
    text=""
    for row in comment:
        text +="{0}\n".format(row)
    return text
         
def get_comment_text_month(inPath):    
    df = pd.read_csv(inPath,header = 0)   
    comment = df['postTitle']
    date = df['postTime']
    ym = []
    if not len(date):
        return None
    for i,d in enumerate(date):
        d = d.split('-')
        ym.append("{}-{}".format(d[0],d[1]))
    
    content=[]
    text=""
    cur_month = ym[0]
    num_per_month =0
    for i,row in enumerate(comment):
        if (not (ym[i] == cur_month)) or (num_per_month>300):
            content.append([cur_month,num_per_month,text])
            text = row
            cur_month = ym[i]
            num_per_month = 1
            continue
        text +="{0}\n".format(row)
        num_per_month+=1
    print "num of request:{}".format(len(content))        
    return content
def get_comment_text_limit(inPath,limit):    
    df = pd.read_csv(inPath,header = 0)   
    comment = df['postTitle']
    #print comment.head()
    start = 0
    if comment.size>limit:
        start = comment.size-limit
    print "num of comment:{}".format(comment.size)
    text=""
    for index in xrange(start,comment.size,1):
        text +="{0}\n".format(comment[index])
        
    return text,start

def gcloud_sentiment_analysis(text):
    document = types.Document(
    content=text,
    language='zh',
    type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document)
    #senetence_list=[]
    #print 'Text: {}'.format(text)
    #for sentence in sentiment.sentences:
        #senetence_list.append([sentence.text.content.encode('utf8'),sentence.sentiment.score])
        #print sentence_sentiment
        #print sentence.text.content.encode('utf8')
    #print "num of score:{}".format(len(sentiment.sentences))
    overall_score = sentiment.document_sentiment.score
    overall_mangitude = sentiment.document_sentiment.magnitude
    #print('Overall Sentiment: score of {} with magnitude of {}'.format(overall_score, overall_mangitude))
    return overall_score,overall_mangitude


main_path = "/home/kaho/Documents/MSBD5001/project/2 Auto sales & House Price Prediction/Auto Sales Data"
commentRaw = main_path+"/carcomment"
commentUTF8 = main_path+"/carcommentUtf8"
result_path = main_path+"/sentiment_result"
overall_result_path = main_path+"/sentiment_result/overall_sentiment_result.csv"
if not os.path.isfile(overall_result_path):
    with open(overall_result_path,'w') as out_file:
        out_file.write("filename,overall_score,magnitude\n")


#convert_files_utf8(commentRaw,commentUTF8)

comment_file_list = os.listdir(u"{0}".format(commentUTF8))

#extract_commentToFile(commentUTF8+'/'+"保时捷968.csv",result_path+'/'+"保时捷968.txt")
fileNum=1
limit=5000
while fileNum > 0:
    fileNum -=1
    # Instantiates a client
    client = language.LanguageServiceClient()
    filename = "大捷龙.csv"
    #filename = "撼路者(海外).csv"
    print filename
    text_path = commentUTF8+'/'+filename
    outfilePath = result_path+'/'+filename
    if os.path.isfile(outfilePath):
        print "[Skipped]{} already here,please delete it if you want to update ".format(outfilePath)
        continue
    with open(outfilePath,'w') as out_file:
        out_file.write("ym,numOfComment,score,mangitude\n")
        #The text to analyze
        text = get_comment_text_month(text_path)
        for t in text:
            print t[0]
            overall_score,overall_mangitude = gcloud_sentiment_analysis(t[2])   
            out_file.write("{},{},{},{}\n".format(t[0],t[1],overall_score,overall_mangitude))
    
print "done"











