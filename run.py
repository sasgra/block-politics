# coding: utf-8
""" This is the entry point for the voting analyzis.
"""

from modules.interface import Interface
from modules.parliament import votes_from_rawdata
from argparse import ArgumentError
from re import sub
from csvkit import DictWriter
import pandas
import requests
import analyzers


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
            'short': "-q", "long": "--query",
            'dest': "query",
            'type': str,
            'choices': ["loyalty", "kingmaking", "supporters"],
            'help': "What should we check for?",
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
        {
            'short': "-d", "long": "--offline",
            'dest': "offline",
            'type': bool,
            'help': """Don't query the Riksdagen API, use only local data.""",
            'default': False
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
    # put dates, and utskott in a smaller dict, for convinience
    metadict = {row[1]["punkt"]: (row[1]["datum"],
                                  row[1]["beteckning"])
                for row in data.iterrows()}
    ui.info("Found %s unique main votes" % num_votes)

    ui.info("Analyzing data")
    output_data = []

    if ui.args.query == "loyalty":
        if ui.args.party is None:
            raise ArgumentError("Party is required for this query")
        analyzer = analyzers.Loyalty(ui.args.party, ui.args.threshold)
    elif ui.args.query == "kingmaking":
        if ui.args.party is None:
            raise ArgumentError("Party is required for this query")
        analyzer = analyzers.Kingmaking(ui.args.party, ui.args.threshold)
    elif ui.args.query == "supporters":
        analyzer = analyzers.Supporters(None, ui.args.threshold)
    else:
        raise NotImplementedError("No analyzer for this query")

    i = 0
    for vote in votes.iterrows():
        i += 1
        vote_id = vote[0]
        ui.info("Checking vote %s/%s: %s" % (i, num_votes, vote_id))

        date = metadict[vote_id][0]
        if ui.args.query == "kingmaking":
            analysis = analyzer.run(vote, date)
        elif ui.args.query == "loyalty":
            analysis = analyzer.run(vote)
        elif ui.args.query == "supporters":
            analysis = analyzer.run(vote, date)

        voting_url = "http://data.riksdagen.se/votering/%s/json" % vote_id
        if ui.args.offline:
            title = None
            doc = None
        else:
            ui.debug("Fetching remote data for %s" % vote_id)
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

        utskott = sub(r'[0-9]', "", metadict[vote_id][1]).decode('utf-8')
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

        if ui.args.outputfile is None:
            analyzer.short_repr(analysis)

    if ui.args.outputfile is not None:
        ui.info("Writing results to %s" % ui.args.outputfile)
        fieldnames = output_data[0].keys()  # Don't complicate things

        with open(ui.args.outputfile, 'wb') as file_:
            writer = DictWriter(file_, fieldnames=fieldnames)
            writer.writeheader()
            for row in output_data:
                    writer.writerow(row)

if __name__ == '__main__':
    main()
