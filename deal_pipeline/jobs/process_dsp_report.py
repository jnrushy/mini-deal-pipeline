from dagster import job, with_resources
from deal_pipeline.assets.dsp_report import raw_dsp_report, cleaned_dsp_report, mongo_dsp_report
from deal_pipeline.resources.mongo_resource import mongo_resource

@job(resource_defs={"mongo_resource": mongo_resource})
def process_dsp_report():
    """Job that processes DSP reports and stores them in MongoDB."""
    mongo_dsp_report(cleaned_dsp_report(raw_dsp_report())) 