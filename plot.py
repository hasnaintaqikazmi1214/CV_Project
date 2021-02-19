#!/usr/bin/env python

import cv2
import numpy as np


# Function to draw Bird Eye View for region of interest(ROI). Red, Yellow, Green points represents risk to human.
# Red: High Risk
# Yellow: Low Risk
# Green: No Risk
def bird_eye_view(frame, distances_mat, bottom_points, scale_w, scale_h):
    h = frame.shape[0]
    w = frame.shape[1]

    red = (0, 0, 255)
    green = (0, 255, 0)
    yellow = (0, 255, 255)
    white = (200, 200, 200)

    blank_image = np.zeros((int(h * scale_h), int(w * scale_w), 3), np.uint8)
    blank_image[:] = white
    warped_pts = []
    r = []
    g = []
    y = []

    # Below three For loop can be replaced by one for loop, to shorten the time
    for i in range(len(distances_mat)):

        if distances_mat[i][2] == 0:
            if (distances_mat[i][0] not in r) and (distances_mat[i][0] not in g) and (distances_mat[i][0] not in y):
                r.append(distances_mat[i][0])
            if (distances_mat[i][1] not in r) and (distances_mat[i][1] not in g) and (distances_mat[i][1] not in y):
                r.append(distances_mat[i][1])

            blank_image = cv2.line(blank_image,
                                   (int(distances_mat[i][0][0] * scale_w), int(distances_mat[i][0][1] * scale_h)),
                                   (int(distances_mat[i][1][0] * scale_w), int(distances_mat[i][1][1] * scale_h)), red,
                                   2)

    for i in range(len(distances_mat)):

        if distances_mat[i][2] == 1:
            if (distances_mat[i][0] not in r) and (distances_mat[i][0] not in g) and (distances_mat[i][0] not in y):
                y.append(distances_mat[i][0])
            if (distances_mat[i][1] not in r) and (distances_mat[i][1] not in g) and (distances_mat[i][1] not in y):
                y.append(distances_mat[i][1])

            blank_image = cv2.line(blank_image,
                                   (int(distances_mat[i][0][0] * scale_w), int(distances_mat[i][0][1] * scale_h)),
                                   (int(distances_mat[i][1][0] * scale_w), int(distances_mat[i][1][1] * scale_h)),
                                   yellow, 2)

    for i in range(len(distances_mat)):

        if distances_mat[i][2] == 2:
            if (distances_mat[i][0] not in r) and (distances_mat[i][0] not in g) and (distances_mat[i][0] not in y):
                g.append(distances_mat[i][0])
            if (distances_mat[i][1] not in r) and (distances_mat[i][1] not in g) and (distances_mat[i][1] not in y):
                g.append(distances_mat[i][1])

    for i in bottom_points:
        blank_image = cv2.circle(blank_image, (int(i[0] * scale_w), int(i[1] * scale_h)), 5, green, 10)
    for i in y:
        blank_image = cv2.circle(blank_image, (int(i[0] * scale_w), int(i[1] * scale_h)), 5, yellow, 10)
    for i in r:
        blank_image = cv2.circle(blank_image, (int(i[0] * scale_w), int(i[1] * scale_h)), 5, red, 10)

    return blank_image


# Function to draw bounding boxes according to risk factor for humans in a frame and draw lines between
# boxes according to risk factor between two humans.
# Red: High Risk
# Yellow: Low Risk
# Green: No Risk 
def social_distancing_view(frame, distances_mat, boxes):
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    red = (0, 0, 255)
    green = (0, 255, 0)
    yellow = (0, 255, 255)
    color = green
    for i in range(len(boxes)):
        x, y, w, h = boxes[i][:]
        frame = cv2.rectangle(frame, (x, y), (w, h), green, 2)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        # for x, y, w, h in face:
        #     img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        #     img[y:y + h, x:x + w] = cv2.medianBlur(img[y:y + h, x:x + w], 35)
        # roi = frame[y:y + h, x:x + w]
        # blur = cv2.GaussianBlur(roi, (5, 5), 0)
        # frame[y:y + h, x:x + w] = blur

    for i in range(len(distances_mat)):

        per1 = distances_mat[i][0]
        per2 = distances_mat[i][1]
        closeness = distances_mat[i][2]

        if closeness == 1:
            x, y, w, h = per1[:]
            frame = cv2.rectangle(frame, (x, y), (w, h), yellow, 2)

            # roi = frame[y:y + h, x:x + w]
            # blur = cv2.GaussianBlur(roi, (5, 5), 0)
            # frame[y:y + h, x:x + w] = blur

            x1, y1, w1, h1 = per2[:]
            frame = cv2.rectangle(frame, (x1, y1), (w1, h1), yellow, 2)
            frame = cv2.line(frame, (int(x + (w - x) / 2), int(y + (h - y) / 2)),
                             (int(x1 + (w1 - x1) / 2), int(y1 + (h1 - y1) / 2)), red, 2)

            # roi = frame[y1:y1 + h1, x1:x1 + w1]
            # blur = cv2.GaussianBlur(roi, (5, 5), 0)
            # frame[y1:y1 + h1, x1:x1 + w1] = blur

            # mistake, change red to yellow
            color = yellow
    for i in range(len(distances_mat)):

        per1 = distances_mat[i][0]
        per2 = distances_mat[i][1]
        closeness = distances_mat[i][2]

        if closeness == 0:
            x, y, w, h = per1[:]
            frame = cv2.rectangle(frame, (x, y), (w, h), red, 2)

            # roi = frame[y:y + h, x:x + w]
            # blur = cv2.GaussianBlur(roi, (5, 5), 0)
            # frame[y:y + h, x:x + w] = blur

            x1, y1, w1, h1 = per2[:]
            frame = cv2.rectangle(frame, (x1, y1), (w1, h1), red, 2)
            color = red
            frame = cv2.line(frame, (int(x + (w - x) / 2), int(y + (h - y) / 2)),
                             (int(x1 + (w1 - x1) / 2), int(y1 + (h1 - y1) / 2)), red, 2)
            # roi = frame[y1:y1 + h1, x1:x1 + w1]
            # blur = cv2.GaussianBlur(roi, (5, 5), 0)
            # frame[y1:y1 + h1, x1:x1 + w1] = blur

    pad = np.full((140, frame.shape[1], 3), [110, 110, 100], dtype=np.uint8)
    # if x1.exists() and y1.exists() and h1.exists() and w1.exists():
    #     roi = frame[y1:y1 + h1, x1:x1 + w1]
    #     blur = anonymize_face_simple(roi, factor=3.0)
    #     # blur = cv2.GaussianBlur(roi, (30, 30), 0)
    #     frame[y1:y1 + h1, x1:x1 + w1] = blur

    # roi = frame[y:y+h, x:x+w]
    # blur = cv2.GaussianBlur(roi, (5, 5), 0)
    # frame[y:y + h, x:x + w] = blur
    # blur = anonymize_face_simple(roi, factor=3.0)
    # frame = anonymize_face_simple(frame, factor=3.0)
    return frame, color


def anonymize_face_simple(image, factor=3.0):
    # automatically determine the size of the blurring kernel based
    # on the spatial dimensions of the input image
    (h, w) = image.shape[:2]
    kW = int(w / factor)
    kH = int(h / factor)
    # ensure the width of the kernel is odd
    if kW % 2 == 0:
        kW -= 1
    # ensure the height of the kernel is odd
    if kH % 2 == 0:
        kH -= 1
    # apply a Gaussian blur to the input image using our computed
    # kernel size
    return cv2.GaussianBlur(image, (kW, kH), 0)
