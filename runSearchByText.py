# -*- coding: utf-8 -*-
"""
This script demonstrates how to search the corpus by some new input text,
specified in a text file 'input.txt'.

It also provides a simple user interface for reviewing the results.

E.g python runSearchByText.py -o "~/sim_corpus/mygtd_2020-11-06/"

@author: Chris McCormick
"""

import logging
import argparse
from simsearch import SimSearch
import os

parser = argparse.ArgumentParser(description="Parses Text")
parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")
parser.add_argument("-o", "--output_dir", help="Glob pattern for output dir")
parser.add_argument("-t", "--text")
args = parser.parse_args()

if args.debug:
    logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.DEBUG)
else:
    logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

###############################################################################
# Load the pre-built corpus.
###############################################################################
print('Loading the saved SimSearch and corpus...')
output_dir = "./mhc_corpus/"
if args.output_dir:
    output_dir = os.path.expanduser(args.output_dir)
(ksearch, ssearch) = SimSearch.load(save_dir=output_dir)

# ###############################################################################
# # Read `input.txt` as input text for search.
# ###############################################################################

# # Load 'input.txt' as the input to the search.
# input_vec = ksearch.getTfidfForFile(os.path.expanduser('~/GittedUtilities/simsearch/input.txt'))

if args.text:
    input_vec = ksearch.getTfidfForText(args.text)

# Number of results to go through.
topn = 10
# topn = 20

###############################################################################
# Perform the search
###############################################################################

print('Searching by contents of input.txt...')

# Perform the search.
results = ssearch.findSimilarToVector(input_vec, topn=topn)

###############################################################################
# Display results.
###############################################################################

# for i in range(0, topn):
for i in range(topn - 1, -1, -1):

    # Show the text for the result.
    ssearch.printResultsBySourceText([results[i]], max_lines=8)

    # Get the tf-idf vector for the result.
    result_vec = ksearch.getTfidfForDoc(results[i][0])

    print('')

    # Interpret the match.
    ssearch.interpretMatch(input_vec, result_vec, min_pos=0)

    # # Wait for user input.
    # command = input("[N]ext result  [F]ull text  [Q]uit\n: ").lower()

    # # q -> Quit.
    # if (command == 'q'):
    #     break
    # # f -> Display full doc source.
    # elif (command == 'f'):
    #     ksearch.printDocSourcePretty(results[i][0], max_lines=100)
    #     input('Press enter to continue...')

    ksearch.printDocSource(results[i][0], max_lines=100)

