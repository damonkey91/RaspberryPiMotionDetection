import io
from PIL import Image

class MotionDetection:
    # Threshold      - (how much a pixel has to change by to be marked as "changed")
    # Sensitivity    - (how many changed pixels before capturing an image) needs to be higher if noisy view
    def __init__(self):
        self.threshold = 10
        self.sensitivity = 180
        self.priorImageBuffer = None
        
    def detectedMotion(self, stream: io.BytesIO):
        stream.seek(0)
        if self.priorImageBuffer is None:
            priorImage = Image.open(stream)
            self.priorImageBuffer = priorImage.load()
            stream.close()
            return False
        else:
            currentImage = Image.open(stream)
            currentImageBuffer = currentImage.load()
            detectedMotion = self.__compareImages(currentImageBuffer, self.priorImageBuffer)            
            self.priorImage = currentImage
            stream.close()
            return detectedMotion
        
    def __compareImages(self, currentImageBuffer, priorImageBuffer):
        changedPixels = 0
        for x in range(0, 100):
            # Scan one line of image then check sensitivity for movement
            for y in range(0, 75):
                # Just check green channel as it's the highest quality channel
                pixdiff = abs(priorImageBuffer[x, y][1] - currentImageBuffer[x, y][1])
                if pixdiff > self.threshold:
                    changedPixels += 1
            # Exit before full image scan complete
            if changedPixels > self.sensitivity:
                return True
            
        return False

#------Cirkular stream https://picamera.readthedocs.io/en/release-1.10/recipes2.html#splitting-to-from-a-circular-stream
