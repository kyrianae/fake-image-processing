
import numpy as np
import cv2
import matplotlib.pyplot as plt
import random
import sys
import getopt

def transform(file, display, output):
    print('read ' + file)

    img = cv2.imread(file)
    picin = img

    if display:
        plt.subplot(331), plt.imshow(img), plt.title('Input')

    rows,cols,ch = img.shape

    print ( 'recalibrate'+file)
    # convert it to grayscale
    img_yuv = cv2.cvtColor(picin, cv2.COLOR_BGR2YUV)
    picin = img_yuv

    # apply histogram equalization
    picin[:, :, 0] = cv2.equalizeHist(picin[:, :, 0])
    hist_eq = cv2.cvtColor(picin, cv2.COLOR_YUV2BGR)
    picin = hist_eq

    if display:
        plt.subplot(332), plt.imshow(hist_eq), plt.title('calibrated')

    print ( 'resize '+file)
    resized_imaged = cv2.copyMakeBorder(picin,
                             int(cols / 2),
                             int(cols / 2),
                             int(rows / 2),
                             int(rows / 2),
                             borderType=cv2.BORDER_CONSTANT,
                             value=127)

    src_points = np.float32([
        [rows/2 , cols/2],
        [rows/2 , cols/2 + rows],
        [rows/2 + cols, cols/2 + rows],
        [rows/2 + cols ,cols/2]
    ])

    if display:
        plt.subplot(333), plt.imshow(resized_imaged), plt.title('resized')

    dst_points = np.float32([
        [int ( random.random()*rows/2 ) , int (random.random()*cols/2) ],
        [int ( random.random()*rows/2 ) , int (random.random()*cols/2) + cols/2 + rows],
        [int ( random.random()*rows/2 ) + rows/2 + cols , int (random.random()*cols/2) +  cols/2 + rows ],
        [int ( random.random()*rows/2 ) + rows/2 + cols , int (random.random()*cols/2)]
    ])

    print ( 'transform '+file)
    projective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    img_protran = cv2.warpPerspective(resized_imaged, projective_matrix, (rows+cols, rows+cols))
    picin = img_protran

    if display:
        plt.subplot(334),plt.imshow(img_protran),plt.title('transform')


    print ( 'oversize '+file)
    oversized_iimage = cv2.resize(picin,(picin.shape[0]*10,picin.shape[0]*10))

    if output != '':
        print('write ' + file)
        cv2.imwrite(output,oversized_iimage)

    print('end of tratment of ' + file)

    if display:
        plt.show()

def errorExec():
    print ('arguments :')
    print(' -i inputfile  input file definition (required)')
    print(' -o savefile   output file definition')
    print(' -d            display images')
    sys.exit(2)

def main(argv):
    file= ''
    output=''
    display= False
    write= False

    try:
        opts, args = getopt.getopt(argv, "di:o:", [])
    except getopt.GetoptError:
        errorExec()
    for opt, arg in opts:
        if opt in ("-o"):
            output = arg
        elif opt in ("-i"):
            file = arg
        elif opt in ("-d"):
            display = True

    if file != '' :
        transform( file, display, output )
    else:
        print ('select an input file')
        errorExec()


if __name__ == "__main__":
    main(sys.argv[1:])