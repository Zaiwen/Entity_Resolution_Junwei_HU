import re
ary = []
aryy = []

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
        total_edge = total_edge+len(aryy[i])
print(total_edge)

print("CSSR:", total_edge/((62830*62829)/2))