import fastf1 as ff
from fastf1.plotting import *
from matplotlib import pyplot as plt
from Track import *

class SubTrack(Track):
  def __init__(self, index):
    Track.__init__(self) # super().__init__()
    self.index = index
