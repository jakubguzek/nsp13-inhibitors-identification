# -*- coding: utf-8 -*-
import sys
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from score_metrics import rmse, spearman, mcc, multiclass_mcc


def get_features_df(activities_file, compound_ft_file, target_ft_file=None):
    activities = pd.read_csv(activities_file, sep=',')
    compounds = pd.read_csv(compound_ft_file, sep=',')
    activities = activities[["assay_chembl_id",
                             "molecule_chembl_id", "standard_value"]].dropna()
    features = activities.merge(compounds, on="molecule_chembl_id")

    if target_ft_file:
        targets = pd.read_csv(target_ft_file, sep=',', header=None)
        targets.columns = ["assay_chembl_id"] + \
            [f"prot_ft_{i}" for i in range(targets.shape[1]-1)]
        features = features[features["assay_chembl_id"].isin(
            targets["assay_chembl_id"])]
        features = features.merge(targets, on="assay_chembl_id")

    features.to_csv("features.csv", index=False)
    return features


def PCM_model(input):
    y = input["standard_value"]
    X_train, X_test, y_train, y_test = train_test_split(
        input, y, test_size=0.3, random_state=0)
    res = X_test.iloc[:, :3]

    X_train = X_train.iloc[:, 3:]
    X_test = X_test.iloc[:, 3:]

    if "prot_ft_0" in X_train.columns: # if we use protein features
        prot_cols = [col for col in X_train.columns if col.startswith("prot_ft")]
        scaler = MinMaxScaler()
        X_train[prot_cols] = scaler.fit_transform(X_train[prot_cols])
        X_test[prot_cols] = scaler.transform(X_test[prot_cols])

    reg = RandomForestRegressor(
        n_estimators=100, max_features=0.3, random_state=0)
    reg.fit(X_train, y_train)
    test_pred = reg.predict(X_test)
    res["predicted"] = test_pred

    med_cor_test_pred = test_pred + np.median(y_train) - np.median(test_pred)
    rmse_test = round(rmse(y_test, test_pred), 2)
    med_cor_rmse_test = round(rmse(y_test, med_cor_test_pred), 2)
    spearman_test = round(spearman(y_test, test_pred), 2)
    multiclass_mcc_test = round(multiclass_mcc(y_test, test_pred), 2) # do poprawienia w score_metrics.py albo do wyrzucenia
    mcc_test = round(mcc(y_test.values, test_pred, np.median(y_train)), 2)
    med_cor_mcc_test = round(
        mcc(y_test.values, med_cor_test_pred, np.median(y_train)), 2)

    return [res, rmse_test, med_cor_rmse_test, spearman_test, mcc_test, med_cor_mcc_test, multiclass_mcc_test]


if __name__ == "__main__":

    activities_file = "../chembl_data/activities.csv"
    compound_ft_file = "../chembl_data/ligand_representations/ligands_ecfp4.csv"
    target_ft_file = "subset_assay_id_embedding.csv"

    input = get_features_df(activities_file, compound_ft_file, target_ft_file)
    model_with_scores = PCM_model(input)
    model_with_scores[0].to_csv("model_out.tsv", sep="\t", index=False)

    scores = ["rmse", "med_cor_rmse", "spearman",
              "mcc", "med_cor_mcc", "multiclass_mcc"]
    print(*zip(scores, model_with_scores[1:]))
