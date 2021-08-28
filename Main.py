from CameraHandler import CameraHandler
from MotionDetection import MotionDetection
from Firestorage import Firebase
from StorageHandler import StorageHandler

fireStorage = Firebase()
storageHandler = StorageHandler(fireStorage)
motionDetector = MotionDetection()
cameraHandler = CameraHandler(motionDetector, storageHandler)
try:
    cameraHandler.startSurveillance()
except Exception as err:
    print(err)
    #LoggerWrapper.logError('Error in your code = {0}'.format(err))
finally:
    cameraHandler.closeCamera()