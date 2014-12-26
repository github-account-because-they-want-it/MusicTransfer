'''
Created on Dec 23, 2014
@author: Mohammed Hamdy
'''

from os import path

class BasePlaylistReader(object):
  """
  All playlist readers should inherit from this class
  Iteration on subclass objects should return successive track paths.
  The playlist reader should also ensure that the track actually exists on disk
  """
  
  def __init__(self):
    self._returned_tracks = set()
  
  @classmethod
  def isCompatiblePlaylist(cls, playlistPath):
    raise NotImplemented
  
  def __iter__(self):
    raise NotImplemented
  
  def checkTrack(self, trackPath):
    # should be called from next method in subclasses
    if path.exists(trackPath) and not trackPath in self._returned_tracks:
      self._returned_tracks.add(trackPath)
      return True
    return False
  
  def next(self):
    raise NotImplemented
  
