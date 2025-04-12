# Mini Deal Pipeline Simulator

A data processing pipeline that simulates the processing of DSP (Demand-Side Platform) reports for advertising campaigns. This project demonstrates a complete ETL (Extract, Transform, Load) workflow using Dagster for orchestration and MongoDB for data storage.

## What It Does

1. **Extracts** data from DSP reports in CSV format
2. **Transforms** the data by:
   - Filtering out low-performing entries (CPM < 7.0)
   - Calculating additional metrics (revenue per impression)
   - Formatting dates properly
3. **Loads** the processed data into MongoDB for storage and analysis
4. **Verifies** data integrity through comprehensive testing

## Data Pipeline Flow

```
CSV Data → [Raw DSP Report] → [Cleaned DSP Report] → [MongoDB Storage]
             |                      |                      |
        Read & Parse      Apply filters & calculations    Store
```

## Features

- **Automated Data Pipeline**: Fully automated ETL process
- **Data Cleaning**: Removes low-quality advertising inventory (low CPM)
- **Data Enrichment**: Calculates additional metrics on processed data
- **Persistent Storage**: Stores data in MongoDB for future analysis
- **Robust Testing**: Includes comprehensive tests for each pipeline stage
- **Configurable**: Easily adjustable thresholds and business rules

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB installed and running
- Pandas, PyMongo, and other dependencies

### Installation

```bash
# Clone the repository
git clone https://github.com/jnrushy/mini-deal-pipeline.git
cd mini-deal-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with:
# MONGO_URI=mongodb://localhost:27017
# MONGO_DB=deal_pipeline
```

### Running Tests

To verify the pipeline works correctly:

```bash
python -m unittest test_deal_pipeline.py
```

The tests validate:
- Data loading from CSV
- Cleaning and filtering logic
- Calculation of metrics
- MongoDB integration
- Data structure and integrity

### Running the Pipeline

To run the complete pipeline:

```bash
dagster dev
```

Then:
1. Open your browser to `http://localhost:3000`
2. Navigate to the Assets tab
3. Click "Materialize All" to run the pipeline

## Extending the Project

### Adding New Data Sources

Modify the `raw_dsp_report` asset to read from different sources:

```python
@asset
def raw_dsp_report() -> Output[pd.DataFrame]:
    # Read from API, database, or different file formats
    df = pd.read_csv('new_data_source.csv')
    # ...
```

### Customizing Cleaning Rules

Adjust the filtering logic in the `cleaned_dsp_report` asset:

```python
@asset
def cleaned_dsp_report(raw_dsp_report: pd.DataFrame) -> Output[pd.DataFrame]:
    # Change CPM threshold or add new filters
    cleaned_df = raw_dsp_report[raw_dsp_report['cpm'] >= 9.0].copy()
    # ...
```

### Adding Visualization with Rill

Future extension plans include adding Rill dashboards for data visualization:

1. Connect Rill to the MongoDB database
2. Create visualizations for:
   - Campaign performance by day
   - CPM distribution
   - Revenue analysis

## Project Structure

```
mini-deal-pipeline/
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies
├── .env                        # Environment variables
├── sample_dsp_report.csv       # Sample input data
├── test_deal_pipeline.py       # Pipeline tests
├── deal_pipeline/
│   ├── __init__.py             # Dagster repository
│   ├── assets/
│   │   ├── __init__.py
│   │   └── dsp_report.py       # Asset definitions
│   ├── jobs/
│   │   ├── __init__.py
│   │   └── process_dsp_report.py  # Pipeline job
│   └── resources/
│       ├── __init__.py
│       └── mongo_resource.py   # MongoDB connector
```

## Usage

1. **Start the Pipeline**
   - Run `dagster dev` to start the Dagster UI
   - Navigate to the Assets page
   - Click "Materialize All" to run the pipeline

2. **Monitor Progress**
   - View job execution in real-time
   - Check asset materialization
   - Monitor MongoDB collection updates

3. **View Results**
   - Access processed data in MongoDB
   - View metadata about the processing steps
   - Analyze cleaned data in your preferred MongoDB client

## Dependencies

- dagster==1.6.7
- dagster-mongo==0.20.7
- pymongo==4.6.1
- pandas==2.2.1
- python-dotenv==1.0.1
- pytest==8.0.2 