import ANNarchy as ann

class Graph:
    def __init__(self):
        self.G = {'nodes':[], 'edges':[]}
        for pop in ann.populations():
            self.add_node(pop)
        for proj in ann.projections():
            self.add_edge(proj)

    def get_graph(self):
        return self.G

    def add_node(self, pop):
        self.G['nodes'].append({
            'data': {
                'label':f"{pop.name}\n{pop.geometry}",
                'id':pop.name,
            },
        })

    def add_edge(self, proj):
        self.G['edges'].append({
            'data': {
                'id': f"{proj.pre.name}_{proj.post.name}_{proj.target}",
                'source':proj.pre.name,
                'target':proj.post.name,
                'label':proj.name,
            },
            'classes': proj.target,
        })
