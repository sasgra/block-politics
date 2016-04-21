# coding: utf-8
""" A collection of analyzer classes for votes
"""
from modules.parliament import Blocks, Votes
from sys import stdout


class Analyzer(object):

    party = None
    block = None
    blocks = Blocks()
    fields = None  # What fields the analysis dictionary will contains

    def __init__(self, party):
        self.party = party
        self.block = self.blocks.what_block(party)

    def run(self, vote):
        """Analyse of this vote. Return a dictionary."""
        raise NotImplementedError("This class must be overridden")

    def short_repr(self, code):
        """A short representation of a vote category,
           for visualizing the voting pattern.
           Normally one character.
        """
        return code


class Friends(Analyzer):
    """Find out who voted with whom
    """

    fields = None  # Populate on init

    def __init__(self):
        Analyzer.__init__(self, None)
        parties = self.blocks.parties
        self.fields = ["%s_%s" % (a, b) for a in parties for b in parties if a != b]

    def run(self, vote):
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
        output_dict = {a: None for a in self.fields}
        for party_a, party_vote_a in party_votes.iteritems():
            for party_b, party_vote_b in party_votes.iteritems():
                if party_a == party_b:
                    continue
                if party_vote_a.max_index() == party_vote_b.max_index():
                    key = "%s_%s" % (party_a, party_b)
                    output_dict[key] = 1
        return output_dict


class Supporters(Analyzer):
    """Find out who supported the government
    """

    fields = ["category", "party"]

    def __init__(self, party, threshold):
        Analyzer.__init__(self, party)
        self.threshold = threshold

    def run(self, vote, date):
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

    def __init__(self, party, threshold):
        Analyzer.__init__(self, party)
        self.threshold = threshold

    def short_repr(self, analysis):
        if analysis["category"] is not None:
            stdout.write(["░", "█"][analysis["category"]])
        else:
            stdout.write(" ")
        stdout.flush()

    def run(self, vote, date):
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

    def __init__(self, party, threshold):
        Analyzer.__init__(self, party)
        self.threshold = threshold

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

    def run(self, vote):
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
