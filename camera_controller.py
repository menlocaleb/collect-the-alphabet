import SimpleCV.Camera
import SimpleCV.Color
import SimpleCV.DrawingLayer
import pygame.event
from pygame.locals import USEREVENT
import random
import time

MYEVENT = USEREVENT + 1

def run_camera_controller(camera, debug=False):        

    # TODO sliding window averaging to make more stable?
    last_y = 0
    change_threshold = 2

    while True:
        img = camera.getImage()
        img_dist_from_red = img.colorDistance(SimpleCV.Color.RED)
        img_binary = img_dist_from_red.binarize()
        blobs = img_binary.findBlobs()
        if debug:
            if blobs:
                circlelayer = SimpleCV.DrawingLayer((img_binary.width, img_binary.height))
                blob_center = blobs[-1].centroid()
                # print blob_center[1] / float(img_binary.height)
                circlelayer.circle(blob_center, 10)
                img_binary.addDrawingLayer(circlelayer)
                img_binary.applyLayers()
            img_binary.show()
        else:
            if blobs:
                blob_center = blobs[-1].centroid()
                height_ratio = blob_center[1] / float(img_binary.height)
                if abs(blob_center[1] - last_y) > change_threshold:
                    pygame.event.post(pygame.event.Event(MYEVENT,{'y': height_ratio}))
                    # print 'posted'
                
                last_y = blob_center[1]
        time.sleep(0.01)



if __name__ == '__main__':
    run_camera_controller(SimpleCV.Camera(), debug=True)
