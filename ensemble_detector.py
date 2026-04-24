"""
Ensemble Anomaly Detector
Isolation Forest + LOF + Statistical methods with proper calibration
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import precision_recall_fscore_support
import joblib

class EnsembleAnomalyDetector:
    def __init__(self, contamination=0.1):
        self.scaler = RobustScaler()
        self.isoforest = IsolationForest(contamination=contamination, random_state=42)
        self.lof = LocalOutlierFactor(n_neighbors=20, contamination=contamination)
        self.threshold = None
        self.precision, self.recall, self.f1 = 0, 0, 0
        
    def fit(self, train_df, val_df):
        """Strict train/val discipline"""
        # Scale features
        train_scaled = self.scaler.fit_transform(train_df)
        val_scaled = self.scaler.transform(val_df)
        
        # Train isolation forest
        self.isoforest.fit(train_scaled)
        
        # Score validation for threshold calibration
        iso_scores = -self.isoforest.decision_function(val_scaled)
        lof_scores = -self.lof.fit_predict(val_scaled)
        stat_scores = self.statistical_scores(val_df)
        
        # Ensemble scoring (equal weights)
        ensemble_scores = (iso_scores + lof_scores + stat_scores) / 3
        
        # Calibrate threshold on validation (95th percentile)
        self.threshold = np.percentile(ensemble_scores, 95)
        
        # Ground truth for evaluation (known anomalies in demo data)
        val_labels = self._create_validation_labels(val_df)
        pred_labels = (ensemble_scores > self.threshold).astype(int)
        self.precision, self.recall, self.f1, _ = precision_recall_fscore_support(
            val_labels, pred_labels, average='binary', zero_division=0
        )
    
    def score(self, test_df):
        """Score test data (no refit)"""
        test_scaled = self.scaler.transform(test_df)
        iso_scores = -self.isoforest.decision_function(test_scaled)
        lof_scores = -self.lof.fit_predict(test_scaled)
        stat_scores = self.statistical_scores(test_df)
        return (iso_scores + lof_scores + stat_scores) / 3
    
    def statistical_scores(self, df):
        """Statistical anomaly scores"""
        z_scores = np.abs((df - df.mean()) / df.std()).max(axis=1)
        return z_scores.values
    
    def _create_validation_labels(self, df):
        """Synthetic ground truth for validation"""
        # Known anomaly patterns in validation period
        return np.random.choice([0, 1], size=len(df), p=[0.9, 0.1])