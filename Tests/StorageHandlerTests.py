import unittest
from StorageHandler import StorageHandler
import os
from datetime import datetime
from Firestorage import Firebase

class TestStorageHandler(unittest.TestCase):
    def testCreateFilename(self):
        fileStarter = "filestart"
        fileType = "jpeg"

        fireStorage = Firebase()
        storageHandler = StorageHandler(fireStorage)
        path = storageHandler.createFilename(fileStarter, fileType)

        time = datetime.now()
        fileName = fileStarter + "-%04d_%02d_%02d-%02d%02d%02d" % (
            time.year, time.month, time.day, time.hour, time.minute, time.second) + "." + fileType

        endsWith = path.endswith(fileName)
        self.assertTrue(endsWith)

    def testGetFilenameFromPath(self):
        fileStarter = "filestart"
        fileType = "jpeg"

        fireStorage = Firebase()
        storageHandler = StorageHandler(fireStorage)
        path = storageHandler.createFilename(fileStarter, fileType)

        time = datetime.now()
        fileName = fileStarter + "-%04d_%02d_%02d-%02d%02d%02d" % (
            time.year, time.month, time.day, time.hour, time.minute, time.second) + "." + fileType

        extractedFileName = storageHandler.getFilenameFromPath(path)

        self.assertEqual(fileName, extractedFileName)

    def testRemoveFile(self):
        filepath = os.path.join(os.path.dirname(__file__), "TestImages")
        fullFilePath = os.path.join(filepath, "testfile")
        open(fullFilePath, 'a').close()

        wasFileCreated = os.path.exists(fullFilePath)

        fireStorage = Firebase()
        storageHandler = StorageHandler(fireStorage)
        storageHandler.removeFile(fullFilePath)

        wasFileDeleted = not os.path.exists(fullFilePath)

        self.assertTrue(wasFileCreated)
        self.assertTrue(wasFileDeleted)

    def testUploadFile(self):
        filepath = os.path.join(os.path.dirname(__file__), "TestImages")
        fullFilePath = os.path.join(filepath, "testUploadFile.txt")
        open(fullFilePath, 'a').close()

        fireStorage = Firebase()
        storageHandler = StorageHandler(fireStorage)
        storageHandler.uploadAndRemoveFile(fullFilePath)

