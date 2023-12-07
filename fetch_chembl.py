"""script for fetching data from ChEMBL."""
import sys
import pprint
from typing import Any, List, Optional

import requests
import pandas as pd

BASE_URL = "https://www.ebi.ac.uk"
DATA_ENDPOINT = f"{BASE_URL}/chembl/api/data"


def fetch_url(endpoint: str, format: str = "json", **params) -> str:
    url = f"{DATA_ENDPOINT}/{endpoint}?format={format}"
    for name, value in params.items():
        url += f"&{name}={value}"
    return url


def next_page(response_body: dict[str, Any]) -> Optional[str]:
    return response_body["page_meta"]["next"]


def get_viruses_ids(batch_size: int = 500) -> List[str | int]:
    url = fetch_url("organism", limit=500, l1="Viruses")
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
            frames.append(
                pd.DataFrame(
                    next_page_body["assays"]
                )
            )
            next = next_page(next_page_body)
    return pd.concat(frames)


def main() -> int:
    print(get_asssays())
    return 0


if __name__ == "__main__":
    sys.exit(main())
