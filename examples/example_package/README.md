# Example Usage

This directory demonstrates a minimal dataset packaged using the template. The
raw CSV files come from the MEDS-Extract repository and the configuration files
are copied from this template with small modifications.

Run the pipeline with the following command:

```bash
DATASET_NAME=EXAMPLE DATASET_VERSION=1.0 \
PRE_MEDS_DIR=examples/example_package/raw_data \
MEDS_COHORT_DIR=examples/example_package/MEDS_output \
MEDS_transform-pipeline pkg://EXAMPLE_MEDS.configs.ETL.yaml \
    --overrides \
    event_conversion_config_fp=pkg://EXAMPLE_MEDS.configs.event_configs.yaml \
    parallelize.launcher=basic
```

After running, the extracted MEDS dataset will be located in
`examples/example_package/MEDS_output`.
