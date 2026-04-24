"""
NexusIQ Pro - Production Streamlit Dashboard
Dark theme, interactive graph, PPT exports
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import pandas as pd
import json
from streamlit_plotly_events import plotly_events

def launch_dashboard(results):
    """Launch premium Streamlit dashboard"""
    st.set_page_config(
        page_title="NexusIQ Pro",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for premium look
    st.markdown("""
    <style>
    .main {background-color: #0e1117;}
    .stApp {background-color: #0e1117;}
    .stMetric {background-color: #1f2937; color: white;}
    h1 {color: #3b82f6; font-family: 'Segoe UI', sans-serif;}
    .stPlotlyChart {border-radius: 12px;}
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🚀 NexusIQ Pro")
    st.markdown("**AIOps Intelligence Platform** - Real-time anomaly detection & root cause analysis")
    
    detector, test_df, test_scores, anomalies, root_causes, blast_radius, incident_memo, service_meta = (
        results['detector'], results['test_df'], results['test_scores'], 
        results['anomalies'], results['root_causes'], results['blast_radius'],
        results['incident_memo'], results['service_meta']
    )
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Anomalies Detected", len(anomalies))
    with col2:
        st.metric("Root Causes", len(root_causes))
    with col3:
        st.metric("Blast Radius", sum(blast_radius.values()))
    with col4:
        st.metric("Confidence", f"{incident_memo['confidence_score']:.1%}")
    
    # Main dashboard
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("🕒 Anomaly Timeline")
        fig = px.line(
            x=test_df.index, 
            y=test_scores,
            title="Anomaly Scores Over Time",
            color_discrete_sequence=['#3b82f6']
        )
        fig.add_hline(y=detector.threshold, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("📊 Incident Memo")
        with st.expander("Details", expanded=True):
            st.json(incident_memo)
        
        # Downloads
        st.download_button(
            "📥 Download Memo JSON",
            data=json.dumps(incident_memo, indent=2),
            file_name="nexusIQ_incident_memo.json"
        )
    
    # Service Graph
    st.subheader("🌐 Service Dependency Graph")
    rca = RootCauseAnalyzer(service_meta)
    graph_data = rca.get_graph_visualization(anomalies.columns.tolist())
    
    # Interactive graph
    fig = go.Figure(data=go.Scatter(
        x=[graph_data['pos'][node][0] for node in graph_data['nodes']],
        y=[graph_data['pos'][node][1] for node in graph_data['nodes']],
        mode='markers+text',
        text=graph_data['nodes'],
        marker=dict(size=20, color=graph_data['colors'], line=dict(width=2, color='white')),
        textposition="middle center",
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    # Add edges
    for src, dst in graph_data['edges']:
        x0, y0 = graph_data['pos'][src]
        x1, y1 = graph_data['pos'][dst]
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode='lines',
            line=dict(width=3, color='#6b7280'),
            hoverinfo='none',
            showlegend=False
        ))
    
    fig.update_layout(title="Service Dependencies (Red=Anomalous)", showlegend=False)
    selected_points = plotly_events(fig)
    
    # Footer
    st.markdown("---")
    st.markdown("*NexusIQ Pro - Production-ready AIOps platform*")

if __name__ == "__main__":
    # For local testing
    from script import main
    results = main()
    launch_dashboard(results)