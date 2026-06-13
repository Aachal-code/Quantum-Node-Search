"""
Main entry point for Quantum Search in Graph Nodes project.
Provides CLI interface for running experiments and demonstrations.
"""

import sys
import os
import argparse
import math

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graphs import create_graph, GraphGenerator
from classical import run_classical_search
from quantum import run_grover_search
from visualization import plot_graph, plot_search_comparison, PerformancePlotter
from experiments.benchmark import run_benchmark
import matplotlib.pyplot as plt
import pandas as pd


def print_header():
    """Print project header."""
    print("\n" + "="*80)
    print(" " * 15 + "🔍 QUANTUM SEARCH IN GRAPH NODES 🔍")
    print(" " * 10 + "Using Grover's Algorithm for Quantum Computing")
    print("="*80 + "\n")


def demo_simple_search():
    """Run a simple demonstration."""
    print("\n📌 SIMPLE DEMONSTRATION")
    print("-" * 80)
    
    # Parameters
    n_nodes = 64
    target = 32
    
    print(f"\nGenerating random graph with {n_nodes} nodes...")
    print(f"Target node: {target}")
    
    # Generate graph
    graph = create_graph('random', n_nodes)
    
    # Run classical search
    print("\n▶ Classical Search (Linear):")
    classical_result = run_classical_search(graph, target, method='linear')
    print(f"  ✓ Found: {classical_result['found']}")
    print(f"  ✓ Nodes Checked: {classical_result['nodes_checked']}")
    print(f"  ✓ Time: {classical_result['execution_time']*1000:.4f} ms")
    
    # Run quantum search
    print("\n▶ Quantum Search (Grover):")
    quantum_result = run_grover_search(n_nodes, target)
    print(f"  ✓ Found: {quantum_result['found']}")
    print(f"  ✓ Grover Iterations: {quantum_result['grover_iterations']}")
    print(f"  ✓ Time: {quantum_result['execution_time']*1000:.4f} ms")
    print(f"  ✓ Success Probability: {quantum_result['success_probability']:.1f}%")
    
    # Comparison
    print("\n▶ Comparison:")
    speedup = classical_result['nodes_checked'] / quantum_result['grover_iterations']
    print(f"  ✓ Theoretical Speedup: {speedup:.2f}x")
    print(f"  ✓ Expected Speedup: ~√{n_nodes} ≈ {math.sqrt(n_nodes):.1f}x")
    
    # Visualize
    print("\nGenerating visualization...")
    fig = plot_graph(
        graph,
        target_node=target,
        title=f"Random Graph ({n_nodes} nodes) - Target: {target}"
    )
    plt.savefig('simple_demo_graph.png', dpi=150, bbox_inches='tight')
    print("✓ Graph saved to simple_demo_graph.png")
    
    # Comparison plot
    results_dict = {
        'classical': classical_result,
        'quantum': quantum_result
    }
    fig = plot_search_comparison(results_dict)
    plt.savefig('simple_demo_comparison.png', dpi=150, bbox_inches='tight')
    print("✓ Comparison plot saved to simple_demo_comparison.png")


def demo_graph_types():
    """Demonstrate different graph types."""
    print("\n📌 GRAPH TYPE DEMONSTRATION")
    print("-" * 80)
    
    n_nodes = 32
    target = 15
    
    graph_types = ['random', 'scale_free', 'small_world']
    
    for graph_type in graph_types:
        print(f"\n▶ {graph_type.upper()} Graph ({n_nodes} nodes):")
        graph = create_graph(graph_type, n_nodes)
        
        generator = GraphGenerator()
        stats = generator.get_graph_stats(graph)
        
        print(f"  Nodes: {stats['nodes']}")
        print(f"  Edges: {stats['edges']}")
        print(f"  Density: {stats['density']:.3f}")
        print(f"  Average Degree: {stats['average_degree']:.2f}")
        print(f"  Is Connected: {stats['is_connected']}")


def demo_complexity_analysis():
    """Demonstrate complexity comparison across sizes."""
    print("\n📌 COMPLEXITY ANALYSIS")
    print("-" * 80)
    
    node_sizes = [8, 16, 32, 64, 128, 256]
    
    print(f"\n{'Nodes':<10}{'Classical':<15}{'Quantum (√N)':<15}{'Theoretical':<15}{'Speedup':<10}")
    print("-" * 65)
    
    for n in node_sizes:
        classical_steps = n
        quantum_steps = math.ceil(math.pi / 4 * math.sqrt(n))
        theoretical = math.sqrt(n)
        speedup = classical_steps / quantum_steps
        
        print(f"{n:<10}{classical_steps:<15}{quantum_steps:<15}{theoretical:<15.1f}{speedup:<10.2f}x")


def demo_benchmark(quick: bool = False):
    """Run benchmark experiments."""
    print("\n📌 BENCHMARK EXPERIMENTS")
    print("-" * 80)
    
    if quick:
        node_sizes = [16, 32, 64, 128]
        shots = 500
        print("\nRunning QUICK benchmark (limited sizes, 500 shots)...")
    else:
        node_sizes = [8, 16, 32, 64, 128, 256, 512, 1024]
        shots = 1000
        print("\nRunning FULL benchmark (all sizes, 1000 shots)...")
        print("⚠️ This may take several minutes...")
    
    print(f"\nNode sizes: {node_sizes}")
    print(f"Shots per experiment: {shots}\n")
    
    experiment = run_benchmark(
        output_file='data/results.csv',
        node_sizes=node_sizes,
        shots=shots
    )
    
    return experiment


def print_educational_content():
    """Print educational content about the project."""
    print("\n" + "="*80)
    print("📚 EDUCATIONAL CONTENT")
    print("="*80)
    
    content = """
    
    1. WHAT IS A GRAPH?
    ───────────────────
    A graph is a mathematical structure consisting of:
    - Vertices (nodes): Represent objects or points
    - Edges: Connect pairs of vertices
    
    Example: Social network where people are nodes and friendships are edges.
    
    
    2. NODE SEARCHING
    ─────────────────
    The problem: Given a graph, find a specific node.
    
    Classical approach: Search through nodes sequentially
    - Linear Search: O(N) complexity
    - DFS/BFS: O(N) in worst case
    
    
    3. CLASSICAL SEARCH ALGORITHMS
    ──────────────────────────────
    
    LINEAR SEARCH:
    - Check each node one by one
    - Simplest approach
    - Complexity: O(N)
    - Best case: O(1), Worst case: O(N)
    
    BREADTH-FIRST SEARCH (BFS):
    - Explore nodes level by level
    - Uses queue data structure
    - Finds shortest path
    - Complexity: O(N + E) where E = edges
    
    DEPTH-FIRST SEARCH (DFS):
    - Explore deep before backtracking
    - Uses stack data structure
    - Memory efficient for deep graphs
    - Complexity: O(N + E)
    
    
    4. GROVER'S QUANTUM ALGORITHM
    ──────────────────────────────
    
    Revolutionary quantum algorithm that:
    - Searches unstructured databases
    - Achieves O(√N) complexity
    - Provides QUADRATIC SPEEDUP over classical
    
    KEY COMPONENTS:
    
    a) QUANTUM SUPERPOSITION:
       - Quantum bits (qubits) exist in multiple states simultaneously
       - N nodes require log₂(N) qubits
       - All states searched in parallel
    
    b) ORACLE:
       - Marks the target state with a phase flip
       - Doesn't collapse superposition
       - Identifies solution without measuring
    
    c) DIFFUSION OPERATOR:
       - Amplifies the marked state's amplitude
       - Suppresses all other amplitudes
       - Based on reflection through average
    
    d) INTERFERENCE:
       - Quantum waves interfere constructively and destructively
       - Target state interference: CONSTRUCTIVE
       - Wrong states interference: DESTRUCTIVE
    
    
    5. COMPLEXITY COMPARISON
    ────────────────────────
    
    Classical: O(N)
    - 1,000 nodes → ~1,000 steps
    - 1,000,000 nodes → ~1,000,000 steps
    
    Quantum: O(√N)
    - 1,000 nodes → ~32 steps
    - 1,000,000 nodes → ~1,000 steps
    
    Grover's speedup is: √N times faster!
    
    
    6. WHY QUANTUM IS FASTER
    ───────────────────────
    
    Classical: Sequential checking
    ┌─────┐
    │ Check node 1  │ → NOT found
    └─────┘
          ↓
    ┌──────┐
    │ Check node 2  │ → NOT found
    └──────┘
              ... (many iterations)
    
    Quantum: Parallel amplitude amplification
    ┌─────────────────────────────────────┐
    │ Superposition of ALL states        │
    │ ├─ Node 1: amplitude a             │
    │ ├─ Node 2: amplitude a             │
    │ ├─ Node TARGET: amplitude a        │
    │ └─ ...                             │
    └─────────────────────────────────────┘
             ↓
    ┌──────────────────────────────────────┐
    │ After k iterations:                 │
    │ ├─ Node 1: amplitude ≈ 0            │
    │ ├─ Node 2: amplitude ≈ 0            │
    │ ├─ Node TARGET: amplitude ≈ 1      │ ← Ready to measure!
    │ └─ ...                              │
    └──────────────────────────────────────┘
    
    
    7. APPLICATIONS
    ───────────────
    
    - Database Search: Find entries in unsorted databases
    - Cryptography: Break classical encryption
    - Optimization: Find optimal solutions
    - Machine Learning: Pattern recognition
    - SAT Solving: NP-complete problem solving
    
    
    8. LIMITATIONS
    ──────────────
    
    - Quantum hardware is noisy (NISQ era)
    - Requires quantum computers with many stable qubits
    - Error correction overhead is significant
    - State preparation and measurement add overhead
    - Currently practical for specific problems
    
    
    9. MATHEMATICAL FORMULAS
    ────────────────────────
    
    Number of qubits needed: n = log₂(N)
    
    Optimal iterations: k ≈ π/4 × √N
    
    Success probability: sin²(θ(k+1/2)) where θ = arcsin(1/√N)
    
    Classical steps: O(N)
    Quantum steps: O(√N)
    
    Speedup ratio: Classical / Quantum = √N
    
    
    10. THIS PROJECT'S FEATURES
    ───────────────────────────
    
    ✓ Three graph types (Random, Scale-Free, Small-World)
    ✓ Three classical search methods (Linear, BFS, DFS)
    ✓ Full Grover's algorithm implementation
    ✓ Quantum oracle and diffusion operator
    ✓ Performance benchmarking
    ✓ Interactive Streamlit dashboard
    ✓ Comprehensive visualizations
    ✓ Educational materials and explanations
    ✓ Production-quality Python code
    
    """
    
    print(content)


def main():
    """Main CLI interface."""
    print_header()
    
    parser = argparse.ArgumentParser(
        description='Quantum Search in Graph Nodes Using Grover\'s Algorithm',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --demo simple          Run simple demonstration
  python main.py --demo all             Run all demonstrations
  python main.py --benchmark            Run full benchmark experiments
  python main.py --benchmark --quick    Run quick benchmark
  python main.py --dashboard            Launch interactive dashboard
  python main.py --education            Print educational content
        """
    )
    
    parser.add_argument(
        '--demo',
        choices=['simple', 'graphs', 'complexity', 'all'],
        help='Run demonstrations'
    )
    
    parser.add_argument(
        '--benchmark',
        action='store_true',
        help='Run benchmark experiments'
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick version of benchmark (fewer sizes, fewer shots)'
    )
    
    parser.add_argument(
        '--dashboard',
        action='store_true',
        help='Launch interactive Streamlit dashboard'
    )
    
    parser.add_argument(
        '--education',
        action='store_true',
        help='Print educational content'
    )
    
    parser.add_argument(
        '--search',
        type=int,
        nargs=2,
        metavar=('NODES', 'TARGET'),
        help='Run single search: --search NODES TARGET'
    )
    
    args = parser.parse_args()
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Execute commands
    if args.demo:
        if args.demo == 'simple' or args.demo == 'all':
            demo_simple_search()
        if args.demo == 'graphs' or args.demo == 'all':
            demo_graph_types()
        if args.demo == 'complexity' or args.demo == 'all':
            demo_complexity_analysis()
    
    elif args.benchmark:
        demo_benchmark(quick=args.quick)
    
    elif args.dashboard:
        print("\n🚀 Launching Streamlit dashboard...")
        print("Run: streamlit run dashboard/app.py")
        os.system('streamlit run dashboard/app.py')
    
    elif args.education:
        print_educational_content()
    
    elif args.search:
        n_nodes, target = args.search
        print(f"\n🔍 Running search: {n_nodes} nodes, target = {target}")
        
        if target >= n_nodes:
            print(f"❌ Error: target must be < {n_nodes}")
            sys.exit(1)
        
        graph = create_graph('random', n_nodes)
        
        print("\nClassical Search:")
        classical = run_classical_search(graph, target, method='linear')
        print(f"  Found: {classical['found']}, Checked: {classical['nodes_checked']}, Time: {classical['execution_time']*1000:.4f}ms")
        
        print("\nQuantum Search:")
        quantum = run_grover_search(n_nodes, target)
        print(f"  Found: {quantum['found']}, Iterations: {quantum['grover_iterations']}, Time: {quantum['execution_time']*1000:.4f}ms")
    
    else:
        print("No command specified. Use --help for options.")
        print("\nQuick Start:")
        print("  python main.py --demo simple        → Simple demonstration")
        print("  python main.py --dashboard          → Interactive dashboard")
        print("  python main.py --benchmark --quick  → Quick benchmark")
        print("  python main.py --education          → Educational content")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Program interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
