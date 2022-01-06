import numpy as np
#import cv2
import os.path

import cv2 as cv

prototxt = r'model/colorization_deploy_v2.prototxt'
model = r'model/colorization_release_v2.caffemodel'
points = r'model/pts_in_hull.npy'

points = os.path.join(os.path.dirname(__file__), points)
prototxt = os.path.join(os.path.dirname(__file__), prototxt)
model = os.path.join(os.path.dirname(__file__), model)

def colorize(input):
    #Network input size
    W_in = 224
    H_in = 224
    imshowSize = (640, 480)
    
    # Create network graph and load weights
    net = cv.dnn.readNetFromCaffe(prototxt, model)

    # load cluster centers
    pts_in_hull = np.load(points) 

    # populate cluster centers as 1x1 convolution kernel
    pts_in_hull = pts_in_hull.transpose().reshape(2, 313, 1, 1)
    net.getLayer(net.getLayerId('class8_ab')).blobs = [pts_in_hull.astype(np.float32)]
    net.getLayer(net.getLayerId('conv8_313_rh')).blobs = [np.full([1, 313], 2.606, np.float32)]

    # Read the input image in BGR format
    frame=cv.imread(input)
    #convert it to rgb format 
    frame= frame[:,:,[2, 1, 0]]
    # Scale the image to handle the variations in intensity
    img_rgb = ( frame * 1.0 / 255).astype(np.float32)
    #convert to Lab color space
    img_lab = cv.cvtColor(img_rgb, cv.COLOR_RGB2Lab)
    # pull out L channel
    img_l = img_lab[:,:,0]
    (H_orig,W_orig) = img_rgb.shape[:2] # original image size

    # resize image to network input size
    img_rs = cv.resize(img_rgb, (W_in, H_in)) # resize image to network input size
    img_lab_rs = cv.cvtColor(img_rs, cv.COLOR_RGB2Lab)
    img_l_rs = img_lab_rs[:,:,0]
    # subtract 50 for mean-centering
    img_l_rs -= 50 

    # Set the input for forwarding through the openCV DNN module
    net.setInput(cv.dnn.blobFromImage(img_l_rs))

    #Inference on network
    ab_dec = net.forward('class8_ab')[0,:,:,:].transpose((1,2,0)) # this is our result

    # Get the a and b channels
    (H_out,W_out) = ab_dec.shape[:2]

    #Resize to original size
    ab_dec_us = cv.resize(ab_dec, (W_orig, H_orig))

    # concatenate with original image i.e. L channel
    img_lab_out = np.concatenate((img_l[:,:,np.newaxis],ab_dec_us),axis=2) 

    # convert to BGR space from Lab space
    img_bgr_out = cv.cvtColor(img_lab_out, cv.COLOR_Lab2BGR)

    # Clip and then rescale to 0-255
    img_bgr_out = 255 * np.clip(img_bgr_out, 0, 1)
    img_bgr_out = np.uint8(img_bgr_out)

    #concatenate input and output image to display
    con = np.hstack([frame,img_bgr_out]) 
    cv.imwrite('out'+input,con)

    return con, img_bgr_out

""" 
def colorize(input):

    prototxt = r'model/colorization_deploy_v2.prototxt'
    model = r'model/colorization_release_v2.caffemodel'
    points = r'model/pts_in_hull.npy'

    points = os.path.join(os.path.dirname(__file__), points)
    prototxt = os.path.join(os.path.dirname(__file__), prototxt)
    model = os.path.join(os.path.dirname(__file__), model)

    if not os.path.isfile(model):
        print('Missing model file', 'You are missing the file "colorization_release_v2.caffemodel"',
                        'Download it and place into your "model" folder', 'You can download this file from this location:\n', r'https://www.dropbox.com/s/dx0qvhhp5hbcx7z/colorization_release_v2.caffemodel?dl=1')
        exit()

    net = cv2.dnn.readNetFromCaffe(prototxt, model)     # load model from disk
    pts = np.load(points)

    # add the cluster centers as 1x1 convolutions to the model
    class8 = net.getLayerId("class8_ab")
    conv8 = net.getLayerId("conv8_313_rh")
    pts = pts.transpose().reshape(2, 313, 1, 1)
    net.getLayer(class8).blobs = [pts.astype("float32")]
    net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    # load the input image from disk, scale the pixel intensities to the range [0, 1], and then convert the image from the BGR to Lab color space
    image = cv2.imread(input)
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    # resize the Lab image to 224x224 (the dimensions the colorization network accepts), split channels, extract the 'L' channel, and then perform mean centering
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # pass the L channel through the network which will *predict* the 'a' and 'b' channel values
    'print("[INFO] colorizing image...")'
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))

    # resize the predicted 'ab' volume to the same dimensions as our input image
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    # grab the 'L' channel from the *original* input image (not the resized one) and concatenate the original 'L' channel with the predicted 'ab' channels
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

    # convert the output image from the Lab color space to RGB, then clip any values that fall outside the range [0, 1]
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)

    # the current colorized image is represented as a floating point data type in the range [0, 1] -- let's convert to an unsigned 8-bit integer representation in the range [0, 255]
    colorized = (255 * colorized).astype("uint8")

    filename, filetype = os.path.splitext(input)
    cv2.imwrite(filename + "_colorized" + filetype, colorized)

    return image, colorized

if __name__ == "__main__":
    out = colorize("examples/oslo_BW.jpg")
    cv2.imshow("color", out[1])
    cv2.waitKey()


 """

if __name__ == "__main__":
    out = colorize("examples/flower_BW.jpg")
    cv.imshow("color", out[1])
    cv.waitKey()