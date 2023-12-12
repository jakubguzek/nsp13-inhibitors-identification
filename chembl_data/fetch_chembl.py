#!/usr/bin/env python
"""script for fetching data from ChEMBL."""
import argparse
import pathlib
import sys
from typing import Any, List, Optional

import requests
import pandas as pd

SCRIPT_NAME = pathlib.Path(__file__).name

BASE_URL = "https://www.ebi.ac.uk"
DATA_ENDPOINT = f"{BASE_URL}/chembl/api/data"


def yellow_text(text: str) -> str:
    return f"\033[33m{text}\033[0m"


def red_text(text: str) -> str:
    return f"\033[31m{text}\033[0m"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "A script for downloading bioactivity assay data from ChEMBL"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="path to a file, to which the output will be wriiten.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="don't ask for confirmation when overwriting existing files.",
    )
    return parser.parse_args()


def fetch_url(endpoint: str, format: str = "json", **params) -> str:
    url = f"{DATA_ENDPOINT}/{endpoint}?format={format}"
    for name, value in params.items():
        url += f"&{name}={value}"
    return url


def next_page(response_body: dict[str, Any]) -> Optional[str]:
    return response_body["page_meta"]["next"]


def get_viruses_ids(batch_size: int = 500) -> List[str | int]:
    url = fetch_url("organism", limit=f"{batch_size}", l1="Viruses")
    ids = []
    response = requests.get(url)
    if response.ok:
        response = response.json()
        next = next_page(response)
        ids = [organism["tax_id"] for organism in response["organisms"]]
        while next is not None:
            next_page_body = requests.get(f"{BASE_URL}{next}").json()
            ids.extend([organism["tax_id"] for organism in next_page_body["organisms"]])
            next = next_page(next_page_body)
    return ids


def get_asssays() -> pd.DataFrame:
    url = fetch_url(
        "assay",
        limit=500,
        assay_type="B",
        description__icontains="Helicase",
        assay_organism__regex=".?virus.?",
    )
    response = requests.get(url)
    frames = []
    if response.ok:
        response_body = response.json()
        df = pd.DataFrame(
            response_body["assays"], columns=response_body["assays"][0].keys()
        )
        frames.append(df)
        next = next_page(response_body)
        # This does not work for now but that's not that importnat
        while next is not None:
            next_page_body = requests.get(f"{BASE_URL}{next}").json()
            frames.append(pd.DataFrame(next_page_body["assays"]))
            next = next_page(next_page_body)
    return pd.concat(frames, ignore_index=True)


def get_activities(assays_ids: List[str]):
    url = fetch_url("activity", limit=500, assay_chembl_id__in=",".join(assays_ids))
    response = requests.get(url)
    frames = []
    if response.ok:
        response_body = response.json()
        df = pd.DataFrame(
            response_body["activities"], columns=response_body["activities"][0].keys()
        )
        frames.append(df)
        next = next_page(response_body)
        # This does not work for now but that's not that importnat
        while next is not None:
            next_page_body = requests.get(f"{BASE_URL}{next}").json()
            frames.append(pd.DataFrame(next_page_body["activities"]))
            next = next_page(next_page_body)
    return pd.concat(frames, ignore_index=True)


def main() -> int:
    args = parse_args()

    assays = get_asssays()
    activities = get_activities(assays["assay_chembl_id"])

    if args.output:
        output_file = pathlib.Path(args.output)

        if output_file.is_dir():
            print(f"{red_text(SCRIPT_NAME)}: error: {output_file} is a directory.")
            return 1
        if (not args.force) and output_file.exists():
            print(f"[{yellow_text('warning')}] File {output_file} exists.", end=" ")
            choice = input("Do you want to overwrite it? [Y/n]: ")

            if choice.lower() not in ["y", "yes"]:
                print(activities.to_csv())
                return 0

        with open(output_file, "w") as file:
            file.write(activities.to_csv())
        return 0

    print(activities.to_csv())
    return 0


if __name__ == "__main__":
    sys.exit(main())
