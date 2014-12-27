'''
Created on Dec 23, 2014
@author: Mohammed Hamdy
'''

from PySide.QtGui import QFileDialog, QMessageBox, QProgressDialog
from os import path

class OpenPlaylistDialog(QFileDialog):
  
  def __init__(self, parent=None, lastPlaylistDir=None):
    super(OpenPlaylistDialog, self).__init__(parent, '',
      lastPlaylistDir if lastPlaylistDir is not None else '.')
    self.setWindowTitle(self.tr("Choose Playlist File"))
    self.setFileMode(QFileDialog.ExistingFile)
  
  
class ChooseOutputFolderDialog(QFileDialog):
  
  def __init__(self, parent=None, lastPlaylistDir=None):
    super(ChooseOutputFolderDialog, self).__init__(parent, '',
      lastPlaylistDir if lastPlaylistDir is not None else '.')
    self.setWindowTitle(self.tr("Choose Output Folder"),)
    self.setFileMode(QFileDialog.Directory)
    
    
class InvalidPlaylistErrorDialog(QMessageBox):
  
  def __init__(self, playlistFile, parent=None):
    super(InvalidPlaylistErrorDialog, self).__init__(parent)
    self.setText(self.tr("No compatible reader for playlist <b>{}</b>".format(playlistFile)))
    self.setWindowTitle(self.tr("Error"))
    self.setIcon(QMessageBox.Critical)
    self.setStandardButtons(QMessageBox.Ok)
    self.setDefaultButton(QMessageBox.Ok)
    

class TransferProgressDialog(QProgressDialog):
  
  def __init__(self, parent=None):
    super(TransferProgressDialog, self).__init__(parent)
    self.setWindowTitle(self.tr("Transferring playlist ..."))
    self.setMinimum(0)
    self.setMaximum(0)
    
  def setCurrentTrack(self, trackPath):
    filename = path.basename(trackPath)
    self.setLabelText(u"Copying {} ...".format(filename))