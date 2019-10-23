""" Designed for continuous object"""
import numpy as np
import random
import copy
import functools
from Network import Network


class Student:
    def __init__(self, gene):
        self.gene = gene
        self.fitness = None

    def set_fitness(self, fitness):
        self.fitness = fitness


class TLBO:
    def __init__(self, net: Network, pop_size=150, learning_rate=0.5, loop_size=300):
        self.lr = learning_rate  # learning rate
        self.loop_size = loop_size
        self.net = net
        self.gene_size = self.net.number_of_nodes
        self.class_size = pop_size
        self.students = []
        for _ in range(self.class_size):
            self.students.append(Student(self._generate_student()))
        self.comparator = functools.cmp_to_key(lambda std1, std2: self.compare(std1, std2))
        self.best_student = random.choice(self.students)
        self.global_root = copy.deepcopy(self.best_student)

    def _generate_student(self):
        counter = 0
        summ = 0
        gene = np.array([0.0 for _ in range(self.gene_size)])
        while counter < self.gene_size-1:
            mean = (1-summ)/(self.gene_size-counter)
            gene[counter] = np.random.uniform(0.0 * mean, 2.0 * mean)
            summ += gene[counter]
            counter += 1
        gene[counter] = (1-summ)/(self.gene_size-counter)
        return gene

    def get_fitness(self, student):
        return self.net.get_fitness(student.gene)

    def print_best(TLBO, student):
        return TLBO.net.get_fitness(student.gene, True)

    def set_class_fitness(self):
        for i in range(self.class_size):
            self.students[i].set_fitness(self.get_fitness(self.students[i]))

    def compare(self, student1: Student, student2: Student):
        if student1.fitness[0] == student2.fitness[0]:
            if student1.fitness[1] < student2.fitness[1]:
                return -1
        else:
            if student1.fitness[0] < student2.fitness[0]:
                return -1
        return 1

    def sort(self):
        sorted(self.students, key=self.comparator)

    def get_best_student(self):
        return self.students[0]

    def learn(self):
        self.sort()
        best_student = self.get_best_student()
        for student in self.students:
            lr = np.random.uniform(0, self.lr)
            student.gene += lr * (best_student.gene - student.gene)

        self.set_class_fitness()

        for i in range(self.class_size):
            student1, student2 = random.choices(self.students, k=2)
            if self.compare(student2, student1):
                student1, student2 = student2, student1
            lr = np.random.uniform(0, self.lr)
            student2.gene += lr * (student1.gene - student2.gene)
        self.set_class_fitness()

    def loop(self):
        self.set_class_fitness()
        # for std in self.students:
        #     print(std.gene, std.fitness)
        self.global_root.set_fitness(self.get_fitness(self.global_root))
        for _ in range(self.loop_size):
            self.learn()
            if not self.compare(self.best_student, self.global_root):
                self.global_root = copy.deepcopy(self.best_student)

        return self.global_root
