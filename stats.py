import pandas as pd
import os

import config


def compute_hlasy_pie_tlace():
    """Prepare data for the hlasy pie charts."""
    if not os.path.isfile(config.FILE_HLASY):
        print("File {} does not exist locally!".format(config.FILE_HLASY))
    if not os.path.isfile(config.FILE_HLASY_METADATA):
        print("File {} does not exist locally!".format(
            config.FILE_HLASY_METADATA))
    hlasy = pd.read_hdf(config.FILE_HLASY)
    meta = pd.read_hdf(config.FILE_HLASY_METADATA)

    meta = meta[meta["tlac"].notnull()]
    id_vysledky = {s: meta.index[meta["Vysledok"] == "Návrh " + s]
                   for s in config.HLASY_STATS_VYSLEDOK}
    stats = {
        vysledok: hlasy.loc[id_vysledky[vysledok]].apply(
            lambda x: x.value_counts()).fillna(0)
        for vysledok in id_vysledky
        }
    for vysledok in stats:
        stats[vysledok].to_hdf(config.FILE_STATS_HLASY_PIE, vysledok,
                               format="table")
