import re
ary = []
aryy = []
ary1 = []
aryy1 = []
how_many_blocks = 0
how_many_purity = 0

def readfile():
    # global how_many_blocks
    with open("iA_network_dl_second_pruning/prune_AM_blocks.txt", 'r', encoding='utf-8')as f:
        for line in f:
            if "target entity" in line:
                num = re.sub(u"([^\u0030-\u0039])","", line)
                ary.append(num)
            if "similar entities" in line:
                num = re.sub(u"([^\u0030-\u0039])"," ", line)
                num = num.strip()
                num = num.split(" ")
                aryy.append(num)
    total_edge = 0
    for i in range(0, len(ary)):
        if aryy[i][0] != '':
            # how_many_blocks = how_many_blocks + 1
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

def traverse_blocks():
    global how_many_purity
    global how_many_blocks
    for i in range(0, len(ary)):
        match_pair = 0
        if ary[i] in ary1:
            how_many_blocks = how_many_blocks + 1
            id1 = [p for p, x in enumerate(ary1) if x == ary[i]]
            for k in range(0, len(id1)):
                for j in range(0, len(aryy[i])):
                    if aryy1[id1[k]] == aryy[i][j]:
                        match_pair = match_pair + 1
            how_many_purity = how_many_purity + (match_pair/len(aryy[i]))

        if ary[i] in aryy1:
            how_many_blocks = how_many_blocks + 1
            id1 = [p for p, x in enumerate(aryy1) if x == ary[i]]
            for k in range(0, len(id1)):
                for j in range(0, len(aryy[i])):
                    if ary1[id1[k]] == aryy[i][j]:
                        match_pair = match_pair + 1
            how_many_purity = how_many_purity + (match_pair/len(aryy[i]))

readfile()
traverse_blocks()
print("average_purity:", how_many_purity/how_many_blocks)
