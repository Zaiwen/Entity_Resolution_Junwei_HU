import re
ary, aryy, aryyy = [], [], []
def readfile(eblocks_path):
    with open(eblocks_path, 'r', encoding='utf-8')as f:
        for line in f:
            if "target entity" in line:
                num=re.sub(u"([^\u0030-\u0039])","", line)
                ary.append(num)
            if "similar entities" in line:
                num=re.sub(u"([^\u0030-\u0039])"," ", line)
                num=num.strip()
                num=num.split(" ")
                aryy.append(num)

def read_nodes_information(entity_attribute):
    with open(entity_attribute, 'r',encoding='utf-8')as f:
        for line in f:
            line = line.strip('\n').split('\t')
            aryyy.append(line)

def find_node_information(node_id):
    for i in range(0, len(aryyy)):
        if aryyy[i][0] == node_id:
            return aryyy[i]
    return 0

def dice_coefficient(a, b):
    """dice coefficient 2nt/na + nb."""
    a_bigrams = set(a)
    b_bigrams = set(b)
    overlap = len(a_bigrams & b_bigrams)
    return overlap * 2.0/(len(a_bigrams) + len(b_bigrams))

def pruning(eblocks_path, dblocks_path, entity_attribute, threshold):
    readfile(eblocks_path)
    read_nodes_information(entity_attribute)
    outfile=open(dblocks_path, 'w', encoding='utf-8')
    for i in range(len(ary)):
        outfile.write("target entity: ")
        outfile.write(ary[i])
        outfile.write("\n")
        outfile.write("similar entities: ")
        for j in range(len(aryy[i])):
            if find_node_information(ary[i]) and find_node_information(aryy[i][j]):
                if dice_coefficient(find_node_information(ary[i])[1], find_node_information(aryy[i][j])[1]) >= threshold:
                    outfile.write(aryy[i][j] + " ")
        outfile.write('\n')

