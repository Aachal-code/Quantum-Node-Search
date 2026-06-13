"""
Unit tests for Quantum Search project.
"""

import unittest
import math
from graphs import create_graph, GraphGenerator
from classical import run_classical_search
from quantum import run_grover_search


class TestGraphGeneration(unittest.TestCase):
    """Test graph generation functions."""
    
    def test_random_graph(self):
        """Test random graph generation."""
        graph = create_graph('random', 16)
        self.assertEqual(graph.number_of_nodes(), 16)
        self.assertTrue(all(isinstance(node, int) for node in graph.nodes()))
    
    def test_scale_free_graph(self):
        """Test scale-free graph generation."""
        graph = create_graph('scale_free', 16)
        self.assertEqual(graph.number_of_nodes(), 16)
        self.assertTrue(graph.number_of_edges() > 0)
    
    def test_small_world_graph(self):
        """Test small-world graph generation."""
        graph = create_graph('small_world', 16)
        self.assertEqual(graph.number_of_nodes(), 16)
        self.assertTrue(graph.number_of_edges() > 0)
    
    def test_graph_stats(self):
        """Test graph statistics calculation."""
        generator = GraphGenerator()
        graph = generator.generate_random_graph(32)
        stats = generator.get_graph_stats(graph)
        
        self.assertEqual(stats['nodes'], 32)
        self.assertGreaterEqual(stats['density'], 0)
        self.assertLessEqual(stats['density'], 1)
        self.assertGreater(stats['average_degree'], 0)


class TestClassicalSearch(unittest.TestCase):
    """Test classical search algorithms."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.graph = create_graph('random', 16, seed=42)
        self.target = 7
    
    def test_linear_search(self):
        """Test linear search."""
        result = run_classical_search(self.graph, self.target, method='linear')
        
        self.assertIn('found', result)
        self.assertIn('nodes_checked', result)
        self.assertIn('execution_time', result)
        self.assertEqual(result['complexity'], 'O(N)')
    
    def test_bfs_search(self):
        """Test BFS search."""
        result = run_classical_search(self.graph, self.target, method='bfs')
        
        self.assertIn('found', result)
        self.assertIn('nodes_checked', result)
        self.assertIn('execution_time', result)
    
    def test_dfs_search(self):
        """Test DFS search."""
        result = run_classical_search(self.graph, self.target, method='dfs')
        
        self.assertIn('found', result)
        self.assertIn('nodes_checked', result)
        self.assertIn('execution_time', result)
    
    def test_search_correctness(self):
        """Test that search actually finds the target."""
        for target in [0, 7, 15]:
            result = run_classical_search(self.graph, target, method='linear')
            self.assertTrue(result['found'], f"Failed to find target {target}")


class TestQuantumSearch(unittest.TestCase):
    """Test quantum search implementation."""
    
    def test_grover_iterations(self):
        """Test optimal Grover iteration calculation."""
        # For N nodes, iterations should be approximately π/4 * √N
        test_cases = [
            (16, math.ceil(math.pi / 4 * math.sqrt(16))),  # Should be 4
            (64, math.ceil(math.pi / 4 * math.sqrt(64))),  # Should be 8
            (256, math.ceil(math.pi / 4 * math.sqrt(256))),  # Should be 16
        ]
        
        for n_nodes, expected_iterations in test_cases:
            result = run_grover_search(n_nodes, target=0)
            self.assertEqual(result['grover_iterations'], expected_iterations,
                           f"Wrong iterations for N={n_nodes}")
    
    def test_grover_success_probability(self):
        """Test that Grover has reasonable success probability."""
        result = run_grover_search(64, target=32, shots=1000)
        
        # Success probability should be reasonably high (>70%)
        self.assertGreater(result['success_probability'], 70,
                          "Success probability too low")
    
    def test_grover_result_structure(self):
        """Test structure of Grover result."""
        result = run_grover_search(16, target=7)
        
        self.assertIn('found', result)
        self.assertIn('measured_node', result)
        self.assertIn('execution_time', result)
        self.assertIn('grover_iterations', result)
        self.assertIn('success_probability', result)
        self.assertEqual(result['complexity'], 'O(√N) = O(√16)')
    
    def test_grover_target_bounds(self):
        """Test that target must be within bounds."""
        with self.assertRaises(ValueError):
            run_grover_search(16, target=20)


class TestComplexityComparison(unittest.TestCase):
    """Test complexity comparisons."""
    
    def test_speedup_increases_with_size(self):
        """Test that speedup increases with problem size."""
        speedups = []
        
        for n_nodes in [16, 32, 64]:
            graph = create_graph('random', n_nodes)
            target = n_nodes // 2
            
            classical = run_classical_search(graph, target, method='linear')
            quantum = run_grover_search(n_nodes, target)
            
            speedup = classical['nodes_checked'] / quantum['grover_iterations']
            speedups.append(speedup)
        
        # Speedup should increase (approximately √N)
        self.assertLess(speedups[0], speedups[1])
        self.assertLess(speedups[1], speedups[2])
    
    def test_quantum_better_than_classical(self):
        """Test that quantum is faster than classical for large N."""
        n_nodes = 128
        graph = create_graph('random', n_nodes)
        target = n_nodes // 2
        
        classical = run_classical_search(graph, target, method='linear')
        quantum = run_grover_search(n_nodes, target)
        
        speedup = classical['nodes_checked'] / quantum['grover_iterations']
        
        # For N=128, speedup should be approximately √128 ≈ 11.3
        self.assertGreater(speedup, 5)


class TestVisualization(unittest.TestCase):
    """Test visualization functions."""
    
    def test_graph_plot(self):
        """Test graph visualization."""
        from visualization import plot_graph
        
        graph = create_graph('random', 16)
        
        try:
            fig = plot_graph(graph, target_node=5)
            self.assertIsNotNone(fig)
        except Exception as e:
            self.fail(f"Graph plot failed: {e}")
    
    def test_comparison_plot(self):
        """Test comparison visualization."""
        from visualization import plot_search_comparison
        
        graph = create_graph('random', 16)
        target = 7
        
        classical = run_classical_search(graph, target, method='linear')
        quantum = run_grover_search(16, target)
        
        results = {
            'classical': classical,
            'quantum': quantum
        }
        
        try:
            fig = plot_search_comparison(results)
            self.assertIsNotNone(fig)
        except Exception as e:
            self.fail(f"Comparison plot failed: {e}")


if __name__ == '__main__':
    unittest.main()
