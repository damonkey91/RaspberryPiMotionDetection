![Platform](https://img.shields.io/badge/platform-raspberry%20pi-C51A4A.svg)
![Languages](https://img.shields.io/badge/language-python-C51A4A.svg)

# Raspberry pi motion camera with firebase
A small project for me to learn python and raspberry pi. The script starts recording from the pi camera and sends images and videos to firebase when motion is detected.

## Requirements
- Raspberry pi with camera
- Firebase account
- python v3.8.0
- python packages

## Installations
Install python packages
```python
sudo apt-get install python3-picamera
python3 -m pip install Pillow
python3 -m pip install Pyrebase
```

To setup firebase project with pyrebase follow [this tutorial](https://www.youtube.com/watch?v=I1eskLk0exg).

## Thanks to
- [Dave Jones](https://github.com/waveform80) for the [picamera library](https://github.com/waveform80/picamera) and [docs](https://picamera.readthedocs.io)
- [James Childs-Maidment](https://github.com/thisbejim?tab=repositories) and [David Vartanian](https://github.com/davidvartanian) for the pyrebase library
