"""
Local Retrieval-Augmented Incident Memo Generation
FAISS + template-based grounding (no APIs)
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import faiss

class IncidentMemoGenerator:
    def __init__(self):
        self.runbooks = self._load_runbooks()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self._build_index()
    
    def _load_runbooks(self):
        """20+ realistic runbook documents"""
        runbooks = [
            "Payment service latency: Check database connection pool exhaustion. Restart connection pool. Scale database read replicas.",
            "Database outage: Primary node failed. Promote replica. Check disk I/O saturation. Run fsck on data volumes.",
            "Auth service 500s: JWT signing key rotation failed. Rollback key rotation. Verify key vault access.",
            "Load balancer 502s: Health check failures. Verify backend service ports. Check security group rules.",
            "Cache miss storm: Redis cluster rebalance. Increase memory limit. Enable eviction policy.",
            "Frontend API timeout: Increase nginx timeout. Check upstream service latency. Add circuit breaker.",
            "Inventory service deadlock: Long-running transactions. Kill blocking queries. Optimize indexes.",
            "Notification queue backlog: Consumer crash. Scale consumer group. Check dead letter queue.",
            "Recommendation service OOM: Model too large. Use model quantization. Add paging to requests.",
            "Search service down: Elasticsearch cluster yellow. Allocate missing replicas. Check disk watermark.",
            "Order service cascade failure: Payment timeout → inventory lock → order rollback. Circuit break payment service.",
            "User service memory leak: Session objects not garbage collected. Restart service. Profile heap dumps.",
            "Analytics service spike: Aggregation query timeout. Add materialized views. Partition fact tables.",
            "Cascade anomaly pattern: Database → payment → order → notification. Isolate database first.",
            "Point anomaly isolation: Single service spike usually self-contained. Monitor for 15 minutes.",
            "Contextual anomaly: High traffic during low baseline indicates real issue. Immediate escalation.",
            "Blast radius calculation: Service A affects 8 downstream services. Prioritize containment.",
            "Root cause verification: Confirm no upstream anomalies before declaring root cause."
        ]
        return runbooks
    
    def _build_index(self):
        """Build FAISS index"""
        self.tfidf_matrix = self.vectorizer.fit_transform(self.runbooks)
        dimension = self.tfidf_matrix.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(self.tfidf_matrix.toarray().astype('float32'))
        self.index = index
    
    def generate(self, anomalies, root_causes, blast_radius, scores):
        """Generate structured incident memo"""
        anomalous_services = list(anomalies.columns[anomalies.iloc[-1] > 0])
        
        # Retrieval query
        query = f"Anomalies in {', '.join(anomalous_services[:3])}. Root causes: {', '.join(root_causes)}"
        query_vec = self.vectorizer.transform([query]).toarray().astype('float32')
        
        # Retrieve top-3
        distances, indices = self.index.search(query_vec, 3)
        evidence = [self.runbooks[i] for i in indices[0]]
        
        # Confidence score
        confidence = 1 - (distances[0][0] / np.max(distances[0]))
        
        memo = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'summary': f'Detected cascade anomaly affecting {len(anomalous_services)} services',
            'root_causes': root_causes,
            'anomalous_services': anomalous_services,
            'blast_radius': {k: v for k, v in blast_radius.items() if v > 0},
            'evidence_snippets': evidence,
            'confidence_score': float(confidence),
            'severity': 'HIGH' if len(root_causes) > 1 else 'MEDIUM',
            'recommended_actions': [
                f"Isolate root cause services: {', '.join(root_causes)}",
                "Scale upstream capacity by 200%",
                "Enable circuit breakers on affected paths",
                "Run post-mortem after stabilization"
            ]
        }
        
        return memo