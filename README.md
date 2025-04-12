# Mini Deal Pipeline Simulator

This project simulates a deal pipeline that processes DSP (Demand-Side Platform) reports and stores the results in MongoDB. It's built using Dagster for orchestration and provides a framework for processing and analyzing advertising data.

## Features

- **Data Ingestion**: Reads DSP reports in CSV format (currently using sample data, but can be extended to read from files)
- **Data Cleaning**: Filters out low-performing entries based on CPM (Cost Per Mille) thresholds
- **Data Storage**: Stores processed data in MongoDB for persistence and analysis
- **Orchestration**: Uses Dagster for workflow management and monitoring
- **Environment Configuration**: Supports different environments through environment variables

## Components

### 1. Data Pipeline
The pipeline consists of three main stages:

1. **Raw Data Ingestion** (`raw_dsp_report`)
   - Currently creates a sample DataFrame with campaign data
   - Can be modified to read from actual CSV files
   - Sample data includes: campaign_id, impressions, revenue, and CPM

2. **Data Cleaning** (`cleaned_dsp_report`)
   - Filters out entries with CPM less than 7.0
   - Provides metadata about the cleaning process
   - Maintains data integrity while removing low-performing entries

3. **Data Storage** (`mongo_dsp_report`)
   - Stores cleaned data in MongoDB
   - Uses a dedicated collection for DSP reports
   - Provides insertion statistics and metadata

### 2. Resources
- **MongoDB Resource**: Manages database connections and provides collection access
- **Environment Configuration**: Uses `.env` file for database connection settings

## Setup

1. **Prerequisites**
   - Python 3.8+
   - MongoDB installed and running locally
   - Virtual environment support

2. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configuration**
   Create a `.env` file with:
   ```
   MONGO_URI=mongodb://localhost:27017
   MONGO_DB=deal_pipeline
   ```

4. **Running the Pipeline**
   ```bash
   dagster dev
   ```
   Access the Dagster UI at `http://localhost:3000`

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .env
├── deal_pipeline/
│   ├── __init__.py              # Dagster repository definition
│   ├── assets/
│   │   ├── __init__.py
│   │   └── dsp_report.py        # Data processing assets
│   ├── jobs/
│   │   ├── __init__.py
│   │   └── process_dsp_report.py # Pipeline job definition
│   └── resources/
│       ├── __init__.py
│       └── mongo_resource.py     # MongoDB connection management
└── tests/
    ├── __init__.py
    └── test_dsp_report.py
```

## Usage

1. **Start the Pipeline**
   - Run `dagster dev` to start the Dagster UI
   - Navigate to the Jobs page
   - Select and run the `process_dsp_report` job

2. **Monitor Progress**
   - View job execution in real-time
   - Check asset materialization
   - Monitor MongoDB collection updates

3. **View Results**
   - Access processed data in MongoDB
   - View metadata about the processing steps
   - Analyze cleaned data in your preferred MongoDB client

## Extending the Project

1. **Adding Real Data Sources**
   - Modify `raw_dsp_report` to read from actual CSV files
   - Add support for different file formats
   - Implement data validation

2. **Customizing Data Cleaning**
   - Adjust CPM threshold
   - Add additional cleaning rules
   - Implement data transformation steps

3. **Enhancing Storage**
   - Add support for different databases
   - Implement data versioning
   - Add data export capabilities

## Dependencies

- dagster==1.6.7
- dagster-mongo==0.20.7
- pymongo==4.6.1
- pandas==2.2.1
- python-dotenv==1.0.1
- pytest==8.0.2 