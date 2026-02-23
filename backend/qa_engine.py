"""
QA Engine — Sewer Flow Analytics.

Implements deterministic QA checks for Sewer Flow Surveys based on 
industry-standard (WaPUG/UDG) criteria.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple

class SewerQAEngine:
    def __init__(self, risk_threshold: float = 0.8):
        self.risk_threshold = risk_threshold
        
    def calculate_completeness(self, actual_rows: int, expected_rows: int) -> float:
        if expected_rows == 0: return 0.0
        return (actual_rows / expected_rows) * 100

    def detect_dropouts(self, series: pd.Series, threshold: float = 0.05) -> float:
        total = len(series)
        if total == 0: return 0.0
        dropouts = (series < threshold).sum()
        return (dropouts / total) * 100

    def calculate_diurnal_flatness(self, series: pd.Series) -> float:
        mu = series.mean()
        sigma = series.std()
        if mu <= 0: return 0.0
        return sigma / mu

    def calculate_hydraulic_coherence(self, flow: pd.Series, depth: pd.Series) -> float:
        if len(flow) < 2 or flow.std() == 0 or depth.std() == 0:
             return 0.0
        return flow.corr(depth)

    def calculate_volume_imbalance(self, upstream_vol: float, downstream_vol: float) -> float:
        if upstream_vol == 0: return 100.0 if downstream_vol > 0 else 0.0
        return ((downstream_vol - upstream_vol) / upstream_vol) * 100

    def generate_rag_status(self, metrics: Dict) -> str:
        flags = 0
        if metrics.get('depth_dropout_pct', 0) > 20: flags += 1
        if metrics.get('flow_cv', 1.0) < 0.05: flags += 1
        if metrics.get('qh_correlation', 1.0) < 0.3: flags += 1
        if metrics.get('completeness', 100) < 95: flags += 1

        if flags == 0: return "GOOD"
        if 1 <= flags <= 2: return "MODERATE"
        return "BAD"

class StormEventAnalyzer:
    def detect_storms(self, rainfall_series: pd.Series, timestamps: pd.Series, dry_gap_hours: int = 6) -> List[Dict]:
        storms = []
        if rainfall_series.empty: return storms
        
        current_storm = None
        last_rain_time = None
        
        for i, (ts, rain) in enumerate(zip(timestamps, rainfall_series)):
            if rain > 0:
                if current_storm is None:
                    current_storm = {"id": len(storms) + 1, "start_time": ts, "end_time": ts, "data": [], "depth_mm": 0, "peak_intensity": 0}
                elif last_rain_time and (ts - last_rain_time).total_seconds() / 3600 > dry_gap_hours:
                    storms.append(self._finalize_storm(current_storm))
                    current_storm = {"id": len(storms) + 1, "start_time": ts, "end_time": ts, "data": [], "depth_mm": 0, "peak_intensity": 0}
                
                current_storm["data"].append(rain)
                current_storm["end_time"] = ts
                current_storm["peak_intensity"] = max(current_storm["peak_intensity"], rain)
                last_rain_time = ts
        
        if current_storm: storms.append(self._finalize_storm(current_storm))
        return storms

    def _finalize_storm(self, storm: Dict) -> Dict:
        storm["depth_mm"] = sum(storm["data"]) 
        storm["duration_mins"] = int((storm["end_time"] - storm["start_time"]).total_seconds() / 60)
        storm["status"] = "Significant" if storm["depth_mm"] > 5 or storm["peak_intensity"] >= 6 else "Minor"
        del storm["data"]
        return storm
