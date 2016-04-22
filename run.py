# coding: utf-8
""" This is the entry point for the voting analyzis.
"""

from modules.interface import Interface
from argparse import ArgumentError
from csvkit import DictWriter
import pandas
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
            'choices': ["loyalty", "kingmaking", "supporters", "friends"],
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
    else:
        raise NotImplementedError("No analyzer for this query")

    analyzer = analyzerClass(ui.args.party,
                             ui.args.threshold,
                             ui.args.offline)

    ui.info("Loading votingdata")
    data = pandas.read_csv(ui.args.csvfile,
                           header=None,
                           names=analyzers.Analyzer.header_names)
    ui.info("Preparing votingdata")
    analyzer.load(data)
    ui.info("Found %s unique main votes" % analyzer.num_votes)

    ui.info("Analyzing data")

    output_data = analyzer.run(screen_dump=(ui.args.outputfile is None))
    print output_data

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
