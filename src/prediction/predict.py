import argparse
import pathlib
import pickle
import subprocess
import sys
from typing import Any, Protocol

import pandas as pd
import numpy as np

from utils.utils import yellow_text, red_text

SCRIPR_NAME = pathlib.Path(__file__).name
NSP13_CHEMBL_ID: str = "CHEMBL4523582"
STEP = 10_000


class FilePath(Protocol):
    def __fspath__(self) -> str:
        ...


class HasFeatureNames(Protocol):
    feature_names_in_: np.ndarray


class TargetNoFoundError(ValueError):
    ...


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "ligand_features", type=str, help="path to csv file with ligand features"
    )
    parser.add_argument(
        "target_features", type=str, help="path to csv file with target features"
    )
    parser.add_argument(
        "model", type=str, help="path to pickled model"
    )
    parser.add_argument(
        "--target-chembl-id",
        type=str,
        default=NSP13_CHEMBL_ID,
        help="ChEMBL id of the target",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="path to file, to which predicted values will be written",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="force writing to existing file. Will remove its contents.",
    )
    parser.add_argument(
        "--step",
        type=int,
        default=STEP,
        help="how many rows of data should be used at a time. Change this number if you run out of RAM.",
    )
    return parser.parse_args()


def get_target_feaetures_df(filepath: FilePath, target_id) -> pd.DataFrame:
    target_features = pd.read_csv(filepath, header=None, index_col=0)
    target_features = target_features[target_features.index == target_id]
    if target_features.empty:
        raise TargetNoFoundError(f"No such id in target features: {target_id}")
    return target_features


def get_ligand_features_df(filepath: FilePath, start: int, step: int) -> pd.DataFrame:
    return pd.read_csv(filepath, skiprows=start, nrows=step, header=None)


def load_model(filepath: FilePath) -> Any:
    with open(filepath, "rb") as file:
        return pickle.load(file)


def create_features_df(
    ligand_features: pd.DataFrame, target_features: pd.DataFrame, model: HasFeatureNames
) -> pd.DataFrame:
    features = pd.concat([ligand_features, target_features], axis=1).set_index(0)
    features.columns = model.feature_names_in_
    return features


def main() -> int:
    args = parse_args()

    ligand_features_path = pathlib.Path(args.ligand_features)
    target_features_path = pathlib.Path(args.target_features)
    model_path = pathlib.Path(args.model)
    if not ligand_features_path.exists():
        print(
            f"{red_text(SCRIPR_NAME)}: {red_text('error')}: {ligand_features_path} No such file or directory!"
        )
        return 1
    if not target_features_path.exists():
        print(
            f"{red_text(SCRIPR_NAME)}: {red_text('error')}: {target_features_path} No such file or directory!"
        )
        return 1
    if not model_path.exists():
        print(
            f"{red_text(SCRIPR_NAME)}: {red_text('error')}: {model_path} No such file or directory!"
        )
        return 1

    try:
        target_features = get_target_feaetures_df(
            target_features_path, args.target_chembl_id
        )
    except TargetNoFoundError as e:
        print(e)
        return 1

    model = load_model(model_path)

    length = int(subprocess.run(["wc", "-l", str(ligand_features_path.resolve())], capture_output=True).stdout.decode().split()[0])
    for i in range(0, length, args.step):
        ligand_features = get_ligand_features_df(ligand_features_path, i, step=args.step)
        features = create_features_df(ligand_features, target_features, model)


    return 0


if __name__ == "__main__":
    sys.exit(main())
