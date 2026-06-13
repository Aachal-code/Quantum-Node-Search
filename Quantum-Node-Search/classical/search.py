"""
Classical search algorithms for finding a target node.
Includes Linear, BFS, and DFS search with performance metrics.
"""

import time
from typing import Tuple, List, Set


class LinearSearch:
    """Linear search through graph nodes."""
    
    def __init__(self, nodes: List[int]):
        """Initialize with list of nodes."""
        self.nodes = nodes
    
    def search(self, target: int) -> Tuple[bool, int, float, List[int]]:
        """
        Perform linear search for target node.
        
        Args:
            target: Target node to find
            
        Returns:
            (found, nodes_checked, execution_time, path)
        """
        start_time = time.time()
        nodes_checked = []
        
        for node in self.nodes:
            nodes_checked.append(node)
            if node == target:
                execution_time = time.time() - start_time
                return True, len(nodes_checked), execution_time, nodes_checked
        
        execution_time = time.time() - start_time
        return False, len(nodes_checked), execution_time, nodes_checked


class BFSSearch:
    """Breadth-First Search implementation."""
    
    def __init__(self, graph):
        """Initialize with NetworkX graph."""
        self.graph = graph
    
    def search(self, start: int, target: int) -> Tuple[bool, int, float, List[int]]:
        """
        Perform BFS to find target node.
        
        Args:
            start: Starting node
            target: Target node to find
            
        Returns:
            (found, nodes_checked, execution_time, path)
        """
        start_time = time.time()
        
        queue = [start]
        visited: Set[int] = {start}
        nodes_checked = [start]
        parent = {start: None}
        
        while queue:
            current = queue.pop(0)
            
            if current == target:
                execution_time = time.time() - start_time
                # Reconstruct path
                path = []
                node = target
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                return True, len(nodes_checked), execution_time, path
            
            for neighbor in self.graph.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    nodes_checked.append(neighbor)
                    parent[neighbor] = current
        
        execution_time = time.time() - start_time
        return False, len(nodes_checked), execution_time, nodes_checked


class DFSSearch:
    """Depth-First Search implementation."""
    
    def __init__(self, graph):
        """Initialize with NetworkX graph."""
        self.graph = graph
    
    def search(self, start: int, target: int) -> Tuple[bool, int, float, List[int]]:
        """
        Perform DFS to find target node.
        
        Args:
            start: Starting node
            target: Target node to find
            
        Returns:
            (found, nodes_checked, execution_time, path)
        """
        start_time = time.time()
        
        stack = [start]
        visited: Set[int] = {start}
        nodes_checked = [start]
        parent = {start: None}
        
        while stack:
            current = stack.pop()
            
            if current == target:
                execution_time = time.time() - start_time
                # Reconstruct path
                path = []
                node = target
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                return True, len(nodes_checked), execution_time, path
            
            for neighbor in self.graph.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    nodes_checked.append(neighbor)
                    parent[neighbor] = current
        
        execution_time = time.time() - start_time
        return False, len(nodes_checked), execution_time, nodes_checked


def run_classical_search(graph, target: int, method: str = 'linear') -> dict:
    """
    Run classical search and return results.
    
    Args:
        graph: NetworkX graph
        target: Target node
        method: 'linear', 'bfs', or 'dfs'
        
    Returns:
        Dictionary with search results
    """
    nodes = sorted(list(graph.nodes()))
    
    if method == 'linear':
        searcher = LinearSearch(nodes)
        found, checked, time_taken, path = searcher.search(target)
    elif method == 'bfs':
        searcher = BFSSearch(graph)
        # Find any starting node
        start = nodes[0]
        found, checked, time_taken, path = searcher.search(start, target)
    elif method == 'dfs':
        searcher = DFSSearch(graph)
        start = nodes[0]
        found, checked, time_taken, path = searcher.search(start, target)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return {
        'method': method,
        'found': found,
        'nodes_checked': checked,
        'execution_time': time_taken,
        'path': path,
        'complexity': 'O(N)'
    }
