import cv2
import streamlit as st
from PIL import Image
from torchvision import models

from bgr import BGR

# neural net
dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()
og, bg = st.beta_columns(2)

st.header('Original Image')
image_file = st.file_uploader("Image to Remove Background:", type=['png', 'jpeg', 'jpg'])

st.header('Background to be replaced with')
bg_file = st.file_uploader("Background to be applied", type=['png', 'jpeg', 'jpg'])


if image_file is not None:
    ip, op = st.beta_columns(2)
    image = Image.open(image_file)
    with ip:
        st.header('Original Image')
        st.image(image)

    with op:
        bgr = BGR()
        st.header('Transformed Image')
        if bg_file is not None:
            output = bgr.segment(dlab, image_file, bg_data=bg_file, dev='cpu')
        else:
            output = bgr.segment(dlab, image_file, dev='cpu')

        st.image(output)