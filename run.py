# coding: utf-8
""" This is the entry point for the voting analyzis.
"""

from modules.interface import Interface
from modules.parliament import Blocks, Votes, votes_from_rawdata
import pandas

# Constants
REBEL = 3
DIVERGING = 2
LOYAL = 1


def main():
    """ Entry point when run from command line
    """
    # pylint: disable=C0103

    cmd_args = [
        {
            'short': "-f", "long": "--csvfile",
            'dest': "csvfile",
            'type': str,
            'help': """CSV file from
http://data.riksdagen.se/Data/Voteringar/""",
            'required': True
        },
        {
            'short': "-p", "long": "--party",
            'dest': "party",
            'type': str,
            'help': "Party to analyze",
            'required': True
        },
        {
            'short': "-t", "long": "--threshold",
            'dest': "threshold",
            'type': float,
            'metavar': "[0.5-1.0]",
            'help': """How large majority should we require to assume
that something was a block line""",
            'default': 0.9
        },
    ]
    ui = Interface("Blocken",
                   "Analyze voting patterns",
                   commandline_args=cmd_args)

    ui.info("Loading votingdata")

    header_names = ["rm", "beteckning", "punkt", "votering_id", "namn",
                    "intressent_id", "parti", "valkrets", "rost",
                    "avser", "banknummer", "kon", "fodd", "datum"]
    data = pandas.read_csv(ui.args.csvfile, header=None, names=header_names)
    # Take only "sakfrågan" in account
    data = data[data.avser == "sakfrågan"]
    votes = pandas.pivot_table(data, values=["rost"], index=["punkt"],
                               columns=["parti"], aggfunc=votes_from_rawdata)
    # put dates in a smaller dict, for convinience
    dates = {row[1]["punkt"]: row[1]["datum"] for row in data.iterrows()}

    blocks = Blocks()
    output_data = {}

    for vote in votes.iterrows():
        vote_id = vote[0]

        # Get sum of votes by block
        # and for out party
        block_votes = {b: Votes(0, 0, 0) for b in blocks.blocks}
        party_votes = None
        for k, v in vote[1].iteritems():
            party = k[1]
            b = blocks.what_block(party)
            block_votes[b] = block_votes[b].sum(v)
            if party == ui.args.party:
                party_votes = v

        # What block does the party we're analyzing belong to?
        block = blocks.what_block(ui.args.party)

        # How did the rest of our block vote (our block - our part)?
        rest_block_votes = block_votes[block].minus(party_votes)
        rel_rest_block_votes = rest_block_votes.relative()
        block_alternative = rest_block_votes.max_index()  # Aye/No/Refrain
        block_margin = rel_rest_block_votes[block_alternative]  # 0-1
        party_alternative = party_votes.max_index()
        rel_party_votes = party_votes.relative()
        party_margin = rel_party_votes[party_alternative]

        category = None
        if block_margin >= ui.args.threshold:
            # There was a clear block line

            if party_alternative != block_alternative:
                # ... but our party didn't follow
                category = REBEL
            elif party_margin < 1:
                # followed, but not entirely
                category = DIVERGING
            elif party_margin == 1:
                # ... and our party followed
                category = LOYAL
            else:
                ui.error("This should never happen!")

        else:
            # There was no clear block line
            pass

        print vote_id,
        print dates[vote_id],
        print category

if __name__ == '__main__':
    main()
