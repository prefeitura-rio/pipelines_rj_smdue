# -*- coding: utf-8 -*-
# flake8: noqa: E501
"""
Schedules for the database dump pipeline
"""

from datetime import datetime, timedelta

import pytz
from prefect.schedules import Schedule
from prefeitura_rio.pipelines_utils.io import untuple_clocks as untuple
from prefeitura_rio.pipelines_utils.prefect import generate_dump_url_schedules

from pipelines.constants import constants

#####################################
#
# Disciplinas sem professor
#
#####################################

gsheets_urls = {
    "auto_inflacao": {
        "dump_mode": "overwrite",
        "url": "https://drive.google.com/file/d/1ELzPpxnDF1dGCkhpz8cHGizeWn8Em0DS/view?usp=sharing",
        "url_type": "google_drive",
        "materialize_after_dump": False,
        "dataset_id": "geosislic",
    },
    "edital_irregularidade": {
        "dump_mode": "overwrite",
        "url": "https://drive.google.com/file/d/1o2_A87kUYYlFZMH9csaLllrvD6eQciAR/view?usp=sharing",
        "url_type": "google_drive",
        "materialize_after_dump": False,
        "dataset_id": "geosislic",
    },
    "embargo": {
        "dump_mode": "overwrite",
        "url": "https://drive.google.com/file/d/14Lh5FYQ--OFSutbhLI0526hYhGK_QL_Z/view?usp=sharing",
        "url_type": "google_drive",
        "materialize_after_dump": False,
        "dataset_id": "geosislic",
    },
    "intimacao": {
        "dump_mode": "overwrite",
        "url": "https://drive.google.com/file/d/1U83WZHPC3TjzHYwJet_SRViliz1Ad5dp/view?usp=sharing",
        "url_type": "google_drive",
        "materialize_after_dump": False,
        "dataset_id": "geosislic",
    },
    "licencas": {
        "dump_mode": "overwrite",
        "url": "https://drive.google.com/file/d/1vPSO1QMIaQGZiBWn48XilxItUMc7QaSh/view?usp=sharing",
        "url_type": "google_drive",
        "materialize_after_dump": False,
        "dataset_id": "geosislic",
    },
    "notificacao": {
        "dump_mode": "overwrite",
        "url": "https://drive.google.com/file/d/1jSksEo8wISadr9E8hKvQDX8CgokRh8RZ/view?usp=sharing",
        "url_type": "google_drive",
        "materialize_after_dump": False,
        "dataset_id": "geosislic",
    },
}

gsheets_clocks = generate_dump_url_schedules(
    interval=timedelta(days=4 * 365),
    start_date=datetime(2022, 11, 4, 20, 0, tzinfo=pytz.timezone("America/Sao_Paulo")),
    labels=[
        constants.RJ_SMDUE_AGENT_LABEL.value,
    ],
    dataset_id="geosislic",
    table_parameters=gsheets_urls,
)

gsheets_four_year_update_schedule = Schedule(clocks=untuple(gsheets_clocks))
