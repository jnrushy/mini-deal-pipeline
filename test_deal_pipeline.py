import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import unittest
from datetime import datetime

class TestDealPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment and load data."""
        load_dotenv()
        cls.client = MongoClient(os.getenv('MONGO_URI'))
        cls.db = cls.client[os.getenv('MONGO_DB')]
        cls.collection = cls.db['dsp_reports']
        
        # Load and process the sample data
        cls.raw_df = pd.read_csv('sample_dsp_report.csv')
        # Clean any whitespace in string columns
        for col in cls.raw_df.select_dtypes(include=['object']):
            cls.raw_df[col] = cls.raw_df[col].str.strip()
        
        # Convert date with explicit format
        cls.raw_df['date'] = pd.to_datetime(cls.raw_df['date'], format='%Y-%m-%d')
        
        # Clean the data (same logic as in the asset)
        cls.cleaned_df = cls.raw_df[cls.raw_df['cpm'] >= 7.0].copy()
        cls.cleaned_df['revenue_per_impression'] = cls.cleaned_df['revenue'] / cls.cleaned_df['impressions']
        
        # Insert into MongoDB
        cls.records = cls.cleaned_df.to_dict('records')
        cls.collection.insert_many(cls.records)

    def test_data_loading(self):
        """Test that the raw data is loaded correctly."""
        self.assertEqual(len(self.raw_df), 7, "Should load all 7 records from CSV")
        self.assertTrue('date' in self.raw_df.columns, "Date column should be present")
        self.assertTrue(isinstance(self.raw_df['date'].iloc[0], pd.Timestamp), "Date should be datetime type")

    def test_data_cleaning(self):
        """Test that the cleaning rules are applied correctly."""
        # Check CPM threshold
        self.assertTrue((self.cleaned_df['cpm'] >= 7.0).all(), "All CPM values should be >= 7.0")
        
        # Check that low CPM records are removed
        low_cpm_count = len(self.raw_df[self.raw_df['cpm'] < 7.0])
        self.assertEqual(len(self.raw_df) - len(self.cleaned_df), low_cpm_count, 
                        "Should remove all records with CPM < 7.0")
        
        # Check revenue per impression calculation
        expected_rpi = (self.cleaned_df['revenue'] / self.cleaned_df['impressions']).rename('revenue_per_impression')
        pd.testing.assert_series_equal(
            self.cleaned_df['revenue_per_impression'],
            expected_rpi,
            check_names=True,
            obj="Revenue per impression calculation should be correct"
        )

    def test_mongo_insertion(self):
        """Test that data is correctly inserted into MongoDB."""
        # Check number of records in MongoDB
        mongo_count = self.collection.count_documents({})
        self.assertEqual(mongo_count, len(self.records), 
                        "Number of records in MongoDB should match cleaned data")
        
        # Check a sample record
        sample_record = self.collection.find_one({"campaign_id": "CAMP001"})
        self.assertIsNotNone(sample_record, "Should find CAMP001 in MongoDB")
        self.assertEqual(sample_record['cpm'], 10.0, "CPM should match original data")
        self.assertAlmostEqual(sample_record['revenue_per_impression'], 0.01, 
                             places=2, msg="Revenue per impression should be calculated correctly")

    def test_deal_package_structure(self):
        """Test that the deal package has the correct structure."""
        # Get all records from MongoDB
        deal_package = list(self.collection.find({}, {'_id': 0}))
        
        # Check required fields
        required_fields = ['campaign_id', 'impressions', 'revenue', 'cpm', 'date', 'revenue_per_impression']
        for record in deal_package:
            for field in required_fields:
                self.assertIn(field, record, f"Required field {field} should be present")
        
        # Check data types
        for record in deal_package:
            self.assertIsInstance(record['campaign_id'], str, "campaign_id should be string")
            self.assertIsInstance(record['impressions'], int, "impressions should be integer")
            self.assertIsInstance(record['revenue'], float, "revenue should be float")
            self.assertIsInstance(record['cpm'], float, "cpm should be float")
            self.assertTrue(isinstance(record['date'], datetime) or isinstance(record['date'], pd.Timestamp),
                          "date should be datetime or Timestamp")
            self.assertIsInstance(record['revenue_per_impression'], float, 
                                "revenue_per_impression should be float")

    @classmethod
    def tearDownClass(cls):
        """Clean up test data."""
        cls.collection.delete_many({})
        cls.client.close()

if __name__ == '__main__':
    unittest.main() 