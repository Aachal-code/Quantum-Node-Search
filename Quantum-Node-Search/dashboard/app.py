"""
Interactive Streamlit Dashboard for Quantum Search in Graphs.
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import math
import os

from graphs import create_graph
from classical import run_classical_search
from quantum import run_grover_search
from visualization import plot_graph, plot_search_comparison, PerformancePlotter

# Set page configuration
st.set_page_config(
    page_title="Quantum Search in Graphs",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='main-title'>🔍 Quantum Search in Graph Nodes</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Grover's Algorithm vs Classical Search</div>", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# Graph settings
st.sidebar.subheader("Graph Settings")
graph_type = st.sidebar.selectbox(
    "Graph Type",
    ["random", "scale_free", "small_world"],
    help="Type of graph to generate"
)

n_nodes = st.sidebar.slider(
    "Number of Nodes",
    min_value=8,
    max_value=256,
    value=64,
    step=8,
    help="Total nodes in the graph (max 256 for practical quantum simulation)"
)

target_node = st.sidebar.slider(
    "Target Node",
    min_value=0,
    max_value=n_nodes - 1,
    value=n_nodes // 2,
    help="Node to search for"
)

quantum_shots = st.sidebar.slider(
    "Quantum Shots",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100,
    help="Number of quantum measurements"
)

# Create columns for main content
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎨 Visualization", 
    "📊 Search Results", 
    "📈 Analysis", 
    "📋 Details",
    "ℹ️ About"
])

# Generate graph when user confirms
if st.sidebar.button("🚀 Run Search", use_container_width=True):
    st.session_state.run_search = True

# Initialize session state
if 'run_search' not in st.session_state:
    st.session_state.run_search = False

if st.session_state.run_search:
    # Progress indicator
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    
    try:
        # Generate graph
        status_text.text("Generating graph...")
        progress_bar.progress(10)
        
        graph = create_graph(graph_type, n_nodes, seed=42)
        
        # Store graph info
        graph_info = {
            'nodes': graph.number_of_nodes(),
            'edges': graph.number_of_edges(),
            'density': nx.density(graph),
            'avg_degree': sum(dict(graph.degree()).values()) / graph.number_of_nodes(),
        }
        
        # Run classical search
        status_text.text("Running classical search...")
        progress_bar.progress(30)
        
        classical_result = run_classical_search(graph, target_node, method='linear')
        bfs_result = run_classical_search(graph, target_node, method='bfs')
        
        # Run quantum search
        status_text.text("Running quantum search...")
        progress_bar.progress(60)
        
        quantum_result = run_grover_search(n_nodes, target_node, shots=quantum_shots)
        
        progress_bar.progress(100)
        status_text.text("Complete! ✓")
        
        # TAB 1: Visualization
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📍 Graph Structure")
                fig = plot_graph(
                    graph,
                    target_node=target_node,
                    title=f"{graph_type.capitalize()} Graph ({n_nodes} nodes)"
                )
                st.pyplot(fig, use_container_width=True)
            
            with col2:
                st.subheader("Graph Statistics")
                col_stats = st.columns(2)
                col_stats[0].metric("Nodes", graph_info['nodes'])
                col_stats[1].metric("Edges", graph_info['edges'])
                col_stats[0].metric("Density", f"{graph_info['density']:.3f}")
                col_stats[1].metric("Avg Degree", f"{graph_info['avg_degree']:.2f}")
                
                st.info(f"**Target Node**: {target_node}")
        
        # TAB 2: Search Results
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Classical Search (Linear)")
                st.metric("Found", "✓ Yes" if classical_result['found'] else "✗ No")
                st.metric("Nodes Checked", classical_result['nodes_checked'])
                st.metric("Execution Time", f"{classical_result['execution_time']*1000:.4f} ms")
                st.metric("Complexity", "O(N)")
            
            with col2:
                st.subheader("Quantum Search (Grover)")
                st.metric("Found", "✓ Yes" if quantum_result['found'] else "✗ No")
                st.metric("Grover Iterations", quantum_result['grover_iterations'])
                st.metric("Execution Time", f"{quantum_result['execution_time']*1000:.4f} ms")
                st.metric("Success Probability", f"{quantum_result['success_probability']:.1f}%")
            
            # Comparison plot
            st.subheader("Comparison")
            results_dict = {
                'classical': classical_result,
                'quantum': quantum_result
            }
            fig = plot_search_comparison(results_dict)
            st.pyplot(fig, use_container_width=True)
        
        # TAB 3: Analysis
        with tab3:
            st.subheader("📊 Performance Analysis")
            
            # Create comparison data
            comparison_data = {
                'Algorithm': ['Classical (Linear)', 'Classical (BFS)', 'Quantum (Grover)'],
                'Steps': [
                    classical_result['nodes_checked'],
                    bfs_result['nodes_checked'],
                    quantum_result['grover_iterations']
                ],
                'Time (ms)': [
                    classical_result['execution_time'] * 1000,
                    bfs_result['execution_time'] * 1000,
                    quantum_result['execution_time'] * 1000
                ]
            }
            
            df_comparison = pd.DataFrame(comparison_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(df_comparison)
                
                # Calculate speedup
                speedup = classical_result['nodes_checked'] / quantum_result['grover_iterations']
                st.metric("Theoretical Speedup", f"{speedup:.2f}x")
                
                expected_speedup = math.sqrt(n_nodes) / (math.pi/4 * math.sqrt(n_nodes))
                st.metric("Expected Speedup", f"~√N ≈ {math.sqrt(n_nodes):.1f}x")
            
            with col2:
                # Visualization
                fig, ax = plt.subplots(figsize=(10, 6))
                
                x_pos = range(len(df_comparison))
                ax.bar(x_pos, df_comparison['Steps'], color=['#3498db', '#95a5a6', '#e74c3c'])
                ax.set_ylabel('Algorithm Steps', fontweight='bold')
                ax.set_title('Algorithm Steps Comparison', fontweight='bold')
                ax.set_xticks(x_pos)
                ax.set_xticklabels(df_comparison['Algorithm'])
                ax.grid(axis='y', alpha=0.3)
                
                # Add value labels
                for i, v in enumerate(df_comparison['Steps']):
                    ax.text(i, v, str(int(v)), ha='center', va='bottom', fontweight='bold')
                
                st.pyplot(fig, use_container_width=True)
        
        # TAB 4: Detailed Results
        with tab4:
            st.subheader("Classical Search Details")
            st.json({
                'Method': classical_result['method'],
                'Found': classical_result['found'],
                'Path': classical_result['path'][:10] if len(classical_result['path']) > 10 else classical_result['path'],
                'Nodes Checked': classical_result['nodes_checked'],
                'Execution Time': f"{classical_result['execution_time']*1000:.6f} ms"
            })
            
            st.subheader("Quantum Search Details")
            quantum_details = quantum_result['all_details']
            st.json({
                'Found': quantum_result['found'],
                'Measured Node': quantum_result['measured_node'],
                'Grover Iterations': quantum_details['iterations'],
                'Number of Qubits': quantum_details['n_qubits'],
                'Measurement Shots': quantum_details['shots'],
                'Success Probability': f"{quantum_details['success_probability']:.1f}%",
                'Success Count': quantum_details['success_count'],
                'Execution Time': f"{quantum_result['execution_time']*1000:.6f} ms"
            })
            
            st.subheader("Measurement Distribution")
            if quantum_details['all_counts']:
                counts_df = pd.DataFrame(
                    list(quantum_details['all_counts'].items()),
                    columns=['Bitstring', 'Count']
                )
                counts_df = counts_df.sort_values('Count', ascending=False).head(10)
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.barh(counts_df['Bitstring'], counts_df['Count'], color='#9b59b6')
                ax.set_xlabel('Measurement Count', fontweight='bold')
                ax.set_ylabel('Quantum State (Bitstring)', fontweight='bold')
                ax.set_title('Top 10 Measurement Results', fontweight='bold')
                ax.grid(axis='x', alpha=0.3)
                st.pyplot(fig, use_container_width=True)
        
        # TAB 5: About
        with tab5:
            st.markdown("""
            ## About This Project
            
            This interactive dashboard demonstrates **Grover's Quantum Search Algorithm** 
            and compares it with classical search methods.
            
            ### Key Concepts
            
            **Classical Search**: O(N)
            - Linear search: Check nodes one by one
            - BFS: Breadth-first traversal
            - DFS: Depth-first traversal
            
            **Quantum Search**: O(√N)
            - Uses quantum superposition and interference
            - Grover's algorithm amplifies the target state
            - Achieves quadratic speedup
            
            ### How Grover's Algorithm Works
            
            1. **Initialization**: Create uniform superposition of all states
            2. **Oracle**: Mark the target state (flip its phase)
            3. **Diffusion**: Amplify the target state's amplitude
            4. **Iteration**: Repeat steps 2-3 approximately π/4 × √N times
            5. **Measurement**: Measure to get the target state
            
            ### Formula
            
            - **Classical Complexity**: O(N)
            - **Quantum Complexity**: O(√N)
            - **Speedup**: √N times faster
            - **Optimal Iterations**: k ≈ π/4 × √N
            
            ### Applications
            
            - Database search
            - Solving NP-complete problems
            - Cryptography and security
            - Optimization problems
            - Pattern matching
            
            ### Technical Details
            
            - **Framework**: Qiskit (IBM's Quantum Computing Framework)
            - **Simulator**: Qiskit Aer StateVector Simulator
            - **Graphs**: NetworkX library
            - **Visualization**: Matplotlib and Seaborn
            
            ---
            
            **Project**: Quantum Search in Graph Nodes Using Grover's Algorithm
            
            **Author**: Quantum Computing Research Team
            
            **Year**: 2026
            """)

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.exception(e)
        progress_bar.progress(0)
        status_text.text("Error occurred!")

else:
    st.info("👈 Configure the parameters in the sidebar and click **Run Search** to start!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.9em;'>
Quantum Search in Graph Nodes | Grover's Algorithm Demo | 2026
</div>
""", unsafe_allow_html=True)
