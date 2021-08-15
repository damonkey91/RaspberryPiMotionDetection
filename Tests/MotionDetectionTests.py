import unittest
from MotionDetection import MotionDetection
import os
import io
from PIL import Image


class TestMotionDetection(unittest.TestCase):
    def testDetectedMotionNoPriorImage(self):
        imagePathNoMotion = self.__pathToTestImages(False)
        stream = self.__getImageStream(imagePathNoMotion)

        motionDetector = MotionDetection()
        detectedMotion = motionDetector.detectedMotion(stream)

        self.assertFalse(detectedMotion)

    def testDetectedMotionWithMotionPictures(self):
        imagePathNoMotion = self.__pathToTestImages(False)
        streamNoMotion = self.__getImageStream(imagePathNoMotion)
        imagePathMotion = self.__pathToTestImages(True)
        streamMotion = self.__getImageStream(imagePathMotion)

        motionDetector = MotionDetection()
        detectedMotionFirstImage = motionDetector.detectedMotion(streamNoMotion)
        detectedMotionSecondImage = motionDetector.detectedMotion(streamMotion)

        self.assertFalse(detectedMotionFirstImage)
        self.assertTrue(detectedMotionSecondImage)

    def testDetectedMotionWithSamePicture(self):
        imagePathNoMotion = self.__pathToTestImages(False)
        streamNoMotion = self.__getImageStream(imagePathNoMotion)
        imagePathNoMotion2 = self.__pathToTestImages(False)
        streamNoMotion2 = self.__getImageStream(imagePathNoMotion2)

        motionDetector = MotionDetection()
        detectedMotionFirstImage = motionDetector.detectedMotion(streamNoMotion)
        detectedMotionSecondImage = motionDetector.detectedMotion(streamNoMotion2)

        self.assertFalse(detectedMotionFirstImage)
        self.assertFalse(detectedMotionSecondImage)

    def __pathToTestImages(self, motion: bool):
        imageName = "motion.jpg" if motion else "nomotion.jpg"
        savedFilesDirPath = os.path.join(os.path.dirname(__file__), "TestImages")
        testPictureFilePath = os.path.join(savedFilesDirPath, imageName)
        return testPictureFilePath

    def __getImageStream(self, filePath):
        stream = None
        with Image.open(filePath) as img:
            stream = io.BytesIO()
            img.save(stream, format='JPEG')
        return stream
