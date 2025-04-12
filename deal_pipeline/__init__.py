from dagster import repository, with_resources, define_asset_job
from deal_pipeline.jobs.process_dsp_report import process_dsp_report
from deal_pipeline.assets.dsp_report import raw_dsp_report, cleaned_dsp_report, mongo_dsp_report
from deal_pipeline.resources.mongo_resource import mongo_resource

# Define your assets with resources
assets_with_resources = with_resources(
    [raw_dsp_report, cleaned_dsp_report, mongo_dsp_report],
    {"mongo_resource": mongo_resource}
)

@repository
def deal_pipeline():
    return [
        process_dsp_report,  # Original job
        *assets_with_resources,  # Assets with resources
    ] 