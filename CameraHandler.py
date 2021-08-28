import picamera
import io

class CameraHandler:
    __camera = picamera.PiCamera()

    # filepath       - location of folder to save photos
    # filenamePrefix - string that prefixes the file name for easier identification of files.
    def __init__(self, motionDetection, storageHandler):
        self.getCamera().resolution = (640, 480)
        self.storageHandler = storageHandler
        self.motionDetector = motionDetection
        self.fileType = "jpeg"
        self.filenamePrefix = "window"

    def startSurveillance(self):
        camera = self.getCamera()
        stream = picamera.PiCameraCircularIO(camera, seconds=10)
        camera.start_recording(stream, format='h264')
        try:
            while True:
                camera.wait_recording(1)
                imageStream = self.getMotionDetectionImage()
                detectedMotion = self.motionDetector.detectedMotion(imageStream)

                if detectedMotion:
                    print('Motion detected!')
                    self.captureImage()
                    # As soon as we detect motion, split the recording to
                    # record the frames "after" motion
                    videoAfterFilePath = self.storageHandler.createFilename("after", "h264")
                    camera.split_recording(videoAfterFilePath)
                    # Write the 10 seconds "before" motion to disk as well
                    self.storageHandler.write_video(stream, picamera.PiVideoFrameType.sps_header)
                    # Wait until motion is no longer detected, then split
                    # recording back to the in-memory circular buffer
                    while self.motionDetector.detectedMotion(self.getMotionDetectionImage()):
                        self.captureImage()
                        camera.wait_recording(1)
                    print('Motion stopped!')
                    camera.split_recording(stream)
                    self.storageHandler.uploadAndRemoveFile(videoAfterFilePath)
        except Exception as err:
            print(err)
            #LoggerWrapper.logError('Error in your code = {0}'.format(err))
            pass
        finally:
            camera.stop_recording()

    def captureImage(self):
        camera = self.getCamera()
        fullfilename = self.storageHandler.createFilename(self.filenamePrefix, self.fileType)
        camera.capture(fullfilename, format='jpeg', use_video_port=True)
        self.storageHandler.uploadAndRemoveFile(fullfilename)

    def startRecording(self):
        pass
    
    def stopRecording(self):
        #stop recording
        #upload file to firestore
        #remove file from disk  
        pass

    def closeCamera(self):
        self.getCamera().close()
    
    def getMotionDetectionImage(self):
        stream = io.BytesIO()
        self.getCamera().capture(stream, format='jpeg', use_video_port=True)
        return stream

    def getCamera(self):
        return CameraHandler.__camera