class ConfusionMatrix:
  _classes = []
  _matrix = []
  _c_len = []
  def __init__(self, classes):
    self._classes = classes
    self._c_len = len(classes)
    self._matrix = [[0 for c in range(self._c_len)] for r in range(self._c_len)]

  def set(self, r, c):
    self._matrix[self._classes.index(r)][self._classes.index(c)] += 1

  def accuracy(self):
    c = self._matrix
    return (c[0][0]+c[1][1])/float(sum(c[0])+sum(c[1]))

  def recall(self):
    c = self._matrix
    return (c[1][1]/float(c[1][1]+c[1][0]))
  
  def precision(self):
    c = self._matrix
    return (c[1][1]/float(c[1][1]+c[0][1]))
  
  def fmeasure(self):
    c = self._matrix
    p = self.precision()
    r = self.recall()
    return 2*(p*r)/(p+r)

  def __str__(self):
    string = ""
    for r in range(len(self._matrix)):
      row = str(self._classes[r])
      for c in range(len(self._matrix[r])):
        row += " | "+str(self._matrix[r][c])
      string += row + "\n"
      string += "-"*len(row) + "\n"
    return string
  
class BasicTestsetEvaluator:
  # Confusion matrix
  cmatrix = []
  classes = []
  c_len = 0

  def __init__(self, classes, testset, class_index):
    c_len = len(classes)
    self.cmatrix = [[0 for col in range(c_len)] for row in range(c_len)]
    self.classes = classes
    self.c_len = c_len
    self.testset = testset
    self.class_index = class_index

  def evaluate(self, classifier):
    print "Evaluating %s with test set" % (classifier,)
    cmatrix = ConfusionMatrix(self.classes)
    if len(self.testset) > 0:
      indices = range(len(self.testset[0]))
      indices.remove(self.class_index)
      for instance in self.testset:
        cmatrix.set( \
          instance[self.class_index], \
          classifier.classify(instance[indices])
        )
    return cmatrix

class MultipleEvaluator:
  _evaluator = None

  def __init__(self, evaluator):
    self._evaluator = evaluator

  def evaluate(self, classifiers):
    l = len(classifiers)
    results = [None for c in range(l)]
    for c in range(l):
      results[c] = self._evaluator.evaluate(classifiers[c])
    return results
