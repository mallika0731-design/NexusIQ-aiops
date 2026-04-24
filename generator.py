"""
Synthetic IT Telemetry Generator
Generates realistic 14-service telemetry with correlated signals
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

SERVICE_NAMES = [
    'auth-service', 'user-service', 'payment-service', 'order-service',
    'inventory-service', 'cart-service', 'recommendation-service',
    'notification-service', 'analytics-service', 'search-service',
    'frontend-api', 'load-balancer', 'database', 'cache'
]

def generate_telemetry(demo_mode=True, seed=42):
    """Generate train/val/test telemetry splits"""
    np.random.seed(seed)
    
    n_samples = 480  # 8 hours @ 1min intervals
    n_train, n_val, n_test = int(0.6*n_samples), int(0.2*n_samples), int(0.2*n_samples)
    
    timestamps = pd.date_range('2026-04-24 08:00', periods=n_samples, freq='1min')
    
    # Base diurnal patterns
    hour = np.sin(2 * np.pi * np.arange(n_samples) / (60*24)) * 0.1
    baseline = 100 + hour * 20
    
    data = {}
    for i, service in enumerate(SERVICE_NAMES):
        # Service-specific patterns
        service_noise = np.random.normal(0, 5, n_samples)
        correlated = np.roll(baseline + service_noise, i*10)  # Time-shifted correlation
        
        # Anomalies (deterministic for demo)
        anomaly_signal = np.zeros(n_samples)
        if demo_mode:
            # Cascade anomaly at hour 6 (14:00)
            cascade_start = 360
            anomaly_signal[cascade_start:cascade_start+60] = np.linspace(0, 50, 60)
            # Point anomaly on payment-service
            anomaly_signal[200] = 80
            # Contextual anomaly on database (high during low baseline)
            anomaly_signal[100:120] = 60
        
        data[service] = correlated + anomaly_signal
    
    df = pd.DataFrame(data, index=timestamps)
    
    # Train/val/test splits (no leakage)
    train_df = df.iloc[:n_train].copy()
    val_df = df.iloc[n_train:n_train+n_val].copy()
    test_df = df.iloc[n_train+n_val:].copy()
    
    service_meta = {
        'services': SERVICE_NAMES,
        'dependencies': build_dependency_graph()
    }
    
    return train_df, val_df, test_df, service_meta

def build_dependency_graph():
    """Service dependency structure"""
    deps = {
        'frontend-api': ['load-balancer'],
        'load-balancer': ['auth-service', 'user-service'],
        'auth-service': ['database'],
        'user-service': ['database', 'cache'],
        'payment-service': ['order-service', 'database'],
        'order-service': ['inventory-service', 'cart-service'],
        'cart-service': ['user-service'],
        'inventory-service': ['database'],
        'recommendation-service': ['analytics-service', 'user-service'],
        'search-service': ['database', 'cache'],
        'notification-service': ['order-service'],
        'analytics-service': ['database']
    }
    return deps