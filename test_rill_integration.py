import unittest
import os
import sys
import yaml
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

class TestRillIntegration(unittest.TestCase):
    """Test suite for verifying Rill integration with MongoDB."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        load_dotenv()
        cls.rill_dir = Path("rill-dashboards")
        
        # Connect to MongoDB
        cls.client = MongoClient(os.getenv('MONGO_URI'))
        cls.db = cls.client[os.getenv('MONGO_DB')]
        cls.collection = cls.db['dsp_reports']

    def test_rill_project_structure(self):
        """Test that the Rill project structure is valid."""
        # Check that all required directories exist
        self.assertTrue(self.rill_dir.exists(), "Rill project directory should exist")
        self.assertTrue((self.rill_dir / "sources").exists(), "Sources directory should exist")
        self.assertTrue((self.rill_dir / "models").exists(), "Models directory should exist")
        self.assertTrue((self.rill_dir / "dashboards").exists(), "Dashboards directory should exist")
        
        # Check that all required files exist
        self.assertTrue((self.rill_dir / "rill.yaml").exists(), "rill.yaml should exist")
        self.assertTrue((self.rill_dir / "sources" / "mongodb.yml").exists(), "MongoDB source config should exist")
        self.assertTrue((self.rill_dir / "models" / "dsp_report.sql").exists(), "DSP report model should exist")
        self.assertTrue((self.rill_dir / "dashboards" / "campaign_performance.yml").exists(), 
                       "Campaign performance dashboard should exist")

    def test_mongodb_source_config(self):
        """Test that the MongoDB source configuration is valid."""
        # Load the source config
        source_path = self.rill_dir / "sources" / "mongodb.yml"
        with open(source_path, 'r') as file:
            source_config = yaml.safe_load(file)
        
        # Verify the structure
        self.assertEqual(source_config['type'], "mongodb", "Source type should be mongodb")
        self.assertIn('connection', source_config, "Source config should have connection settings")
        self.assertIn('uri', source_config['connection'], "Connection should have URI")
        self.assertIn('database', source_config['connection'], "Connection should have database name")
        self.assertIn('collection', source_config['connection'], "Connection should have collection name")

    def test_dsp_report_model(self):
        """Test that the DSP report model has valid SQL."""
        # Load the model
        model_path = self.rill_dir / "models" / "dsp_report.sql"
        with open(model_path, 'r') as file:
            model_sql = file.read()
        
        # Basic validation of SQL content
        self.assertIn("SELECT", model_sql, "Model should contain SELECT statement")
        self.assertIn("campaign_id", model_sql, "Model should select campaign_id")
        self.assertIn("impressions", model_sql, "Model should select impressions")
        self.assertIn("revenue", model_sql, "Model should select revenue")
        self.assertIn("cpm", model_sql, "Model should select cpm")
        self.assertIn("EXTRACT", model_sql, "Model should extract date parts")

    def test_dashboard_definition(self):
        """Test that the dashboard definition is valid."""
        # Load the dashboard
        dashboard_path = self.rill_dir / "dashboards" / "campaign_performance.yml"
        with open(dashboard_path, 'r') as file:
            dashboard = yaml.safe_load(file)
        
        # Verify the structure
        self.assertIn('title', dashboard, "Dashboard should have a title")
        self.assertIn('model', dashboard, "Dashboard should reference a model")
        self.assertIn('metrics', dashboard, "Dashboard should define metrics")
        self.assertIn('visualizations', dashboard, "Dashboard should define visualizations")
        
        # Check metrics
        self.assertTrue(any(m['name'] == 'total_impressions' for m in dashboard['metrics']), 
                      "Dashboard should have total_impressions metric")
        self.assertTrue(any(m['name'] == 'total_revenue' for m in dashboard['metrics']), 
                      "Dashboard should have total_revenue metric")
        
        # Check visualizations
        self.assertTrue(any(v['name'] == 'daily_performance' for v in dashboard['visualizations']), 
                      "Dashboard should have daily_performance visualization")
        self.assertTrue(any(v['name'] == 'cpm_by_campaign' for v in dashboard['visualizations']), 
                      "Dashboard should have cpm_by_campaign visualization")

    @classmethod
    def tearDownClass(cls):
        """Clean up resources."""
        if hasattr(cls, 'client'):
            cls.client.close()

if __name__ == '__main__':
    unittest.main() 