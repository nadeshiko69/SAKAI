##### ***SAKAI.py***                     #####
##### main関数的な                       #####
##### これを実行すればok                 #####

import LyricGenerate
import Validation

import os
import pandas as pd
import math
import random

def isNaN(num):
    return num != num

THRESH = 0.55 # 評価値のしきい値 0.5 < THRESH < 1.0

# ここではInitでsample.txt読み込みしているだけ
dataGenerate = LyricGenerate.DataGenerate()
 
# if os.path.exists('resource/TestData.csv') == False:
#     dataGenerate.DataGenerate()
#     print("Test data generated.")

dataGenerate.DataGenerate()

# フレーズ作って、評価
# ここの処理もメソッド化するべき、そのうち
suffix = [] # __label__0のindexと評価値を格納
testData = pd.read_csv('resource/TestData.csv')
dataValidation = Validation.DataValidation()

for i in range(len(testData)):
    if isNaN(testData.iloc[i,1]) == False :
        value = dataValidation.PhraseValidation(testData.iloc[i,1])
    else:
        value = (('__label__1',), [1])

    testData.iloc[i,0] = value
    if value[0][0] == '__label__0' and float(value[1][0])>THRESH: # エモいと評価されたフレーズの情報を覚えておく
        print(i,value[1][0])
        suffix.append([i, value[1][0]])
    sortSuffix = sorted(suffix, reverse=True, key=lambda x: x[1]) #評価値が大きい順にソート
    sortSuffix = list(map(list, set(map(tuple, sortSuffix))))     # 重複要素を削除

# エモいフレーズを評価値にしたがってピックアップしていく
# 今は降順ソートして上位10%, 20%, 30%がサビ、Bメロ、Aメロ
sabi   = sortSuffix[:len(sortSuffix)//10]
bMelo = sortSuffix[(len(sortSuffix)//10)+1 : (len(sortSuffix)//10)*2]
aMelo = sortSuffix[(len(sortSuffix)//10)*2+1 : (len(sortSuffix)//10)*3]
# Memo
# 本来はエモ度0.9以上、0.8以上、0.7以上のような分割をしたほうが良い？(現状、生成と評価の精度が低すぎて全部0.5台なので)
# ↑今後上位に90%台がゴロゴロ出てくるなら、Aメロとサビでエモ度に差をつけたほうがいい？


##### 出力 
##### 各パートの候補フレーズから重複を
##### 許して4フレーズをランダムに選択して出力
print("***A-Melo***")
aMeloIndex = random.choices(aMelo, k=4)
for i in range(4):
    print(testData.iloc[aMeloIndex[i][0],1])

print("***B-Melo***")
bMeloIndex = random.choices(bMelo, k=4)
for i in range(4):
    print(testData.iloc[bMeloIndex[i][0],1])

print("***Sabi***")
sabiIndex = random.choices(sabi, k=4)
for i in range(4):
    print(testData.iloc[sabiIndex[i][0],1])

##### Revision
# 20/12/14 Revision 00 | 初期ver作成
# 20/12/25 Revision 01 | testdataの存在チェック追加、validation動作確認
# 20/12/25 Revision 02 | エモいフレーズのみ抽出
# 20/12/25 Revision 03 | 出力まで完成、v1.0
# 21/02/11 Revision 04 | modeの概念を削除