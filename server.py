import os
import constants
import json
import pandas as pd
import pdb

from flask import Flask, make_response, render_template, jsonify, request
from utils import Review
import utils

cached_reviews = []

def create_app(testing=False):
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def main_dashboard():
        return render_template('home.html')

    @app.route('/load_reviews', methods=['POST'])
    def load_reviews():
        if request.method == 'POST':
            global cached_reviews
            cached_reviews = []
            raw_list = utils.load_reviews_from_aws()
            for r in raw_list:
                cached_reviews.append(Review(r))
            
            return make_response(str(len(cached_reviews)))

    @app.route('/get_cached_reviews', methods=['GET'])
    def get_cached_reviews():
        global cached_reviews
        if cached_reviews is None:
            return make_response('')

        if request.method == 'GET':
            prep_reviews = [r.serialize_to_json() for r in cached_reviews]
            return make_response(jsonify(prep_reviews))

    # this health check is for kubernetes to make sure the container is up and running.
    @app.route(constants.KUBERNETES_LIVENESS_CHECK, methods=['GET'])
    def healthz():
        return make_response({'message': 'app is up and running'})

    # this readiness check is for kubernetes to make sure the container is ready to receive requests.
    @app.route(constants.KUBERNETES_READINESS_CHECK , methods=['GET'])
    def readyz():
        return make_response({'message': 'app is ready to receive connections'})

    return app

if __name__ == "__main__":
    app = create_app(True)
    app.run(host='0.0.0.0', port=8080, debug=True)
