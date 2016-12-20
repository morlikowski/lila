import logging
import os
import csv

import wikidump.utils
import wikidump.dataset
import wikidump.sampling
from wikidump.counter import Counter

import pb

logger = logging.getLogger(__name__)

class ReTry(Exception): pass

@wikidump.sampling.CheckRNG
def generate_documents( target_dir
                      , langs=wikidump.utils.all_prefixes
                      , count=5000
                      , pri_thresh = 1000
                      , sec_thresh = 1000
                      , overall_thresh = 2000
                      , rng=None 
                      ):
  assert len(set(langs)) == len(langs)
  if not os.path.exists(target_dir): os.mkdir(target_dir)

  dumps = wikidump.utils.load_dumps(langs)
  background = dict((d.get_dumpfile_prefix(), d.metadata['size']) for d in dumps.values())

  with open(os.path.join(target_dir, 'summary'), 'w') as summary:
    summary_writer = csv.writer(summary)
    summary_writer.writerow(['docid', 'pri_lang', 'pri_id', 'pri_len', 'sec_lang', 'sec_id', 'sec_len'])

    # Select an exact number of documents for each language
    lang_dist_raw =\
      wikidump.sampling.weighted_choice\
        ( background
        , count=count
        , rng=rng
        )
    assert len(lang_dist_raw) == count

    lang_dist = Counter(lang_dist_raw)
    assert sum(lang_dist.values()) == count

    doc_count = 0
    for lang in set(langs):
      considered = set()
      selected = set()
      required = lang_dist[lang]

      # Skip the language if we end up with no documents required
      if required == 0: continue
      
      with pb.ProgressBar(maxval=required, widgets=pb.get_widget(lang)) as pbar:
        #TODO: Possible infinite loop if we simply can't find enough docs
        while len(selected) < required:
          try:
            # Choose a random id
            id = rng.randint(background[lang])

            # Skip if considered before
            if id in considered: raise ReTry, "Previously considered"
            considered.add(id)

            # Get the primary page, extract linkset
            pri_page = dumps[lang].get_page_by_index(id)
            lang_avail = set( l for l in langs if pri_page.lang_equiv(l) )
            # Skip if no links
            if len(lang_avail) == 0: raise ReTry, "No links available"

            # Clean the primary_text
            pri_text = wikidump.dataset.remove_mediawiki_syntax(pri_page.text)
            # Skip if empty
            if not pri_text: raise ReTry, "Empty Primary"

            # Try to pick a secondary document
            sec_selected = False 
            sec_lang_choices = dict((l, background[l]) for l in lang_avail if background[l] > 0)
            while not sec_selected:
              if len(sec_lang_choices) == 0: raise ReTry, "No links left"
              sec_lang = wikidump.sampling.weighted_choice(sec_lang_choices, rng=rng)
              try:
                try:
                  sec_id = dumps[sec_lang].get_page_index(pri_page.lang_equiv(sec_lang))
                  sec_page = dumps[sec_lang].get_page_by_index(sec_id)
                except KeyError:
                  # Reject if the link goes nowhere
                  raise ReTry, "Broken Link"

                sec_text = wikidump.dataset.remove_mediawiki_syntax(sec_page.text)
                # Reject if nothing left after cleaning
                if not sec_text: raise ReTry, "Empty Secondary"
                sec_para = wikidump.dataset.paragraphs(sec_text)
                sec_out_text = '\n\n'.join(wikidump.sampling.ceil_half(sec_para))
                sec_selected = True
              except ReTry, e:
                logger.debug("Reject Secondary: %s", e)
                # Remove this language from consideration as a secondary
                del sec_lang_choices[sec_lang]

            # Reject if secondary is too short
            if len(sec_out_text) < sec_thresh: raise ReTry, "Secondary too short"

            pri_para = wikidump.dataset.paragraphs(pri_text)
            pri_out_text = '\n\n'.join(wikidump.sampling.ceil_half(pri_para))+'\n\n'
            # Reject if primary is too short
            if len(pri_out_text) < pri_thresh: raise ReTry, "Primary too short"
            if len(pri_out_text) + len(sec_out_text) < overall_thresh: raise ReTry, "Child too short"

            selected.add(id)
            pbar.update(len(selected))

            doc_name = 'doc%04d.txt'%doc_count
            doc_count += 1
            doc_path = os.path.join(target_dir, doc_name)
            with open(doc_path, 'w') as doc:
              doc.write(pri_out_text)
              doc.write(sec_out_text)
            summary_writer.writerow([doc_name, lang, id, len(pri_out_text), sec_lang, sec_id, len(sec_out_text)])
          except ReTry, e:
            logger.debug("Reject Primary: %s", e.args[0])
            continue

def partition(raw, rng):
  rawfiles = [ f for f in os.listdir(raw) if f.endswith('.txt') ]
  rng.shuffle(rawfiles)
  mapping = {}
  mapping.update( dict((file, 'trn-%04d.txt'%i) for i, file in enumerate(rawfiles[:8000])) )
  mapping.update( dict((file, 'dev-%04d.txt'%i) for i, file in enumerate(rawfiles[8000:9000])) )
  mapping.update( dict((file, 'tst-%04d.txt'%i) for i, file in enumerate(rawfiles[9000:10000])) )
  return mapping


def main():
  import numpy
  import os
  import shutil
  import csv
  rng = numpy.random.mtrand.RandomState(433352)
  langs =\
    ['af', 'an', 'ar', 'ast', 'az', 'be', 'bg', 'bn', 'bpy', 'br', 'bs', 'ca', 'ceb', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'eu', 
    'fa', 'fi', 'fr', 'gl', 'he', 'hi', 'hr', 'ht', 'hu', 'id', 'io', 'is', 'it', 'ja', 'jv', 'ka', 'ko', 'ku', 'la', 'lb', 'lt', 'lv', 'mk', 
    'mr', 'ms', 'nap', 'nds', 'new', 'nl', 'nn', 'no', 'oc', 'pl', 'pms', 'pt', 'ro', 'ru', 'scn', 'sh', 'sk', 'sl', 'sq', 'su', 'sv', 'ta', 
    'te', 'th', 'tl', 'tr', 'uk', 'vi', 'wa', 'zh']

  target = '../scratch/altw2010-langid'
  if not os.path.exists(target): os.mkdir(target)
  raw = os.path.join(target, 'raw')
  #generate_documents( raw, langs, count=10000, rng=rng)
  mapping = partition(raw, rng)
  dataset = os.path.join(target, 'dataset')


  # Create directories
  os.mkdir(dataset)
  os.mkdir(os.path.join(dataset,'trn'))
  os.mkdir(os.path.join(dataset,'dev'))
  os.mkdir(os.path.join(dataset,'tst'))

  summary_by_doc = {}
  raw_summaries = csv.DictReader(open(os.path.join(raw,'summary')))
  for row in raw_summaries:
    summary_by_doc[row['docid']] = row

  # Initialize metadata writers
  summary_writers = {}
  langid_writers = {}
  segments = ['trn','dev','tst']
  for seg in segments:
    summary_writers[seg] = csv.DictWriter(open(os.path.join(dataset,'%s-summary'%seg),'w'), raw_summaries.fieldnames)
    langid_writers[seg] = csv.writer(open(os.path.join(dataset,'%s-lang'%seg),'w'))


  # Create files
  for src,dst in mapping.iteritems():
    seg = dst[:3]
    # Copy the file over to its final partition.
    shutil.copyfile(os.path.join(raw,src),os.path.join(dataset,seg,dst))
    # Copy summary data
    summary = summary_by_doc[src]
    summary['docid'] = dst
    summary_writers[seg].writerow(summary)
    # Write individual lang data
    langid_writers[seg].writerow([dst,summary['pri_lang']])
    if summary['pri_lang'] != summary['sec_lang']:
      langid_writers[seg].writerow([dst,summary['sec_lang']])

  # TODO RUN THIS!!!
  


 
  
if __name__=="__main__":
  #logging.basicConfig(level=logging.DEBUG)
  main()
