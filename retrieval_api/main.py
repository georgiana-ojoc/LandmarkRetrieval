import io
import os

from PIL import Image
from flask import Flask, request, jsonify, abort, make_response
from flask_cors import CORS
from google.cloud import vision

from predictor import Predictor

application = Flask(__name__)
CORS(application)


def get_image_from_local_file(file):
    try:
        image = Image.open(file.stream)
    except IOError:
        return None
    byte_array = io.BytesIO()
    image.save(byte_array, format='JPEG')
    byte_array = byte_array.getvalue()
    return vision.Image(content=byte_array)


def get_image_from_remote_file(file):
    image = vision.Image()
    image.source.image_uri = file
    return image


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
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'landmark_retrieval.json'
    field = 'file'
    file = request.files.get(field, None)
    if file is None:
        body = request.json
        if field in body:
            file = body[field]
            image = get_image_from_remote_file(file)
        else:
            return make_response(jsonify({
                'error': 'Missing image'
            }), 400)
    else:
        image = get_image_from_local_file(file)
    if image is None:
        return make_response(jsonify({
            'error': 'Invalid image'
        }), 400)
    client = vision.ImageAnnotatorClient()
    response = client.landmark_detection(image=image)
    if response.error.message:
        return make_response(jsonify({
            'error': 'Could not detect landmark with Vision API'
        }), 500)
    landmarks = response.landmark_annotations
    response = []
    for landmark in landmarks:
        locations = []
        for location in landmark.locations:
            locations += [{
                'latitude': location.lat_lng.latitude,
                'longitude': location.lat_lng.longitude
            }]
        response += [{
            'name': landmark.description,
            'score': landmark.score,
            'locations': locations
        }]
    return make_response(jsonify(response), 200)


if __name__ == "__main__":
    application.run(debug=False)
