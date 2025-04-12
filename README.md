# Mini Deal Pipeline Simulator

A data processing pipeline that simulates the processing of DSP (Demand-Side Platform) reports for advertising campaigns. This project demonstrates a complete ETL (Extract, Transform, Load) workflow using Dagster for orchestration, MongoDB for data storage, and Rill for visualization.

## What It Does

1. **Extracts** data from DSP reports in CSV format
2. **Transforms** the data by:
   - Filtering out low-performing entries (CPM < 7.0)
   - Calculating additional metrics (revenue per impression)
   - Formatting dates properly
3. **Loads** the processed data into MongoDB for storage and analysis
4. **Visualizes** the data using Rill dashboards
5. **Verifies** data integrity through comprehensive testing

## Data Pipeline Flow

```
CSV Data → [Raw DSP Report] → [Cleaned DSP Report] → [MongoDB Storage] → [Rill Dashboards]
             |                      |                      |                   |
        Read & Parse      Apply filters & calculations    Store          Visualize
```

## Features

- **Automated Data Pipeline**: Fully automated ETL process
- **Data Cleaning**: Removes low-quality advertising inventory (low CPM)
- **Data Enrichment**: Calculates additional metrics on processed data
- **Persistent Storage**: Stores data in MongoDB for future analysis
- **Data Visualization**: Creates interactive dashboards with Rill
- **Robust Testing**: Includes comprehensive tests for each pipeline stage
- **Configurable**: Easily adjustable thresholds and business rules

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB installed and running
- Pandas, PyMongo, and other dependencies (see requirements.txt)
- For Rill: See [RILL_INSTALL_NOTES.md](RILL_INSTALL_NOTES.md)

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
pip install dagster dagster-webserver  # For running the Dagster UI
```

### Environment Setup

Create a `.env` file with the following:
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=deal_pipeline
```

### Running Tests

To verify the pipeline works correctly:

```bash
# Test MongoDB integration
python -m unittest test_deal_pipeline.py

# Test Rill integration (no Rill installation required)
python -m unittest test_rill_integration.py

# Run all tests
python -m unittest discover
```

The tests validate:
- Data loading from CSV
- Cleaning and filtering logic
- Calculation of metrics
- MongoDB integration
- Data structure and integrity
- Rill project structure and configuration

### Running the Pipeline

To run the complete pipeline using Dagster:

```bash
# Start the Dagster UI
dagster dev -m deal_pipeline
```

Then:
1. Open your browser to `http://localhost:3000`
2. Navigate to the Assets tab
3. Click "Materialize All" to run the pipeline

### Verifying Dagster and Rill Integration

This project includes tests specifically for validating the integration with both Dagster and Rill:

**Testing Dagster Integration:**
```bash
# Test running the Dagster pipeline
dagster job execute -j process_dsp_report -m deal_pipeline
```

**Testing Rill Integration:**
```bash
# Validate Rill configuration (without running Rill)
python -m unittest test_rill_integration.py

# To run Rill (if installed)
cd rill-dashboards
rill start
```

See [RILL_INSTALL_NOTES.md](RILL_INSTALL_NOTES.md) for details on Rill installation and usage.

## Rill Dashboard Features

The Rill integration provides:

1. **Campaign Performance Analysis Dashboard**:
   - Daily performance trends
   - CPM comparison by campaign
   - Performance metrics by CPM tier
   - Detailed campaign comparison table

2. **Interactive Filters**:
   - Filter by campaign ID
   - Filter by CPM tier (High, Medium, Low)
   - Filter by date range

3. **Key Metrics**:
   - Total impressions
   - Total revenue
   - Average CPM
   - Revenue per 1K impressions

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

### Creating New Rill Dashboards

Add new dashboards to the Rill project:

1. Create a new dashboard definition in `rill-dashboards/dashboards/`
2. Define metrics and visualizations
3. Restart the Rill server to see changes

## Project Structure

```
mini-deal-pipeline/
├── README.md                   # Project documentation
├── RILL_INSTALL_NOTES.md       # Rill installation instructions
├── requirements.txt            # Dependencies
├── .env                        # Environment variables
├── sample_dsp_report.csv       # Sample input data
├── test_deal_pipeline.py       # Pipeline tests
├── test_rill_integration.py    # Rill integration tests
├── setup_rill.sh               # Rill setup script
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
└── rill-dashboards/
    ├── rill.yaml               # Rill project config
    ├── sources/
    │   └── mongodb.yml         # MongoDB connection
    ├── models/
    │   └── dsp_report.sql      # Data model
    └── dashboards/
        └── campaign_performance.yml  # Dashboard definition
```

## Dependencies

- dagster, dagster-webserver - Workflow orchestration
- pymongo - MongoDB interface
- pandas - Data processing
- python-dotenv - Environment management
- pytest - Testing
- tabulate - Table formatting for Dagster
- pyyaml - YAML parsing for Rill configuration
- Rill - Data visualization (installed separately) 