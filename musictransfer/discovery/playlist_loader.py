'''
Created on Dec 23, 2014
@author: Mohammed Hamdy
'''

from os import path
from musictransfer.playlist_readers.base import BasePlaylistReader
from musictransfer.util import parseSubclasses
from musictransfer.exceptions import UnsupportedPlaylistException

class PlaylistLoader(object):
  """
  Searches for subclasses of BasePlaylistReader in musictransfer.playlist_readers package
  and makes them available to get a compatible reader for a playlist type.
  """
  
  _instance = None
  
  @classmethod
  def getInstance(cls):
    """
    There's no reason to create multiple instances of this class so it's a Singleton
    """
    if cls._instance is None:
      cls._instance = PlaylistLoader()
    return cls._instance
  
  def __init__(self):
    readers_package = "musictransfer.playlist_readers"
    self._playlist_reader_classes = parseSubclasses(readers_package, BasePlaylistReader)
    
  def getPlaylistReader(self, playlistPath):
    for playlist_reader_cls in self._playlist_reader_classes:
      if playlist_reader_cls.isCompatiblePlaylist(playlistPath):
        return playlist_reader_cls(playlistPath)
    else:
      raise UnsupportedPlaylistException("No compatible reader found for playlist : {}".format(playlistPath))
    