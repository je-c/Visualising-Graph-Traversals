import sys
import random
import string
import pprint
from .graph import Graph
import pandas as pd
# from tests import UnitTest

class InitialiseNetwork(Graph):

    def __init__(self):
        super().__init__()
        possible_names = list(string.ascii_uppercase)
        Nodes = [self.insert_vertex(0, 0, possible_names[0])]
        depth, branching_complexity = [random.randint(2,5) for i in range(2)]
        for i in range(depth*branching_complexity):
            Nodes.append(
                self.insert_vertex(
                    random.randint(-10, 10),
                    random.randint(-10, 10),
                    possible_names[i]
                )
            )

        num_nodes = len(Nodes)
        for node in Nodes:
            for i in random.sample(range(num_nodes), random.randint(0, branching_complexity)):
                if not node.name == Nodes[i].name:
                    self.insert_edge(
                        node,
                        Nodes[i]
                    )
        # idx = random.randint(0,num_nodes)
        # start, finish = Nodes[0], Nodes[idx]
        # print(f'Finding path between nodes at index 0, {idx}')
        # print(
        #     G.find_path(
        #         start,
        #         finish
        #     )
        # )

    def to_adjMat(self):
        """
        Generates the initial adjacency matrix (tight matrix) of a businesses suppliers
        
        Args:
            customers (list(str)): list of names of businesses (customers in this scenario)
            suppliers_per_business (list(list(str))): list of suppliers per business
            
        Returns:
            Transpose of matrix such that each row i is a supplier, and each column j is a customer
            Dictionary of suppliers for each business (sanity check)
        """
        incident = {
            vert.name: [
                self.opposite(e, vert).name for e in vert.edges
            ] for vert in self._vertices
        }

        adj_matrix = {
            vert.name: {
                incd_v.name: 1 if incd_v.name in incident[vert.name] else 0 for incd_v in self._vertices
            } for vert in self._vertices
        }
        
        return incident

    def get_elements(self):
        return [v.name for v in self._vertices], self.to_adjMat()
