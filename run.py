# coding: utf-8
""" This is the entry point for the voting analyzis.
"""

from modules.interface import Interface
from modules.parliament import Blocks, Votes, votes_from_rawdata
from csvkit import DictWriter
import pandas
import requests

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
            'short': "-o", "long": "--outputfile",
            'dest': "outputfile",
            'type': str,
            'help': """File to write results to.
Leave empty to print to stdout.""",
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

    ui.info("Peparing data")
    votes = pandas.pivot_table(data, values=["rost"], index=["punkt"],
                               columns=["parti"], aggfunc=votes_from_rawdata)
    num_votes = len(votes)
    # put dates in a smaller dict, for convinience
    dates = {row[1]["punkt"]: row[1]["datum"] for row in data.iterrows()}
    ui.info("Found %s unique main votes" % num_votes)

    ui.info("Analyzing data")
    output_data = []
    blocks = Blocks()

    # What block does the party we're analyzing belong to?
    block = blocks.what_block(ui.args.party)

    i = 0
    for vote in votes.iterrows():
        i += 1
        vote_id = vote[0]
        ui.debug("Checking vote %s/%s: %s" % (i, num_votes, vote_id))

        # Get sum of votes by block
        # and for out party
        block_votes = {b: Votes(0, 0, 0) for b in blocks.blocks}
        party_votes = Votes(0, 0, 0)
        for k, v in vote[1].iteritems():
            party = k[1]
            # Ugly hardcoded fix for now
            if party == "L":
                party = "FP"
            b = blocks.what_block(party)
            if b in block_votes.keys() and v is not None:
                block_votes[b] = block_votes[b].sum(v)
            if party == ui.args.party and v is not None:
                party_votes = v

        if party_votes is None:
            ui.error("Failed to fetch %s votes in vote %s" % (ui.args.party, vote_id))

        # How did the rest of our block vote (our block - our part)?
        rest_block_votes = block_votes[block].minus(party_votes)
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

        ui.info("Fetching remote data for %s" % vote_id)
        voting_url = "http://data.riksdagen.se/votering/%s/json" % vote_id
        r = requests.get(voting_url)
        if r.status_code == 200:
            res = r.json()
            title = res["votering"]["dokument"]["titel"]
            if res["votering"]["dokument"]["subtitel"]:
                title += u" – "
                title += res["votering"]["dokument"]["subtitel"]
            doc = res["votering"]["dokument"]["dokument_url_html"]
        else:
            ui.warning("Failed fetching %s" % voting_url)
            title = None
            doc = None

        output_data.append({'id': vote_id,
                            'date': dates[vote_id],
                            'month': dates[vote_id][:7],
                            'category': category,
                            'url': voting_url,
                            'title': title,
                            'document': doc
                            })

        if ui.args.outputfile is None:
            print ",".join(output_data.values())

    if ui.args.outputfile is not None:
        ui.info("Writing results to %s" % ui.args.outputfile)
        with open(ui.args.outputfile, 'wb') as file_:
            writer = DictWriter(file_, fieldnames=['id', 'date', 'month', 'category', 'url', 'title', 'document'])
            writer.writeheader()
            for row in output_data:
                    writer.writerow(row)

if __name__ == '__main__':
    main()
