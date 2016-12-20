"""
Generate documents for document order N, where N is the number of languages
in the document.

Marco Lui, July 2012
"""

import os, sys, shutil, csv
import optparse
import random
import math
from collections import defaultdict
import numpy as np

from util import mkdir_p

random.seed(61383441363)

# adapted from http://code.google.com/p/hydrat/source/browse/src/hydrat/common/sampling.py
def partition(num_items, weights, probabilistic = False):
  """
  Partition a number of items into partitions according to weights
  Modified from hydrat: http://hydrat.googlecode.com/svn/trunk/task/sampler.py
  @return: map of doc_index -> partition membership
  @rtype: numpy boolean array (items * partitions)
  """
  rng = np.random
  weights = np.array(weights)
  probabilities = weights / float(np.sum(weights))

  num_parts   = len(probabilities)
  partition_map = np.zeros((num_items,num_parts), dtype = 'bool')
  if probabilistic:
    c = np.cumsum(probabilities)
    r = rng.random_sample(num_items)
    partition_indices = np.searchsorted(c, r)
    for doc_index, part_index in enumerate(partition_indices):
      partition_map[doc_index, part_index] = True
  else:
    partition_sizes = np.floor(probabilities * num_items).astype(int)
    items_partitioned = partition_sizes.sum()
    gap = num_items - items_partitioned
    # Distribute the gap amongst the biggest partitions, adding one to each
    # This behaviour was deprecated as it does not behave well when partitions
    # all have the same size. The later partitions get favored by nature of the
    # argsort.
    # distribute_gap_to = np.argsort(partition_sizes) >= (num_parts - gap)
    # Randomly distribute it
    distribute_gap_to = np.concatenate(( np.ones(gap, dtype=bool), np.zeros(num_parts-gap, dtype=bool) ))
    rng.shuffle(distribute_gap_to)
    partition_sizes[distribute_gap_to] += 1
    assert partition_sizes.sum() == num_items
    indices = np.arange(num_items)
    rng.shuffle(indices)
    index        = 0
    for part_index, part_size in enumerate(partition_sizes):
      for i in xrange(part_size):
        doc_index = indices[index]
        partition_map[doc_index, part_index] = True
        index += 1
  return partition_map.argmax(1)

def get_segment(path, denominator):
  """
  Open file at the given path and read a segment.
  @param path the path
  @param denominator the proportion of the file to read (1/denominator)
  """
  with open(path) as f:
    lines = [l.strip() for l in f if l.strip()]

  keep_lines = int(math.ceil(len(lines)/float(denominator)))
  segment = ' '.join(lines[:keep_lines])
  return segment

PRIORS = ['natural', 'uniform']

def main(opts, args):
  if not (os.path.exists(opts.output) and os.path.isdir(opts.output)):
    mkdir_p(opts.output)

  exclude_paths = set()
  for p in opts.exclude:
    with open(p) as f:
      exclude_paths |= set(l.strip() for l in f)
  print "generating {0} {1}-language documents at {2}".format(opts.count, opts.segments, opts.output)
  print "excluding {0} paths".format(len(exclude_paths))

  with open(opts.langs) as f:
    LANGS = [l.strip() for l in f]

  docs_per_lang = defaultdict(set)
  with open(opts.input) as f:
    for row in (l.strip() for l in f):
      if row not in exclude_paths:
        path, docid = os.path.split(row)
        path, lang = os.path.split(path)
        docs_per_lang[lang].add(row)

  lang_allocations = []
  if opts.prior == 'uniform':
    dist = np.fromiter((1 for l in LANGS), dtype=float)
  elif opts.prior == 'natural':
    dist = np.fromiter((len(docs_per_lang[l]) for l in LANGS), dtype=float)
  else:
    raise ValueError("unknown prior")

  dist = np.sum(dist) / len(dist)

  
  """
  lang_allocations = []
  for i in xrange(opts.segments):
    allocation = [LANGS[i] for i in partition(opts.count, dist)]

    # TODO: We have to ensure that we do not allow a single document to contain multiple
    # copies of the same language. We don't have this capacity now. Need to think if it 
    # can be done in this allocation strategy.
     
    # Print the allocation over classes
    c = defaultdict(int)
    for a in allocation:
      c[a] += 1
    print dict(c)
    
    random.shuffle(allocation)
    lang_allocations.append(allocation)
  """

  with open(opts.metadata,'w') as meta_f:
    writer = csv.writer(meta_f)
    with open(opts.used,'w') as used_f:
      for i in xrange(opts.count):
        ordered_langs = sorted(zip(np.random.random(len(LANGS)) * dist, LANGS), reverse=True)
        doc_langs = [l for p,l in ordered_langs[:opts.segments]]
        print doc_langs
        doc_id = "doc{0:0{1}}".format(i+1,len(str(opts.count)))
        new_doc = []
        for j, lang in enumerate(doc_langs):
          segment = None
          while not segment:
            # Keep looping until we get a valid segment. This handles empty segments
            try:
              path = docs_per_lang[lang].pop()
            except KeyError:
              import pdb;pdb.post_mortem()
            exclude_paths.add(path)
            used_f.write(path + '\n')
            segment = get_segment(path, opts.segments)

          new_doc.append(segment)
          # Write the segment metadata
          writer.writerow((doc_id, j+1, len(new_doc), lang, len(segment)))

        # Write the document
        with open(os.path.join(opts.output, doc_id), 'w') as out_f:
          out_f.write(''.join(new_doc))

      

if __name__ == "__main__":
  parser = optparse.OptionParser()
  parser.add_option("-i","--input",help="list of input documents")
  parser.add_option("-o","--output",help="output directory", default='output')
  parser.add_option("-e","--exclude",help="paths to exclude", action='append', default=[])
  parser.add_option("-c","--count",help="number of documents", default=2000, type=int)
  parser.add_option("-s","--segments",help="number segments", default=2, type=int)
  parser.add_option("-u","--used",help="file to output list of paths used to", default='used')
  parser.add_option("-m","--metadata",help="file to output metadata to", default='metadata')
  parser.add_option("-p","--prior",help="file to output metadata to", default='natural')
  parser.add_option("-l","--langs",help="read list of languages from file", default='selected_langs')
  opts, args = parser.parse_args()

  if opts.prior not in PRIORS:
    parser.error("Prior must be one of {0}, not {1}".format(PRIORS, opts.prior))

  main(opts, args)

