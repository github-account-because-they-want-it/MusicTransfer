'''
Created on Dec 23, 2014
@author: Mohammed Hamdy
'''

import os.path as path
import codecs
from .base import BasePlaylistReader

class M3UPlaylistReader(BasePlaylistReader):
  
  def __init__(self, playlistFile):
    super(M3UPlaylistReader, self).__init__()
    self._playlist_file = playlistFile
    self._file_reader = None
  
  @classmethod
  def isCompatiblePlaylist(cls, playlistPath):
    playlist_extension = path.splitext(playlistPath)[1].lower()
    return playlist_extension == ".m3u" or playlist_extension == ".m3u8" # maybe also m3u8
  
  def __iter__(self):
    self._file_reader = codecs.open(self._playlist_file, mode="r", encoding="utf-8")
    return self
  
  def next(self):
    for line in self._file_reader:
      line = line.strip()
      if line.startswith('#') or not self.checkTrack(line): # a comment line
        continue
      return line
    else:
      raise StopIteration