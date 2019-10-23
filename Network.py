import numpy as np
from collections import defaultdict


class MC:
    def __init__(self, velocity=5, charging_power=5, init_energy=108000, traveling_power=1):
        self.v = velocity
        self.p = charging_power
        self.init_energy = init_energy
        self.energy = init_energy
        self.pm = traveling_power  # J/m


class Network:
    def __init__(self, file_path, mc=MC()):
        self.file_path = file_path
        self.mc = mc
        # self.moving_path = None
        self.path = np.array([])
        self.number_of_nodes = 0  # nodes are indexed from 1 to number_of_nodes
        self.energy = None
        self.min_e = 540
        self.max_e = 10800
        self.p = None  # energy consumption rate
        self.coordinates = None
        self.bs_pos = np.array([0, 0])
        self.distance_matrix = None
        self.time = 0
        self.total_time = None
        self._initialize()
        self.dead = {i: False for i in range(self.number_of_nodes + 1)}
        self.last_charging_time = [0 for _ in range(self.number_of_nodes + 1)]
        self.moving_time = np.array([0 for _ in range(self.number_of_nodes + 1)])
        self._extract_path()

    def get_fitness(self, solution, printing=False):
        for i in self.dead:
            self.dead[i] = False
        time = 0
        energy = np.copy(self.energy)
        for i in range(1, self.number_of_nodes+1):
            self.last_charging_time[i] = 0
        for i in range(self.number_of_nodes):
            node = self.path[i]
            time += self.moving_time[node]
            energy[node] -= (time - self.last_charging_time[node]) * self.p[node]
            if energy[node] < self.min_e:
                self.dead[node] = True
                continue
            charging_time = min((self.max_e - energy[node]) / (self.mc.p - self.p[node]), solution[i] * self.total_time)
            energy[node] += charging_time * (self.mc.p - self.p[node])
            time += charging_time
            self.last_charging_time[node] = time

        for node in range(1, self.number_of_nodes + 1):
            energy[node] = max(0, energy[node] - self.p[node] * (time - self.last_charging_time[node]))
            if energy[node] < self.min_e and not self.dead[node]:
                self.dead[node] = True

        remaining_time = energy[1:] / self.p[1:]
        dead = 0
        for i in self.dead:
            if self.dead[i]:
                dead += 1
        if printing:
            # dead_node = [i for i in self.dead if self.dead[i]]
            print(solution)
            print(energy)
        return [dead, np.std(remaining_time)]

    def _initialize(self):
        coordinates = [self.bs_pos]
        p = [0.0]
        energy = [0.0]
        f = open(self.file_path[0])
        data = None
        while True:
            data = f.readline().split()
            if len(data) == 0:
                break
            pos = np.array([float(data[0]), float(data[1])])
            p.append(float(data[2]))
            energy.append(float(data[3]))
            # print(i, pos, traveling_power, E_remain)
            coordinates.append(pos)
            self.number_of_nodes += 1
        f.close()
        self.coordinates = coordinates
        self.energy = energy
        self.p = p
        distance_matrix = np.array([[0.0 for _ in range(self.number_of_nodes+1)]for _ in range(self.number_of_nodes+1)])
        fn = lambda pos1, pos2: np.sqrt(sum(t ** 2 for t in (pos1 - pos2)))
        for i in range(self.number_of_nodes):
            for j in range(i + 1, self.number_of_nodes):
                distance_matrix[i, j] = fn(self.coordinates[i], self.coordinates[j])
                distance_matrix[j, i] = distance_matrix[i, j]
        self.distance_matrix = distance_matrix
        # get path
        f = open(self.file_path[1])
        self.path = np.array([int(i) for i in f.readline().split()])
        f.close()
        # print(self.number_of_nodes, self.path)

    def _extract_path(self):
        path_length = 0
        prev = 0
        for i in self.path:
            path_length += self.distance_matrix[prev, i]
            self.moving_time[i] = self.distance_matrix[prev, i] / self.mc.v
            prev = i
        path_length += self.distance_matrix[prev, 0]
        traveling_energy = path_length * self.mc.pm / self.mc.v
        self.mc.energy -= traveling_energy
        charging_energy = self.mc.energy
        self.total_time = self.mc.energy / self.mc.p
        # print("path: {}, traveling: {}\n charging: {}\n time: {}".format(self.path, traveling_energy, charging_energy, self.total_time))

