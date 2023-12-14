import re
import Levenshtein as ls
ary, aryy, aryyy = [], [], []
def readfile(dblocks_path):
    with open(dblocks_path, 'r', encoding='utf-8')as f:
        for line in f:
            if "target entity" in line:
                num = re.sub(u"([^\u0030-\u0039])","", line)
                ary.append(num)
            if "similar entities" in line:
                num = re.sub(u"([^\u0030-\u0039])"," ", line)
                num = num.strip()
                num = num.split(" ")
                aryy.append(num)

def read_nodes_information(entity_attribute):
    with open(entity_attribute, 'r',encoding='utf-8')as f:
        for line in f:
            line = line.strip('\n').split('\t')
            aryyy.append(line)

def find_node_information(node_id):
    for i in range(len(aryyy)):
        if aryyy[i][0] == node_id:
            return aryyy[i]

def matching(dblocks_path, matching_pairs_path, entity_attribute, rule):
    readfile(dblocks_path)
    read_nodes_information(entity_attribute)
    items, result = [], []
    with open(rule, 'r', encoding='utf-8')as f:
        for line in f:
            if '->' in line:
                line1 = line.strip('\n').split('->')[0].rsplit(' ', 1)[0]
                line2 = line.strip('\n').split('->')[0].rsplit(' ', 1)[1]
                line3 = line1.split('=')[0]
                line4 = line1.split('=')[1]
                items.append([line3, line4, float(line2)])
    outfile=open(matching_pairs_path, 'w', encoding='utf-8')
    for i in range(len(items)):
        item1 = items[i][0].split('.')[1]
        item2 = items[i][1].split('.')
        if len(item2) == 1:
            item2 = item2[0]
        else:
            item2 = item2[1]
        if item1 == item2:
            for j in range(len(ary)):
                if aryy[j][0] != '':
                    for k in range(len(aryy[j])):
                        if (1 - ls.ratio(find_node_information(ary[j])[aryyy[0].index(item1)], find_node_information(aryy[j][k])[aryyy[0].index(item2)])) <= items[i][2] and [ary[j], aryy[j][k]] not in result and [aryy[j][k], ary[j]] not in result:
                            result.append([ary[j], aryy[j][k]])
                            outfile.write(ary[j] + '|' + aryy[j][k] + '\n')
