import datetime
import time

import pygame
import pygame.camera

pygame.camera.init()
pygame.camera.list_cameras()
cam = pygame.camera.Camera("/dev/video0", (640, 480))
cam.start()
cam.saveSnapshot('image.jpg')
time.sleep(0.1)  # You might need something higher in the beginning
img = cam.get_image()
pygame.image.save(img, f"pygame-{datetime.datetime.now()}.jpg")
cam.stop()
