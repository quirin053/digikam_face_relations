from digikamdb import Digikam
from dotenv import load_dotenv
import os
import time
import gui
import pandas as pd
import math
import viz
import people as pl

load_dotenv()
dk = Digikam('sqlite:///' + os.getenv('DATABASE_PATH'))

# get all face tags
personen = dk.tags[4]
ptags = [t for t in dk.tags if t in personen]

# create people object
people = pl.People(dk)
#  -> people init?
for p in ptags[2:]:
    people.add_person(pl.Person(p.id, p.name, len(p.images.all())))

for k in people:
    print(k.name + " " + str(k.anzahl))

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

def draw_all(people,filter=1):
    print("draw all")
    # draw a bar chat with the number of images per person
    Menschen = [[people.get_person(p[0]).name,p[1]] for p in people.get_most('all',20,filter)]
    data = [[m[0], m[1]] for m in Menschen]
    bc = viz.Bar_Chart(data, len(dk.images.select().all()), "Alle")
    bc.show()

def draw_selected(people,id,filter=1):
    connections = people.get_most(id,20,filter)
    Menschen = [[people.get_person(p[0]), p[1]] for p in connections]
    data = [[m[0].name, m[1]] for m in Menschen]
    bc = viz.Bar_Chart(data, people.get_person(id).anzahl, people.get_person(id).name)
    bc.show()


def draw_connections(people,mainp,secondp,filter=1,buttons=False):
    df = pd.DataFrame(columns=['source', 'target', 'type', 'weight'])
    edges = people.edges
    # collect persons that will be on the graph
    Menschen = people.get_most('all',n=mainp,filter=filter)
    Menschen = [m[0] for m in Menschen]
    cMenschen = set(Menschen)
    for m in Menschen:
        for p in people.get_most(m,secondp):
            if p[1] > filter:
                cMenschen.add(p[0])

    dMenschen = cMenschen.copy()
    for c in cMenschen:
        dMenschen.remove(c)
        for d in dMenschen:
            if not (c in edges):
                edges[c] = {}
            if not (d in edges[c]):
                cd = people.get_connections(c)[d]
                edges[c][d] = cd
            if edges[c][d] >= 1:
                df = pd.concat([pd.DataFrame({'source': people.get_person(c).name,
                                                'target': people.get_person(d).name,
                                                'type': 'undirected',
                                                'weight': math.log(edges[c][d])},
                                                index=[0]),df], ignore_index=True)
    people.edges = edges
    cg = viz.Connection_Graph(df)
    cg.show(buttons)

class edge_rec:
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

def draw_selected_connections(root,size,filter=1,buttons=False):
    df = pd.DataFrame(columns=['source', 'target', 'type', 'weight'])
    connections = edge_rec(df,size)
    roots = [root]
    selected_connections(roots,connections,filter)
    cg = viz.Connection_Graph(connections.df)
    cg.show(buttons)

root = gui.build(people,draw_all,draw_selected,ptags,draw_connections,draw_selected_connections)
root.mainloop()