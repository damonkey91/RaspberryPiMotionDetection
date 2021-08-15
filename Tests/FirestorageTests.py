import unittest
from Firestorage import Firebase
import os

class TestFirestorage(unittest.TestCase):
    def testInitiateFirestorage(self):
        fireStorage = Firebase()
        rootFirebase = fireStorage.getFirebase()
        fireStorage2 = Firebase()
        rootFirebase2 = fireStorage2.getFirebase()
        self.assertIsNotNone(rootFirebase)
        self.assertIsNotNone(rootFirebase2)

    def testUploadFileToFirestorage(self):
        savedFilesDirPath = os.path.join(os.path.dirname(__file__), os.path.pardir, "SavedFiles")
        testPictureFilePath = os.path.join(savedFilesDirPath, "Picture.py")
        fireStorage = Firebase()
        fireStorage.uploadFile(testPictureFilePath, "Picture2.py")


