import fastf1 as ff
from fastf1.plotting import *
from matplotlib import pyplot as plt

class Track():
  def __init__(self, session, circuit):
    self.session = session
    self.circuit = circuit
