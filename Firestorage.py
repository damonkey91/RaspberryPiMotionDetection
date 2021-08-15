import pyrebase
import ConstantsGitIgnore

class Firebase:
  __firebase = None

  def __init__(self):
    if (Firebase.__firebase is None):
      Firebase.__firebase = pyrebase.initialize_app(ConstantsGitIgnore.firebaseConfig)

  def getFirebase(self):
    if(Firebase.__firebase is None):
      Firebase.__firebase = pyrebase.initialize_app(ConstantsGitIgnore.firebaseConfig)

    return Firebase.__firebase

  def uploadFile(self, filePath, filePathInStorage):
    self.getFirebase().storage().child(filePathInStorage).put(filePath)
