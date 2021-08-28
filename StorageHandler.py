import os
import io
from Firestorage import Firebase
from datetime import datetime

class StorageHandler:

  def __init__(self, fireStorage):
    self.fireStorage = fireStorage
    self.filepath = os.path.join(os.path.dirname(__file__), "SavedFiles")

  def createFilename(self, fileStarter: str, filetype: str):
    time = datetime.now()
    filename = fileStarter + "-%04d_%02d_%02d-%02d%02d%02d" % (
      time.year, time.month, time.day, time.hour, time.minute, time.second) + "." + filetype
    fullfilename = os.path.join(self.filepath, filename)
    return fullfilename

  def uploadAndRemoveFile(self, filePath):
    fileName = self.getFilenameFromPath(filePath)
    self.fireStorage.uploadFile(filePath, fileName)
    #self.removeFile(filePath)

  def removeFile(self, filePath):
    os.remove(filePath)

  def getFilenameFromPath(self, filePath):
    return os.path.basename(filePath)

  def write_video(self, stream, sps_header):
    # Write the entire content of the circular buffer to disk. No need to
    # lock the stream here as we're definitely not writing to it
    # simultaneously
    videoBeforeFileName = self.__createFilename("before", "h264")
    with io.open(videoBeforeFileName, 'wb') as output:
      for frame in stream.frames:
        if frame.frame_type == sps_header:
          stream.seek(frame.position)
          break
      while True:
        buf = stream.read1()
        if not buf:
          break
        output.write(buf)
    # Wipe the circular stream once we're done
    stream.seek(0)
    stream.truncate()
    self.uploadAndRemoveFile(videoBeforeFileName)