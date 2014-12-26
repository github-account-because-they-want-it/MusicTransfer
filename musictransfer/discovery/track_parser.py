'''
Created on Dec 23, 2014
@author: Mohammed Hamdy
'''

from os import path
from musictransfer.parsers.base import BaseTrackParser
from musictransfer.util import parseSubclasses
from musictransfer.exceptions import UnsupportedTrackException

class TrackParser(object):
  """
  A playlist can contain any type of track; mp3, aac, etc. So for each playlist track,
  this class helps find a suitable track parser, if there's one implemented.
  """
  
  _instance = None
  
  @classmethod
  def getInstance(cls):
    if cls._instance is None:
      cls._instance = TrackParser()
    return cls._instance
  
  def __init__(self):
    parsers_package = "musictransfer.parsers"
    self._track_parsers = parseSubclasses(parsers_package, BaseTrackParser)
    
  def getCompatibleParser(self, trackPath):
    for track_parser_cls in self._track_parsers:
      if track_parser_cls.isCompatibleTrack(trackPath):
        return track_parser_cls(trackPath)
    else:
      raise UnsupportedTrackException("Couldn't find parser for track : {}".format(trackPath))