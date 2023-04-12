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
import webbrowser

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

    def count_connections(self,ptags,filter=1,drawing=True):
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


        # delete all elements in connections with value < filter and exclude the person itself
        self.connections = {k: v for k, v in self.connections.items() if v >= filter and k != self.id}
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

def draw_all(Menschen,filter):
    print("draw all")
    # draw a bar chat with the number of images per person
    Menschen = [m for m in Menschen if m.anzahl > filter]
    # sort the list by anzahl
    Menschen.sort(key=lambda x: x.anzahl, reverse=True)
    # only the first 20 elements
    Menschen = Menschen[:20]
    alle = Personentag(4, "alle", len(dk.images.select().all()))
    alle.draw_barchart(Menschen)


def draw_connections(Menschen,mainp,secondp,filter): # TODO Draw connections between all people that are considered
    Menschen = Menschen[:mainp]
    df = pd.DataFrame(columns=['source', 'target', 'type', 'weight'])
    for m in Menschen:
        m.count_connections(ptags,False)
        cMenschen = [Personentag(k, dk.tags[k].name, v) for k, v in m.connections.items() if v >=filter]
        cMenschen.sort(key=lambda x: x.anzahl, reverse=True)
        # only the first 20 elements
        cMenschen = cMenschen[:secondp]
        for c in cMenschen:
            df = pd.concat([pd.DataFrame({'source': m.name, 'target': c.name, 'type': 'undirected', 'weight': math.log(c.anzahl)}, index=[0]),df], ignore_index=True)
    G = nx.from_pandas_edgelist(df, source='source', target='target', edge_attr='weight')
    
    nt = net.Network(notebook=True)
    nt.from_nx(G)
    nt.show_buttons(filter_=['physics'])
    nt.show("relations.html")
    webbrowser.open("relations.html",new=2)

class connection_rec:
    def __init__(self, dataframe, number):
        self.df = dataframe
        self.number = number

def selected_connections(roots,con,filter):
    if con.number > 0:
        cMenschen = []
        for root in roots:
            root.count_connections(ptags, False) # TODO in count_connections standardmäßig nicht zeichnen, zeichnen in separate Funktion auslagern
            ccMenschen = [[root, Personentag(k, dk.tags[k].name, v)] for k, v in root.connections.items() if v >= filter]
            cMenschen.extend(ccMenschen)
        cMenschen.sort(key=lambda x: x[1].anzahl, reverse=True)
        i = 0
        while con.number > 0 and i < len(cMenschen):
            con.df = pd.concat([pd.DataFrame({'source': cMenschen[i][0].name, 'target': cMenschen[i][1].name, 'type': 'undirected', 'weight': math.log(cMenschen[i][1].anzahl)}, index=[0]),con.df], ignore_index=True)
            con.number -= 1
            i += 1
        if con.number > 0:
            # call function again with the secend element of each element in cMenschen
            roots = [x[1] for x in cMenschen]
            selected_connections(roots,con,filter)
    return

def draw_selected_connections(root,number,filter):
    df = pd.DataFrame(columns=['source', 'target', 'type', 'weight'])
    connections = connection_rec(df,number)
    roots = [root]
    selected_connections(roots,connections,filter)
    G = nx.from_pandas_edgelist(connections.df, source='source', target='target', edge_attr='weight')    
    nt = net.Network(notebook=True)
    nt.from_nx(G)
    # nt.show_buttons(filter_=['physics'])
    nt.show("relations.html")
    webbrowser.open("relations.html",new=2)

# GUI
root = tk.Tk()
combo = ttk.Combobox(root, values=[m.name for m in Menschen], state="readonly")
combo.current(0)
combo.pack()
entry4 = tk.Entry(root)
entry4.insert(0, "5")
button1 = tk.Button(root, text="draw for selected")
button1.pack()

button1.bind("<Button-1>", lambda button: Menschen[combo.current()].count_connections(ptags,int(entry4.get())))
button2 = tk.Button(root, text="draw for all")
button2.bind("<Button-1>", lambda button: draw_all(Menschen,int(entry4.get())))
button2.pack()
button3 = tk.Button(root, text="draw connections")


mainp = tk.Entry(root)
mainp.insert(0, "10")
mainp.pack()
secondp = tk.Entry(root)
secondp.insert(0, "10")
secondp.pack()
button3.pack()

button3.bind("<Button-1>", lambda button: draw_connections(Menschen,int(mainp.get()),int(secondp.get()),int(entry4.get())))

entry3 = tk.Entry(root)
entry3.insert(0, "20")
entry3.pack()
button4 = tk.Button(root, text="connections for selected")
button4.pack()
button4.bind("<Button-1>", lambda button: draw_selected_connections(Menschen[combo.current()],int(entry3.get()),int(entry4.get())))


entry4.pack()
root.mainloop()

# TODO cutoff: add filter to only show for people with more than x images