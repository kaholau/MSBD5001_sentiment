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
main_path = "/home/kaho/Documents/MSBD5001/project/2 Auto sales & House Price Prediction/Auto Sales Data"
commentRaw = main_path+"/carcomment"
commentUTF8 = main_path+"/carcommentUtf8"
result_path = main_path+"/sentiment_result"

#convert_files_utf8(commentRaw,commentUTF8)

#comment_file_list = os.listdir(u"{0}".format(commentUTF8))

#extract_commentToFile(commentUTF8+'/'+"保时捷968.csv",result_path+'/'+"保时捷968.txt")

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = get_comment_text(commentUTF8+'/'+"保时捷968.csv")
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document)

print 'Text: {}'.format(text)
for index, sentence in enumerate(sentiment.sentences):
        sentence_sentiment = sentence.sentiment.score
        print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))
score = sentiment.document_sentiment.score
magnitude = sentiment.document_sentiment.magnitude
print('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))
















