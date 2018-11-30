from math import log
import operator
import pickle


def creatData():

    data = [[1, 3, 3, 0, 'no'],
            [1, 2, 3, 1, 'no'],
            [2, 3, 2, 0, 'yes'],
            [3, 1, 4, 0, 'yes'],
            [3, 1, 2, 0, 'yes'],
            [3, 1, 1, 1, 'no'],
            [2, 1, 1, 1, 'yes'],
            [1, 2, 4, 0, 'no'],
            [1, 1, 1, 0, 'yes'],
            [3, 2, 2, 0, 'yes'],
            [1, 2, 1, 1, 'yes'],
            [2, 2, 3, 1, 'yes'],
            [2, 3, 2, 0, 'yes'],
            [3, 2, 2, 1, 'no']]
    label = ['天气', '温度', '湿度', '风况']
    print('天气:晴(1),多云(2),有雨(3)')
    print("温度:60<(1)<=70,70<(2)<=80,80<(3)<=90")
    print("湿度:60<(1)<=70,70<(2)<=80,80<(3)<=90,90<(4)<=100")
    print("风况:有(1),无(0)")
    print("结果:适宜运动(yes)，不适宜运动(no)")
    return(data, label)


def dataformat(tianqi, wendu, shidu, fengkuang):
    data = []
    if tianqi == '晴':
        tianqi = 1
    if tianqi == '多云':
        tianqi = 2
    if tianqi == '有雨':
        tianqi = 3
    if wendu <= 70 and wendu > 60:
        wendu = 1
    if wendu > 70 and wendu <= 80:
        wendu = 2
    if wendu > 80 and wendu <= 90:
        wendu = 3
    if shidu <= 70 and shidu > 60:
        shidu = 1
    if shidu > 70 and shidu <= 80:
        shidu = 2
    if shidu > 80 and shidu <= 90:
        shidu = 3
    if shidu > 90 and shidu <= 100:
        shidu = 4
    if fengkuang == '有':
        fengkuang = 1
    if fengkuang == '无':
        fengkuang = 0
    data = [tianqi, wendu, shidu, fengkuang]
    return(data)


def inforEnt(data):
    datanum = len(data)
    labelsdict = {}
    for each in data:
        label = each[-1]
        labelsdict[label] = labelsdict.get(label, 0) + 1
    Ent = 0.0

    for key in labelsdict:
        P = labelsdict[key] / datanum
        Ent -= P * log(P, 2)
    return(Ent)


def splitData(data, axis, value):
    newdata = []
    for each in data:
        if each[axis] == value:

            data1 = each[:axis]
            data1.extend(each[axis + 1:])
            newdata.append(data1)
    return(newdata)


def bestfeature(data):
    bestfea = -1
    bestinforgain = 0.0
    numfea = len(data[0]) - 1
    oriEnt = inforEnt(data)

    for i in range(numfea):
        feavalue = [each[i] for each in data]
        uniquefea = set(feavalue)
        newent = 0.0
        for each in uniquefea:

            spliteddata = splitData(data, i, each)
            P = len(spliteddata) / len(data)
            newent += P * inforEnt(spliteddata)
        inforgain = oriEnt - newent
        if (inforgain > bestinforgain):
            bestinforgain = inforgain
            bestfea = i
    return(bestfea)


def votebest(classlist):
    classcount = {}
    for each in classlist:
        classcount[each] = classcount.get('each', 0) + 1
    sortedclasscount = sorted(
        classcount.items(), key=operator.itemgetter(1), reverse=True)
    return(sortedclasscount[0][0])


def creattrees(data, labels):
    label = list(labels)
    classlist = [each[-1] for each in data]
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    if len(data[0]) == 1:
        return votebest(classlist)
    bestfeat = bestfeature(data)
    bestfeatlabel = label[bestfeat]
    mytree = {bestfeatlabel: {}}
    del(label[bestfeat])
    bestfeatvalue = [each[bestfeat] for each in data]
    uniquevalue = set(bestfeatvalue)
    for value in uniquevalue:
        sublabel = label[:]
        mytree[bestfeatlabel][value] = creattrees(
            splitData(data, bestfeat, value), sublabel)
    return(mytree)


# def classify(inputtree, featlabels, testvec):
#     classlabel = str()
#     firstkey = inputtree.keys()
#     firstlabel = list(firstkey)[0]
#     # print(firstlabel)
#     seconddict = inputtree[firstlabel]
#     featindex = featlabels.index(firstlabel)
#     for key in seconddict.keys():
#         if testvec[featindex] == key:
#             if type(seconddict[key]).__name__ == 'dict':

#                 classlabel = classify(seconddict[key], featlabels, testvec)
#             else:
#                 classlabel = seconddict[key]
#     return(classlabel)


def writetree(inputtree, filename):  # 保存决策树
    with open(filename, 'wb') as f:

        pickle.dump(inputtree, f)


def readtree(filename):  # 读取决策树
    with open(filename, 'rb') as f:
        return(pickle.load(f))


def list_dic(dic):
    for k in dic:
        print(k + "(root)")
        for k1 in dic[k]:
            if type(dic[k][k1]) == type('str'):
                print(k1, end='  ')
                print(dic[k][k1])
            else:
                print(k1, end='  ')
                for k2 in dic[k][k1]:
                    print(k2, end='  ')
                    print(dic[k][k1][k2])


if __name__ == '__main__':
    data, label = creatData()
    i = 0
    tree = creattrees(data, label)
    print('\n决策树规则为: ')
    list_dic(tree)
    # root = tree.keys()
    # print(tree.values())
    # for key in tree:
    #     #print(key)
    #     print(tree[key])
    #     for k in tree[key]:
    #         print(tree[key][k])
    # print(root)
    # print(root[0])
    # print(tree['天气'])
