#Installation

    pip install -r requirements.txt

or, depending on your environment: 

    sudo pip install -r requirements.txt

#Running

    python run.py --help

This example will analyze he votingpattern of C, during 2014/15, and output or overwrite C-1415.csv:

    python run.py --csvfile data/votering-201415.csv --party C --outputfile C-1415.csv

This example will analyze he votingpattern of C, during 2014/15, and print debug messages to the screen:

    python run.py --csvfile data/votering-201415.csv --party C --loglevel 1
