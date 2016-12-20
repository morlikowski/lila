"""
Create metadata files representing paritions of the data
"""

import sys, os, csv
import random
import optparse

from util import mkdir_p

random.seed(61383441363)

def write_part(path, content):
  with open(path, 'w') as of:
    of.writelines(c + '\n' for c in content)

if __name__ == "__main__":
  parser = optparse.OptionParser()
  parser.add_option("-o", "--output", help="output directory")
  parser.add_option("-t", "--train", help="dir with docs for train part", action='append', default=[])
  parser.add_option("-e", "--test", help="dir with docs for dev/test part", action='append', default=[])
  parser.add_option("--devprop", help="proportion of test data to allocate to dev", default=0.5, type=float)
  opts, args = parser.parse_args()

  if not os.path.exists(opts.output):
    mkdir_p(opts.output)

  train_docs = []
  for p in opts.train:
    train_docs.extend(os.path.join(p,f) for f in os.listdir(p))

  dev_docs = []
  test_docs = []
  for p in opts.test:
    # split dev/test according to the specified proportion
    part_docs = [os.path.join(p,f) for f in os.listdir(p)]
    random.shuffle(part_docs)

    dev_count = int(round(opts.devprop * len(part_docs)))

    dev_docs.extend(part_docs[:dev_count])
    test_docs.extend(part_docs[dev_count:])

  write_part(os.path.join(opts.output, 'train'), train_docs)
  write_part(os.path.join(opts.output, 'dev'), dev_docs)
  write_part(os.path.join(opts.output, 'test'), test_docs)

  print "summary- train:{0} dev:{1} test:{2}".format(len(train_docs), len(dev_docs), len(test_docs))

  


