# importing libraries
import cv2
import streamlit as st
from PIL import Image
from torchvision import models
from bgr import BGR

# deeplabv3 pretrained model
dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()

# The uploaded files will be read as bytes
# Region for the first image upload
st.header('Original Image')
image_file = st.file_uploader("Image to Remove Background:", type=['png', 'jpeg', 'jpg'])

# Region for the second image upload
st.header('Background to be replaced with')
bg_file = st.file_uploader("Background to be applied", type=['png', 'jpeg', 'jpg'])

# check if the image file is uploaded
if image_file is not None:
    # create two columns
    ip, op = st.beta_columns(2)

    # convert the bytes files to Image object
    image = Image.open(image_file)
    # display for column 1
    with ip:
        st.header('Original Image')
        st.image(image)

    # display for column 2
    with op:
        # loading animation start
        gif_run = st.image('images/loading.gif')
        # create a BGR object
        bgr = BGR()
        st.header('Transformed Image')
        # check if we have a replacement background
        # if it is there use it
        if bg_file is not None:
            output = bgr.segment(dlab, image_file, bg_data=bg_file, dev='cpu')
        else:  # the result will be on a white background
            output = bgr.segment(dlab, image_file, dev='cpu')
        # stop the animation
        gif_run.empty()
        # show the results
        st.image(output)