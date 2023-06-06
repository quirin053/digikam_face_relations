# from digikamdb import Digikam
# Identifier (id) for a person is the tag id
class Person:
    def __init__(self,id, name, anzahl):
        self.id = id
        self.name = name
        self.anzahl = anzahl
        self.connections = {}
        self.most = []

    def add_connection(self, id, count):
        self.connections[id] = count

    def get_connections(self):
        return self.connections

class People:
    def __init__(self,dk):
        self.person_dict = {}
        self.most = []
        self.dk = dk
        self.indexmap = {}
        self.edges = {} # will maybe be moved

    def __iter__(self):
        return iter(self.person_dict.values())
    
    def __len__(self):
        return len(self.person_dict)
    
    def add_person(self, person):
        self.person_dict[person.id] = person

    def get_person(self, n):
        if n in self.person_dict:
            return self.person_dict[n]
        else:
            return 
        
    def get_by_index(self, index):
        if len(self.indexmap) == 0:
            self.indexmap = {i: id for i, id in enumerate(self.person_dict.keys())}
        if index in self.indexmap:
            return self.person_dict[self.indexmap[index]]
        else:
            return None
    
    def count_connections(self, id):
        images1 = self.dk.tags[id].images.all()
        search = (p for p in self.person_dict.keys() if p != id and p not in self.person_dict[id].get_connections().keys())
        for p in search:
            images2 = self.dk.tags[p].images.all()
            count = 0
            one = True if len(images1) < len(images2) else False
            short = images1 if one else images2.copy()
            long = images2.copy() if one else images1
            for i in short:
                if i in long:
                    count += 1
                    long.remove(i)
            self.person_dict[id].add_connection(p, count)
            self.person_dict[p].add_connection(id, count)

    def get_connections(self, id):
        if len(self.person_dict[id].connections) <= len(self.person_dict):
            self.count_connections(id)
        return self.person_dict[id].get_connections()

    def get_most(self, id, n=0, filter=1):
        if id == 'all':
            if len(self.most) == 0:
                most = []
                for p, person in self.person_dict.items():
                    most.append([p,person.anzahl])
                most.sort(key=lambda x: x[1], reverse=True)
                self.most = most
            result = self.most
        else:
            if len(self.person_dict[id].most) == 0:
                most = []
                for p, count in self.get_connections(id).items():
                    most.append([p,count])
                most.sort(key=lambda x: x[1], reverse=True)
                self.person_dict[id].most = most
            result = self.person_dict[id].most
        # returns a list of [id, count] with count >= filter and the first n entries
        # returns all entries if n == 0
        result = [m for m in result if m[1] >= filter]
        if n > 0:
            result = result[:n]
        return result
