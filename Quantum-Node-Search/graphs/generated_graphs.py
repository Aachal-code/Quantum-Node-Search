"""
Graph generation module for Quantum Search project.
Generates various types of graphs: Random, Scale-Free, and Small-World.
"""

import networkx as nx
import random
from typing import Tuple, Dict, Any


class GraphGenerator:
    """Generate different types of graphs for quantum search experiments."""
    
    def __init__(self, seed: int = 42):
        """Initialize graph generator with optional seed for reproducibility."""
        self.seed = seed
        random.seed(seed)
    
    def generate_random_graph(self, n_nodes: int, edge_probability: float = 0.3) -> nx.Graph:
        """
        Generate an Erdős-Rényi random graph.
        
        Args:
            n_nodes: Number of nodes
            edge_probability: Probability of edge between any two nodes
            
        Returns:
            NetworkX Graph object
        """
        return nx.erdos_renyi_graph(n_nodes, edge_probability, seed=self.seed)
    
    def generate_scale_free_graph(self, n_nodes: int) -> nx.Graph:
        """
        Generate a scale-free graph using Barabási-Albert model.
        Models networks where some nodes are highly connected hubs.
        
        Args:
            n_nodes: Number of nodes
            
        Returns:
            NetworkX Graph object
        """
        # m=2 means each new node connects to 2 existing nodes
        return nx.barabasi_albert_graph(n_nodes, m=2, seed=self.seed)
    
    def generate_small_world_graph(self, n_nodes: int, k: int = 4, p: float = 0.3) -> nx.Graph:
        """
        Generate a small-world graph using Watts-Strogatz model.
        Models networks with high clustering and short average path lengths.
        
        Args:
            n_nodes: Number of nodes
            k: Each node is connected to k nearest neighbors
            p: Probability of rewiring edge
            
        Returns:
            NetworkX Graph object
        """
        return nx.watts_strogatz_graph(n_nodes, k, p, seed=self.seed)
    
    def get_graph_stats(self, graph: nx.Graph) -> Dict[str, Any]:
        """
        Calculate and return statistics about the graph.
        
        Args:
            graph: NetworkX Graph object
            
        Returns:
            Dictionary with graph statistics
        """
        return {
            'nodes': graph.number_of_nodes(),
            'edges': graph.number_of_edges(),
            'density': nx.density(graph),
            'average_degree': sum(dict(graph.degree()).values()) / graph.number_of_nodes(),
            'average_shortest_path': nx.average_shortest_path_length(graph) if nx.is_connected(graph) else float('inf'),
            'diameter': nx.diameter(graph) if nx.is_connected(graph) else float('inf'),
            'is_connected': nx.is_connected(graph),
        }
    
    def validate_graph(self, graph: nx.Graph) -> bool:
        """
        Validate that graph is suitable for quantum search.
        
        Args:
            graph: NetworkX Graph object
            
        Returns:
            True if graph is valid, False otherwise
        """
        return (graph.number_of_nodes() > 0 and 
                graph.number_of_edges() >= 0 and
                all(isinstance(node, int) for node in graph.nodes()))


def create_graph(graph_type: str, n_nodes: int, seed: int = 42) -> nx.Graph:
    """
    Convenience function to create a graph of specified type.
    
    Args:
        graph_type: 'random', 'scale_free', or 'small_world'
        n_nodes: Number of nodes
        seed: Random seed
        
    Returns:
        NetworkX Graph object
    """
    generator = GraphGenerator(seed=seed)
    
    if graph_type.lower() == 'random':
        return generator.generate_random_graph(n_nodes)
    elif graph_type.lower() == 'scale_free':
        return generator.generate_scale_free_graph(n_nodes)
    elif graph_type.lower() == 'small_world':
        return generator.generate_small_world_graph(n_nodes)
    else:
        raise ValueError(f"Unknown graph type: {graph_type}")
