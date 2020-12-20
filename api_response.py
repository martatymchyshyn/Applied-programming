from flask import jsonify

class Response:

    def __init__(self, json=None, code=None):
        self.__json = json
        self.code = code

    def get_json(self):
        return jsonify(self.__json)