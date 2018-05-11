import pygame
import pygame.camera
import time
import datetime

pygame.camera.init()
pygame.camera.list_cameras()
cam = pygame.camera.Camera("/dev/video0", (640, 480))
cam.start()
cam.saveSnapshot('image.jpg')
time.sleep(0.1)  # You might need something higher in the beginning
img = cam.get_image()
pygame.image.save(img, "pygame-{}.jpg".format(datetime.datetime.now()))
cam.stop()
