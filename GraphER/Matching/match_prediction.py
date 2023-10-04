import Levenshtein as ls
ary = []

with open('produce_Table02.txt', 'r', encoding='utf-8')as f:
    for line in f:
        line = line.strip('\n').split(';;')
        ary.append(line)

aryy = []
with open('produce_Table01.txtresult01.txt', 'r', encoding='utf-8')as f:
    for line in f:
        if '->' in line:
            line1 = line.strip('\n').split('->')[0].rsplit(' ', 1)[0]
            line2 = line.strip('\n').split('->')[0].rsplit(' ', 1)[1]
            line3 = line1.split('=')[0]
            line4 = line1.split('=')[1]
            aryy.append([line3, line4, float(line2)])

outfile = open('result_Table.txt', 'w', encoding='utf-8')
result = []
for i in range(len(aryy)):
    item1 = aryy[i][0].split('.')[1]
    item2 = aryy[i][1].split('.')
    if len(item2) == 1:
        item2 = item2[0]
    else:
        item2 = item2[1]
    print(item1, item2)
    if item1 == item2:
        for j in range(len(ary)):
            if j == 0:
                id1 = [p for p, x in enumerate(ary[j]) if item1 in x]
            else:
                if (1 - ls.ratio(ary[j][id1[0]], ary[j][id1[1]])) <= aryy[i][2] and [ary[j][4], ary[j][12]] not in result:
                    result.append([ary[j][4], ary[j][12]])
                    outfile.write(str([ary[j][4], ary[j][12]]) + '\n')
    else:
        for j in range(len(ary)):
            if j == 0:
                id1 = [p for p, x in enumerate(ary[j]) if item1 in x]
            else:
                if (1 - ls.ratio(ary[j][id1[0]], aryy[i][1])) <= aryy[i][2] and (1 - ls.ratio(ary[j][id1[1]], aryy[i][1])) <= aryy[i][2] and [ary[j][4], ary[j][12]] not in result:
                    result.append([ary[j][4], ary[j][12]])
                    outfile.write(str([ary[j][4], ary[j][12]]) + '\n')