import os
import time
import csv
from os.path import join
import copy

from TLBO import TLBO
from Network import Network

# <<<<<<< HEAD
# data1_dir = os.getcwd() + '\\DataICC\\Sen1'
# data2_dir = os.getcwd() + '\\ResultICC\\Sen1'
# =======
data1_dir = os.getcwd() + '/DataICC/Sen1'
data2_dir = os.getcwd() + '/ResultICC/Sen1'
# >>>>>>> de629cf682ca0fd65605642c77f213af86bb6fbd
# print(data2_dir)
if "result.csv" not in os.listdir(os.getcwd()):
    with open("result.csv", mode="w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['File Name', 'Best - Num Dead', 'Best - Std of Remaining Time',
                         'Worst - Num Dead', 'Worst - Std of Remaining Time', 'Average num dead', 'Time Execute'])

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
        if alg.gene_size < 100:
            continue
        best_std = alg.loop()
        # print(TLBO.print_best(alg, best))
        best = copy.copy(best_std)
        worst = copy.copy(best_std)
        avg = best.fitness[0]
        for loop in range(1, 30):
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
        avg = round(avg/30, 2)
        time_len = round(time.time() - start, 2)
        with open("result.csv", mode="a") as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([file_name[i], best.fitness[0], round(best.fitness[1], 2),
                         worst.fitness[0], round(worst.fitness[1], 2), avg, time_len])

        # break
    # break

# net = Network(file_path)
# alg = TLBO(net)
#
# best = alg.loop()
#
# # print(best.gene, best.fitness)
#
# print(TLBO.print_best(alg, best))
