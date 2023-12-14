import pandas as pd
import numpy as np
import time

time_start = time.time()
data1 = pd.read_csv("relational-dataset/fodors-zagats/tableA.csv")
data1 = np.array(data1)
# data1 = np.nan_to_num(data1, nan=None)
data2 = pd.read_csv("relational-dataset/fodors-zagats/tableB.csv")
data2 = np.array(data2)
# data2 = np.nan_to_num(data2, nan=None)
data3 = pd.read_csv("relational-dataset/fodors-zagats/matches.csv")
data3 = np.array(data3)
data3 = data3.tolist()
# print(data3)

data = np.append(data1, data2, axis=0)
# data = np.array(data)
data1_length = len(data1)
data2_length = len(data2)
data = data.tolist()
# print(data)
# if data[0][3] in data[0]:
#     print(True)
type1 = [0, 1, 4, 5]
type2 = [2]
type3 = [3]
entity_type1 = []
entity_type2 = []
entity_type3 = []
ary = []
for i in range(len(data)):
    for j in range(len(type1)):
        ary.append(data[i][type1[j]])
    entity_type1.append(ary)
    ary = []
    for j in range(len(type2)):
        ary.append(data[i][type2[j]])
    entity_type2.append(ary)
    ary = []
    for j in range(len(type3)):
        ary.append(data[i][type3[j]])
    entity_type3.append(ary)
    ary = []

entity_type2_new = list(set([tuple(t) for t in entity_type2]))
for i in range(len(entity_type2_new)):
    entity_type2_new[i] = list(entity_type2_new[i])
entity_type2_new.sort(key=entity_type2.index)

entity_type3 = list(set([tuple(t) for t in entity_type3]))
for i in range(len(entity_type3)):
    entity_type3[i] = list(entity_type3[i])


for i in range(len(data)):
    data[i].insert(0, i)
# print(data)

id = 0
for i in range(len(entity_type1)):
    entity_type1[i].insert(0, id)
    id += 1
for i in range(len(entity_type2_new)):
    entity_type2_new[i].insert(0, id)
    id += 1
for i in range(len(entity_type3)):
    entity_type3[i].insert(0, id)
    id += 1

# print(len(data))
# print(len(entity_type2_new))
# print(entity_type2_new)

# outfile = open('ground_truth_fodors_zagat.txt', 'w', encoding='utf-8')
# for i in range(len(data3)):
#     for j in range(len(data3[i])):
#         for k in range(len(entity_type1)):
#             if data3[i][j] == entity_type1[k][1] and j == 0 and k >= 0 and k <= 532:
#                 outfile.write(str(entity_type1[k][0]) + '\n')
#             if data3[i][j] == entity_type1[k][1] and j == 1 and k > 532:
#                 outfile.write(str(entity_type1[k][0]) + '\n' * 2)

outfile = open('network/restaurant.txt', 'w', encoding='utf-8')
for i in range(len(entity_type1)):
    for j in range(len(entity_type1[i])):
        if j != len(entity_type1[i]) - 1:
            if not pd.isna(entity_type1[i][j]):
                outfile.write(str(entity_type1[i][j]) + '\t')
            else:
                outfile.write('\t')
        else:
            if not pd.isna(entity_type1[i][j]):
                outfile.write(str(entity_type1[i][j]))
            else:
                outfile.write('\t')
    outfile.write('\n')

outfile = open('network/address.txt', 'w', encoding='utf-8')
for i in range(len(entity_type2_new)):
    for j in range(len(entity_type2_new[i])):
        if j != len(entity_type2_new[i]) - 1:
            outfile.write(str(entity_type2_new[i][j]) + '\t')
        else:
            outfile.write(str(entity_type2_new[i][j]))
    outfile.write('\n')

outfile = open('network/city.txt', 'w', encoding='utf-8')
for i in range(len(entity_type3)):
    for j in range(len(entity_type3[i])):
        if j != len(entity_type3[i]) - 1:
            outfile.write(str(entity_type3[i][j]) + '\t')
        else:
            outfile.write(str(entity_type3[i][j]))
    outfile.write('\n')


address_city = []
outfile = open('network/restaurant-address.txt', 'w', encoding='utf-8')
for i in range(len(entity_type1)):
    for j in range(len(entity_type2_new)):
        if entity_type1[i][0] == data[i][0] and entity_type2_new[j][1] in data[i]:
            outfile.write(str(entity_type1[i][0]) + '\t' + str(entity_type2_new[j][0]) + '\n')
            for k in range(len(entity_type3)):
                if entity_type3[k][1] in data[i] and [entity_type2_new[j][0], entity_type3[k][0]] not in address_city: # and [entity_type2_new[j][0], entity_type3[k][0]] not in address_city
                    address_city.append([entity_type2_new[j][0], entity_type3[k][0]])

outfile = open('network/address-city.txt', 'w', encoding='utf-8')
for i in range(len(address_city)):
    outfile.write(str(address_city[i][0]) + '\t' + str(address_city[i][1]) + '\n')

def delete_type_add_symbol():
    ary_restaurant=[]
    ary_address=[]
    ary_city=[]
    with open("network/restaurant.txt",'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n').split('\t')
            ary_restaurant.append(line)
    outfile = open("network/restaurant.txt",'w',encoding='utf-8')
    for i in range(0,len(ary_restaurant)):
        outfile.write(ary_restaurant[i][0]+'\t'+'a'+ary_restaurant[i][0]+'\t'+ary_restaurant[i][2]+'\t'+ary_restaurant[i][3]+'\t'+ary_restaurant[i][4]+'\n')

    with open("network/address.txt",'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n').split('\t')
            ary_address.append(line)
    outfile = open("network/address.txt",'w',encoding='utf-8')
    for i in range(0,len(ary_address)):
        outfile.write(ary_address[i][0]+'\t'+'f'+ary_address[i][0]+'\t'+ary_address[i][1]+'\n')

    with open("network/city.txt",'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n').split('\t')
            ary_city.append(line)
    outfile = open("network/city.txt",'w',encoding='utf-8')
    for i in range(0,len(ary_city)):
        outfile.write(ary_city[i][0]+'\t'+'v'+ary_city[i][0]+'\t'+ary_city[i][1]+'\n')

delete_type_add_symbol()
time_end = time.time()
print(time_end - time_start)