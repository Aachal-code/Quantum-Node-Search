# 🚀 Quick Start Guide

## Installation & Setup

### 1. Prerequisites
- Python 3.8 or higher
- pip package manager
- 4GB RAM recommended

### 2. Install Dependencies

```bash
cd Quantum-Node-Search
pip install -r requirements.txt
```

**Installation Time**: ~5-10 minutes (first time only)

## Running the Project

### Option 1: Interactive Dashboard (Recommended for Learning)

```bash
streamlit run dashboard/app.py
```

**What you get**:
- 🎨 Real-time graph visualization
- 🔍 Select graph type and size
- ⚡ Run classical and quantum searches instantly
- 📊 Visual comparison of results
- 📈 Performance metrics and charts

**Access**: Open http://localhost:8501 in your browser

### Option 2: Command Line Interface

#### Simple Demonstration
```bash
python main.py --demo simple
```
Runs a quick demo on 64-node graph showing classical vs quantum search.

#### All Demonstrations
```bash
python main.py --demo all
```
Runs demonstrations of:
- Simple search
- Different graph types
- Complexity analysis

#### Quick Benchmark
```bash
python main.py --benchmark --quick
```
Tests graph sizes 16, 32, 64, 128 (faster, ~2 minutes)

#### Full Benchmark
```bash
python main.py --benchmark
```
Tests all sizes 8-1024 (comprehensive, ~10+ minutes)

#### Educational Content
```bash
python main.py --education
```
Prints detailed explanations of quantum computing concepts.

#### Single Search
```bash
python main.py --search 64 32
```
Searches for node 32 in a 64-node graph.

### Option 3: Python API

```python
from graphs import create_graph
from classical import run_classical_search
from quantum import run_grover_search

# Create graph
graph = create_graph('random', n_nodes=64)
target = 32

# Classical search
classical = run_classical_search(graph, target, method='linear')
print(f"Classical: {classical['nodes_checked']} nodes checked")

# Quantum search
quantum = run_grover_search(64, target)
print(f"Quantum: {quantum['grover_iterations']} iterations")
print(f"Speedup: {classical['nodes_checked'] / quantum['grover_iterations']:.1f}x")
```

## Output Files Generated

After running benchmarks, you'll find:

| File | Purpose |
|------|---------|
| `data/results.csv` | Detailed benchmark results |
| `complexity_comparison.png` | O(N) vs O(√N) plot |
| `execution_time_comparison.png` | Time comparison chart |
| `success_probability.png` | Quantum success rates |
| `results_table.png` | Summary table |
| `simple_demo_graph.png` | Graph visualization |
| `simple_demo_comparison.png` | Search comparison |

## Project Structure

```
├── graphs/                 # Graph generation
├── classical/              # Classical search algorithms
├── quantum/                # Grover's algorithm implementation
├── visualization/          # Plotting and analysis
├── experiments/            # Benchmark runner
├── dashboard/              # Interactive Streamlit app
├── tests/                  # Unit tests
├── main.py                 # CLI entry point
├── README.md               # Full documentation
└── requirements.txt        # Dependencies
```

## Key Concepts

### Classical Search: O(N)
- **Linear Search**: Check items one by one
- **Execution**: 64 nodes → ~64 checks

### Quantum Search: O(√N)
- **Grover's Algorithm**: Quantum superposition + interference
- **Execution**: 64 nodes → ~8 iterations
- **Speedup**: √64 = 8x faster!

## Troubleshooting

### Issue: "Module not found"
**Solution**: Make sure you're in the project directory and dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: "Permission denied" on Linux/Mac
**Solution**: Make files executable
```bash
chmod +x main.py
```

### Issue: Low quantum success probability
**Solution**: This is normal for large qubit numbers. Try:
- Increase `shots` parameter (more measurements)
- Use smaller graph sizes for testing
- Check that target node is within valid range

### Issue: Slow benchmark runs
**Solution**: 
- Use `--quick` flag for faster results
- Reduce benchmark sizes in the code
- Use dashboard for real-time feedback

## Performance Tips

### For Faster Execution
1. Use smaller graph sizes (8-64 nodes)
2. Run quick benchmark instead of full
3. Use dashboard for interactive testing

### For Better Quantum Results
1. Increase `shots` parameter (1000-5000)
2. Use graphs with 2^n nodes (8, 16, 32, 64...)
3. Try different graph types

### For Exploration
1. Start with simple demo
2. Try different node sizes
3. Compare classical algorithms
4. Analyze results in dashboard

## Educational Value

This project teaches:
- ✅ Quantum computing fundamentals
- ✅ Superposition and entanglement
- ✅ Quantum algorithm design
- ✅ Performance analysis
- ✅ Python scientific computing
- ✅ Graph algorithms
- ✅ Benchmarking techniques

## Next Steps

1. **Learn**: Run `python main.py --education` to understand concepts
2. **Explore**: Try dashboard with different parameters
3. **Analyze**: Review benchmark results and plots
4. **Extend**: Modify code to experiment with variations
5. **Share**: Generate plots and results for presentations

## Documentation

For detailed information:
- **Project details**: See `README.md`
- **API reference**: See docstrings in each module
- **Theory**: Run `--education` command
- **Code examples**: See inline comments

## Support

If you encounter issues:
1. Check `README.md` for detailed documentation
2. Review code comments and docstrings
3. Try `python main.py --help` for command options
4. Look at test files for usage examples

---

**Happy Quantum Computing! 🚀**

For more information, visit the full documentation in README.md
