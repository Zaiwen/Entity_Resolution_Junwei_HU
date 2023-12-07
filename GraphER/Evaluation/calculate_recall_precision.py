import re
ary = []
aryy = []
ary1 = []
aryy1 = []
def readfile():
    with open("iA_network_final_match/match_pairs_rule.txt", 'r', encoding='utf-8')as f:
        for line in f:
            if "target entity" in line:
                num = re.sub(u"([^\u0030-\u0039])","", line)
                # print(num)
                ary.append(num)
                # print(len(ary))
            if "similar entities" in line:
                num = re.sub(u"([^\u0030-\u0039])"," ", line)
                num = num.strip()
                num = num.split(" ")
                # print(num)
                aryy.append(num)
    # ary[0]="</s>"
    # print(ary)
    # print(aryy)
    total_edge = 0
    for i in range(0, len(ary)):
        if aryy[i][0] != '':
            # print(ary[i], aryy[i])
            total_edge = total_edge + len(aryy[i])
    print(total_edge)

    i = 1
    with open("ground_truth_itunes_amazon_test.txt", 'r', encoding='utf-8') as f:
        for line in f:
            i = i + 1
            line = line.strip('\n').split('\t')
            line = line[0].strip('a')
            # line = line[1:4]
            if len(line) > 0:
                if i % 2 != 0:
                    ary1.append(line)
                else:
                    aryy1.append(line)

    # print(i)
    # print(ary1)
    # print(aryy1)
    match_pair = 0
    for i in range(0, len(ary)):
        if ary[i] in ary1:
            id1 = [p for p, x in enumerate(ary1) if x == ary[i]]
            for k in range(0, len(id1)):
                for j in range(0, len(aryy[i])):
                    if aryy1[id1[k]] == aryy[i][j]:
                        match_pair = match_pair + 1
        if ary[i] in aryy1:
            id1 = [p for p, x in enumerate(aryy1) if x == ary[i]]
            for k in range(0, len(id1)):
                for j in range(0, len(aryy[i])):
                    if ary1[id1[k]] == aryy[i][j]:
                        match_pair = match_pair + 1

    print("recall:", match_pair/(2 * len(ary1)))
    print("precision:", match_pair/total_edge)

if __name__ == '__main__':
    readfile()
