# coding: utf-8
""" A collection of analyzer classes for votes
"""
from modules.parliament import Blocks, Votes, votes_from_rawdata
from sys import stdout
from re import sub
import pandas
import requests


class Analyzer(object):

    party = None
    block = None
    threshold = None
    offline = None

    blocks = Blocks()
    votes = None
    num_votes = None
    metadict = None
    """Headers in voting data from the API"""
    header_names = ["rm", "beteckning", "punkt", "votering_id", "namn",
                    "intressent_id", "parti", "valkrets", "rost",
                    "avser", "banknummer", "kon", "fodd", "datum"]

    def __init__(self, party=None, threshold=None, offline=False):
        self.party = party
        self.block = self.blocks.what_block(party)
        self.threshold = threshold
        self.offline = offline

    def analyze_vote(self, vote):
        """Analyse of this vote. Return a dictionary with values to
           add to an output row"""
        raise NotImplementedError("This class must be overridden")

    def short_repr(self, code):
        """A short representation of a vote category,
           for visualizing the voting pattern.
           Normally one character.
        """
        return code

    def load(self, data):
        """Prepare voting data from the Riksdagen API for analyze.
           data is a pandas dataframe
        """
        # Take only "sakfrågan" in account
        data = data[data.avser == "sakfrågan"]
        self.votes = pandas.pivot_table(data, values=["rost"],
                                        index=["punkt"], columns=["parti"],
                                        aggfunc=votes_from_rawdata)
        self.num_votes = len(self.votes)

        # put dates, and utskott in a smaller dict, for convinience
        self.metadict = {row[1]["punkt"]: (row[1]["datum"],
                                           row[1]["beteckning"])
                         for row in data.iterrows()}

    def run(self, screen_dump=False):
        i = 0
        output_data = []
        for vote in self.votes.iterrows():
            i += 1
            vote_id = vote[0]
            # print("Analyzing vote %s/%s: %s" % (i, self.num_votes, vote_id))
            analysis = self.analyze_vote(vote)

            voting_url = "http://data.riksdagen.se/votering/%s/json" % vote_id
            if self.offline:
                title = None
                doc = None
            else:
                r = requests.get(voting_url)
                if r.status_code == 200:
                    res = r.json()
                    title = res["votering"]["dokument"]["titel"]
                    if res["votering"]["dokument"]["subtitel"]:
                        title += u" – "
                        title += res["votering"]["dokument"]["subtitel"]
                    doc = res["votering"]["dokument"]["dokument_url_html"]
                else:
                    title = None
                    doc = None

            utskott = sub(r'[0-9]', "",
                          self.metadict[vote_id][1]).decode('utf-8')
            date = self.metadict[vote_id][0]
            row_data = {'id': vote_id,
                        'date': date,
                        'month': date[:7],
                        'halfyear': (int(date[5:7]) > 6) + 1,
                        'url': voting_url,
                        'title': title,
                        'document': doc,
                        'utskott': utskott
                        }
            for k, v in analysis.iteritems():
                row_data[k] = v

            output_data.append(row_data)

            if screen_dump is True:
                self.short_repr(analysis)

        return output_data


class Friends(Analyzer):
    """Find out who voted with whom
    """

    fields = None  # Populate on init

    def __init__(self, party=None, threshold=None, offline=False):
        Analyzer.__init__(self, None)

        # create pairs of parties
        parties = self.blocks.parties
        self.party_pairs = list(set([frozenset([a, b])
                                for a in parties for b in parties if a != b]))

    def run(self, screen_dump=False):
        """Do some postprocessing"""
        i = 0
        output_data = []
        for vote in self.votes.iterrows():
            i += 1
            vote_id = vote[0]
            analysis = self.analyze_vote(vote)
            print analysis



    def analyze_vote(self, vote):
        party_votes = {}
        for k, v in vote[1].iteritems():
            party = k[1]
            # Ignore MPs with no party affiliation
            if party == '-':
                continue
            # Ugly hardcoded fix for now
            if party == "L":
                party = "FP"
            if v is not None:
                party_votes[party] = v
        output_dict = {}
        for pair in self.party_pairs:
            a, b = list(pair)
            key = "%s_%s" % (a, b)
            if party_votes[a].max_index() == party_votes[b].max_index():
                output_dict[key] = 1
            else:
                output_dict[key] = 0
        return output_dict


class Supporters(Analyzer):
    """Find out who supported the government
    """

    fields = ["category", "party"]

    def analyze_vote(self, vote):
        date = self.metadict[vote[0]][0]

        self.gov = self.blocks.what_gov(date)
        gov_votes = Votes(0, 0, 0)
        party_votes = {}
        for k, v in vote[1].iteritems():
            party = k[1]
            # Ignore MPs with no party affiliation
            if party == '-':
                continue
            # Ugly hardcoded fix for now
            if party == "L":
                party = "FP"
            if v is not None:
                party_votes[party] = v
                if party in self.gov["parties"]:
                    gov_votes = gov_votes.sum(v)
        gov_line = gov_votes.max_key()
        output_dict = {}
        if gov_votes.margin() > self.threshold:
            """There was a governement line (anything else
               would be extremely remarkable)
            """
            for party in self.blocks.parties:
                if party in self.gov["parties"]:
                    # Ignore govt members
                    pass
                elif party_votes[party].max_key() == gov_line:
                    output_dict[party] = 1
                else:
                    output_dict[party] = 0
        else:
            pass

        return output_dict


class Kingmaking(Analyzer):
    """Find out if a party supported the government
    """

    SUPPORT = 1
    OPPOSE = 0

    fields = ["category"]

    def short_repr(self, analysis):
        if analysis["category"] is not None:
            stdout.write(["░", "█"][analysis["category"]])
        else:
            stdout.write(" ")
        stdout.flush()

    def analyze_vote(self, vote):
        date = self.metadict[vote[0]][0]
        # Find out what government is in charge
        self.gov = self.blocks.what_gov(date)["parties"]

        # Get sum of votes for government
        # and for out party
        gov_votes = Votes(0, 0, 0)
        party_votes = Votes(0, 0, 0)
        for k, v in vote[1].iteritems():
            party = k[1]
            # Ugly hardcoded fix for now
            if party == "L":
                party = "FP"
            if party in self.gov and v is not None:
                gov_votes = gov_votes.sum(v)
            if party == self.party and v is not None:
                party_votes = v

        gov_line = gov_votes.max_index()
        party_line = party_votes.max_index()

        if gov_votes.margin() > self.threshold:
            if party_line == gov_line:
                category = self.SUPPORT
            else:
                category = self.OPPOSE
        else:
            category = None

        return {"category": category}


class Loyalty(Analyzer):
    """Find out if a party followed their block line or not.
    """

    REBEL = 3
    DIVERGING = 2
    LOYAL = 1

    fields = ["category"]

    def short_repr(self, analysis):
        if analysis["category"] is not None:
            stdout.write(["░",
                          "\033[92m▒\033[0m",
                          "\033[93m▓\033[0m",
                          "\033[91m█\033[0m"
                          ][analysis["category"]])
        else:
            stdout.write(" ")
        stdout.flush()

    def analyze_vote(self, vote):
        # Get sum of votes by block
        # and for out party
        block_votes = {b: Votes(0, 0, 0) for b in self.blocks.blocks}
        party_votes = Votes(0, 0, 0)
        for k, v in vote[1].iteritems():
            party = k[1]
            # Ugly hardcoded fix for now
            if party == "L":
                party = "FP"
            b = self.blocks.what_block(party)
            if b in block_votes.keys() and v is not None:
                block_votes[b] = block_votes[b].sum(v)
            if party == self.party and v is not None:
                party_votes = v

        # How did the rest of our block vote (our block - our part)?
        rest_block_votes = block_votes[self.block].minus(party_votes)
        block_alternative = rest_block_votes.max_index()  # Aye/No/Refrain
        party_alternative = party_votes.max_index()

        # If alternative i Aye/No, don't take Refrain into account
        # This elliminates some possible errors related to “kvittning”
        block_margin = rest_block_votes.margin()
        party_margin = party_votes.margin()

        category = None
        if block_margin >= self.threshold:
            # There was a clear block line

            if party_alternative != block_alternative:
                # ... but our party didn't follow
                category = self.REBEL
            elif party_margin < 1:
                # followed, but not entirely
                category = self.DIVERGING
            elif party_margin == 1:
                # ... and our party followed
                category = self.LOYAL
            else:
                raise Exception("This should never happen!")
        else:
            # There was no clear block line
            pass
        return {"category": category}
