"""
Root Cause Analysis using Service Dependency Graph
Graph traversal + blast radius computation
"""

import networkx as nx
import pandas as pd
import numpy as np

class RootCauseAnalyzer:
    def __init__(self, service_meta):
        self.services = service_meta['services']
        self.deps = service_meta['dependencies']
        self.graph = self._build_graph()
    
    def _build_graph(self):
        G = nx.DiGraph()
        for service in self.services:
            G.add_node(service)
        
        for parent, children in self.deps.items():
            for child in children:
                G.add_edge(parent, child)  # Edge direction: parent → child
        
        return G
    
    def analyze(self, anomalies_df):
        """Find root causes and blast radius"""
        anomalous_services = anomalies_df.columns[anomalies_df.iloc[-1] > 0].tolist()
        
        root_causes = []
        blast_radii = {}
        
        for service in anomalous_services:
            # Find root causes (services with no incoming edges from other anomalies)
            predecessors = list(self.graph.predecessors(service))
            anomaly_preds = [p for p in predecessors if p in anomalous_services]
            
            if not anomaly_preds:  # No anomalous predecessors = root cause
                root_causes.append(service)
            
            # Compute blast radius (downstream impact)
            downstream = nx.descendants(self.graph, service)
            blast_radii[service] = len(downstream)
        
        return root_causes, blast_radii
    
    def get_graph_visualization(self, anomalous_services=None):
        """Graph viz data for dashboard"""
        pos = nx.spring_layout(self.graph, k=1, iterations=50)
        
        if anomalous_services:
            anomalous_set = set(anomalous_services)
            node_colors = ['red' if node in anomalous_set else 'lightblue' 
                          for node in self.graph.nodes]
        else:
            node_colors = 'lightblue'
            
        return {
            'pos': pos,
            'nodes': list(self.graph.nodes),
            'edges': list(self.graph.edges),
            'colors': node_colors
        }