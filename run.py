# coding: utf-8
""" This is the entry point for the voting analyzis.
"""

from modules.interface import Interface
from modules.parliament import PARTIES
from argparse import ArgumentError
# from csvkit import DictWriter
import pandas
import analyzers


def main():
    """ Entry point when run from command line
    """
    # pylint: disable=C0103

    cmd_args = [{
        'short': "-f", "long": "--csvfile(s)",
        'dest': "csvfile",
        'type': str,
        'help': """CSV file(s) from
http://data.riksdagen.se/Data/Voteringar/,
separate multiple files with pipe (|)""",
        'required': True
    }, {
        'short': "-q", "long": "--query",
        'dest': "query",
        'type': str,
        'choices': ["loyalty",
                    "kingmaking",
                    "supporters",
                    "friends",
                    "commonground",
                    "rebels"],
        'help': "What should we check for?",
        'required': True
    }, {
        'short': "-o", "long": "--outputfile",
        'dest': "outputfile",
        'type': str,
        'help': """File to write results to.
Leave empty to print to stdout.""",
    }, {
        'short': "-p", "long": "--party",
        'dest': "party",
        'type': str,
        'default': "*",
        'help': """Party or parties to analyze.
Separate multiple parties with pipe (|)""",
    }, {
        'short': "-r", "long": "--party2",
        'dest': "party2",
        'type': str,
        'help': "Comparison party, when relevant",
    }, {
        'short': "-t", "long": "--threshold",
        'dest': "threshold",
        'type': float,
        'metavar': "[0.5-1.0]",
        'help': """How large majority should we require to assume
that something was a block line""",
        'default': 0.9
    }, {
        'short': "-d", "long": "--offline",
        'dest': "offline",
        'type': bool,
        'help': """Don't query the Riksdagen API, use only local data.""",
        'default': True
    }, {
        'short': "-s", "long": "--start",
        'dest': "start",
        'type': str,
        'help': """Startdate, e.g. `2014-10-01`""",
        'default': "0"
    }, {
        'short': "-e", "long": "--end",
        'dest': "end",
        'type': str,
        'help': """Enddate, e.g. `2014-10-01`""",
        'default': "9"
    }]
    ui = Interface("Blocken",
                   "Analyze voting patterns",
                   commandline_args=cmd_args)

    if ui.args.query == "loyalty":
        analyzerClass = analyzers.Loyalty
        if ui.args.party is None:
            raise ArgumentError("Party is required for this query")
    elif ui.args.query == "kingmaking":
        analyzerClass = analyzers.Kingmaking
        if ui.args.party is None:
            raise ArgumentError("Party is required for this query")
    elif ui.args.query == "supporters":
        analyzerClass = analyzers.Supporters
    elif ui.args.query == "friends":
        analyzerClass = analyzers.Friends
    elif ui.args.query == "rebels":
        analyzerClass = analyzers.Rebels
        ui.args.offline = True
    elif ui.args.query == "commonground":
        analyzerClass = analyzers.CommonGround
        if ui.args.party2 is None:
            raise ArgumentError("Party2 is required for this query")
    else:
        raise NotImplementedError("No analyzer for this query")

    ui.info("Loading votingdata")
    data = pandas.DataFrame()
    for file_ in ui.args.csvfile.split("|"):
        frame = pandas.read_csv(file_,
                                header=None,
                                names=analyzers.Analyzer.header_names)
        data = data.append(frame, ignore_index=True)
    ui.info("Converting to upper case")
        data.loc[:,'parti'] = map(lambda x: x.upper(), data['parti']) #converts parti to upper
    ui.info("Preparing votingdata")
    if ui.args.party == "*":
        ui.args.party = "|".join(PARTIES)
    for party in ui.args.party.split("|"):
        analyzer = analyzerClass(party,
                                 threshold=ui.args.threshold,
                                 offline=ui.args.offline,
                                 start_date=ui.args.start,
                                 end_date=ui.args.end,
                                 party_2=ui.args.party2)

        analyzer.load(data)
        ui.info("Found %s unique main votes" % analyzer.num_votes)

        ui.info("Analyzing data")
        analyzer.run(screen_dump=(ui.args.outputfile is None))

"""
    if ui.args.outputfile is not None:
        ui.info("Writing results to %s" % ui.args.outputfile)
        fieldnames = output_data[0].keys()  # Don't complicate things

        with open(ui.args.outputfile, 'wb') as file_:
            writer = DictWriter(file_, fieldnames=fieldnames)
            writer.writeheader()
            for row in output_data:
                    writer.writerow(row)
"""

if __name__ == '__main__':
    main()
