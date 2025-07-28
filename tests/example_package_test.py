import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


def test_example_package_pipeline():
    """Run the example package pipeline and check outputs."""
    with TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        env = os.environ.copy()
        env.update(
            {
                "DATASET_NAME": "EXAMPLE",
                "DATASET_VERSION": "1.0",
                "N_WORKERS": "1",
                "PRE_MEDS_DIR": str(Path("examples/example_package/raw_data").resolve()),
                "MEDS_COHORT_DIR": str(output_dir.resolve()),
            }
        )
        env["PYTHONPATH"] = f"examples/example_package/src:{env.get('PYTHONPATH', '')}"

        event_cfg = Path("examples/example_package/src/EXAMPLE_MEDS/configs/event_configs.yaml").resolve()
        command_parts = [
            "MEDS_transform-pipeline",
            "pkg://EXAMPLE_MEDS.configs.ETL.yaml",
            "--overrides",
            f"event_conversion_config_fp={event_cfg}",
            "parallelize.launcher=basic",
        ]
        result = subprocess.run(command_parts, capture_output=True, env=env)

        if result.returncode != 0:
            raise RuntimeError(
                f"Command failed with code {result.returncode}\n"
                f"stdout:\n{result.stdout.decode()}\n"
                f"stderr:\n{result.stderr.decode()}"
            )

        # Check for expected output files
        metadata_dir = output_dir / "metadata"
        assert (metadata_dir / "dataset.json").exists()
        assert (metadata_dir / "subject_splits.parquet").exists()
        assert (metadata_dir / "codes.parquet").exists()
