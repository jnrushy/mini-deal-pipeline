import pandas as pd
from dagster import asset, Output
from typing import List, Dict
import os

@asset
def raw_dsp_report() -> Output[pd.DataFrame]:
    """Reads the raw DSP report from CSV file."""
    # In a real implementation, this would read from an actual file
    # For now, we'll create a sample DataFrame
    data = {
        'campaign_id': ['C1', 'C2', 'C3', 'C4'],
        'impressions': [1000, 2000, 1500, 3000],
        'revenue': [10.0, 15.0, 7.5, 30.0],
        'cpm': [10.0, 7.5, 5.0, 10.0]
    }
    df = pd.DataFrame(data)
    return Output(df, metadata={"num_rows": len(df)})

@asset
def cleaned_dsp_report(raw_dsp_report: pd.DataFrame) -> Output[pd.DataFrame]:
    """Cleans the DSP report by removing low CPM entries."""
    # Filter out entries with CPM less than 7.0
    cleaned_df = raw_dsp_report[raw_dsp_report['cpm'] >= 7.0]
    return Output(
        cleaned_df,
        metadata={
            "num_rows": len(cleaned_df),
            "removed_rows": len(raw_dsp_report) - len(cleaned_df)
        }
    )

@asset
def mongo_dsp_report(cleaned_dsp_report: pd.DataFrame, mongo_resource) -> Output[Dict]:
    """Stores the cleaned DSP report in MongoDB."""
    collection = mongo_resource.get_collection('dsp_reports')
    
    # Convert DataFrame to list of dictionaries
    records = cleaned_dsp_report.to_dict('records')
    
    # Insert records into MongoDB
    result = collection.insert_many(records)
    
    return Output(
        {"inserted_ids": len(result.inserted_ids)},
        metadata={"num_records": len(records)}
    ) 