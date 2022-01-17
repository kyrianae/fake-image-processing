# import the opencv library
import cv2
import matplotlib.pyplot as plt
import numpy as np


# define a video capture object
vid = cv2.VideoCapture(0)
threshold=127
switch_input= 1
nb_input = 3
blursize=1

while (True):
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    blur = cv2.blur(frame, (blursize, blursize))
    cv2.imshow('blur', blur)
    # # convert to RGB
    # image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # # convert to grayscale
    gray = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)

    cv2.imshow('grayscale', gray)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # image = np.array(image, dtype=np.uint8)
    kernel = np.array([[-2, -1, 0],
                       [-1, 1, 1],
                       [0, 1, 2]])
    emboss = cv2.filter2D(frame, -1, kernel)
    cv2.imshow('emboss', emboss)

    emboss2= cv2.filter2D(gray, -1, kernel)
    cv2.imshow('emboss2', emboss2)
    #
    #
    #
    # apply binary thresholding
    input =   emboss  if switch_input else emboss2
    if switch_input ==1 :
        input  = emboss
    elif switch_input == 2:
        input = emboss2
    elif switch_input == 3:
        input = gray

    ret, thresh = cv2.threshold(input, threshold, 255, 0)
    #
    cv2.imshow('thresh', thresh)
    if switch_input ==1 :
        gray2 = cv2.cvtColor(thresh, cv2.COLOR_RGB2GRAY)
    elif switch_input == 2:
        gray2 = thresh
    elif switch_input == 3:
        gray2 = thresh

    cv2.imshow('gray2', gray2)

    # find the contours from the thresholded image
    contours, hierarchy = cv2.findContours(gray2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # draw all contours
    image = cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    cv2.imshow('contoured image', image)

    # im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('contouredqqq', im2)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    k = cv2.waitKey(1)
    # if cv2.waitKey(1):
    #     if 0xFF == ord('q'):
    if k == ord('q'):
        break

    elif k == ord('p'):
        threshold=threshold + 1
        print('threshold :'+str(threshold))
    elif k == ord('o'):
        threshold=threshold - 1
        print('threshold :'+str(threshold))
    elif k == ord('i'):
        switch_input= switch_input + 1
        if switch_input > nb_input:
            switch_input = nb_input
        print('switch input :'+str(switch_input))

    elif k == ord('u'):
        switch_input= switch_input - 1
        if switch_input < 1:
            switch_input = 1
        print('switch input :'+str(switch_input))


    elif k == ord('k'):
        blursize = blursize - 1
        if blursize < 1:
            blursize = 1
        print('blur :'+str(blursize))
    elif k == ord('l'):
        blursize = blursize + 1

        print('blur :'+str(blursize))



# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()