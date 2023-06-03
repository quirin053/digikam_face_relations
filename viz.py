import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import networkx as nx
import pyvis.network as net
import webbrowser

class Bar_Chart:
    def __init__(self, data, anzahl=0, title=""):
        self.data = data
        self.title = title
        self.anzahl = anzahl
    
    def show(self):
        # draw a bar chat with the number of images per person
        x = np.arange(len(self.data))
        plt.bar(x, [m[1] for m in self.data])
        plt.bar_label(plt.bar(x, [m[1] for m in self.data]), padding=3)
        # bottom space for the x labels
        plt.subplots_adjust(bottom=0.27)
        plt.xticks(x, [m[0] for m in self.data], rotation=90)
        # display the total number of images for this person in the title
        plt.title(self.title + " (" + str(self.anzahl) + ")")
        plt.show()

class Connection_Graph:
    def __init__(self, data):
        self.data = data
        G = nx.from_pandas_edgelist(self.data, source='source', target='target', edge_attr='weight')
        self.nt = net.Network(notebook=True)
        self.nt.from_nx(G)

    def show(self, buttons=False):
        if buttons: self.nt.show_buttons()
        self.nt.show("relations.html")
        webbrowser.open("relations.html",new=2)