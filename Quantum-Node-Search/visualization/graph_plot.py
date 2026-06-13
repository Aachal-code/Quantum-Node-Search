"""
Visualization utilities for graph and search results.
"""

import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Dict, Tuple, Optional
import numpy as np


class GraphVisualizer:
    """Visualize graphs and search results."""
    
    @staticmethod
    def plot_graph(
        graph: nx.Graph,
        target_node: Optional[int] = None,
        visited_nodes: Optional[List[int]] = None,
        path: Optional[List[int]] = None,
        title: str = "Graph Visualization",
        figsize: Tuple[int, int] = (10, 8)
    ) -> plt.Figure:
        """
        Plot a graph with optional highlighting.
        
        Args:
            graph: NetworkX graph
            target_node: Target node to highlight in red
            visited_nodes: List of visited nodes to highlight in yellow
            path: Path to highlight in green
            title: Plot title
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Use spring layout for better visualization
        pos = nx.spring_layout(graph, k=0.5, iterations=50, seed=42)
        
        # Draw all nodes (default blue)
        node_colors = ['lightblue'] * graph.number_of_nodes()
        
        # Color visited nodes (yellow)
        if visited_nodes:
            for node in visited_nodes:
                if node in graph.nodes():
                    node_colors[node] = 'lightyellow'
        
        # Color path nodes (green)
        if path:
            for node in path:
                if node in graph.nodes():
                    node_colors[node] = 'lightgreen'
        
        # Color target node (red)
        if target_node is not None and target_node in graph.nodes():
            node_colors[target_node] = 'lightcoral'
        
        # Draw network
        nx.draw_networkx_nodes(
            graph, pos, node_color=node_colors, node_size=500, ax=ax
        )
        nx.draw_networkx_edges(graph, pos, alpha=0.3, ax=ax)
        nx.draw_networkx_labels(graph, pos, font_size=8, ax=ax)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='lightblue', label='Normal nodes'),
            Patch(facecolor='lightyellow', label='Visited nodes'),
            Patch(facecolor='lightgreen', label='Path'),
            Patch(facecolor='lightcoral', label='Target node'),
        ]
        ax.legend(handles=legend_elements, loc='upper left')
        
        return fig
    
    @staticmethod
    def plot_search_comparison(
        results: Dict,
        title: str = "Classical vs Quantum Search Comparison",
        figsize: Tuple[int, int] = (14, 5)
    ) -> plt.Figure:
        """
        Plot comparison between classical and quantum searches.
        
        Args:
            results: Dictionary with search results
            title: Plot title
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        # Extract data
        classical = results.get('classical', {})
        quantum = results.get('quantum', {})
        
        # Plot 1: Nodes Checked
        methods = ['Classical\n(Linear)', 'Quantum\n(Grover)']
        nodes_checked = [
            classical.get('nodes_checked', 0),
            quantum.get('nodes_checked', 0)
        ]
        colors = ['#3498db', '#e74c3c']
        axes[0].bar(methods, nodes_checked, color=colors)
        axes[0].set_ylabel('Nodes Checked', fontsize=11)
        axes[0].set_title('Nodes Inspected', fontsize=12, fontweight='bold')
        axes[0].grid(axis='y', alpha=0.3)
        for i, v in enumerate(nodes_checked):
            axes[0].text(i, v, str(int(v)), ha='center', va='bottom')
        
        # Plot 2: Execution Time
        times = [
            classical.get('execution_time', 0) * 1000,  # Convert to ms
            quantum.get('execution_time', 0) * 1000
        ]
        axes[1].bar(methods, times, color=colors)
        axes[1].set_ylabel('Execution Time (ms)', fontsize=11)
        axes[1].set_title('Execution Time', fontsize=12, fontweight='bold')
        axes[1].grid(axis='y', alpha=0.3)
        for i, v in enumerate(times):
            axes[1].text(i, v, f'{v:.4f}ms', ha='center', va='bottom')
        
        # Plot 3: Success Probability
        success = [100, quantum.get('success_probability', 0)]
        axes[2].bar(methods, success, color=colors)
        axes[2].set_ylabel('Success Probability (%)', fontsize=11)
        axes[2].set_title('Success Probability', fontsize=12, fontweight='bold')
        axes[2].set_ylim([0, 105])
        axes[2].grid(axis='y', alpha=0.3)
        for i, v in enumerate(success):
            axes[2].text(i, v, f'{v:.1f}%', ha='center', va='bottom')
        
        fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        return fig


def plot_graph(graph, target_node=None, visited_nodes=None, path=None, title="Graph"):
    """Convenience function to plot graph."""
    return GraphVisualizer.plot_graph(graph, target_node, visited_nodes, path, title)


def plot_search_comparison(results, title="Classical vs Quantum Search Comparison"):
    """Convenience function to plot comparison."""
    return GraphVisualizer.plot_search_comparison(results, title)
