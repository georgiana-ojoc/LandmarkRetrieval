import json
import os
import re
import subprocess

import PIL
import torch
from PIL import Image

from flask import Flask, request, jsonify, abort

from ModelPredictor import ModelPredictor, GeM

app = Flask(__name__)


def get_labels_and_probabilities(img: PIL.Image, model: str):

    img.save("image.jpg")
    response = (subprocess.check_output(["python", "script.py", "image.jpg"]).decode('utf-8'))
    regex = eval((re.search(r"<BEGIN>(.*?)<END>", response)).group(1))
    os.remove("image.jpg")
    return regex[0], regex[1]


@app.errorhandler(400)
def page_not_found(e):
    return jsonify(error=str(e)), 400


@app.route('/similar-images', defaults={'model': 'ResNetIbnGeM'},  methods=["POST"])
@app.route("/similar-images/<model>", methods=["POST"])
def process_image(model='ResNetIbnGeM'):
    file = request.files.get('file', False)
    if not file:
        abort(400, description="Image missing")
    img = Image.open(file.stream)
    labels, probabilities = get_labels_and_probabilities(img, model)

    return jsonify({'labels': labels, 'probabilities': probabilities})


if __name__ == "__main__":
    app.run(debug=True)
