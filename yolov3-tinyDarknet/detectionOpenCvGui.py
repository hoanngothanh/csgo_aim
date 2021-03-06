import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
import mss
import pyautogui
import time
import keyboard
import constants as consts
import logging
from datetime import datetime
pyautogui.FAILSAFE = False
monitor = {"top": 80, "left": 0, "width": consts.width, "height": consts.height}
sct = mss.mss()
# Load names of classes
try:
    classes = None
    with open(consts.classesFile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    # Give the configuration and weight files for the model and load the network using them.
    net = cv.dnn.readNetFromDarknet(consts.modelConfiguration, consts.modelWeights)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
except:
    logging.info(str(datetime.now()) + " Failed to initialize the model")
else:
    logging.info(str(datetime.now()) + " Model is initialized")
# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Draw the predicted bounding box
def drawPred(classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)
    
    label = '%.2f' % conf
        
    # Get the label for the class name and its confidence
    print(classId)
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    #Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)
def Shoot(mid_x, mid_y):
  pyautogui.moveTo(mid_x,mid_y+50)
  #pyautogui.click()
# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > consts.confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, consts.confThreshold, consts.nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        #Comment this out if you want to see boxes 
        if classIds[i] not in consts.friendlyTeam:
            Shoot(center_x, center_y)
        drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
# Process inputs
winName = 'CSGO ObjectDetection'
cv.namedWindow(winName, cv.WINDOW_NORMAL)


while True:
    
    # get frame from the video
    
    image_np = np.array(sct.grab(monitor))
      # To get real color we do this:
    frame = cv.cvtColor(image_np, cv.COLOR_BGR2RGB)

    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    # Create a 4D blob from a frame.
    blob = cv.dnn.blobFromImage(frame, 1/255, (consts.inpWidth, consts.inpHeight), [0,0,0], 1, crop=False)

    net.setInput(blob)

    # Runs the forward pass to get output of the output layers
    outs = net.forward(getOutputsNames(net))

    # Remove the bounding boxes with low confidence
    postprocess(frame, outs)
    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))


    cv.imshow(winName, frame)
    
    if cv.waitKey(25) & 0xFF == ord("q"):
        cv.destroyAllWindows()
        break