"""Performs pre-MEDS data wrangling for INSERT DATASET NAME HERE."""

from datetime import datetime
from pathlib import Path

import polars as pl
from loguru import logger
from MEDS_transforms.utils import get_shard_prefix, write_lazyframe
from omegaconf import DictConfig

from . import premeds_cfg
from .pre_meds_utils import (
    DATASET_NAME,
    SUBJECT_ID,
    get_patient_link,
    join_and_get_pseudotime_fntr,
    load_raw_file,
)

# List of file extensions to be processed
DATA_FILE_EXTENSIONS = premeds_cfg.raw_data_extensions
# List of tables to be ignored during processing
IGNORE_TABLES = []


def main(cfg: DictConfig) -> None:
    """Performs pre-MEDS data wrangling for INSERT DATASET NAME HERE."""

    logger.info(f"Loading table preprocessors from {premeds_cfg}...")
    preprocessors = premeds_cfg
    functions = {}

    input_dir = Path(cfg.raw_input_dir)
    MEDS_input_dir = Path(cfg.root_output_dir) / "pre_MEDS"
    MEDS_input_dir.mkdir(parents=True, exist_ok=True)

    done_fp = MEDS_input_dir / ".done"
    if done_fp.is_file() and not cfg.do_overwrite:
        logger.info(
            f"Pre-MEDS transformation already complete as {done_fp} exists and "
            f"do_overwrite={cfg.do_overwrite}. Returning."
        )
        exit(0)

    all_fps = []
    for ext in DATA_FILE_EXTENSIONS:
        all_fps.extend(input_dir.rglob(f"*/{ext}"))
        all_fps.extend(input_dir.rglob(f"{ext}"))

    for table_name, preprocessor_cfg in preprocessors.items():
        if table_name not in ["subject_id", "admission_id", "raw_data_extensions"]:
            logger.info(f"  Adding preprocessor for {table_name}:\n{preprocessor_cfg}")
            functions[table_name] = join_and_get_pseudotime_fntr(table_name=table_name, **preprocessor_cfg)

    unused_tables = {}
    patient_out_fp = MEDS_input_dir / ""
    references_out_fp = MEDS_input_dir / ""
    link_out_fp = MEDS_input_dir / ""

    if patient_out_fp.is_file() and link_out_fp.is_file():
        logger.info(f"Reloading processed patient df from {str(patient_out_fp.resolve())}")
        patient_df = pl.read_parquet(patient_out_fp, use_pyarrow=True)
        link_df = pl.read_parquet(link_out_fp, use_pyarrow=True)
    else:
        logger.info("Processing patient table...")

        admissions_fp = input_dir / "admissions.csv"  # Adjust to the actual path pattern
        logger.info(f"Loading {str(admissions_fp.resolve())}...")
        raw_admissions_df = load_raw_file(admissions_fp)

        patient_df, link_df = get_patient_link(raw_admissions_df)
        write_lazyframe(patient_df, patient_out_fp)
        write_lazyframe(link_df, link_out_fp)

    if references_out_fp.is_file():
        logger.info(f"Reloading processed references df from {str(references_out_fp.resolve())}")
        references_df = pl.read_parquet(references_out_fp, use_pyarrow=True).lazy()
    else:
        logger.info("Processing references table first...")
        references_fp = input_dir / "references.csv"  # Adjust to the actual path pattern
        logger.info(f"Loading {str(references_fp.resolve())}...")
        references_df = load_raw_file(references_fp)
        write_lazyframe(references_df, references_out_fp)

    patient_df = patient_df.join(link_df, on=SUBJECT_ID)

    for in_fp in all_fps:
        pfx = get_shard_prefix(input_dir, in_fp)
        if pfx in unused_tables:
            logger.warning(f"Skipping {pfx} as it is not supported in this pipeline.")
            continue
        elif pfx not in functions:
            logger.warning(f"No function needed for {pfx}. For {DATASET_NAME}, THIS IS UNEXPECTED")
            continue

        out_fp = MEDS_input_dir / f"{pfx}.parquet"

        if out_fp.is_file():  # and not pfx == "data_float_h" :
            logger.info(f"Done with {pfx}. Continuing")
            continue

        out_fp.parent.mkdir(parents=True, exist_ok=True)

        st = datetime.now()
        logger.info(f"Processing {pfx}...")
        df = load_raw_file(in_fp)

        fn = functions[pfx]
        processed_df = fn(df, patient_df, references_df)

        # Sink throws errors, so we use collect instead
        logger.info(
            f"patient_df schema: {patient_df.collect_schema()}, "
            f"processed_df schema: {processed_df.collect_schema()}"
        )
        processed_df.sink_parquet(out_fp)
        logger.info(f"Processed and wrote to {str(out_fp.resolve())} in {datetime.now() - st}")

    logger.info(f"Done! All dataframes processed and written to {str(MEDS_input_dir.resolve())}")
    return
