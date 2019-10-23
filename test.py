import functools
def compare(student1, student2):
    if student1[0] == student2[0]:
        if student1[1] < student2[1]:
            return 1
    else:
        if student1[0] > student2[0]:
            return 1
    return -1

comparator = functools.cmp_to_key(lambda std1, std2: compare(std1, std2))

l = [[1,2], [0,7], [2,7], [0,6]]

l = sorted(l, key = comparator)
print(l)
