import utils
import config

import pandas as pd


class Zakon:
    def __init__(self, cislo):
        self.cislo = cislo
        self.url = ("https://www.nrsr.sk/web/Default.aspx?sid=zakony/zakon"
                    "&ZakZborID=13&CisObdobia=7&CPT={}".format(self.cislo))
        self.soup = utils.get_soup(self.url)
        self.data = {}

    def get_metadata(self):
        self.data["date"] = self.soup.find("span", attrs={
            "id": "_sectionLayoutContainer_ctl01_ctl00__DatumDoruceniaLabel"
            }).text.strip()
        self.data["navrhovatel"] = self.soup.find("span", attrs={
            "id": "_sectionLayoutContainer_ctl01_ctl00__NavrhovatelLabel"
            }).text.strip()
        self.data["stav"] = self.soup.find("span", attrs={
            "id": "_sectionLayoutContainer_ctl01__ProcessStateLabel"
            }).text.strip()
        self.data["vysledok"] = self.soup.find("span", attrs={
            "id": "_sectionLayoutContainer_ctl01__CurrentResultLabel"
            }).text.strip()[1:-1]
        table = self.soup.find("div", attrs={
            "id": "_sectionLayoutContainer_ctl01_ctl05__PdnList__pdnListPanel"
            })
        if table is not None:
            self.data["zmeny"] = list(set(
                [utils.change_name_order(tr("td")[1].text.strip())
                 for tr in table.find("table")("tr")]))
        else:
            self.data["zmeny"] = []

    def get_connections(self):
        meta = pd.read_hdf(config.FILE_HLASY_METADATA)
        meta_zakon = meta[meta["tlac"] == self.cislo]["Nazov"]
        connections = {}
        for poslanec in self.data["zmeny"]:
            name = poslanec.split(" ")[1]
            inds = meta_zakon.index[[name in t for t in meta_zakon]]
            connections[poslanec] = list(inds)
        self.data["zmeny"] = connections
