'''
Created on Dec 23, 2014
@author: Mohammed Hamdy
'''

import os.path as path
from mutagen.easyid3 import EasyID3
from mutagen.id3._util import MutagenError
from .base import BaseTrackParser

class MP3TrackParser(BaseTrackParser):
  
  def __init__(self, trackPath):
    self._track_path = trackPath
    try:
      self._track_id3 = EasyID3(trackPath)
    except MutagenError:
      self._track_id3 = {"title":"Unknown Track {}".format(self.unknown_track_count),
                         "artist":"Unknown Artist", "album":"Unknown Album"}
      self.unknown_track_count += 1
    
  def parseTrack(self):
    return {"title":self._track_id3.get("title", ['Unknown Title'])[0], 
            "artist":self._track_id3.get("performer", ['Unknown Artist'])[0],
            "album":self._track_id3.get("album", ['Unknown Album'])[0]}
    
  def updateTrack(self, **kwargs):
    self._track_id3.update(kwargs)
    self._track_id3.save()
  
  @classmethod
  def isCompatibleTrack(cls, trackPath):
    track_extension = path.splitext(trackPath)[1].lower()
    return track_extension == ".mp3"