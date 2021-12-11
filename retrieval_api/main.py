from PIL import Image
from flask import Flask, request, jsonify, abort, make_response

from predictor import Predictor

application = Flask(__name__)


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


if __name__ == "__main__":
    application.run(debug=True)
