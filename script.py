"""
NexusIQ Pro - Complete AIOps Pipeline Orchestrator
Single entrypoint for end-to-end execution
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from datetime import datetime, timedelta

# Local imports
from data.generator import generate_telemetry
from models.ensemble_detector import EnsembleAnomalyDetector
from graph.rca import RootCauseAnalyzer
from rag.local import IncidentMemoGenerator
from dashboard.pro import launch_dashboard

def main(demo_mode=True):
    """Complete pipeline execution"""
    print("🚀 NexusIQ Pro - AIOps Intelligence Platform")
    print("=" * 50)
    
    # 1. Generate synthetic telemetry
    print("\n📊 [1/5] Generating synthetic IT telemetry...")
    train_df, val_df, test_df, service_meta = generate_telemetry(demo_mode=demo_mode)
    
    # 2. Train anomaly detector
    print("\n🔍 [2/5] Training ensemble anomaly detector...")
    detector = EnsembleAnomalyDetector()
    detector.fit(train_df, val_df)
    test_scores = detector.score(test_df)
    
    # 3. Root cause analysis
    print("\n📈 [3/5] Performing graph-based root cause analysis...")
    rca = RootCauseAnalyzer(service_meta)
    anomalies = test_df[test_scores > detector.threshold]
    root_causes, blast_radius = rca.analyze(anomalies)
    
    # 4. Generate incident memo
    print("\n📝 [4/5] Generating retrieval-augmented incident memo...")
    memo_gen = IncidentMemoGenerator()
    incident_memo = memo_gen.generate(
        anomalies=anomalies,
        root_causes=root_causes,
        blast_radius=blast_radius,
        test_scores=test_scores
    )
    
    # 5. Generate PPT visuals
    print("\n🎨 [5/5] Generating PPT-ready visuals...")
    generate_ppt_visuals(test_df, test_scores, detector, rca, incident_memo)
    
    # Results
    results = {
        'detector': detector,
        'test_df': test_df,
        'test_scores': test_scores,
        'anomalies': anomalies,
        'root_causes': root_causes,
        'blast_radius': blast_radius,
        'incident_memo': incident_memo,
        'service_meta': service_meta
    }
    
    print("\n✅ Pipeline complete! Launching dashboard...")
    return results

def generate_ppt_visuals(test_df, test_scores, detector, rca, incident_memo):
    """Generate slide-ready PNGs and CSV"""
    os.makedirs("PPT_Visuals", exist_ok=True)
    
    # Anomaly heatmap
    import plotly.express as px
    fig = px.imshow(
        test_scores.values.reshape(1, -1),
        title="Anomaly Heatmap - Test Period",
        color_continuous_scale="Reds"
    )
    fig.write_image("PPT_Visuals/anomaly_heatmap.png")
    
    # Save metrics
    metrics = pd.DataFrame({
        'Metric': ['Precision', 'Recall', 'F1', 'Threshold'],
        'Value': [detector.precision, detector.recall, detector.f1, detector.threshold]
    })
    metrics.to_csv("PPT_Visuals/metrics_table.csv", index=False)

if __name__ == "__main__":
    results = main(demo_mode=True)
    launch_dashboard(results)