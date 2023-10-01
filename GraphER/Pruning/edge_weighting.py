import re
import interspace
ary = []
aryy = []
match = dict()
def readfile():
    with open("GDS_dm/ACA1+ARA_0.1+0.1.txt", encoding='utf-8')as f:
        for line in f:
            if "target entity" in line:
                num=re.sub(u"([^\u0030-\u0039])","", line)
                #print(num)
                ary.append(num)
                # print(len(ary))
            if "similar entities" in line:
                num=re.sub(u"([^\u0030-\u0039])"," ", line)
                num=num.strip()
                num=num.split(" ")
                #print(num)
                aryy.append(num)
    total_edge = 0
    for i in range(0, len(ary)):
        if aryy[i][0] != '':
            total_edge = total_edge+len(aryy[i])
    return total_edge

if __name__ == '__main__':
    # blocks=0
    # for i in range(0,len(aryy)):
    #     if aryy[i][0]!='':
    #         blocks=blocks+1
    # print(blocks)
    # max_similar_len=len(aryy[0])
    # for i in range(0,len(aryy)):
    #     if len(aryy[i])>max_similar_len:
    #         max_similar_len=len(aryy[i])
    # print(max_similar_len)
    max_Arcs = 0
    max_Cbs = 0
    total_edge = readfile()
    total_weight = 0
    
    for i in range(0, len(ary)):
        for j in range(0, len(aryy[i])):
            if aryy[i][0] != '':
                for k in range(0,len(ary)):
                    if aryy[i][j] == ary[k]:
                        Cbs = 2
                        Arcs = (1/len(aryy[i])+1/len(aryy[k]))
                        if Cbs > max_Cbs:
                            max_Cbs = Cbs
                        if Arcs > max_Arcs:
                            max_Arcs = Arcs
                        break
    for i in range(0, len(ary)):
        for j in range(0, len(aryy[i])):
            if aryy[i][0] != '':
                for k in range(0, len(ary)):
                    if aryy[i][j] == ary[k]:
                        Cbs = 2/max_Cbs
                        Arcs = (1/len(aryy[i])+1/len(aryy[k]))/max_Arcs
                        weight = 2*(Cbs*Arcs)/(Cbs+Arcs)
                        total_weight += weight
                        break
    average_weight = total_weight/total_edge
    outfile = open("GDS_dm_first_pruning/prune_AM_blocks_(1).txt", 'w', encoding='utf-8')
    for i in range(0, len(ary)):
        outfile.write("target entity: ")
        outfile.write(ary[i])
        outfile.write("\n")
        outfile.write("similar entities: ")
        for j in range(0, len(aryy[i])):
            if aryy[i][0] != '':
                for k in range(0, len(ary)):
                    if aryy[i][j] == ary[k]:
                        Cbs = 2/max_Cbs
                        Arcs = (1/len(aryy[i])+1/len(aryy[k]))/max_Arcs
                        weight = 2*(Cbs*Arcs)/(Cbs+Arcs)
                        if weight >= average_weight*(1/2):
                            outfile.write(aryy[i][j] + " ")
                        break
        outfile.write("\n")
                        
    