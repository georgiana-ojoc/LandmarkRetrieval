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
    return ModelPredictor("ResNetIbnGeM").predict(img=img)


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
