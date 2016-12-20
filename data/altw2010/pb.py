import progressbar as pb

def get_widget(label):
  return [ label, ' ', pb.Percentage(), ' ', pb.Bar(marker='>',left='[',right=']'), ' ', pb.ETA() ]

class ProgressBar(pb.ProgressBar):
  def __enter__(self):
    self.start()
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.finish()

class ProgressIter(object):
  def __init__(self, sequence, label='Progress'):
    self.seq = iter(sequence)
    self.pb = ProgressBar(widgets=get_widget(label),maxval=len(sequence))
    self.pb.start()
    self.count = 0

  def __iter__(self):
    return self

  def next(self):
    self.count += 1
    try:
      next = self.seq.next()
      self.pb.update(self.count)
      return next
    except StopIteration,e :
      self.pb.finish()
      raise e
    
