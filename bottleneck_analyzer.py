"""
Bottleneck Analysis App - Streamlit Cloud Optimized Version
Based on Iravani's Operations Engineering and Management
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Process Bottleneck Analyzer",
    page_icon="🏭",
    layout="wide"
)

# Initialize session state
if 'process_steps' not in st.session_state:
    st.session_state.process_steps = []

# Header
st.title("🏭 Process Bottleneck Analyzer")
st.markdown("*Based on Iravani's Operations Engineering and Management methodology*")

# Sidebar for instructions
with st.sidebar:
    st.header("📚 How to Use")
    st.markdown("""
    ### Step 1: Define Process Steps
    - Enter the name of each process step
    - Specify the processing time for each step
    - Add the number of resources available
    
    ### Step 2: Analyze
    - View capacity calculations
    - Identify the bottleneck
    - Review utilization metrics
    
    ### Key Formula:
    **Capacity = Resources / Processing Time**
    """)
    
    st.info("💡 The bottleneck determines the maximum flow rate")

# Main content area
tab1, tab2, tab3 = st.tabs(["📝 Process Input", "📊 Analysis", "📈 Visualizations"])

with tab1:
    st.header("Define Your Process")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Add Process Steps")
        
        with st.form("add_step_form"):
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                step_name = st.text_input("Step Name")
            with col_b:
                duration = st.number_input("Processing Time (min)", min_value=0.1, value=1.0)
            with col_c:
                resources = st.number_input("Resources", min_value=1, value=1)
            
            if st.form_submit_button("➕ Add Step", type="primary"):
                if step_name:
                    st.session_state.process_steps.append({
                        'name': step_name,
                        'duration': duration,
                        'resources': resources,
                        'capacity': resources / duration
                    })
                    st.success(f"Added: {step_name}")
                    st.rerun()
    
    with col2:
        st.subheader("Quick Example")
        
        if st.button("Load Example"):
            st.session_state.process_steps = [
                {'name': 'Cutting', 'duration': 2.0, 'resources': 2, 'capacity': 1.0},
                {'name': 'Welding', 'duration': 3.0, 'resources': 2, 'capacity': 0.67},
                {'name': 'Assembly', 'duration': 4.0, 'resources': 3, 'capacity': 0.75},
                {'name': 'Testing', 'duration': 1.5, 'resources': 1, 'capacity': 0.67},
                {'name': 'Packaging', 'duration': 1.0, 'resources': 2, 'capacity': 2.0}
            ]
            st.rerun()
        
        if st.button("Clear All"):
            st.session_state.process_steps = []
            st.rerun()
    
    # Display current process steps
    if st.session_state.process_steps:
        st.subheader("Current Process Steps")
        
        df = pd.DataFrame(st.session_state.process_steps)
        df['capacity'] = df['capacity'].round(3)
        
        # Identify bottleneck
        bottleneck_idx = df['capacity'].idxmin()
        df['Status'] = ''
        df.loc[bottleneck_idx, 'Status'] = '🔴 BOTTLENECK'
        
        st.dataframe(df, use_container_width=True, hide_index=True)

with tab2:
    st.header("Bottleneck Analysis")
    
    if st.session_state.process_steps:
        df = pd.DataFrame(st.session_state.process_steps)
        
        # Calculate metrics
        bottleneck_idx = df['capacity'].idxmin()
        bottleneck_step = df.loc[bottleneck_idx]
        system_throughput = bottleneck_step['capacity']
        
        # Calculate utilization
        df['utilization'] = (system_throughput / df['capacity'] * 100).round(1)
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "🔴 Bottleneck",
                bottleneck_step['name'],
                f"{bottleneck_step['capacity']:.3f} units/min"
            )
        
        with col2:
            st.metric(
                "⚡ Throughput",
                f"{system_throughput:.3f} units/min",
                f"{system_throughput * 60:.1f} units/hour"
            )
        
        with col3:
            st.metric(
                "📊 Avg Utilization",
                f"{df['utilization'].mean():.1f}%"
            )
        
        st.divider()
        
        # Step details
        st.subheader("Step Details")
        
        for idx, step in df.iterrows():
            if idx == bottleneck_idx:
                st.error(f"🔴 **{step['name']}** - BOTTLENECK")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.write(f"**{step['name']}**")
            with col2:
                st.write(f"Time: {step['duration']:.1f} min")
            with col3:
                st.write(f"Capacity: {step['capacity']:.3f}")
            with col4:
                st.write(f"Util: {step['utilization']:.1f}%")
        
        # Recommendations
        st.divider()
        st.subheader("💡 Recommendations")
        st.info(f"""
        Focus on **{bottleneck_step['name']}**:
        - Add 1 resource → Capacity: {(bottleneck_step['resources']+1)/bottleneck_step['duration']:.3f} units/min
        - Reduce time 20% → Capacity: {bottleneck_step['resources']/(bottleneck_step['duration']*0.8):.3f} units/min
        """)
    else:
        st.info("Add process steps in the Process Input tab")

with tab3:
    st.header("Visualizations")
    
    if st.session_state.process_steps:
        df = pd.DataFrame(st.session_state.process_steps)
        bottleneck_idx = df['capacity'].idxmin()
        system_throughput = df.loc[bottleneck_idx, 'capacity']
        df['utilization'] = (system_throughput / df['capacity'] * 100).round(1)
        
        # Capacity chart
        st.subheader("Capacity Comparison")
        
        fig_capacity = go.Figure()
        colors = ['red' if i == bottleneck_idx else 'lightblue' for i in range(len(df))]
        
        fig_capacity.add_trace(go.Bar(
            x=df['name'],
            y=df['capacity'],
            marker_color=colors,
            text=[f"{cap:.3f}" for cap in df['capacity']],
            textposition='auto'
        ))
        
        fig_capacity.add_hline(
            y=system_throughput, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Throughput: {system_throughput:.3f}"
        )
        
        fig_capacity.update_layout(
            xaxis_title="Process Step",
            yaxis_title="Capacity (units/min)",
            height=400
        )
        
        st.plotly_chart(fig_capacity, use_container_width=True)
        
        # Utilization chart
        st.subheader("Resource Utilization")
        
        fig_util = go.Figure(go.Bar(
            x=df['name'],
            y=df['utilization'],
            text=[f"{util:.1f}%" for util in df['utilization']],
            textposition='auto'
        ))
        
        fig_util.update_layout(
            xaxis_title="Process Step",
            yaxis_title="Utilization (%)",
            yaxis_range=[0, 105],
            height=400
        )
        
        st.plotly_chart(fig_util, use_container_width=True)
    else:
        st.info("Add process steps to see visualizations")

# Footer
st.divider()
st.caption("Built for Operations Management education | Based on Iravani's methodology")
