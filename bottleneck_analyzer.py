"""
Bottleneck Analysis App
Based on concepts from Iravani's Operations Engineering and Management (Chapters 2 & 4)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Tuple
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Process Bottleneck Analyzer",
    page_icon="🏭",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .bottleneck-highlight {
        background-color: #ffcccc;
        padding: 10px;
        border-radius: 5px;
        border: 2px solid #ff4444;
    }
    .capacity-good {
        color: #00aa00;
    }
    .capacity-bottleneck {
        color: #ff0000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'process_steps' not in st.session_state:
    st.session_state.process_steps = []
if 'resources' not in st.session_state:
    st.session_state.resources = {}

# Header
st.title("🏭 Process Bottleneck Analyzer")
st.markdown("*Based on Iravani's Operations Engineering and Management methodology*")

# Sidebar for instructions
with st.sidebar:
    st.header("📚 How to Use")
    st.markdown("""
    ### Step 1: Define Process Steps
    - Enter the name of each process step
    - Specify the processing time (duration) for each step
    - Add the number of resources (workers, machines) available
    
    ### Step 2: Analyze
    - View capacity calculations for each step
    - Identify the bottleneck (lowest capacity)
    - Review throughput and utilization metrics
    
    ### Key Concepts:
    - **Capacity** = Resources / Processing Time
    - **Bottleneck** = Step with lowest capacity
    - **System Throughput** = Bottleneck capacity
    - **Utilization** = System Throughput / Step Capacity
    """)
    
    st.divider()
    st.info("💡 The bottleneck determines the maximum flow rate through the entire system")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📝 Process Input", "📊 Analysis", "📈 Visualizations", "📋 Report"])

with tab1:
    st.header("Define Your Process")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Add Process Steps")
        
        with st.form("add_step_form"):
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                step_name = st.text_input("Step Name", placeholder="e.g., Assembly, Testing")
            with col_b:
                duration = st.number_input("Processing Time (minutes)", min_value=0.1, value=1.0, step=0.1)
            with col_c:
                resources = st.number_input("Number of Resources", min_value=1, value=1, step=1)
            
            col_submit, col_clear = st.columns([1, 1])
            with col_submit:
                if st.form_submit_button("➕ Add Step", type="primary", use_container_width=True):
                    if step_name:
                        st.session_state.process_steps.append({
                            'name': step_name,
                            'duration': duration,
                            'resources': resources,
                            'capacity': resources / duration
                        })
                        st.success(f"Added step: {step_name}")
                        st.rerun()
            
            with col_clear:
                if st.form_submit_button("🗑️ Clear All Steps", use_container_width=True):
                    st.session_state.process_steps = []
                    st.rerun()
    
    with col2:
        st.subheader("Quick Templates")
        
        if st.button("📦 Load Manufacturing Example", use_container_width=True):
            st.session_state.process_steps = [
                {'name': 'Cutting', 'duration': 2.0, 'resources': 2, 'capacity': 1.0},
                {'name': 'Welding', 'duration': 3.0, 'resources': 2, 'capacity': 0.67},
                {'name': 'Assembly', 'duration': 4.0, 'resources': 3, 'capacity': 0.75},
                {'name': 'Testing', 'duration': 1.5, 'resources': 1, 'capacity': 0.67},
                {'name': 'Packaging', 'duration': 1.0, 'resources': 2, 'capacity': 2.0}
            ]
            st.success("Loaded manufacturing example")
            st.rerun()
        
        if st.button("🍕 Load Service Example", use_container_width=True):
            st.session_state.process_steps = [
                {'name': 'Order Taking', 'duration': 1.0, 'resources': 2, 'capacity': 2.0},
                {'name': 'Food Preparation', 'duration': 10.0, 'resources': 3, 'capacity': 0.3},
                {'name': 'Cooking', 'duration': 8.0, 'resources': 4, 'capacity': 0.5},
                {'name': 'Quality Check', 'duration': 0.5, 'resources': 1, 'capacity': 2.0},
                {'name': 'Delivery', 'duration': 2.0, 'resources': 5, 'capacity': 2.5}
            ]
            st.success("Loaded service example")
            st.rerun()
    
    st.divider()
    
    # Display current process steps
    if st.session_state.process_steps:
        st.subheader("Current Process Steps")
        
        # Create DataFrame for display
        df = pd.DataFrame(st.session_state.process_steps)
        df['Capacity (units/min)'] = df['capacity'].round(3)
        
        # Identify bottleneck
        bottleneck_idx = df['capacity'].idxmin()
        df['Status'] = ''
        df.loc[bottleneck_idx, 'Status'] = '🔴 BOTTLENECK'
        
        # Display with custom formatting
        st.dataframe(
            df[['name', 'duration', 'resources', 'Capacity (units/min)', 'Status']].rename(columns={
                'name': 'Step Name',
                'duration': 'Processing Time (min)',
                'resources': 'Resources'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Option to remove individual steps
        if st.checkbox("Enable step removal"):
            step_to_remove = st.selectbox("Select step to remove", 
                                         [step['name'] for step in st.session_state.process_steps])
            if st.button("Remove Selected Step"):
                st.session_state.process_steps = [s for s in st.session_state.process_steps 
                                                 if s['name'] != step_to_remove]
                st.rerun()
    else:
        st.info("👆 Add process steps above to begin analysis")

with tab2:
    st.header("Bottleneck Analysis Results")
    
    if st.session_state.process_steps:
        df = pd.DataFrame(st.session_state.process_steps)
        
        # Calculate key metrics
        bottleneck_idx = df['capacity'].idxmin()
        bottleneck_step = df.loc[bottleneck_idx]
        system_throughput = bottleneck_step['capacity']
        
        # Calculate utilization for each step
        df['utilization'] = (system_throughput / df['capacity'] * 100).round(1)
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🔴 Bottleneck Step",
                bottleneck_step['name'],
                f"{bottleneck_step['capacity']:.3f} units/min"
            )
        
        with col2:
            st.metric(
                "⚡ System Throughput",
                f"{system_throughput:.3f} units/min",
                f"{system_throughput * 60:.1f} units/hour"
            )
        
        with col3:
            avg_utilization = df['utilization'].mean()
            st.metric(
                "📊 Average Utilization",
                f"{avg_utilization:.1f}%",
                f"Range: {df['utilization'].min():.1f}% - {df['utilization'].max():.1f}%"
            )
        
        with col4:
            cycle_time = 1 / system_throughput if system_throughput > 0 else float('inf')
            st.metric(
                "⏱️ System Cycle Time",
                f"{cycle_time:.2f} min/unit",
                f"Max output: {1/cycle_time * 60:.1f} units/hour"
            )
        
        st.divider()
        
        # Detailed step analysis
        st.subheader("Step-by-Step Analysis")
        
        for idx, step in df.iterrows():
            if idx == bottleneck_idx:
                st.markdown(f"""
                <div class="bottleneck-highlight">
                    <h4>🔴 {step['name']} - BOTTLENECK</h4>
                    <p>This step limits the entire system's throughput</p>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(f"{step['name']}", f"{step['resources']} resources")
            with col2:
                st.metric("Processing Time", f"{step['duration']:.1f} min")
            with col3:
                capacity_class = "capacity-bottleneck" if idx == bottleneck_idx else "capacity-good"
                st.metric("Capacity", f"{step['capacity']:.3f} units/min")
            with col4:
                utilization_color = "🔴" if step['utilization'] >= 90 else "🟡" if step['utilization'] >= 70 else "🟢"
                st.metric("Utilization", f"{utilization_color} {step['utilization']:.1f}%")
        
        st.divider()
        
        # Improvement suggestions
        st.subheader("💡 Improvement Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Primary Focus: {bottleneck_step['name']}**
            
            Options to increase capacity:
            1. Add {1} more resource → New capacity: {(bottleneck_step['resources']+1)/bottleneck_step['duration']:.3f} units/min
            2. Reduce processing time by 20% → New capacity: {bottleneck_step['resources']/(bottleneck_step['duration']*0.8):.3f} units/min
            3. Implement parallel processing if feasible
            """)
        
        with col2:
            # Find next bottleneck
            df_sorted = df.sort_values('capacity')
            if len(df_sorted) > 1:
                next_bottleneck = df_sorted.iloc[1]
                st.warning(f"""
                **Secondary Bottleneck: {next_bottleneck['name']}**
                
                Current capacity: {next_bottleneck['capacity']:.3f} units/min
                
                Once the primary bottleneck is resolved, this will become the new constraint.
                """)
    else:
        st.info("📝 Please add process steps in the Process Input tab")

with tab3:
    st.header("Process Visualizations")
    
    if st.session_state.process_steps:
        df = pd.DataFrame(st.session_state.process_steps)
        bottleneck_idx = df['capacity'].idxmin()
        system_throughput = df.loc[bottleneck_idx, 'capacity']
        df['utilization'] = (system_throughput / df['capacity'] * 100).round(1)
        
        # Capacity comparison chart
        st.subheader("📊 Capacity Comparison")
        
        fig_capacity = go.Figure()
        
        colors = ['red' if i == bottleneck_idx else 'lightblue' for i in range(len(df))]
        
        fig_capacity.add_trace(go.Bar(
            x=df['name'],
            y=df['capacity'],
            marker_color=colors,
            text=[f"{cap:.3f}" for cap in df['capacity']],
            textposition='auto',
            name='Capacity'
        ))
        
        # Add throughput line
        fig_capacity.add_hline(
            y=system_throughput, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"System Throughput: {system_throughput:.3f}"
        )
        
        fig_capacity.update_layout(
            title="Process Step Capacities (units/minute)",
            xaxis_title="Process Step",
            yaxis_title="Capacity (units/min)",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_capacity, use_container_width=True)
        
        # Utilization chart
        st.subheader("📈 Resource Utilization")
        
        fig_util = go.Figure()
        
        # Color based on utilization level
        util_colors = []
        for util in df['utilization']:
            if util >= 90:
                util_colors.append('red')
            elif util >= 70:
                util_colors.append('orange')
            else:
                util_colors.append('green')
        
        fig_util.add_trace(go.Bar(
            x=df['name'],
            y=df['utilization'],
            marker_color=util_colors,
            text=[f"{util:.1f}%" for util in df['utilization']],
            textposition='auto'
        ))
        
        fig_util.update_layout(
            title="Resource Utilization by Process Step",
            xaxis_title="Process Step",
            yaxis_title="Utilization (%)",
            yaxis_range=[0, 105],
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_util, use_container_width=True)
        
        # Process flow diagram
        st.subheader("🔄 Process Flow Diagram")
        
        # Create a simple flow diagram
        fig_flow = go.Figure()
        
        # Calculate positions
        x_positions = list(range(len(df)))
        y_position = 0
        
        # Add process boxes
        for i, (idx, step) in enumerate(df.iterrows()):
            box_color = 'red' if idx == bottleneck_idx else 'lightblue'
            
            fig_flow.add_trace(go.Scatter(
                x=[x_positions[i]],
                y=[y_position],
                mode='markers+text',
                marker=dict(size=60, color=box_color, line=dict(width=2, color='black')),
                text=[f"{step['name']}<br>{step['capacity']:.2f} u/m"],
                textposition='middle center',
                showlegend=False
            ))
            
            # Add arrows between steps
            if i < len(df) - 1:
                fig_flow.add_annotation(
                    x=x_positions[i] + 0.5,
                    y=y_position,
                    ax=x_positions[i] + 0.3,
                    ay=y_position,
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="black"
                )
        
        fig_flow.update_layout(
            title="Process Flow with Capacities",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 1]),
            height=200,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig_flow, use_container_width=True)
        
        # Resource allocation pie chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥧 Resource Distribution")
            fig_pie = px.pie(
                df, 
                values='resources', 
                names='name',
                title="Resource Allocation Across Steps"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("⏱️ Time Distribution")
            fig_time = px.pie(
                df, 
                values='duration', 
                names='name',
                title="Processing Time Distribution"
            )
            st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("📝 Please add process steps in the Process Input tab")

with tab4:
    st.header("📋 Analysis Report")
    
    if st.session_state.process_steps:
        df = pd.DataFrame(st.session_state.process_steps)
        bottleneck_idx = df['capacity'].idxmin()
        bottleneck_step = df.loc[bottleneck_idx]
        system_throughput = bottleneck_step['capacity']
        df['utilization'] = (system_throughput / df['capacity'] * 100).round(1)
        
        # Generate report
        report = f"""
# Process Bottleneck Analysis Report
        
## Executive Summary
- **Bottleneck Step:** {bottleneck_step['name']}
- **System Throughput:** {system_throughput:.3f} units/minute ({system_throughput * 60:.1f} units/hour)
- **Bottleneck Capacity:** {bottleneck_step['capacity']:.3f} units/minute
- **Average Utilization:** {df['utilization'].mean():.1f}%

## Process Steps Analysis

| Step Name | Resources | Processing Time (min) | Capacity (units/min) | Utilization (%) | Status |
|-----------|-----------|---------------------|---------------------|----------------|---------|
"""
        
        for idx, step in df.iterrows():
            status = "**BOTTLENECK**" if idx == bottleneck_idx else "Normal"
            report += f"| {step['name']} | {step['resources']} | {step['duration']:.1f} | {step['capacity']:.3f} | {step['utilization']:.1f}% | {status} |\n"
        
        report += f"""

## Key Findings

1. The bottleneck step **{bottleneck_step['name']}** limits the entire system to {system_throughput:.3f} units per minute.
2. This step has {bottleneck_step['resources']} resource(s) with a processing time of {bottleneck_step['duration']:.1f} minutes.
3. All other steps are operating below full capacity due to this constraint.

## Recommendations

### Immediate Actions
1. **Focus on {bottleneck_step['name']}:**
   - Consider adding resources to this step
   - Investigate ways to reduce processing time
   - Evaluate if work can be redistributed

### Capacity Improvements
- Adding 1 resource to {bottleneck_step['name']} would increase capacity to {(bottleneck_step['resources']+1)/bottleneck_step['duration']:.3f} units/min
- Reducing processing time by 20% would increase capacity to {bottleneck_step['resources']/(bottleneck_step['duration']*0.8):.3f} units/min

### Long-term Considerations
- Monitor the next constraining step after improvements
- Consider implementing buffer management before the bottleneck
- Evaluate overall process redesign opportunities
        """
        
        st.markdown(report)
        
        # Download button for report
        st.download_button(
            label="📥 Download Report (Markdown)",
            data=report,
            file_name="bottleneck_analysis_report.md",
            mime="text/markdown"
        )
        
        # Export data as CSV
        export_df = df[['name', 'duration', 'resources', 'capacity', 'utilization']].copy()
        export_df.columns = ['Step Name', 'Processing Time (min)', 'Resources', 'Capacity (units/min)', 'Utilization (%)']
        
        csv = export_df.to_csv(index=False)
        st.download_button(
            label="📊 Download Data (CSV)",
            data=csv,
            file_name="process_data.csv",
            mime="text/csv"
        )
    else:
        st.info("📝 Please add process steps in the Process Input tab to generate a report")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>Built for Operations Management education | Based on Iravani's methodology</p>
    <p>Understanding bottlenecks is key to process improvement 🎯</p>
</div>
""", unsafe_allow_html=True)
