'''
Created on Dec 24, 2014
@author: Mohammed Hamdy
'''

from shutil import copy
import os, sys
from os import path
from PySide.QtGui import QTreeView, QApplication
from PySide.QtCore import Signal
from .tree_model import MusicTreeModel
from .dialogs import TransferProgressDialog
from .tree_items import SongTreeItem

class MusicTreeView(QTreeView):
  
  track_changed = Signal(str)
  track_deselected = Signal() # when no tracks are currently selected. Other selections might have been made, like an album or artist
  
  
  def __init__(self, parent=None):
    super(MusicTreeView, self).__init__(parent)
    self.setSelectionMode(self.SingleSelection)
  
  def selectionChanged(self, selected, deselected):
    selected_indexes = selected.indexes()
    if selected_indexes:
      selected_item = selected_indexes[0].internalPointer()
      if isinstance(selected_item, SongTreeItem):
        self.track_changed.emit(selected_item.track_path)
      else:
        self.track_deselected.emit() # album or artist selected
    else:
      self.track_deselected.emit() # the tree view maybe lost focus
    
  def setPlaylist(self, playlistPath):
    music_model = MusicTreeModel()
    music_model.setPlaylist(playlistPath)
    self.setModel(music_model)
    
  def transferPlaylistTo(self, outputDir):
    music_model = self.model()
    root_item = music_model.rootItem()
    progress_dialog = TransferProgressDialog()
    progress_dialog.show()
    for artist_item in root_item.children():
      if not artist_item.isChecked(): continue
      for album_item in artist_item.children():
        if not album_item.isChecked(): continue
        for song_item in album_item.children():
          if progress_dialog.wasCanceled():
            return
          if not song_item.isChecked(): continue
          progress_dialog.setCurrentTrack(song_item.track_path)
          QApplication.processEvents() # update progress dialog message
          output_dir = path.join(outputDir, artist_item.data().strip(), album_item.data().strip()) #dir/Breaking Benjamin/Dear Agony/
          if not path.exists(output_dir):
            os.makedirs(output_dir)
          if not path.exists(path.join(output_dir, path.basename(song_item.track_path))):
            copy(song_item.track_path, output_dir)
    progress_dialog.hide()