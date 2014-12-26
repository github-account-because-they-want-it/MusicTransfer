'''
Created on Dec 24, 2014
@author: Mohammed Hamdy
'''

from PySide.QtCore import QAbstractItemModel, Qt, QModelIndex
from PySide.QtGui import QPixmap
from .tree_items import RootTreeItem, SongTreeItem
from musictransfer.discovery.playlist_loader import PlaylistLoader
from musictransfer.ui.tree_items import AlbumTreeItem, ArtistTreeItem

class MusicTreeModel(QAbstractItemModel):
  
  def __init__(self, parent=None):
    super(MusicTreeModel, self).__init__(parent)
    self._playlist_loader = PlaylistLoader.getInstance()
    self._root_item = None
    
  def rootItem(self):
    return self._root_item
    
  def setPlaylist(self, playlistPath):
    self._root_item = RootTreeItem()
    playlist_reader = self._playlist_loader.getPlaylistReader(playlistPath)
    for track in playlist_reader:
      self._root_item.appendChild(track)
    self.dataChanged.emit(QModelIndex(), QModelIndex())
      
  def headerData(self, section, orientation, role):
    if role == Qt.DisplayRole and orientation == Qt.Horizontal:
      if section == 0:
        return self.tr("Artist")
      elif section == 1:
        return self.tr("Album")
      elif section == 2:
        return self.tr("Track")
    else:
      return None
    
  def index(self, row, column, parentIndex):
    parent_item = self._getItemAt(parentIndex)
    if isinstance(parent_item, SongTreeItem):
      return QModelIndex()
    child_item = parent_item.child(row)
    return self.createIndex(row, column, child_item)
    
  def parent(self, childIndex):
    if childIndex.isValid():
      child_item  = childIndex.internalPointer()
      parent_item = child_item.parent()
      if parent_item is self._root_item:
        return QModelIndex()
      return self.createIndex(parent_item.childIndex(), 0, parent_item)
    else:
      return QModelIndex()
    
  def rowCount(self, parentIndex):
    return self._getItemAt(parentIndex).childCount()
  
  def columnCount(self, parentIndex):
    return 1
  
  def flags(self, modelIndex):
    if modelIndex.isValid():
      return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsUserCheckable
    else:
      return 0
    
  def data(self, modelIndex, role):
    if modelIndex.isValid():
      item = self._getItemAt(modelIndex)
      if role == Qt.DisplayRole:
        return item.data()
      elif role == Qt.DecorationRole:
        if isinstance(item, SongTreeItem):
          return QPixmap(":track")
        elif isinstance(item, AlbumTreeItem):
          return QPixmap(":album")
        elif isinstance(item, ArtistTreeItem):
          return QPixmap(":artist")
      elif role == Qt.CheckStateRole:
        if item.isChecked():
          return Qt.Checked
        return Qt.Unchecked
    else:
      return self.tr("Playlist") # maybe use the name part of the playlist here 
    
  def setData(self, modelIndex, value, role):
    if role == Qt.EditRole:
      self._getItemAt(modelIndex).setData(value)
      self.dataChanged.emit(modelIndex, modelIndex)
      return True
    elif role == Qt.CheckStateRole:
      self._getItemAt(modelIndex).setChecked(value)
      self.dataChanged.emit(modelIndex, modelIndex)
    return False
  
  def _getItemAt(self, modelIndex):
    if modelIndex.isValid():
      return modelIndex.internalPointer()
    return self._root_item