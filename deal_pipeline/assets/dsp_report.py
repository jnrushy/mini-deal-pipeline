import pandas as pd
from dagster import asset, Output, MetadataValue, AssetIn
from typing import List, Dict
import os
from datetime import datetime

@asset
def raw_dsp_report() -> Output[pd.DataFrame]:
    """Reads the raw DSP report from CSV file."""
    # Read the CSV file
    df = pd.read_csv('sample_dsp_report.csv')
    
    # Clean string columns to remove whitespace
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].str.strip()
    
    # Now convert date with explicit format
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    
    return Output(
        df,
        metadata={
            "num_rows": len(df),
            "date_range": f"{df['date'].min()} to {df['date'].max()}",
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )

@asset
def cleaned_dsp_report(raw_dsp_report: pd.DataFrame) -> Output[pd.DataFrame]:
    """Cleans the DSP report by removing low CPM entries and adding metrics."""
    # Filter out entries with CPM less than 7.0
    cleaned_df = raw_dsp_report[raw_dsp_report['cpm'] >= 7.0].copy()
    
    # Add some basic metrics
    cleaned_df['revenue_per_impression'] = cleaned_df['revenue'] / cleaned_df['impressions']
    
    return Output(
        cleaned_df,
        metadata={
            "num_rows": len(cleaned_df),
            "removed_rows": len(raw_dsp_report) - len(cleaned_df),
            "avg_cpm": cleaned_df['cpm'].mean(),
            "total_revenue": cleaned_df['revenue'].sum(),
            "preview": MetadataValue.md(cleaned_df.head().to_markdown())
        }
    )

@asset(required_resource_keys={"mongo_resource"})
def mongo_dsp_report(context, cleaned_dsp_report: pd.DataFrame) -> Output[Dict]:
    """Stores the cleaned DSP report in MongoDB."""
    mongo_resource = context.resources.mongo_resource
    collection = mongo_resource.get_collection('dsp_reports')
    
    # Convert DataFrame to list of dictionaries
    records = cleaned_dsp_report.to_dict('records')
    
    # Insert records into MongoDB
    result = collection.insert_many(records)
    
    return Output(
        {"inserted_ids": len(result.inserted_ids)},
        metadata={
            "num_records": len(records),
            "collection": "dsp_reports",
            "database": os.getenv('MONGO_DB')
        }
    ) 