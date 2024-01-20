import pathlib
import sys

import pandas as pd


def get_nsp13_chembl_assay_ids(
    assays_metadata_path: pathlib.Path, pattern: str
) -> list[str]:
    """Returns a list of ids of assays whose description matches pattern.

    args:
        - assays_metadata_path: path to csv file with assay metadata, including
          the `assay_description` column.
        - pattern against which assay description will be matched.

    returns:
        list of assay ids as strings.
    """
    assays = pd.read_csv(assays_metadata_path, index_col=0)
    nsp13_assays = assays[assays.assay_description.str.contains(pattern, case=False)]
    return nsp13_assays.index.tolist()  # type: ignore


def main() -> int:
    assays_metadata_path = pathlib.Path("./activities_targets/assays_targets.csv")
    nsp13_sequence_path = pathlib.Path("./nsp13.fasta")
    sequence_subset_path = pathlib.Path(
        "./activities_targets/sequence_subset_assay_id.fa"
    )

    ids = get_nsp13_chembl_assay_ids(assays_metadata_path, "nsp13|sars-.*-2")

    with open(nsp13_sequence_path, "r") as file:
        nsp13_sequence_lines = file.readlines()[1:]

    with open(sequence_subset_path, "r") as output:
        ids_in_file = set(
            line.strip(">\n") for line in output.readlines() if line.startswith(">")
        )
        if ids_in_file.intersection(set(ids)):
            print(
                "[\033[33mwarning\033[0m] Some of assay ids that would be "  # ]]
                "appended to sequence subset file are already there."
            )
            choice = input("Do you wish to append nsp13 with those ids anyway: [Y/n]: ")
            if choice.lower() not in ["y", "yes"]:
                return 1

    with open(sequence_subset_path, "a") as output:
        for assay_id in ids:
            lines = [f">{assay_id}\n"] + nsp13_sequence_lines
            output.writelines(lines)
    return 0


if __name__ == "__main__":
    sys.exit(main())
