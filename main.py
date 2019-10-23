import os
import time
import xlsxwriter as writer
from os.path import join
import copy

from TLBO import TLBO
from Network import Network

data1_dir = 'DataICC\\Sen1'
data2_dir = 'ResultICC\\Sen1'
workbook = writer.Workbook('Result.xlsx')
worksheet = workbook.add_worksheet()

offset = 0
rows = 0
for sub_dir1 in os.listdir(data1_dir):
    des1 = [join(data1_dir, sub_dir1, f) for f in os.listdir(join(data1_dir, sub_dir1))]
    des2 = [join(data2_dir, sub_dir1, f) for f in os.listdir(join(data2_dir, sub_dir1))]
    file_name = os.listdir(join(data2_dir, sub_dir1))
    offset = len(des1)
    row = 0
    for i in range(offset):
        file_path = [des1[i], des2[i]]
        start = time.time()
        # print(file_path)
        net = Network(file_path)
        alg = TLBO(net)
        # if alg.gene_size < 100:
        #     continue
        best_std = alg.loop()
        # print(TLBO.print_best(alg, best))
        best = copy.copy(best_std)
        worst = copy.copy(best_std)
        avg = best.fitness[0]
        for loop in range(1, 20):
            net = Network(file_path)
            alg = TLBO(net)
            best_std = alg.loop()
            avg += best_std.fitness[0]
            if alg.compare(best_std, best) == -1:
                best = copy.copy(best_std)
            if alg.compare(worst, best_std) == -1:
                worst = copy.copy(best_std)
            # print(TLBO.print_best(alg, best))
        print("Best: ", TLBO.print_best(alg, best))
        print("Worst: ", TLBO.print_best(alg, worst))
        avg = round(avg/20, 2)
        time_len = round(time.time() - start, 2)

        worksheet.write(row, 0, file_name[i])
        worksheet.write(row, 1, best.fitness[0])
        worksheet.write(row, 2, round(best.fitness[1], 2))
        worksheet.write(row, 3, worst.fitness[0])
        worksheet.write(row, 4, round(worst.fitness[1], 2))
        worksheet.write(row, 5, avg)
        worksheet.write(row, 6, time_len)
        row += 1
        # break
    # break

workbook.close()

# net = Network(file_path)
# alg = TLBO(net)
#
# best = alg.loop()
#
# # print(best.gene, best.fitness)
#
# print(TLBO.print_best(alg, best))
