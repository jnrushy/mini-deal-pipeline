from dagster import repository, with_resources, define_asset_job, AssetGroup
from deal_pipeline.jobs.process_dsp_report import process_dsp_report
from deal_pipeline.assets.dsp_report import raw_dsp_report, cleaned_dsp_report, mongo_dsp_report
from deal_pipeline.resources.mongo_resource import mongo_resource

# Create an asset group with resources
asset_group = AssetGroup(
    [raw_dsp_report, cleaned_dsp_report, mongo_dsp_report],
    resource_defs={"mongo_resource": mongo_resource}
)

# Create a job from the asset group
dsp_asset_job = define_asset_job(
    name="dsp_asset_job", 
    selection=asset_group.get_asset_keys()
)

@repository
def deal_pipeline():
    return [
        process_dsp_report,
        asset_group,
        dsp_asset_job,
    ] 