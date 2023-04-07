from digikamdb import Digikam
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import os
import time
import tkinter as tk
from tkinter import ttk
import networkx as nx
import pandas as pd
import math
import pyvis.network as net

load_dotenv()
dk = Digikam('sqlite:///' + os.getenv('DATABASE_PATH'))

# get all face tags
personen = dk.tags[4]
ptags = [t for t in dk.tags if t in personen]


class Personentag:
    def __init__(self,id, name, anzahl):
        self.id = id
        self.name = name
        self.anzahl = anzahl

    def draw_barchart(self, Menschen):
        # draw a bar chat with the number of images per person
        x = np.arange(len(Menschen))
        plt.bar(x, [m.anzahl for m in Menschen])
        plt.bar_label(plt.bar(x, [m.anzahl for m in Menschen]), padding=3)
        # bottom space for the x labels
        plt.subplots_adjust(bottom=0.27)
        plt.xticks(x, [m.name for m in Menschen], rotation=90)
        # display the total number of images for this person in the title
        plt.title(self.name + " (" + str(self.anzahl) + ")")
        plt.show()

    def count_connections(self,ptags,drawing=True):
        print("count connections for " + self.name)
        # dictionary with the number of images and the other person id
        
        self.connections = {}
        # get all images with this person
        images2 = dk.tags[self.id].images.all()
        start_time = time.time()
        # count connections
        for p in ptags:
            images1 = dk.tags[p.id].images.all()
            count = 0
            one = True if len(images1) < len(images2) else False
            short = images1 if one else images2.copy()
            long = images2.copy() if one else images1
            for i in short:
                if i in long:
                    count += 1
                    long.remove(i)
            self.connections.update({p.id: count})

        end_time = time.time()
        duration = end_time - start_time
        print(f"Dauer der Operation: {duration} Sekunden")


        # delete all elements in connections with value = 0 and exclude the person itself
        self.connections = {k: v for k, v in self.connections.items() if v != 0 and k != self.id}
        print(self.connections)

        cMenschen = [Personentag(k, dk.tags[k].name, v) for k, v in self.connections.items()]
        cMenschen.sort(key=lambda x: x.anzahl, reverse=True)
        # only the first 20 elements
        cMenschen = cMenschen[:21]
        if drawing:
            self.draw_barchart(cMenschen)




Menschen = []
for x in range (2,len(ptags)):
    z = len(ptags[x].images.all())
    Menschen.append(Personentag(ptags[x].id, ptags[x].name, z))
Menschen.sort(key=lambda x: x.anzahl, reverse=True)

def draw_all(Menschen):
    print("draw all")
    # draw a bar chat with the number of images per person
    # delete all elements in Menschen with anzahl < 10
    Menschen = [m for m in Menschen if m.anzahl > 10]
    # sort the list by anzahl
    Menschen.sort(key=lambda x: x.anzahl, reverse=True)
    # only the first 20 elements
    Menschen = Menschen[:20]
    alle = Personentag(4, "alle", len(dk.images.select().all()))
    alle.draw_barchart(Menschen)


def draw_connections(Menschen,mainp,secondp):
    Menschen = Menschen[:mainp]
    df = pd.DataFrame(columns=['source', 'target', 'type', 'weight'])
    for m in Menschen:
        m.count_connections(ptags,False)
        cMenschen = [Personentag(k, dk.tags[k].name, v) for k, v in m.connections.items()]
        cMenschen.sort(key=lambda x: x.anzahl, reverse=True)
        # only the first 20 elements
        cMenschen = cMenschen[:secondp]
        for c in cMenschen:
            df = pd.concat([pd.DataFrame({'source': m.name, 'target': c.name, 'type': 'undirected', 'weight': math.log(c.anzahl)}, index=[0]),df], ignore_index=True)
    G = nx.from_pandas_edgelist(df, source='source', target='target', edge_attr='weight')
    
    nt = net.Network(notebook=True)
    nt.from_nx(G)
    nt.show_buttons(filter_=['physics'])
    nt.show("test.html")


# GUI
root = tk.Tk()
combo = ttk.Combobox(root, values=[m.name for m in Menschen])
combo.pack()

button1 = tk.Button(root, text="draw for this person")
button1.pack()

button1.bind("<Button-1>", lambda button: Menschen[combo.current()].count_connections(ptags))
button2 = tk.Button(root, text="draw for all persons")
button2.bind("<Button-1>", lambda button: draw_all(Menschen))
button2.pack()
button3 = tk.Button(root, text="draw connections")


mainp = tk.Entry(root)
mainp.pack()
secondp = tk.Entry(root)
secondp.pack()
button3.pack()

button3.bind("<Button-1>", lambda button: draw_connections(Menschen,int(mainp.get()),int(secondp.get())))
root.mainloop()

