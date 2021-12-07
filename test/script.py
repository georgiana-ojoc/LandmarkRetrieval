import io

from PIL import Image

from ModelPredictor import ModelPredictor, GeM


import sys

image = Image.open(sys.argv[1])

x = ModelPredictor("ResNetIbnGeM").predict(img=image)
print("<BEGIN>" + x + "<END>")
