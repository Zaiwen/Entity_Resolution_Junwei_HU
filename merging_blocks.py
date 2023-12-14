import re
m_ary, m_aryy, d_ary, d_aryy = [], [], [], []
def readfile(sblocks_path, ablocks_path, blocks_path):
    with open(sblocks_path, encoding='utf-8')as f:
        for line in f:
            if "target entity" in line:
                num = re.sub(u"([^\u0030-\u0039])","", line)
                m_ary.append(num)
            if "similar entities" in line:
                num = re.sub(u"([^\u0030-\u0039])"," ", line)
                num = num.strip()
                num = num.split(" ")
                m_aryy.append(num)
    with open(ablocks_path, encoding='utf-8')as f:
        for line in f:
            if "target entity" in line:
                num = re.sub(u"([^\u0030-\u0039])","", line)
                d_ary.append(num)
            if "similar entities" in line:
                num = re.sub(u"([^\u0030-\u0039])"," ", line)
                num = num.strip()
                num = num.split(" ")
                d_aryy.append(num)
    k = 0
    outfile = open(blocks_path, 'w', encoding='utf-8')
    for i in range(0, len(m_ary)):
        if m_ary[i] in d_ary:
            k = k + 1
            outfile.write("target entity: ")
            outfile.write(m_ary[i])
            outfile.write("\n")
            outfile.write("similar entities: ")
            ml_arry = list(set(m_aryy[i]+d_aryy[d_ary.index(m_ary[i])]))
            # print(ml_arry)
            for j in range(0, len(ml_arry)):
                if ml_arry[j] != '':
                    outfile.write(ml_arry[j])
                    outfile.write(" ")
            outfile.write("\n") 
        else:
            k = k + 1
            outfile.write("target entity: ")
            outfile.write(m_ary[i])
            outfile.write("\n")
            outfile.write("similar entities: ")
            for j in range(0, len(m_aryy[i])):
                outfile.write(m_aryy[i][j])
                outfile.write(" ")
            outfile.write("\n")
    for i in range(0, len(d_ary)):
        if d_ary[i] not in m_ary:
            k = k + 1
            outfile.write("target entity: ")
            outfile.write(d_ary[i])
            outfile.write("\n")
            outfile.write("similar entities: ")
            for j in range(0,len(d_aryy[i])):
                outfile.write(d_aryy[i][j])
                outfile.write(" ")
            outfile.write("\n")
