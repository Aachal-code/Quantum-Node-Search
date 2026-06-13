"""
Performance analysis and plotting utilities.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple


class PerformancePlotter:
    """Create performance analysis plots."""
    
    @staticmethod
    def plot_complexity_comparison(
        nodes_list: List[int],
        classical_steps: List[int],
        quantum_steps: List[int],
        figsize: Tuple[int, int] = (12, 6)
    ) -> plt.Figure:
        """
        Plot classical O(N) vs quantum O(√N) complexity.
        
        Args:
            nodes_list: List of node counts
            classical_steps: Classical algorithm steps
            quantum_steps: Quantum algorithm iterations
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Plot 1: Absolute comparison
        x = np.arange(len(nodes_list))
        width = 0.35
        
        ax1.bar(x - width/2, classical_steps, width, label='Classical O(N)', color='#3498db', alpha=0.8)
        ax1.bar(x + width/2, quantum_steps, width, label='Quantum O(√N)', color='#e74c3c', alpha=0.8)
        
        ax1.set_xlabel('Number of Nodes', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Algorithm Steps', fontsize=11, fontweight='bold')
        ax1.set_title('Classical vs Quantum Search Steps', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(nodes_list)
        ax1.legend(fontsize=10)
        ax1.grid(axis='y', alpha=0.3)
        
        # Plot 2: Line plot with exponential scale
        ax2.semilogy(nodes_list, classical_steps, 'o-', label='Classical O(N)', 
                    linewidth=2, markersize=8, color='#3498db')
        ax2.semilogy(nodes_list, quantum_steps, 's-', label='Quantum O(√N)', 
                    linewidth=2, markersize=8, color='#e74c3c')
        
        ax2.set_xlabel('Number of Nodes', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Algorithm Steps (log scale)', fontsize=11, fontweight='bold')
        ax2.set_title('Complexity Growth (Log Scale)', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3, which='both')
        
        fig.suptitle('Complexity Analysis: Classical vs Quantum', 
                    fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_execution_time_comparison(
        nodes_list: List[int],
        classical_times: List[float],
        quantum_times: List[float],
        figsize: Tuple[int, int] = (12, 6)
    ) -> plt.Figure:
        """
        Plot execution time comparison.
        
        Args:
            nodes_list: List of node counts
            classical_times: Classical execution times (seconds)
            quantum_times: Quantum execution times (seconds)
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Convert to milliseconds
        classical_times_ms = [t * 1000 for t in classical_times]
        quantum_times_ms = [t * 1000 for t in quantum_times]
        
        # Plot 1: Bar chart
        x = np.arange(len(nodes_list))
        width = 0.35
        
        ax1.bar(x - width/2, classical_times_ms, width, label='Classical', 
               color='#3498db', alpha=0.8)
        ax1.bar(x + width/2, quantum_times_ms, width, label='Quantum', 
               color='#e74c3c', alpha=0.8)
        
        ax1.set_xlabel('Number of Nodes', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Execution Time (ms)', fontsize=11, fontweight='bold')
        ax1.set_title('Execution Time Comparison', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(nodes_list)
        ax1.legend(fontsize=10)
        ax1.grid(axis='y', alpha=0.3)
        
        # Plot 2: Speedup ratio
        speedup = [c / q if q > 0 else 1 for c, q in zip(classical_times, quantum_times)]
        
        ax2.plot(nodes_list, speedup, 'o-', linewidth=2, markersize=8, color='#2ecc71')
        ax2.axhline(y=1, color='red', linestyle='--', linewidth=1, label='No speedup', alpha=0.7)
        ax2.fill_between(nodes_list, 1, speedup, alpha=0.2, color='#2ecc71')
        
        ax2.set_xlabel('Number of Nodes', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Speedup Ratio (Classical/Quantum)', fontsize=11, fontweight='bold')
        ax2.set_title('Quantum Speedup', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        fig.suptitle('Execution Time Analysis', fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_success_probability(
        nodes_list: List[int],
        probabilities: List[float],
        figsize: Tuple[int, int] = (10, 6)
    ) -> plt.Figure:
        """
        Plot quantum success probability across different system sizes.
        
        Args:
            nodes_list: List of node counts
            probabilities: Success probabilities (0-100)
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.plot(nodes_list, probabilities, 'o-', linewidth=2, markersize=8, 
               color='#9b59b6', label='Success Probability')
        ax.axhline(y=90, color='green', linestyle='--', linewidth=1.5, 
                  label='90% Threshold', alpha=0.7)
        ax.fill_between(nodes_list, 90, 100, alpha=0.2, color='green')
        
        ax.set_xlabel('Number of Nodes', fontsize=11, fontweight='bold')
        ax.set_ylabel('Success Probability (%)', fontsize=11, fontweight='bold')
        ax.set_title('Grover Algorithm Success Probability', fontsize=13, fontweight='bold')
        ax.set_ylim([0, 105])
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Add value labels on points
        for x, y in zip(nodes_list, probabilities):
            ax.text(x, y + 2, f'{y:.1f}%', ha='center', fontsize=9)
        
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def plot_results_table(
        results_df: pd.DataFrame,
        figsize: Tuple[int, int] = (14, 8)
    ) -> plt.Figure:
        """
        Display results as a formatted table.
        
        Args:
            results_df: Pandas DataFrame with results
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        ax.axis('tight')
        ax.axis('off')
        
        # Format the dataframe
        df_display = results_df.copy()
        
        # Round numeric columns
        for col in df_display.columns:
            if df_display[col].dtype in ['float64', 'int64']:
                if 'time' in col.lower():
                    df_display[col] = df_display[col].apply(lambda x: f'{x:.6f}s')
                elif 'probability' in col.lower():
                    df_display[col] = df_display[col].apply(lambda x: f'{x:.1f}%')
                elif 'steps' in col.lower():
                    df_display[col] = df_display[col].apply(lambda x: f'{int(x)}')
        
        # Create table
        table = ax.table(
            cellText=df_display.values,
            colLabels=df_display.columns,
            cellLoc='center',
            loc='center',
            colWidths=[0.12] * len(df_display.columns)
        )
        
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        # Style header
        for i in range(len(df_display.columns)):
            table[(0, i)].set_facecolor('#3498db')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        # Alternate row colors
        for i in range(1, len(df_display) + 1):
            for j in range(len(df_display.columns)):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#ecf0f1')
                else:
                    table[(i, j)].set_facecolor('#ffffff')
        
        plt.title('Quantum Search Benchmark Results', fontsize=14, fontweight='bold', pad=20)
        
        return fig


def plot_complexity(nodes, classical, quantum):
    """Convenience function."""
    return PerformancePlotter.plot_complexity_comparison(nodes, classical, quantum)


def plot_execution_time(nodes, classical_times, quantum_times):
    """Convenience function."""
    return PerformancePlotter.plot_execution_time_comparison(nodes, classical_times, quantum_times)


def plot_success_prob(nodes, probs):
    """Convenience function."""
    return PerformancePlotter.plot_success_probability(nodes, probs)


def plot_results_table(df):
    """Convenience function."""
    return PerformancePlotter.plot_results_table(df)
