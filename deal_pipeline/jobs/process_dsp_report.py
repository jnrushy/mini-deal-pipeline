from dagster import job, with_resources, op
from deal_pipeline.assets.dsp_report import raw_dsp_report, cleaned_dsp_report, mongo_dsp_report
from deal_pipeline.resources.mongo_resource import mongo_resource

# Create a job with the MongoDB resource
@job(resource_defs={"mongo_resource": mongo_resource})
def process_dsp_report():
    """Job that processes DSP reports and stores them in MongoDB."""
    # Execute each asset in sequence
    raw_data = raw_dsp_report()
    cleaned_data = cleaned_dsp_report(raw_data)
    mongo_dsp_report(cleaned_data) 