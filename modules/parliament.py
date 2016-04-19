# encoding: utf-8
""" This class contains helper classes for working with
    the Swedish parliament
"""
from collections import namedtuple, defaultdict


utskott = {
    "AU": "Arbetsmarknadsutskottet",
    "CU": "Civilutskottet",
    "FiU": "Finansutskottet",
    "FöU": "Försvarsutskottet",
    "JuU": "Justitieutskottet",
    "KU": "Konstitutionsutskottet",
    "KrU": "Kulturutskottet",
    "MjU": "Miljö- och jordbruksutskottet",
    "NU": "Näringsutskottet",
    "SkU": "Skatteutskottet",
    "SfU": "Socialförsäkringsutskottet",
    "SoU": "Socialutskottet",
    "TU": "Trafikutskottet",
    "UbU": "Utbildningsutskottet",
    "UU": "Utrikesutskottet",
    "UFöU": "Sammansatta utrikes- och försvarsutskottet",
    "BoU": "Bostadsutskottet",  # Former
    "LU": "Lagutskottet",  # Former
}


class Blocks(object):
    """Contains parliament coalition data
    """
    FIRST = "0"  # Has no predecessor
    LAST = "9"  # Has no successor

    blocks = {
        "alliansen": ["C", "FP", "L", "M", "KD"],
        "rodgrona": ["V", "S", "MP"],
        "sd": ["SD"]
    }
    gov = [{
        "name": "Löfven",
        "start": "2014-10-03",
        "end": LAST,
        "parties": ["S", "MP"]
        },
        {
        "name": "Reinfeldt",
        "start": "2006-10-06",
        "end": "2014-10-03",
        "parties": ["S", "MP"]
        }]

    def what_block(self, party):
        try:
            block = list(self.blocks)[
                [party in self.blocks[b] for b in self.blocks].index(True)
            ]
        except ValueError:
            # Unknown party
            block = None
        return block

    def what_gov(self, date):
        """What government was in power at a certain date?
           Use an ISO date, e.g. 2012-06-13.
        """
        for gov in self.gov:
            if gov["start"] <= date < gov["end"]:
                return gov
        raise ValueError("No government found for this date: %s" % date)


class Votes(namedtuple('Votes', 'Aye No Refrain')):
    """Named for storing voting patterns"""

    def relative(self):
        """Return relative values."""
        if isinstance(self.Aye, float):
            raise TypeError("Vote count is already a float.")
        total = float(self.Aye + self.No + self.Refrain)
#        return Votes((float(v)/total for v in self))
        return Votes(float(self.Aye)/total,
                     float(self.No)/total,
                     float(self.Refrain)/total)

    def sum(self, a):
        """Adds two Votes together"""
        return Votes(a.Aye + self.Aye,
                     a.No + self.No,
                     a.Refrain + self.Refrain)

    def minus(self, a):
        """Subtract a from Votes"""
        return Votes(self.Aye - a.Aye,
                     self.No - a.No,
                     self.Refrain - a.Refrain)

    def max_index(self):
        """Return the winning alternative, as a tuple index.
           On draw, return the first alternative.
        """
        return self.index(max(self))

    def max_key(self):
        """Return name of the winning alternative (Aye, No, Refrain).
           On draw, return the first alternative.
        """
        return self._fields[self.index(max(self))]


def votes_from_rawdata(votes):
    dict_ = defaultdict(int, votes.value_counts())
    """ Exclude absent MP's (`Fr\xc3\xa5nvarande`) """
    votes = Votes(dict_["Ja"], dict_["Nej"], dict_["Avst\xc3\xa5r"])
    return votes
