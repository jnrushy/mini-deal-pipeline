from dagster import repository
from deal_pipeline.jobs.process_dsp_report import process_dsp_report
from deal_pipeline.assets.dsp_report import raw_dsp_report, cleaned_dsp_report, mongo_dsp_report

@repository
def deal_pipeline():
    return [
        process_dsp_report,
        raw_dsp_report,
        cleaned_dsp_report,
        mongo_dsp_report,
    ] 