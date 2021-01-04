# 9. Vorlesung 28.11.2020, Skript Python 5 (07_Python_05.pdf) 
# Übung: Bilder skalieren + Bilder rotieren + Histogramme anzeigen

import cv2
from matplotlib import pyplot

scale     = 1.0
rotation  = 0
filename  = "opencv.jpg"
display_histogram = 0 # 0: none, 1: grey, 2: rgb

def load_image():
    """Load image from file, then scale and rotate. 
       Returns CV2 object."""
    if display_histogram == 1:
        image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    else:
        image = cv2.imread(filename, cv2.IMREAD_COLOR)

    image_resized = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    rows, cols = image_resized.shape[0:2] # get height and width 

    rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), rotation, 1)
    image_rotated = cv2.warpAffine(image_resized, rotation_matrix, (cols, rows))

    return image_rotated


while True:
    image = load_image()
    cv2.imshow(filename, image)

    if display_histogram > 0:
        if display_histogram == 1: # grey
            pyplot.hist(image.ravel(), 256, [0,256])
        
        if display_histogram == 2: # rgb
            color = ('b', 'g', 'r')
            for i, col in enumerate(color):
                histr = cv2.calcHist([image], [i], None, [256], [0, 256])
                pyplot.plot(histr, color = col)
                pyplot.xlim([0,256])

        pyplot.show()

        # pyplot.show() blocks program
        # > on close, reset histogram, reload image
        display_histogram = 0      
        image = load_image()
        cv2.imshow(filename, image)


    key_pressed = cv2.waitKey()
    if key_pressed == 27:         # esc: close app
        cv2.destroyWindow(filename)
        break
    elif key_pressed == 43:       # +: scale up
        scale = scale * 1.2
    elif key_pressed == 45:       # -: scale down
        scale = scale * 0.8
    elif key_pressed == 114:      # r: rotale right
        rotation = rotation - 10
    elif key_pressed == 108:      # l: rotate left 
        rotation = rotation + 10
    elif key_pressed == 49:       # 1: histogram grey
        display_histogram = 1
    elif key_pressed == 50:       # 2: histogram rgb
        display_histogram = 2
   
    print ("Skalierung: %0.0f%%, Rotation: %d°" % ((scale * 100), rotation))
