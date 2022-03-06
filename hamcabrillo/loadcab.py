import pandas as pd
from hamcabrillo.cabrecord import cabrecord

""" Example cbr file
START-OF-LOG: 3.0
CALLSIGN: A45WG
CONTEST: CQ-WW-CW
CATEGORY-OPERATOR: SINGLE-OP
CATEGORY-ASSISTED: ASSISTED
CATEGORY-BAND: ALL
CATEGORY-POWER: HIGH
CATEGORY-MODE: CW
CATEGORY-TRANSMITTER: ONE
CERTIFICATE: YES
CLAIMED-SCORE: 305181
CLUB:
LOCATION: DX
CREATED-BY: RUMlogNG (2.14) by DL2RUM
NAME: Tim Seed
ADDRESS: PO Box 2260
ADDRESS: Ruwi
ADDRESS: PC 112
ADDRESS: Oman
OPERATORS: A45WG
SOAPBOX: Very enjoyable with some good and surprising openings.
QSO:  7007 CW 2016-11-26 0212 A45WG         599 21     LZ3ZZ         599 20     0
QSO:  7012 CW 2016-11-26 0215 A45WG         599 21     IR2L          599 15     0
QSO:  7013 CW 2016-11-26 0216 A45WG         599 21     SM5F          599 14     0
QSO:  7016 CW 2016-11-26 0217 A45WG         599 21     UN9L          599 17     0
"""


class LoadCab:

    def __init__(self):
        self.header = {'CALLSIGN': "",
                       'CONTEST': "",
                       'CATEGORY-OPERATOR': "",
                       'CATEGORY-ASSISTED': "",
                       'CATEGORY-BAND': "",
                       'CATEGORY-POWER': "",
                       'CATEGORY-MODE': "",
                       'CATEGORY-TRANSMITTER': "",
                       'CERTIFICATE:': "",
                       'CLAIMED-SCORE': ""}

    def read_cab(self, filename):
        with open(filename, 'rt') as ifp:
            data = ifp.read().split('\n')
        self.header_data(data)
        return data

    def header_data(self, data):

        for f in self.header.keys():
            for d in data:
                if d.find(f) != -1:
                    self.header[f] = d.split(':')[1].strip()
                    break

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

    def get_header(self) -> dict:
        return self.header
