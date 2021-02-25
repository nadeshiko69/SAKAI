##### ***LyricGenerate.py***             #####
##### マルコフ連鎖を用いた１フレーズ作成 #####
#####                                    #####

import markovify
import pandas as pd
import os
import string
import re
import sys
import MeCab
from tqdm import tqdm
import csv
import numpy as np

import random

class DataGenerate:
    def __init__(self):
        with open('resource/sample_rev.txt') as f:
            self.text = f.read()

    def DataGenerate(self):
        text_model = markovify.Text(self.text)    
        sample = 100000                          #サンプル数
        sentence = 150                           #文字数
        filename = 'resource/TestData.csv'       #ファイル名
        print("Test Data Generating...")

        ################
        # フレーズ生成 #
        ################
        phrase = []
        cnt    = 0
        pbar   = tqdm(total=100)
        for i in range(sample):
            cnt += 1
            phrase.append(text_model.make_short_sentence(sentence))
            if cnt== sample/100:
                pbar.update(1)
                cnt=0
        pbar.close()

        #################
        # csvとして保存 #
        #################
        #fasttextに読ませる形式に変換
        label = ['']*sample

        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(label) #インデックスいれて
            writer.writerow(label) #ラベル入れる場所作って
            writer.writerow(phrase)#Phrase入れる
            #UTF-8で保存されてるの注意！！！
        #転置
        tmp = pd.read_csv(filename)
        tmp = tmp.T
        tmp.to_csv(filename, index=False)#, header=False)

        print("Done.")


    # 連鎖数3のマルコフ連鎖
    # 実装自体は残すが、現状使用していない
    # 今後必要なさそうなら消す
    def MarkovGenerate(self, wordlist):
        markov = {}
        w1 = ""
        w2 = ""
        w3 = ""
        endword = ["。", "!", "？"]
        for word in list(wordlist):
            if w1 and w2 and w3:
                if(w1, w2, w3) not in markov:
                    markov[(w1, w2, w3)] = []
                markov[(w1, w2, w3)].append(word)
            w1, w2, w3 = w2, w3, word
            
        count = 0
        sentence = ""
        w1, w2, w3 = random.choice(markov.keys())
        while count < len(wordlist):
            tmp = random.choice(markov[w1, w2, w3])
            # 句読点などの区切りがついたら文章作成を終了
            if tmp in endword:
                break
            sentence += tmp
            w1, w2, w3 = w2, w3, tmp
            count += 1
            if count > 20:
                break
        return sentence


# Memo
# testdataはcsv化する必要なさそうなのでいずれdataframeにreturnする形式にrevする

##### Revision
# 20/12/14 Revision 00 | 初期ver作成
# 21/02/02 Revision 01 | MarkovGenerate追加
# 21/02/11 Revision 02 | modeの概念を削除