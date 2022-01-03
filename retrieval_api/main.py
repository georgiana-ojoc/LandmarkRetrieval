from PIL import Image
from flask import Flask, request, jsonify, abort, make_response
from google.cloud import vision
import io
import os
from flask_cors import CORS

from predictor import Predictor

application = Flask(__name__)
CORS(application)


@application.errorhandler(404)
def not_found(_):
    return make_response(jsonify({
        'error': 'Not found'
    }), 404)


@application.route("/similar-images/<model>", methods=["POST"])
def process_image(model):
    file = request.files.get('file', None)
    if file is None:
        return make_response(jsonify({
            'error': 'Missing image'
        }), 400)
    try:
        image = Image.open(file.stream)
    except IOError:
        return make_response(jsonify({
            'error': 'Invalid image'
        }), 400)
    response = Predictor(model).predict(image)
    if response is None:
        abort(404)
    return make_response(jsonify(response), 200)


@application.route("/landmark", methods=["POST"])
def get_landmark():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "landmarkretrieval-7465959cdf7b.json"
    file = request.files.get('file', None)
    if file is None:
        return make_response(jsonify({
            'error': 'Missing image'
        }), 400)
    try:
        image = Image.open(file.stream)
    except IOError:
        return make_response(jsonify({
            'error': 'Invalid image'
        }), 400)
    client = vision.ImageAnnotatorClient()

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    image = vision.Image(content=img_byte_arr)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    json_response = {"landmark": []}
    for landmark in landmarks:
        json_response["landmark"].append((landmark.description, landmark.score))

    if response.error.message:
        json_response["error"] = "{}".format(response.error.message)
        return make_response(jsonify(json_response), 500)
    return make_response(jsonify(json_response), 200)


if __name__ == "__main__":
    print("OK")
    application.run(debug=False)
