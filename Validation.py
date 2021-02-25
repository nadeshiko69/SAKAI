##### ***Validation.py***                #####
##### フレーズの評価値を決定             #####
#####                                    #####

import MeCab
import markovify
import pandas as pd
import fasttext as ft
import random
import os
import csv


class DataValidation:
    def __init__(self):
        self.model = ft.train_supervised(input='resource/FastTextModelData_rev.txt', lr=0.01, dim=100, epoch=30, word_ngrams=5, loss='softmax')
        # コンソール上にこんな出力を出す
        # --------------------------------------------------------------------------------------------
        # Read 0M words
        # Number of words:  2118
        # Number of labels: 2
        # Progress: 100.0% words/sec/thread:  435454 lr:  0.000000 avg.loss:  0.562217 ETA:   0h 0m 0s
        # --------------------------------------------------------------------------------------------

    def PhraseValidation(self, phrase):
        # print(self.model.predict(phrase,k=2))
        # このpredictがほぼ機能していない
        # 殆どがlabel1の判定、評価値も全部0.5xxxxxx
        return self.model.predict(phrase,k=1)


##### Revision
# 20/12/14 Revision 00 | ファイルのみ仮作成
# 20/12/15 Revision 01 | class DataValidation実装
# 20/12/24 Revision 02 | ModelSet実装
# 20/12/25 Revision 03 | ModelSet削除、initでmodelを作成(txtファイルをwith opendでReadするとtrainにinputできないため)
