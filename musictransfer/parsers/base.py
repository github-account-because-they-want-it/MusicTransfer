'''
Created on Dec 23, 2014
@author: Mohammed Hamdy
'''

class BaseTrackParser(object):
  """
  Track parsers read track information from a specific format and also
  update it
  """
  
  unknown_track_count = 0
  
  @classmethod
  def isCompatibleTrack(cls, trackPath):
    raise NotImplemented
  
  def parseTrack(self):
    raise NotImplemented
  
  def updateTrack(self):
    raise NotImplemented
  
  