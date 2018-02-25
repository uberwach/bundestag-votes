#!/usr/bin/python
# -*- coding: utf-8 -*-
""" preprocessing.py

"""

from glob import glob
import os
from os import path
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from constants import FACTION_LABELS


def csv_to_df(file_path):
    df = pd.read_csv(file_path)
    df = df[df["Wahlperiode"] == 19]

    if df.size == 0:
        print "Warning: Only the 19th Bundestag is selected here. This file is not from there."

    df = remove_columns(df)
    df = patch_votes(df)
    df = encode_faction(df)
    df["source"] = path.splitext(file_path)[0]
    return df


def remove_columns(df):
    """Removes useless columns"""
    COLUMNS_TO_DROP = ["Wahlperiode",
                       "Sitzungnr",
                       "Name",
                       "Vorname",
                       "Titel",
                       "Enthaltung",
                       "ungültig",
                       "nichtabgegeben",
                       "Bemerkung"]

    df.drop(COLUMNS_TO_DROP, axis=1, inplace=True)
    return df


def patch_votes(df):
    df["vote"] = df["ja"] - df["nein"]
    df.drop(["ja", "nein"], axis=1, inplace=True)
    return df


def encode_faction(df):
    le = LabelEncoder()
    le.fit(FACTION_LABELS)
    df["Fraktion"] = le.transform(df["Fraktion/Gruppe"])
    return df


if __name__ == "__main__":
    DATA_PATH = "data"
    CSV_DATA_PATH = path.join(DATA_PATH, "raw_csv")
    TARGET_FILE = path.join(DATA_PATH, "preprocessed", "voting.csv")

    if path.exists(TARGET_FILE):
        os.remove(TARGET_FILE)

    FILE_LIST = glob(CSV_DATA_PATH + "/*.csv")
    for i, FILE_PATH in enumerate(FILE_LIST):
        print("Processing %s (%d/%d)" % (FILE_PATH, i, len(FILE_LIST)))
        df = csv_to_df(FILE_PATH)
        df.to_csv(TARGET_FILE,
                  mode="a",
                  header=not path.exists(TARGET_FILE),
                  index=False)
