import picamera
import os
import io
import time

class CameraHandler:
    __camera = picamera.PiCamera()

    # filepath       - location of folder to save photos
    # filenamePrefix - string that prefixes the file name for easier identification of files.
    def __init__(self, motionDetection, storage):
        self.getCamera().resolution = (640, 480)
        self.storage = storage
        self.motionDetector = motionDetection
        self.fileType = "jpg"
        self.filepath = "/home/pi/images/"
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
                    # As soon as we detect motion, split the recording to
                    # record the frames "after" motion
                    camera.split_recording('after.h264')
                    # Write the 10 seconds "before" motion to disk as well
                    self.write_video(stream)
                    # Wait until motion is no longer detected, then split
                    # recording back to the in-memory circular buffer
                    while self.motionDetector.detectedMotion(self.getMotionDetectionImage()):
                        camera.wait_recording(1)
                    print('Motion stopped!')
                    camera.split_recording(stream)
        except Exception as err:
            #LoggerWrapper.logError('Error in your code = {0}'.format(err))
            pass
        finally:
            camera.stop_recording()

    def write_video(self, stream):
        # Write the entire content of the circular buffer to disk. No need to
        # lock the stream here as we're definitely not writing to it
        # simultaneously
        with io.open('before.h264', 'wb') as output:
            for frame in stream.frames:
                if frame.frame_type == picamera.PiVideoFrameType.sps_header:
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

    def captureImage(self):
        camera = self.getCamera()
        time = datetime.now()
        filename = filenamePrefix + "-%04d_%02d_%02d-%02d%02d%02d" % (
            time.year, time.month, time.day, time.hour, time.minute, time.second) + "." + fileType
        fullfilename = filepath + filename
        camera.capture(fullfilename, format='jpeg', use_video_port=True)
        camera.wait_recording(60)
    
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
