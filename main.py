from digikamdb import Digikam
from dotenv import load_dotenv
import os
import time
import tkinter as tk
from tkinter import ttk
import pandas as pd
import math
import viz

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

    def draw_barchart(self, ptags,filter=1):
        self.count_connections(ptags,filter)
        
        cMenschen = [Personentag(k, dk.tags[k].name, v) for k, v in self.connections.items()]
        cMenschen.sort(key=lambda x: x.anzahl, reverse=True)
        cMenschen = cMenschen[:21]

        bc = viz.Bar_Chart(cMenschen, self.anzahl, self.name)
        bc.show()

    def count_connections(self,ptags,filter=1):
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
    bc = viz.Bar_Chart(Menschen, len(dk.images.select().all()), "Alle")
    bc.show()


def draw_connections(Menschen,mainp,secondp,filter,buttons): # TODO Draw connections between all people that are considered
    Menschen = Menschen[:mainp]
    df = pd.DataFrame(columns=['source', 'target', 'type', 'weight'])
    for m in Menschen:
        m.count_connections(ptags,filter)
        cMenschen = [Personentag(k, dk.tags[k].name, v) for k, v in m.connections.items()]
        cMenschen.sort(key=lambda x: x.anzahl, reverse=True)
        # only the first 20 elements
        cMenschen = cMenschen[:secondp]
        for c in cMenschen:
            df = pd.concat([pd.DataFrame({'source': m.name, 'target': c.name, 'type': 'undirected', 'weight': math.log(c.anzahl)}, index=[0]),df], ignore_index=True)
    cg = viz.Connection_Graph(df)
    cg.show(buttons)

class connection_rec:
    def __init__(self, dataframe, number):
        self.df = dataframe
        self.number = number

def selected_connections(roots,con,filter):
    if con.number > 0:
        cMenschen = []
        for root in roots:
            root.count_connections(ptags,filter)
            ccMenschen = [[root, Personentag(k, dk.tags[k].name, v)] for k, v in root.connections.items()]
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

def draw_selected_connections(root,number,filter,buttons):
    df = pd.DataFrame(columns=['source', 'target', 'type', 'weight'])
    connections = connection_rec(df,number)
    roots = [root]
    selected_connections(roots,connections,filter)
    cg = viz.Connection_Graph(connections.df)
    cg.show(buttons)

# GUI
root = tk.Tk()
root.title("Digikam Face Ralations")

tabControl = ttk.Notebook(root)
tabAppearances = ttk.Frame(tabControl)
tabConnections = ttk.Frame(tabControl)
tabHistory = ttk.Frame(tabControl)
tabControl.add(tabAppearances, text='Appearances')
tabControl.add(tabConnections, text='Relations')
tabControl.add(tabHistory, text='History')
tabControl.pack(expand = 1, fill ="both")

comboAppearances = ttk.Combobox(tabAppearances, values=[m.name for m in Menschen], state="readonly")
comboAppearances.current(0)
comboAppearances.pack()
cutoffAppearances = tk.Entry(tabAppearances)
cutoffAppearances.insert(0, "5")
button_draw = tk.Button(tabAppearances, text="draw for selected")
button_draw.pack()

button_draw.bind("<Button-1>", lambda button: Menschen[comboAppearances.current()].draw_barchart(ptags,filter=int(cutoffAppearances.get())))
button_drawall = tk.Button(tabAppearances, text="draw all")
button_drawall.bind("<Button-1>", lambda button: draw_all(Menschen,int(cutoffAppearances.get())))
button_drawall.pack()

button_drawconnections = tk.Button(tabConnections, text="draw connections")
mainp = tk.Entry(tabConnections)
mainp.insert(0, "10")
mainp.pack()
secondp = tk.Entry(tabConnections)
secondp.insert(0, "10")
secondp.pack()
button_drawconnections.pack()
show_buttons = tk.BooleanVar()
cb_buttons = tk.Checkbutton(tabConnections, text="Graph Buttons", variable=show_buttons, onvalue=True, offvalue=False)

button_drawconnections.bind("<Button-1>", lambda button: draw_connections(Menschen,int(mainp.get()),int(secondp.get()),int(cutoffAppearances.get()),show_buttons.get()))

entry_graphsize = tk.Entry(tabConnections)
entry_graphsize.insert(0, "20")
entry_graphsize.pack()
button4 = tk.Button(tabConnections, text="connections for selected")
button4.bind("<Button-1>", lambda button: draw_selected_connections(Menschen[comboAppearances.current()],int(entry_graphsize.get()),int(cutoffAppearances.get()),show_buttons.get()))
button4.pack()
cutoffAppearances.pack()
cb_buttons.pack()
root.mainloop()