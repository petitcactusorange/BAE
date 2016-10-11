import ROOT as r
from module import module
from math import *
print 'hello'
class cut(module):

  def __init__(self,var,boolean,threshold):
    self.name = 'add_rest_frame_vars'
    self.requiredBranches = [var]

  def run(self,t):
    value = t.GetLeaf(var).GetValue()
    if boolean is ">" and value < threshold:
      return False
    if boolean is "<" and value > threshold:
      return False
    return True
  


