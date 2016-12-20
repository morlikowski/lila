from build import build

PARAMS = {
  'outdir':"wikipedia-multi-test",
  'exclude':[],
  'langs':'selected_langs',
  'prior':'uniform',
  'input':'docs_available',
  }

PARTS = [
  ('docsMR', 50, 1, ),
  ('docsME', 10, 1, ),
  ('docsUR1', 10, 1, ),
  ('docsUR2', 10, 2, ),
  ('docsUR3', 10, 3, ),
  ('docsUR4', 10, 4, ),
  ('docsUR5', 10, 5, ),
  ('docsUE1', 2, 1, ),
  ('docsUE2', 2, 2, ),
  ('docsUE3', 2, 3, ),
  ('docsUE4', 2, 4, ),
  ('docsUE5', 2, 5, ),
  ]

if __name__ == "__main__":
  build(PARTS, PARAMS)
