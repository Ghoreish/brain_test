import random
import time
import os
import _thread
import networkx as nx
import matplotlib.pyplot as plt
import cv2

# Defining a Class
class GraphVisualization:

    def __init__(self):
        # visual is a list which stores all
        # the set of edges that constitutes a
        # graph
        self.visual = []

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.DiGraph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()




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

    def pulse_to(self, n, v):
        self.neuron_list[n].vol += int(v)

    def start_pulsing(self):
        for i in self.neuron_list:
            i.send_pulse()

    def make_custom_connection(self, connection_list):
        for i in connection_list:
            x, y = self.neuron_list[i[0]], i[1]
            for j in y:
                x.connect_to(self.neuron_list[j])
        self.synaps = connection_list



def pulser(x):
    while True:
        x.start_pulsing()

def inp(x):
    while True:
        for i in range(10):
            r = random.randint(0, 1)
            x.pulse_to(i, r)


b = Brain(900)
b.make_random_cnnection()
b2 = Brain(900)
b2.make_random_cnnection()
cam = cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    ret2, frame2 = cam.read()
    frame = cv2.resize(frame,(30, 30))
    frame2 = cv2.resize(frame, (30, 30))
    frame3 = cv2.resize(frame, (30, 30))
    n = 0
    for i in frame:
        for j in i:
            b.pulse_to(n, j[0])
            b2.pulse_to(n, j[0])
            n += 1
    b.start_pulsing()
    b2.start_pulsing()
    n = 0
    for i in frame:
        for j in i:
            j[0] = b.neuron_list[n].vol
            j[1], j[2] = 0, 0
            n += 1
    n = 0
    for i in frame2:
        for j in i:
            j[0] = b2.neuron_list[n].vol
            j[1], j[2] = 0, 0
            n += 1
    frame = cv2.resize(frame, (450, 450))
    cv2.imshow('frame', frame)
    frame2 = cv2.resize(frame2, (450, 450))
    cv2.imshow('frame2', frame2)
    frame3 = cv2.resize(frame3, (450, 450))
    cv2.imshow('frame3', frame3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
