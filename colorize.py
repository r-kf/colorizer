import os.path

import cv2 as cv
import numpy as np

prototxt = r'model/colorization_deploy_v2.prototxt'
model = r'model/colorization_release_v2.caffemodel'
points = r'model/pts_in_hull.npy'

points = os.path.join(os.path.dirname(__file__), points)
prototxt = os.path.join(os.path.dirname(__file__), prototxt)
model = os.path.join(os.path.dirname(__file__), model)

def colorize(input):
    """Use caffe-model to add colors to given black and white image

    Args:
        input (string): path of black and white image

    Returns:
        con [ndarray]: view of original and colorized image side by side
        img_bgr_out [ndarray]: colored version of input image
    """
    #Network input size
    W_IN = 224
    H_IN = 224
    
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
    img_rs = cv.resize(img_rgb, (W_IN, H_IN)) # resize image to network input size
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


if __name__ == "__main__":
    out = colorize("examples/bliss.JPEG")
    cv.imshow("color", out[1])
    cv.waitKey()
