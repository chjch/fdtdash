import os
import numpy as np
import pandas as pd
import requests
import logging


from dotenv import load_dotenv

load_dotenv()

STATE = 12  # Florida
COUNTY = "031"  # Duval County
START_YEAR = 2013
END_YEAR = 2022
CSV_PATH = "../data/CSV/duval_2020_census_tract_blkgrp.csv"

str_cols = ["TRACT", "BLKGRP", "GEOID20"]
blkgrp_df = pd.read_csv(
    CSV_PATH,
    dtype={col: str for col in str_cols},
)
means_to_work = dict(
    total="B08301_001E",  # total working population
    car="B08301_002E",
    bus="B08301_010E",
    bike="B08301_018E",
    walk="B08301_019E",
    wfh="B08301_021E",
    others="B08301_020E",
)
n_blkgrp = len(blkgrp_df)
n_years = END_YEAR - START_YEAR + 1
n_means = len(means_to_work.keys())

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="error_blkgrp.log",
    encoding="utf-8",
    format="%(levelname)s:%(message)s",
    level=logging.DEBUG,
)


def create_base_df():
    return pd.DataFrame(
        {
            "GEOID20": blkgrp_df["GEOID20"]
            .repeat(n_years * n_means)
            .reset_index(drop=True),
            "TRACT": blkgrp_df["TRACT"]
            .repeat(n_years * n_means)
            .reset_index(drop=True),
            "BLKGRP": blkgrp_df["BLKGRP"]
            .repeat(n_years * n_means)
            .reset_index(drop=True),
            "year": pd.concat(
                [
                    pd.Series(np.arange(START_YEAR, END_YEAR + 1)).repeat(
                        n_means
                    )
                    for _ in range(n_blkgrp)
                ],
                ignore_index=True,
            ),
            "means_to_work": pd.concat(
                [
                    pd.Series(means_to_work.keys())
                    for _ in range(n_blkgrp * n_years)
                ],
                ignore_index=True,
            ),
        },
        index=range(n_blkgrp * n_years * n_means),
    )


def get_acs_5yr_estimates(year, variable, tract, blkgrp):
    r = requests.get(
        f"https://api.census.gov/data/{year}"
        f"/acs/acs5?get={variable}&for=block%20group:{blkgrp}"
        f"&in=state:{STATE}&in=county:{COUNTY}&in=tract:{tract}"
        f"&key={os.getenv('CENSUS_API_KEY')}"
    )
    return int(r.json()[1][0])


base_df = create_base_df()
n = 70
for g, sub_df in base_df.groupby(np.arange(len(base_df)) // n):
    GEOID20 = sub_df.value_counts("GEOID20").index.values[0]
    if os.path.exists(f"../data/CSV/means_to_work/{GEOID20}.csv"):
        print(f"Skipping GEOID: {GEOID20} at row {n * (g + 1)}.")
        continue
    try:
        sub_df["value"] = sub_df.apply(
            lambda x: get_acs_5yr_estimates(
                x["year"],
                means_to_work[x["means_to_work"]],
                x["TRACT"],
                x["BLKGRP"],
            ),
            axis=1,
        )
        print(f"Finished GEOID: {GEOID20}.")
        print(f"Totally, completed {n * (g + 1)} rows!")
        sub_df.to_csv(
            f"../data/CSV/means_to_work/{GEOID20}.csv",
            index=False,
        )
        base_df.loc[sub_df.index, "value"] = sub_df["value"]
    except Exception as e:
        logger.debug(f"{GEOID20} failed with error: {e}!")

base_df.to_csv(
    f"../data/CSV/means_to_work_{START_YEAR}_{END_YEAR}.csv", index=False
)
