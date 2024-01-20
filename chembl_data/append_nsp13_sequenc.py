import pathlib
import re
import sys

import pandas as pd

SCRIPT_NAME = pathlib.Path(__file__).name


def get_nsp13_chembl_assay_ids(
    assays_metadata_path: pathlib.Path, pattern: str
) -> list[str]:
    assays = pd.read_csv(assays_metadata_path, index_col=0)
    nsp13_assays = assays[assays.assay_description.str.contains(pattern, case=False)]
    return nsp13_assays.index.tolist() # type: ignore

def main() -> int:
    assays_metadata_path = pathlib.Path("./activities_targets/assays_targets.csv")
    print("Getting ids of assays with nsp13")
    ids = get_nsp13_chembl_assay_ids(assays_metadata_path, "nsp13|sars-.*-2")

    with open("./nsp13.fasta", "r") as file:
        nsp13_sequence_lines = file.readlines()[1:]
       
    with open("./activities_targets/sequence_subset_assay_id.fa", "a") as output:
        for assay_id in ids:
            lines = [f">{assay_id}\n"] + nsp13_sequence_lines
            output.writelines(lines)

    return 0


if __name__ == "__main__":
    sys.exit(main())
