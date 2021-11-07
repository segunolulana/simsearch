from corpusbuilder import CorpusBuilder
from simsearch import SimSearch
from os import makedirs
from os.path import exists
import logging
import argparse
import os


parser = argparse.ArgumentParser(description="Parses Text")
parser.add_argument("-d", "--debug", action="store_true", help="Debug mode")
parser.add_argument("-i", "--input_dir", help="Glob pattern for input dir")
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
# logging.getLogger("gensim").setLevel(logging.INFO)

# Create the CorpusBuilder.
cb = CorpusBuilder()

# Set the list of stop words.
cb.setStopList(os.path.join(os.path.dirname(__file__), "stop_words.txt"))

# Match blank lines as the separator between "documents".
cb.setDocStartPattern(r"^\s*$")

# The MHC text includes a number of patterns which need to be filtered out...
sub_patterns = []

# Remove line breaks of the form "___________"
sub_patterns.append((r"_+", " "))

# Remove verse references like "ver. 5-7" or "ver. 25, 26"
sub_patterns.append((r"ver\. \d+(-|, )*\d*", " "))

# Remove verse numbers of the form "18.", "2.", etc., as well as any other
# remaining numbers.
sub_patterns.append((r"\d+\.?", " "))

non_words = ["(:PROPERTIES:.*)", "(:END:)", "(:CREATED:.*)", "(:id:.*)", r"(mygtd\d*:)", r"(:[a-zA-Z]+:)"]
pattern = r"(" + r"|".join(non_words) + r")"
sub_patterns.append((pattern, ""))

cb.setSubstitutions(sub_patterns)


print("Parsing Matthew Henry's Commentary...")
# Parse all of the text files in the directory.
cb.addDirectory(args.input_dir)

print("Done.")

print("Building corpus...")

cb.buildCorpus()

# Initialize a KeySearch object from the corpus.
ksearch = cb.toKeySearch()

# Print the top 30 most common words.
ksearch.printTopNWords(topn=30)

print("\nVocabulary contains", ksearch.getVocabSize(), "unique words.")

print("Corpus contains", len(
    ksearch.corpus_tfidf
), '"documents" represented by tf-idf vectors.')

# Initialize a SimSearch object from the KeySearch.
ssearch = SimSearch(ksearch)

# Train LSI with 100 topics.
print("\nTraining LSI...")
ssearch.trainLSI(num_topics=300)

print("\nSaving to disk...")

output_dir = "./mhc_corpus/"
if args.output_dir:
    output_dir = os.path.expanduser(args.output_dir)
if not exists(output_dir):
    makedirs(output_dir)

ssearch.save(save_dir=output_dir)

print("Done!")
