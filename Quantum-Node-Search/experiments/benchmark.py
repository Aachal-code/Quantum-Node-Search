"""
Benchmark experiments comparing classical and quantum search.
"""

import csv
import time
from typing import List, Dict
import math

from graphs import create_graph
from classical import run_classical_search
from quantum import run_grover_search
from visualization import PerformancePlotter
import matplotlib.pyplot as plt
import pandas as pd


class BenchmarkExperiment:
    """Run benchmark experiments and collect results."""
    
    def __init__(self, output_file: str = 'results.csv'):
        """
        Initialize benchmark experiment.
        
        Args:
            output_file: Path to save CSV results
        """
        self.output_file = output_file
        self.results = []
    
    def run_experiments(
        self,
        node_sizes: List[int] = None,
        graph_types: List[str] = None,
        shots: int = 1000
    ) -> List[Dict]:
        """
        Run benchmark experiments for various graph sizes.
        
        Args:
            node_sizes: List of node counts to test
            graph_types: List of graph types to test
            shots: Number of quantum measurements
            
        Returns:
            List of result dictionaries
        """
        if node_sizes is None:
            node_sizes = [8, 16, 32, 64, 128, 256, 512, 1024]
        
        if graph_types is None:
            graph_types = ['random']
        
        results = []
        
        for graph_type in graph_types:
            print(f"\n{'='*70}")
            print(f"Testing {graph_type.upper()} graphs")
            print(f"{'='*70}")
            
            for n_nodes in node_sizes:
                # Skip if nodes exceed practical quantum simulation
                if n_nodes > 1024:
                    print(f"Skipping n={n_nodes} (too large for quantum simulation)")
                    continue
                
                # Select random target node
                target = n_nodes // 2
                
                print(f"\nTesting n={n_nodes} nodes (target={target})...", end=' ', flush=True)
                
                # Generate graph
                graph = create_graph(graph_type, n_nodes)
                
                # Run classical search (linear)
                classical_result = run_classical_search(graph, target, method='linear')
                
                # Run classical BFS
                bfs_result = run_classical_search(graph, target, method='bfs')
                
                # Run quantum search
                quantum_result = run_grover_search(n_nodes, target, shots=shots)
                
                # Compile results
                result_entry = {
                    'nodes': n_nodes,
                    'graph_type': graph_type,
                    'target_node': target,
                    'classical_method': 'linear',
                    'classical_steps': classical_result['nodes_checked'],
                    'classical_time': classical_result['execution_time'],
                    'classical_found': classical_result['found'],
                    'bfs_steps': bfs_result['nodes_checked'],
                    'bfs_time': bfs_result['execution_time'],
                    'bfs_found': bfs_result['found'],
                    'quantum_steps': quantum_result['nodes_checked'],
                    'quantum_iterations': quantum_result['grover_iterations'],
                    'quantum_time': quantum_result['execution_time'],
                    'quantum_found': quantum_result['found'],
                    'success_probability': quantum_result['success_probability'],
                    'theoretical_speedup': classical_result['nodes_checked'] / math.sqrt(n_nodes),
                }
                
                results.append(result_entry)
                self.results.append(result_entry)
                
                print("✓ Done")
                print(f"  Classical: {classical_result['nodes_checked']} steps, {classical_result['execution_time']*1000:.4f}ms")
                print(f"  BFS:       {bfs_result['nodes_checked']} steps, {bfs_result['execution_time']*1000:.4f}ms")
                print(f"  Quantum:   {quantum_result['grover_iterations']} iterations, {quantum_result['execution_time']*1000:.4f}ms")
                print(f"  Success:   {quantum_result['success_probability']:.1f}%")
        
        return results
    
    def save_results(self) -> str:
        """
        Save results to CSV file.
        
        Returns:
            Path to saved file
        """
        if not self.results:
            print("No results to save")
            return None
        
        try:
            df = pd.DataFrame(self.results)
            df.to_csv(self.output_file, index=False)
            print(f"\nResults saved to {self.output_file}")
            return self.output_file
        except Exception as e:
            print(f"Error saving results: {e}")
            return None
    
    def generate_plots(self, output_dir: str = '.') -> List[str]:
        """
        Generate visualization plots.
        
        Args:
            output_dir: Directory to save plots
            
        Returns:
            List of saved plot file paths
        """
        if not self.results:
            print("No results to plot")
            return []
        
        df = pd.DataFrame(self.results)
        saved_files = []
        
        try:
            # Filter for first graph type and linear results
            df_filtered = df[df['graph_type'] == 'random'].copy()
            
            # Complexity comparison
            fig = PerformancePlotter.plot_complexity_comparison(
                df_filtered['nodes'].tolist(),
                df_filtered['classical_steps'].tolist(),
                df_filtered['quantum_iterations'].tolist()
            )
            path = f"{output_dir}/complexity_comparison.png"
            fig.savefig(path, dpi=150, bbox_inches='tight')
            saved_files.append(path)
            plt.close(fig)
            print(f"Saved: {path}")
            
            # Execution time comparison
            fig = PerformancePlotter.plot_execution_time_comparison(
                df_filtered['nodes'].tolist(),
                df_filtered['classical_time'].tolist(),
                df_filtered['quantum_time'].tolist()
            )
            path = f"{output_dir}/execution_time_comparison.png"
            fig.savefig(path, dpi=150, bbox_inches='tight')
            saved_files.append(path)
            plt.close(fig)
            print(f"Saved: {path}")
            
            # Success probability
            fig = PerformancePlotter.plot_success_probability(
                df_filtered['nodes'].tolist(),
                df_filtered['success_probability'].tolist()
            )
            path = f"{output_dir}/success_probability.png"
            fig.savefig(path, dpi=150, bbox_inches='tight')
            saved_files.append(path)
            plt.close(fig)
            print(f"Saved: {path}")
            
            # Results table
            fig = PerformancePlotter.plot_results_table(df_filtered)
            path = f"{output_dir}/results_table.png"
            fig.savefig(path, dpi=150, bbox_inches='tight')
            saved_files.append(path)
            plt.close(fig)
            print(f"Saved: {path}")
            
        except Exception as e:
            print(f"Error generating plots: {e}")
        
        return saved_files
    
    def print_summary(self):
        """Print summary statistics."""
        if not self.results:
            print("No results to summarize")
            return
        
        df = pd.DataFrame(self.results)
        
        print("\n" + "="*70)
        print("BENCHMARK SUMMARY")
        print("="*70)
        
        print("\nAverage Performance (Linear Scale):")
        print(f"  Classical (Linear) - Steps: {df['classical_steps'].mean():.0f}")
        print(f"  Classical (BFS)    - Steps: {df['bfs_steps'].mean():.0f}")
        print(f"  Quantum (Grover)   - Iterations: {df['quantum_iterations'].mean():.0f}")
        
        print("\nSpeedup Analysis:")
        speedup = df['classical_steps'] / df['quantum_iterations']
        print(f"  Average Speedup: {speedup.mean():.2f}x")
        print(f"  Max Speedup: {speedup.max():.2f}x")
        print(f"  Min Speedup: {speedup.min():.2f}x")
        
        print("\nQuantum Success Rate:")
        print(f"  Average Success Probability: {df['success_probability'].mean():.1f}%")
        print(f"  Min Success Probability: {df['success_probability'].min():.1f}%")
        print(f"  Success Rate (>90%): {len(df[df['success_probability'] > 90]) / len(df) * 100:.0f}%")
        
        print("\nExecution Time (Classical vs Quantum):")
        classical_time_ms = df['classical_time'].mean() * 1000
        quantum_time_ms = df['quantum_time'].mean() * 1000
        print(f"  Classical Average: {classical_time_ms:.4f} ms")
        print(f"  Quantum Average: {quantum_time_ms:.4f} ms")
        
        print("\n" + "="*70)


def run_benchmark(
    output_file: str = 'data/results.csv',
    node_sizes: List[int] = None,
    shots: int = 1000
) -> BenchmarkExperiment:
    """
    Run complete benchmark experiment.
    
    Args:
        output_file: Path to save results
        node_sizes: List of node sizes to test
        shots: Number of quantum measurements
        
    Returns:
        BenchmarkExperiment object with results
    """
    experiment = BenchmarkExperiment(output_file)
    
    # Run experiments
    experiment.run_experiments(node_sizes=node_sizes, shots=shots)
    
    # Save results
    experiment.save_results()
    
    # Generate plots
    experiment.generate_plots('.')
    
    # Print summary
    experiment.print_summary()
    
    return experiment


if __name__ == '__main__':
    # Run with default parameters
    experiment = run_benchmark()
