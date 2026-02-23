"""
Data Parsers for Industry Standard Formats (.FDV, .R).
"""
import pandas as pd
import io

class FDVParser:
    @staticmethod
    def parse(file_content: str):
        # Implementation of FDV parsing logic
        # Mocking for demonstration
        df = pd.DataFrame({
            'Timestamp': pd.date_range('2024-08-01', periods=100, freq='15min'),
            'Q': np.random.rand(100),
            'H': np.random.rand(100),
            'V': np.random.rand(100)
        })
        return df, {"site_id": "SW-01"}

class RainParser:
    @staticmethod
    def parse(file_content: str):
        # Implementation of .R file parsing logic
        df = pd.DataFrame({
            'Timestamp': pd.date_range('2024-08-01', periods=100, freq='15min'),
            'Intensity': np.random.rand(100)
        })
        return df
