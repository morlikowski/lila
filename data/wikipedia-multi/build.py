"""
Build the actual dataset through repeated calls to generate.main

Marco Lui, July 2012
"""

import os, sys, optparse

from copy import copy

import generate

def build(parts, params):
  parser = optparse.OptionParser()
  parser.add_option("-i","--input",help="list of input documents", default=PARAMS['input'])
  parser.add_option("-p","--prior",help="file to output metadata to", default=PARAMS['prior'])
  parser.add_option("-l","--langs",help="read list of languages from file", default=PARAMS['langs'])
  parser.add_option("-e","--exclude",help="paths to exclude", action='append', default=PARAMS['exclude'])
  parser.add_option("-o","--outdir",help="directory to output to", default=PARAMS["outdir"])
  opts, args = parser.parse_args()

  for path, count, order in parts:
    p_opts = copy(opts)
    p_opts.count = count
    p_opts.segments = order
    p_opts.output = os.path.join(opts.outdir, path)
    p_opts.metadata = os.path.join(opts.outdir, path+'-meta')
    p_opts.used = os.path.join(opts.outdir, path+'-used')

    generate.main(p_opts, args)
    opts.exclude.append(p_opts.used)

PARAMS = {
  'outdir':"wikipedia-multi",
  'exclude':[],
  'langs':'selected_langs',
  'prior':'uniform',
  'input':'docs_available',
  }

PARTS = [
  ('docsMR', 5000, 1, ),
  ('docsME', 1000, 1, ),
  ('docsUR1', 1000, 1, ),
  ('docsUR2', 1000, 2, ),
  ('docsUR3', 1000, 3, ),
  ('docsUR4', 1000, 4, ),
  ('docsUR5', 1000, 5, ),
  ('docsUE1', 200, 1, ),
  ('docsUE2', 200, 2, ),
  ('docsUE3', 200, 3, ),
  ('docsUE4', 200, 4, ),
  ('docsUE5', 200, 5, ),
  ]

if __name__ == "__main__":
  build(PARTS, PARAMS)
