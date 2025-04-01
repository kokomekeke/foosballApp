from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.route('/ping', methods=['GET'])
    def ping_pong():
        return jsonify('pong!')

    return app
