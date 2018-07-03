# -*- coding: utf-8 -*-
import jieba
import jieba.analyse

text = '为政之要，唯在得人；治国理政，关键在人。“领导干部”是习近平总书记每年都会多次提及的群体。2013年6月28日，他在全国组织工作会议上首次提出“好干部”标准。四年后，他在党的十九大报告中阐述加强干部队伍建设时，首次在“高素质”后加上了“专业化”三个字。今年党的生日前夕，他组织中央政治局集体学习，再次强调要把树立正确选人用人导向作为重要着力点，突出政治标准。五年来，习近平总书记在不同场合反复叮嘱，时刻“提醒”，期之殷殷，言之切切。让我们一起重温习总书记选人用人“标尺”，争当新时代好干部。'
seg_list = jieba.cut(text, cut_all=True)
seg_list_1 = jieba.cut(text, cut_all=False)
print(" ".join(seg_list))
print(" ".join(seg_list_1))

seg_list_search = jieba.cut_for_search(text)
print(" ".join(seg_list_search))

for x, w in jieba.analyse.extract_tags(text, withWeight=True):
    print('%s %s'% (x, w))
