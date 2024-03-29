import random
import json


class Neuron:
    def __init__(self):
        self.vol = 0
        self.connections = []

    def connect_to(self, x):
        self.connections.append(x)

    def connector(self, neuron_list):
        n = random.randint(1, len(neuron_list))
        self.connection_no_list = []
        while self.connection_no_list == []:
            for i in range(n):
                selecter_no = random.randint(0, len(neuron_list) - 1)
                selected = neuron_list[selecter_no]
                if selected != self:
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

    def pulse_to(self, n, v=10):
        self.neuron_list[n].vol += v

    def start_pulsing(self):
        for i in self.neuron_list:
            i.send_pulse()

    def make_custom_connection(self, connection_list):
        for i in connection_list:
            x, y = self.neuron_list[i[0]], i[1]
            for j in y:
                x.connect_to(self.neuron_list[j])
        self.synaps = connection_list

    def output(self, *args):
        output_list = []
        for i in args:
            output_list.append(self.neuron_list[i].vol)
        if len(output_list) == 1:
            return output_list[0]
        else:
            return output_list

    def reset(self):
        for i in self.neuron_list:
            i.vol = 0

    def save(self):
        return json.dumps(self.synaps)

    def load(self, syn: str):
        synaps = json.loads(syn)
        self.make_custom_connection(synaps)


def breed(x: Brain, y: Brain):
    neuron_len = len(x.neuron_list)
    z = Brain(neuron_len)
    slicer = random.randint(0, neuron_len - 1)
    new_synaps = x.synaps[:slicer] + y.synaps[slicer:]
    z.make_custom_connection(new_synaps)
    return z


def mut(x: Brain):
    neuron_len = len(x.neuron_list)
    random_selected = random.randint(0, neuron_len - 1)
    y = Brain(neuron_len)
    y.make_random_cnnection()
    z = Brain(neuron_len)
    l = x.synaps
    l[random_selected] = y.synaps[random_selected]
    z.make_custom_connection(l)
    return z
