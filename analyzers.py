# coding: utf-8
""" A collection of analyzer classes for votes
"""
from modules.parliament import Blocks, Votes
from sys import stdout


class Analyzer(object):

    party = None
    block = None
    blocks = Blocks()

    def __init__(self, party):
        self.party = party
        self.block = self.blocks.what_block(party)

    def run(self, vote):
        """Categorize of this vote."""
        raise NotImplementedError("This class must be overridden")

    def short_repr(self, code):
        """A short representation of a vote category,
           for visualizing the voting pattern.
           Normally one character.
        """
        return str(code)


class Loyalty(Analyzer):
    """Find out if a party followed their block line or not.
    """

    REBEL = 3
    DIVERGING = 2
    LOYAL = 1

    def __init__(self, party, threshold):
        Analyzer.__init__(self, party)
        self.threshold = threshold

    def short_repr(self, category):
        if category:
            stdout.write(["░", "\033[92m▒\033[0m", "\033[93m▓\033[0m", "\033[91m█\033[0m"][category])
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
        rel_rest_block_votes = rest_block_votes.relative()
        block_alternative = rest_block_votes.max_index()  # Aye/No/Refrain
        block_margin = rel_rest_block_votes[block_alternative]  # 0-1
        party_alternative = party_votes.max_index()
        rel_party_votes = party_votes.relative()
        party_margin = rel_party_votes[party_alternative]

        # If alternative i Aye/No, don't take Refrain into account
        # This elliminates some possible errors related to “kvittning”
        if rest_block_votes.max_key() in ["Aye", "No"]:
            total = rest_block_votes.Aye + rest_block_votes.No
            block_margin = float(rest_block_votes[block_alternative]) / float(total)
        if party_votes.max_key() in ["Aye", "No"]:
            total = party_votes.Aye + party_votes.No
            party_margin = float(party_votes[party_alternative]) / float(total)

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
        return category
