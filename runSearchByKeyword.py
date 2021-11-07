# -*- coding: utf-8 -*-
"""
This script demonstrates how to search the corpus by keyword, and provides
a simple user inteface for reviewing the results.

Make sure to enter your search terms using the `includes` and `excludes`
variables!

@author: Chris McCormick
"""
from simsearch import SimSearch

parser = argparse.ArgumentParser(description="Parses Text")
parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")
parser.add_argument("-o", "--output_dir", help="Glob pattern for output dir")
args = parser.parse_args()

if args.debug:
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s", level=logging.DEBUG
    )
else:
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
    )


###############################################################################
# Load the pre-built corpus.
###############################################################################
print ("Loading the saved SimSearch and corpus...")
output_dir = "./mhc_corpus/"
if args.output_dir:
    output_dir = args.output_dir
(ksearch, ssearch) = SimSearch.load(save_dir=output_dir)

###############################################################################
# Define search terms!
###############################################################################
includes = ["blind", "birth"]
excludes = ["samson"]

###############################################################################
# Perform the search
###############################################################################

print "Performing keyword search..."
print "    Including: %s" % ", ".join(includes)
print "    Excluding: %s" % ", ".join(excludes)

# Perform the search.
results = ksearch.keywordSearch(includes=includes, excludes=excludes, docs=[])

###############################################################################
# Display results.
###############################################################################

print "Found %d results." % len(results)

# Wait to display the first result.
user_input = raw_input("Press enter to display first result...\n")

# Display each of the results.
for doc_id in results:

    # Display the result, concatenated to 8 lines.
    ksearch.printDocSourcePretty(doc_id, max_lines=8)

    # Wait to display the next result.
    user_input = raw_input("[N]ext result  [F]ull text  [Q]uit\n: ")

    command = user_input.lower()

    # q -> Quit.
    if command == "q":
        break
    # f -> Display full doc source.
    elif command == "f":
        ksearch.printDocSourcePretty(doc_id, max_lines=100)
        raw_input("Press enter to continue...")
