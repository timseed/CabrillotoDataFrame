import pandas as pd
from hamcabrillo.cabrecord import cabrecord

class LoadCab:

    def read_cab(self, filename):
        with open(filename, 'rt') as ifp:
            data = ifp.read().split('\n')

        return data

    def only_qso(self, data):
        qso_data = [a for a in data if a.startswith('QSO')]
        return qso_data

    def convert(self, filename: str) -> list:
        records_as_str = self.only_qso(self.read_cab(filename))
        return records_as_str

    def make_records(self, records_as_str) -> list:
        """
        This will return a list of CabRecord

        Cabrillo Format 3

                                   --------info sent------- -------info rcvd--------
        QSO: freq  mo date       time call          rst exch   call          rst exch   t
        QSO: ***** ** yyyy-mm-dd nnnn ************* nnn ****** ************* nnn ****** n
        QSO:  3799 PH 1999-03-06 0711 HC8N          59  001    W1AW          59  001    0
        000000000111111111122222222223333333333444444444455555555556666666666777777777788
        123456789012345678901234567890123456789012345678901234567890123456789012345678901
        """
        # Locations of each field. The field will be left as str. If you need
        # to make say a numeric or a DateTime, please do this in the dataframe afterwards.


        fields = [(5, 10),
                  (11, 13),
                  (14, 29),
                  (30, 43),
                  (44, 46),
                  (48, 54),
                  (55, 68),
                  (69, 72),
                  (73, 79),
                  (80, 81)]
        recs = []

        for n in records_as_str:
            parts = [n[f[0]:f[1]].strip() for f in fields]
            # self.data.append(parts)
            recs.append(cabrecord(*parts))
        return recs

    def convert_to_df(self, filename: str) -> pd.DataFrame:
        return pd.DataFrame(self.make_records(self.only_qso(self.read_cab(filename))))
