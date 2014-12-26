'''
Created on Dec 24, 2014
@author: Mohammed Hamdy
'''

from musictransfer.discovery.track_parser import TrackParser
from musictransfer.exceptions import UnsupportedTrackException

class RootTreeItem(object):
  
  def __init__(self):
    self._parent = None
    self._children = [] # children here are artists
    self._checked = True # used in the view to select songs, artists and albums
    
  def parent(self):
    return self._parent
  
  def isChecked(self):
    return self._checked
  
  def setChecked(self, state):
    self._checked = state
  
  def child(self, childIndex):
    return self._children[childIndex]
  
  def children(self):
    return self._children
  
  def childIndex(self):
    if self._parent is None:
      return 0
    return self._parent._children.index(self)
  
  def appendChild(self, trackPath):
    """
    This can lead to 3 outcomes:
      1- Either the artist associated with the track doesn't exist yet, and so I should
         create a new artist, album and track tree items
      2- The artist exists but a new album. A new album item and track item should be created
      3- The artist exists and album but a new track. So I should only add the track to the existing artist.
    """
    try:
      track_parser = TrackParser.getInstance().getCompatibleParser(trackPath)
    except UnsupportedTrackException as exc:
      print(exc)
      return
    track_data = track_parser.parseTrack()
    for artist_item in self._children:
      if artist_item.data() == track_data["artist"]:
        # artist already exists. add a new song (album?) to it
        artist_item.appendChild(trackPath)
        break
    else:
      # create a new artist and add the track to it
      new_artist_item = ArtistTreeItem(self, track_data["artist"])
      new_artist_item.appendChild(trackPath)
      self._children.append(new_artist_item)
    
  def hasArtist(self, artistName):
    for artist_item in self._children:
      if artist_item.data() == artist_item:
        return True
    else:
      return False
    
  def appendChildrenToArtist(self, artistName, childAlbumItems):
    for artist_item in self._children:
      if artist_item.data() == artistName:
        for album_item in childAlbumItems:
          artist_item.appendAlbumTreeItem(album_item)
        break
          
  def removeChild(self, child):
    self._children.remove(child)
    
  def childCount(self):
    return len(self._children)
    
class SongTreeItem(RootTreeItem):
  
  def __init__(self, parentAlbumItem, trackPath):
    super(SongTreeItem, self).__init__()
    self.track_path = trackPath
    self._parent = parentAlbumItem
    track_parser = TrackParser.getInstance()
    self._track_parser = track_parser.getCompatibleParser(trackPath)
    self._data = self._track_parser.parseTrack()["title"] # the track title is the data
    
  def parent(self):
    return self._parent
  
  def data(self):
    return self._data
  
  def setData(self, newTrackTitle):
    self._track_parser.updateTrack(title=newTrackTitle)
    self._data = newTrackTitle
    
  def updateAlbum(self, newAlbumName):
    self._track_parser.updateTrack(album=newAlbumName)
    
  def updateArtist(self, newArtistName):
    self._track_parser.updateTrack(artist=newArtistName)
    
  def childCount(self):
    return 0
    
  def __str__(self):
    return "<SongTreeItem {}>".format(self._data)
  
class AlbumTreeItem(RootTreeItem):
  
  def __init__(self, parentArtistItem, albumName):
    super(AlbumTreeItem, self).__init__()
    self._parent = parentArtistItem
    self._data = albumName
    self._children = []
    
    
  def appendChild(self, childTrack):
    self._children.append(SongTreeItem(self, childTrack))
    
  def appendSongTreeItem(self, songTreeItem):
    # called when pre-existing song tree items are relocated to this album
    self._children.append(songTreeItem)
    
  def removeChild(self, childIndex):
    self._children.pop(childIndex)
    
  def setData(self, newAlbumName):
    for child in self._children:
      child.updateAlbum(newAlbumName)
    # if the new album name matches an existing album for the same artist, all child tracks
    # should be moved to that album
    if self._parent.hasAlbum(newAlbumName):
      self._parent.appendChildrenToAlbum(newAlbumName, self._children)
      self._parent.removeChild(self)
    else:
      self._data = newAlbumName
      
  def setChecked(self, state):
    RootTreeItem.setChecked(self, state)
    for song_item in self._children:
      song_item.setChecked(state)
      
  def updateArtist(self, newAritstName):
    for song_item in self._children:
      song_item.updateArtist(newAritstName)
    
  def data(self):
    return self._data
  
  def __str__(self):
    return "<AlbumTreeItem {}>".format(self._data)
  
class ArtistTreeItem(RootTreeItem):
  
  def __init__(self, rootTreeItem, artistName):
    super(ArtistTreeItem, self).__init__()
    self._parent = rootTreeItem
    self._data = artistName
    self._children = [] # children are albums
    
  def appendChild(self, trackPath):
    # if an album for this track already exists, just append a song item to it.
    # otherwise, create an album and a song item
    track_parser = TrackParser.getInstance().getCompatibleParser(trackPath)
    track_data = track_parser.parseTrack()
    if self.hasAlbum(track_data["album"]):
      for album_item in self._children:
        if album_item.data() == track_data["album"]:
          album_item.appendChild(trackPath)
    else:
      new_album_item = AlbumTreeItem(self, track_data["album"])
      new_album_item.appendChild(trackPath)
      self._children.append(new_album_item)
    
  def appendAlbumTreeItem(self, albumTreeItem):
    # called when relocating a pre-existing album to this artist item
    self._children.append(albumTreeItem)
  
  def hasAlbum(self, albumName):
    for album_item in self._children:
      if album_item.data() == albumName:
        return True
    else:
      return False
    
  def data(self):
    return self._data
  
  def setData(self, newArtistName):
    for album_item in self._children:
      album_item.updateArtist(newArtistName)
    # if the new artist name matches an existing artist, all child albums should be moved to that artist
    if self._parent.hasArtist(newArtistName):
      self._parent.appendChildrenToArtist(newArtistName, self._children)
      self._parent.removeChild(self)
    self._data = newArtistName
    
  def setChecked(self, state):
    RootTreeItem.setChecked(self, state)
    for album_item in self._children:
      album_item.setChecked(state)
  
  def appendChildrenToAlbum(self, albumName, children):
    for album_item in self._children:
      if album_item.data() == album_item:
        for child in children:
          album_item.appendSongTreeItem(child)
  
  def removeChild(self, childAlbum):
    self._children.remove(childAlbum)
    
  def __str__(self):
    return "<ArtistTreeItem {}>".format(self._data)