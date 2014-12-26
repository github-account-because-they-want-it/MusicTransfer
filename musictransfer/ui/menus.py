'''
Created on Dec 23, 2014
@author: Mohammed Hamdy
'''

from PySide.QtGui import QMenu, QAction, QKeySequence

class FileMenu(QMenu):
  
  def __init__(self, parent=None):
    super(FileMenu, self).__init__(parent)
    self.setTitle(self.tr("File"))
    self.action_open_playlist = QAction(self.tr("Open playlist ..."), None)
    self.action_open_playlist.setShortcut(QKeySequence("Ctrl+O"))
    self.action_transfer_playlist = QAction(self.tr("&Transfer playlist ..."), None)
    self.action_transfer_playlist.setShortcut(QKeySequence("Ctrl+T"))
    self.action_transfer_playlist.setEnabled(False) # by default, until a playlist is opened
    self.action_exit = QAction(self.tr("Exit"), None)
    self.action_exit.setShortcut(QKeySequence("Ctrl+Q"))
    self.addAction(self.action_open_playlist)
    self.addAction(self.action_transfer_playlist)
    self.addAction(self.action_exit)
    
class MusicMenu(QMenu):
  
  def __init__(self, parent=None):
    super(MusicMenu, self).__init__(parent)
    self.setTitle(self.tr("Music"))
    self.action_play_track = QAction(self.tr("Play"), None)
    self.action_play_track.setShortcut(QKeySequence("Ctrl+P"))
    self.action_play_track.setEnabled(False)
    self.action_stop_track = QAction(self.tr("Stop"), None)
    self.action_stop_track.setShortcut(self.action_play_track.shortcut())
    self.action_stop_track.setEnabled(False)
    self.addAction(self.action_play_track)
    self.addAction(self.action_stop_track)