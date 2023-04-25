import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import networkx as nx
import pandas as pd
import math
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
        plt.bar(x, [m.anzahl for m in self.data])
        plt.bar_label(plt.bar(x, [m.anzahl for m in self.data]), padding=3)
        # bottom space for the x labels
        plt.subplots_adjust(bottom=0.27)
        plt.xticks(x, [m.name for m in self.data], rotation=90)
        # display the total number of images for this person in the title
        plt.title(self.title + " (" + str(self.anzahl) + ")")
        plt.show()

# class Connection_Graph: