import csv

index_to_delete = [1]
outfile = open('network/table.txt', 'w', encoding='utf-8')
outfile.write("id" + '\t' + "name" + '\t' + "phone" + '\t' + "type" +'\n')
with open('network/restaurant.txt', 'r', encoding='utf-8')as f:
    for line in f:
        line = line.strip().split('\t')
        line = [line[i] for i in range(0, len(line), 1) if i not in index_to_delete]
        for i in range(0, len(line)):
            if i != len(line) - 1:
                outfile.write(line[i] + '\t')
            else:
                outfile.write(line[i])
        outfile.write('\n')
outfile.close()

out = open('network/table.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(out, dialect='excel')

f = open("network/table.txt", "r", encoding='utf-8')
for line in f.readlines():
    #line = line.replace(',', '\t')  # 将每行的逗号替换成空格
    line = line.strip('\n')
    list = line.split('\t')  # 将字符串转为列表，从而可以按单元格写入csv
    csv_writer.writerow(list)