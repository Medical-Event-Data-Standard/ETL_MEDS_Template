"""Validates that the packaged MESSY config parses under MEDS-Extract's schema.

This runs fully offline (no download, no env vars needed): ``MessyConfig.parse`` strips the
``sources:`` block before resolving interpolations, so it checks the event-conversion side of the
combined MESSY file. Update the expected table prefixes when you customize ``event_configs.yaml``
for your dataset.
"""

from MEDS_extract.config import MessyConfig

from ETL_MEDS import event_config


def test_messy_config_parses():
    cfg = MessyConfig.parse(event_config)
    assert cfg.table_prefixes == ["patients", "labs_vitals", "medications", "diagnoses"]
