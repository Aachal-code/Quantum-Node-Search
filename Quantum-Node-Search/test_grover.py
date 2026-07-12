"""
Test script for Grover's Algorithm
Run this from the parent directory of your quantum folder
"""

from quantum.grover_search import run_grover_search

print("=" * 60)
print("GROVER'S ALGORITHM TEST")
print("=" * 60)

# Test 1: Small problem (8 nodes, find node 5)
print("\n### Test 1: Search among 8 nodes for node 5 ###")
result = run_grover_search(n_nodes=8, target=5, shots=1000)

print(f"\n--- Results ---")
print(f"Target found: {result['found']}")
print(f"Measured node: {result['measured_node']}")
print(f"Success probability: {result['success_probability']:.1f}%")
print(f"Execution time: {result['execution_time']:.4f} seconds")
print(f"Quantum iterations: {result['grover_iterations']}")
print(f"Complexity: {result['complexity']}")

if result['found']:
    print("✅ SUCCESS - Target found!")
else:
    print("❌ FAILED - Target not found")

# Test 2: Medium problem (16 nodes, find node 10)
print("\n" + "=" * 60)
print("### Test 2: Search among 16 nodes for node 10 ###")
result = run_grover_search(n_nodes=16, target=10, shots=1000)

print(f"\n--- Results ---")
print(f"Target found: {result['found']}")
print(f"Measured node: {result['measured_node']}")
print(f"Success probability: {result['success_probability']:.1f}%")
print(f"Execution time: {result['execution_time']:.4f} seconds")
print(f"Quantum iterations: {result['grover_iterations']}")
print(f"Complexity: {result['complexity']}")

if result['found']:
    print("✅ SUCCESS - Target found!")
else:
    print("❌ FAILED - Target not found")

# Test 3: Different target (8 nodes, find node 0)
print("\n" + "=" * 60)
print("### Test 3: Search among 8 nodes for node 0 ###")
result = run_grover_search(n_nodes=8, target=0, shots=1000)

print(f"\n--- Results ---")
print(f"Target found: {result['found']}")
print(f"Measured node: {result['measured_node']}")
print(f"Success probability: {result['success_probability']:.1f}%")
print(f"Execution time: {result['execution_time']:.4f} seconds")

if result['found']:
    print("✅ SUCCESS - Target found!")
else:
    print("❌ FAILED - Target not found")

print("\n" + "=" * 60)
print("TESTS COMPLETE")
print("=" * 60)