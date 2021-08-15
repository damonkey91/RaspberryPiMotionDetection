from CameraHandler import CameraHandler
from MotionDetection import MotionDetection
from Firestorage import Firebase

fireStorage = Firebase()
motionDetector = MotionDetection()
cameraHandler = CameraHandler(motionDetector, fireStorage)
try:
    cameraHandler.startSurveillance()
except Exception as err:
    LoggerWrapper.logError('Error in your code = {0}'.format(err))
finally:
    cameraHandler.closeCamera()