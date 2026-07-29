"""Performs pre-MEDS data wrangling for the sample dataset.

Customize this file with any steps needed to prepare your raw data for MEDS extraction, such as:

1. De-compressing files or otherwise preparing the raw data for extraction at a technical level.
2. Joining tables together so that all relevant rows include the unifying ``subject_id`` (though
   simple joins can be expressed directly in ``event_configs.yaml`` via ``_table.join``).
3. Converting any offsets into timestamps.
4. Any other modifications of interest.

If your dataset needs no pre-MEDS wrangling at all, you can simply delete this file -- the pipeline
will then run extraction directly against the raw input directory. The sample implementation below
copies the raw files through unchanged so the end-to-end sample pipeline is runnable as-is.
"""

import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


def main(input_dir: Path, output_dir: Path, do_overwrite: bool | None = None):
    """Performs pre-MEDS data wrangling for the sample dataset.

    The sample dataset needs no wrangling, so this simply copies the raw files to the output
    directory. Replace this with your dataset's real pre-MEDS logic (or delete this file if your
    dataset needs none).

    Args:
        input_dir: Directory containing the staged raw data files.
        output_dir: Directory to which the pre-MEDS data should be written.
        do_overwrite: If True, re-process files whose outputs already exist.
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    for in_fp in sorted(input_dir.rglob("*")):
        if not in_fp.is_file():
            continue
        out_fp = output_dir / in_fp.relative_to(input_dir)
        if out_fp.exists() and not do_overwrite:
            logger.info(f"Skipping {out_fp} as it already exists.")
            continue
        out_fp.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(in_fp, out_fp)
        logger.info(f"Copied {in_fp} to {out_fp}.")
