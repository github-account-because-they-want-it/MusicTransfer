'''
Created on Dec 22, 2014
@author: Mohammed Hamdy
'''

from PySide.QtGui import QMainWindow, QApplication, qApp
from pygame import mixer
from musictransfer.ui.menus import FileMenu, MusicMenu
from musictransfer.ui.dialogs import OpenPlaylistDialog, ChooseOutputFolderDialog, InvalidPlaylistErrorDialog
from musictransfer.ui.tree_view import MusicTreeView
import sys, os.path as path
from musictransfer.exceptions import UnsupportedPlaylistException

class MusicTransfer(QMainWindow):
  
  def __init__(self):
    super(MusicTransfer, self).__init__()
    self._last_used_folder = None
    self._selected_track = None
    self._currently_playing = False
    self._treeview_music = MusicTreeView()
    self._treeview_music.track_changed.connect(self._handleSelectedTrackChanged)
    self._treeview_music.track_deselected.connect(self._handleTrackDeselected)
    self.setCentralWidget(self._treeview_music)
    self.setWindowTitle(self.tr("Music Transfer"))
    self._setupMenubar()
    mixer.init()
    
  def _setupMenubar(self):
    file_menu = FileMenu()
    file_menu.action_open_playlist.triggered.connect(self._handleOpenPlaylist)
    file_menu.action_transfer_playlist.triggered.connect(self._handleTransferPlaylist)
    file_menu.action_exit.triggered.connect(self._exitApp)
    self.menuBar().addMenu(file_menu)
    self._file_menu = file_menu
    # the music menu
    self._music_menu = MusicMenu()
    self.menuBar().addMenu(self._music_menu)
    self._music_menu.action_play_track.triggered.connect(self._handlePlayTrack)
    self._music_menu.action_stop_track.triggered.connect(self._handleStopTrack)
    
  def _handleOpenPlaylist(self):
    open_playlist_dialog = OpenPlaylistDialog(lastPlaylistDir=self._last_used_folder)
    if open_playlist_dialog.exec_():
      playlist = open_playlist_dialog.selectedFiles()[0]
      self._last_used_folder = path.dirname(playlist)
      try:
        self._treeview_music.setPlaylist(playlist)
      except UnsupportedPlaylistException:
        InvalidPlaylistErrorDialog(playlist).exec_()
      else:
        self._file_menu.action_transfer_playlist.setEnabled(True)
  
  def _handleTransferPlaylist(self):
    transfer_playlist_dialog = ChooseOutputFolderDialog(lastPlaylistDir=self._last_used_folder)
    if transfer_playlist_dialog.exec_():
      selected_folder = transfer_playlist_dialog.selectedFiles()[0]
      self._last_used_folder = selected_folder
      self._treeview_music.transferPlaylistTo(selected_folder)
  
  def _handlePlayTrack(self):
    mixer.music.load(self._selected_track)
    mixer.music.play()
    self._music_menu.action_play_track.setEnabled(False)
    self._music_menu.action_stop_track.setEnabled(True)
    
  def _handleStopTrack(self):
    mixer.music.stop()
    self._music_menu.action_play_track.setEnabled(True)
    self._music_menu.action_stop_track.setEnabled(False)
    
  def _handleSelectedTrackChanged(self, selectedPath):
    self._handleStopTrack()
    self._selected_track = selectedPath
    
  def _handleTrackDeselected(self):
    if not self._currently_playing:
      self._music_menu.action_play_track.setEnabled(False)
      self._music_menu.action_stop_track.setEnabled(False)
    self._selected_track = None
  
  def _exitApp(self):
    qApp.exit()
    

if __name__ == "__main__":
  import musictransfer.res
  app = QApplication(sys.argv)
  main = MusicTransfer()
  main.show()
  sys.exit(app.exec_())