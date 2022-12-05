import random
import time
import os

class Neuron:
    def __init__(self):
        self.vol = 0
        self.connections = []

    def connect_to(self, x):
        self.connections.append(x)

    def connector(self, neuron_list):
        n = random.randint(0, len(neuron_list))
        self.connection_no_list = []
        for i in range(n):
            selecter_no = random.randint(0, len(neuron_list) - 1)
            selected = neuron_list[selecter_no]
            if selected != self and selected not in self.connections and self not in selected.connections:
                self.connect_to(selected)
                self.connection_no_list.append(selecter_no)

    def send_pulse(self):
        n = len(self.connections)
        while True:
            if n == 0:
                break
            for i in range(n):
                if self.vol >= 2:
                    self.connections[i].vol += 1
                    self.vol -= 2
                else:
                    break
            if self.vol < 2:
                break

class Brain:
    def __init__(self, n):
        self.neuron_list = []
        for i in range(n):
            self.neuron_list.append(Neuron())

    def make_random_cnnection(self):
        n = len(self.neuron_list)
        for i in self.neuron_list:
            i.connector(self.neuron_list)
        self.synaps = []
        for i in range(n):
            selecter = self.neuron_list[i]
            self.synaps.append((i, selecter.connection_no_list))

    def pulse_to(self, n):
        self.neuron_list[n].vol += 10

    def start_pulsing(self):
        for i in self.neuron_list:
            i.send_pulse()

    def make_custom_connection(self, connection_list):
        for i in connection_list:
            x, y = self.neuron_list[i[0]], i[1]
            for j in y:
                x.connect_to(self.neuron_list[j])
        self.synaps = connection_list


b = Brain(100)
b.make_random_cnnection()
for i in range(2):
    b.pulse_to(i)
n = 0
l = ''
num = 1
while True:
    print(num)
    num += 1
    for i in b.neuron_list:
        l += '  ' + str(i.vol)
        n += 1
        if n == 10:
            print(l)
            l = ''
            n = 0
    print('\n\n')
    b.start_pulsing()
    for i in range(2):
        b.pulse_to(i)
