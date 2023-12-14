import re
ary, aryy = [], []
match = dict()
def readfile(blocks_path):
    with open(blocks_path, encoding='utf-8')as f:
        for line in f:
            if "target entity" in line:
                num=re.sub(u"([^\u0030-\u0039])", "", line)
                ary.append(num)
            if "similar entities" in line:
                num=re.sub(u"([^\u0030-\u0039])", " ", line)
                num=num.strip()
                num=num.split(" ")
                aryy.append(num)
    total_edge = 0
    for i in range(0,len(ary)):
        if aryy[i][0] != '':
            total_edge=total_edge+len(aryy[i])
    return total_edge

def pruning(blocks_path, eblocks_path):
    max_Arcs, max_Cbs, total_weight = 0, 0, 0
    total_edge = readfile(blocks_path)

    for i in range(0, len(ary)):
        for j in range(0, len(aryy[i])):
            if aryy[i][0]!='':
                for k in range(0,len(ary)):
                    if aryy[i][j]==ary[k]:
                        Cbs=2
                        Arcs=(1/len(aryy[i])+1/len(aryy[k]))
                        if Cbs > max_Cbs:
                            max_Cbs = Cbs
                        if Arcs > max_Arcs:
                            max_Arcs = Arcs
                        break
    for i in range(0, len(ary)):
        for j in range(0, len(aryy[i])):
            if aryy[i][0]!='':
                for k in range(0,len(ary)):
                    if aryy[i][j]==ary[k]:
                        Cbs=2/max_Cbs
                        Arcs=(1/len(aryy[i])+1/len(aryy[k]))/max_Arcs
                        weight=2*(Cbs*Arcs)/(Cbs+Arcs)
                        total_weight += weight
                        break
    average_weight = total_weight/total_edge
    outfile = open(eblocks_path, 'w', encoding='utf-8')
    for i in range(len(ary)):
        outfile.write("target entity: ")
        outfile.write(ary[i])
        outfile.write("\n")
        outfile.write("similar entities: ")
        for j in range(len(aryy[i])):
            if aryy[i][0] != '':
                for k in range(len(ary)):
                    if aryy[i][j]==ary[k]:
                        Cbs=2/max_Cbs
                        Arcs=(1/len(aryy[i])+1/len(aryy[k]))/max_Arcs
                        weight=2*(Cbs*Arcs)/(Cbs+Arcs)
                        if weight >= average_weight*(1/2):
                            outfile.write(aryy[i][j] + " ")
                        break
        outfile.write("\n")
    